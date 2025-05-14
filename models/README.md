# DICE Model

This folder provides tools for generating and training machine learning models for pattern generation, using various architectures. It simplifies the process of creating, configuring, and testing models for experimentation and deployment using custom configuration files.

## Installation

### Clone the Repository:

```
git clone https://github.com/eilseq/dice.git
cd ./dice/models
```

### Create a Conda Environment:

```
conda create --name dice-models python=3.12
conda activate dice-models
```

### Install Dependencies:

```
pip install pytest torch onnx onnxruntime
pip install -e .
```

## Usage

### Run Tests

```
pytest
```

### Train a Model

```
python scripts/train_model.py --id test1 --augmentation_preset default --architecture att_unet --loss mse_poly_penalty --noise_level 0.2
```

### Export to ONNX

```
python scripts/export_onnx.py --id test --augmentation_preset default --architecture att_unet --loss mse_poly_penalty
```

### Run Experiments

```
[
  {
    "id": "default_unet_mse_noise_low",
    "augmentation_preset": "default",
    "architecture": "att_unet",
    "loss": "mse_poly_penalty",
    "noise_level": 0.1,
    "batch_size": 32,
    "epochs": 6,
    "learning_rate": 0.001,
    "augmentation_factor": 3
  },
  ... more experiments
]
```

```
python scripts/run_experiments.py
```

## License

See [LICENSE](../LICENSE.md)
