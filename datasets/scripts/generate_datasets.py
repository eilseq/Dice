import argparse
import os
import torch

from dice_datasets import PatternDataset, Pattern, RandomPatternConfig
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from rich.progress import Progress, Live, BarColumn, TimeElapsedColumn, TaskProgressColumn


def parse_args():
    parser = argparse.ArgumentParser(description="Process some inputs.")
    parser.add_argument('--id', type=str, required=True,
                        help='Selected folder containing patterns in JSON format')

    parser.add_argument('--json', type=str, required=True,
                        help='Selected folder containing patterns in JSON format')

    parser.add_argument('--augmentation_factor', type=str, required=True,
                        help='Increase size of the pattern dataset by a selected factor using random preset')

    parser.add_argument('--augmentation_preset', type=str, required=True,
                        help='Selected augmentation preset')

    args = parser.parse_args()
    return args.json, int(args.augmentation_factor), args.augmentation_preset, args.id


def create_dataset(json_folder_path, augmentation_factor, augmentation_preset_path):
    patterns = Queue()
    config = RandomPatternConfig.from_json(augmentation_preset_path)

    json_files = [
        f for f in os.listdir(json_folder_path) if f.endswith(".json")
    ]

    total = len(json_files)
    if augmentation_factor is not None:
        total = total * augmentation_factor

    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    )

    with Live(progress, refresh_per_second=10):
        task_id = progress.add_task(
            "[cyan]Generating Patterns...", total=total)

        def load_pattern(file_name):
            path = os.path.join(json_folder_path, file_name)
            pattern = Pattern.from_json(path)
            progress.update(task_id, advance=1)
            return pattern

        def load_and_modify_pattern(file_name):
            path = os.path.join(json_folder_path, file_name)
            pattern = Pattern.from_json(path)
            pattern.fill_empty_sequences_with_random(config)
            progress.update(task_id, advance=1)
            return pattern

        with ThreadPoolExecutor(10) as executor:
            futures = []
            for filename in json_files:
                futures.append(executor.submit(load_pattern, f"{filename}"))

                if augmentation_factor is not None:
                    for _ in range(augmentation_factor):
                        futures.append(executor.submit(
                            load_and_modify_pattern, f"{filename}"))

        for future in as_completed(futures):
            pattern = future.result()
            patterns.put(pattern)

    return PatternDataset(list(patterns.queue))


def get_preset_path(preset):
    return os.path.join("presets", preset + ".json")


def get_workspace_path():
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", ".."))


def get_dist_path(id):
    return os.path.join(get_workspace_path(), "dist", id)


if __name__ == "__main__":
    json_folder, factor, preset, id = parse_args()
    dataset = create_dataset(json_folder, factor, get_preset_path(preset))

    os.makedirs(get_dist_path(id), exist_ok=True)
    destination_path = os.path.join(get_dist_path(id), id + ".pt")

    torch.save(dataset, destination_path)
