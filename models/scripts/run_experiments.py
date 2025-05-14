import os
import json
import time

EXPERIMENTS_JSON = "experiments.json"
SUMMARY_JSON = "summary.json"
DIST_DIR = "dist"


def get_workspace_path():
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", ".."))


def get_preset_path(preset):
    return os.path.join(get_workspace_path(), "datasets", "presets", preset + ".json")


def get_dist_path(id):
    return os.path.join(get_workspace_path(), "dist", id)


def get_cargo_debug():
    return os.path.join(get_workspace_path(), "app", "target", "debug")


def run_command(cmd):
    print(f"[RUNNING] {cmd}")
    return os.system(cmd) == 0


def run_experiment(exp):
    required_keys = [
        "id", "architecture", "loss", "augmentation_preset", "augmentation_factor",
        "noise_level", "batch_size", "epochs", "learning_rate"
    ]
    for key in required_keys:
        if key not in exp:
            raise ValueError(
                f"Missing required key '{key}' in experiment config.")

    dataset_cmd = (
        f"cd {get_workspace_path()} && "
        f"cd datasets && "
        f"python scripts/generate_datasets.py "
        f"--id {exp['id']} --json ./json "
        f"--augmentation_factor {exp['augmentation_factor']} "
        f"--augmentation_preset {exp['augmentation_preset']}"
    )
    if not run_command(dataset_cmd):
        return {"id": exp["id"], "status": "dataset_failed"}

    train_cmd = (
        f"cd {get_workspace_path()} && "
        f"cd models && "
        f"python scripts/train_model.py "
        f"--id {exp['id']} "
        f"--augmentation_preset {exp['augmentation_preset']} "
        f"--architecture {exp['architecture']} "
        f"--loss {exp['loss']} "
        f"--noise_level {exp['noise_level']} "
        f"--batch_size {exp['batch_size']} "
        f"--epochs {exp['epochs']} "
        f"--learning_rate {exp['learning_rate']}"
    )
    if not run_command(train_cmd):
        return {"id": exp["id"], "status": "train_failed"}

    onnx_cmd = (
        f"cd {get_workspace_path()} && "
        f"cd models && "
        f"python scripts/export_onnx.py "
        f"--id {exp['id']} "
        f"--architecture {exp['architecture']} "
    )
    if not run_command(onnx_cmd):
        return {"id": exp["id"], "status": "onnx_failed"}

    cargo_cmd = (
        f"cd {get_workspace_path()} && "
        f"cd app && "
        f"ONNX_MODEL_PATH=\"../../dist/{exp['id']}/{exp['id']}.onnx\" cargo make dice-m4l && "
        f"mv {get_cargo_debug()}/dice.zip {get_dist_path(exp['id'])}/{exp['id']}.zip"
    )
    if not run_command(cargo_cmd):
        return {"id": exp["id"], "status": "cargo_failed"}


def main():
    with open(EXPERIMENTS_JSON) as f:
        experiments = json.load(f)

    results = []
    for exp in experiments:
        print(f"[RUN] Experiment: {exp['id']}")
        results.append(run_experiment(exp))


if __name__ == "__main__":
    main()
