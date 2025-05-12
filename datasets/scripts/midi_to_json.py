import os
import json
import mido
from mido import MidiFile


LABELS = ["SAMPLE4", "SAMPLE3", "SAMPLE2", "SAMPLE1", "CB", "CY", "OH", "CH", "HT",
          "MT", "LT", "BT", "CP", "RS", "SD", "BD"]

MIDI_NOTES = [51, 49, 48, 47, 45, 44, 46, 42, 50,
              43, 41, 39, 37, 38, 40, 36]


def create_empty_matrix(length=128):
    return (
        {label: [0] * length for label in LABELS},
        {label: [0] * length for label in LABELS},
        {label: [0] * length for label in LABELS},
        {label: [0.0] * length for label in LABELS},
    )


def extract_genre(filename):
    parts = filename.split()
    if len(parts) > 1:
        return parts[1].lower()
    return "unknown"


def is_section_nonzero(pattern, start, end):
    for label in LABELS:
        if any(pattern[label][start:end]):
            return True
    return False


def parse_midi_to_full_matrix(filepath):
    midi = MidiFile(filepath)
    bpm = 120
    ticks_per_beat = midi.ticks_per_beat

    for track in midi.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                bpm = round(mido.tempo2bpm(msg.tempo))
                break

    ticks_per_sixteenth = ticks_per_beat // 4

    notes = []
    for track in midi.tracks:
        abs_time = 0
        ongoing_notes = {}
        for msg in track:
            abs_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                ongoing_notes[msg.note] = (abs_time, msg.velocity)
            elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and msg.note in ongoing_notes:
                start_time, velocity = ongoing_notes.pop(msg.note)
                notes.append({
                    "note": msg.note,
                    "start": start_time,
                    "end": abs_time,
                    "velocity": velocity
                })

    # Matrices
    pattern, velocity_mat, duration_mat, swing_mat = create_empty_matrix(128)

    for note in notes:
        if note["note"] not in MIDI_NOTES:
            continue

        label = LABELS[MIDI_NOTES.index(note["note"])]

        # Evaluate pre-quantization values
        raw_start = note["start"]
        raw_end = note["end"]
        velocity = note["velocity"]

        # Compute swing from ideal step before quantization
        step_float = raw_start / ticks_per_sixteenth
        quantized_step = int(step_float)
        if not (0 <= quantized_step < 128):
            continue  # skip if out of range

        ideal_tick = quantized_step * ticks_per_sixteenth
        swing_offset = (raw_start - ideal_tick) / ticks_per_sixteenth
        swing_offset = round(swing_offset, 4)

        # Quantize start and duration
        quantized_end_step = int(raw_end / ticks_per_sixteenth)
        quantized_duration = quantized_end_step - quantized_step
        quantized_duration = max(1, min(quantized_duration, 15))  # Clamp

        # Save into matrices
        pattern[label][quantized_step] = 1
        velocity_mat[label][quantized_step] = velocity
        duration_mat[label][quantized_step] = quantized_duration
        swing_mat[label][quantized_step] = swing_offset

    return pattern, velocity_mat, duration_mat, swing_mat, bpm


def export_sliced_bars(filepath, output_dir):
    filename = os.path.basename(filepath)
    genre = extract_genre(filename)

    pattern, velocity, duration, swing, bpm = parse_midi_to_full_matrix(
        filepath)

    for bar_index in range(8):
        start = bar_index * 16
        end = start + 16

        if not is_section_nonzero(pattern, start, end):
            continue

        sliced_pattern = {label: pattern[label][start:end] for label in LABELS}
        sliced_velocity = {
            label: velocity[label][start:end] for label in LABELS}
        sliced_duration = {
            label: duration[label][start:end] for label in LABELS}
        sliced_swing = {label: swing[label][start:end] for label in LABELS}

        output_data = {
            "file": filename,
            "bar_index": bar_index,
            "bpm": bpm,
            "genre": genre,
            "triggers": sliced_pattern,
            "velocity": sliced_velocity,
            "duration": sliced_duration,
            "swing": sliced_swing
        }

        out_name = f"{genre}_{os.path.splitext(filename)[0]}_bar{bar_index}.json"
        out_path = os.path.join(output_dir, out_name)
        print(f"Exporting: {out_path}")
        with open(out_path, "w") as f:
            json.dump(output_data, f, indent=2)


def process_directory(root_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.mid'):
                midi_path = os.path.join(root, file)
                export_sliced_bars(midi_path, output_dir)


def rename_json_files_sequentially(output_dir):
    files = [f for f in os.listdir(output_dir) if f.endswith(".json")]
    files.sort()

    for i, file in enumerate(files):
        old_path = os.path.join(output_dir, file)
        new_name = f"DICE_{i:04d}.json"
        new_path = os.path.join(output_dir, new_name)
        os.rename(old_path, new_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert MIDI files into 16x16 bar JSONs with pre-quantization swing/duration evaluation.")
    parser.add_argument("directory", help="Directory containing MIDI files")
    parser.add_argument("-o", "--output", default="json",
                        help="Output directory for JSON files")
    args = parser.parse_args()

    process_directory(args.directory, args.output)
    rename_json_files_sequentially(args.output)

    print(f"Finished processing. Output in: {args.output}")
