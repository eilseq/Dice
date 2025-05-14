# DICE Dataset

This folder provides tools for generating synthetic datasets to support creation machine learning models for pattern generation. This simplifies the process of creating structured datasets with customizable distributions, enabling experimentation and algorithm development from custom configuration files.

## Installation

### Clone the repository:

```
git clone https://github.com/eilseq/dice.git
cd ./dice/datasets
```

### Create a conda environment:

```
conda create --name dice-datasets python=3.12
conda activate dice-datasets
```

### Install dependencies:

```
pip install pytest torch pandas seaborn
pip install -e .
```

## Usage

### Run Tests

```
pytest
```

### Generate Datasets

```
python scripts/generate_datasets.py --id test --json ./json --augmentation_preset default --augmentation_factor 3
```

## License

See [LICENSE](../LICENSE.md)
