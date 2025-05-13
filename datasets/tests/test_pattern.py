import pytest

from dice_datasets import Pattern, RandomPatternConfig, RandomSequenceConfig, WeightedCluster


@pytest.fixture
def ones_and_zeros_random_pattern_config():
    ones_and_zeros = RandomSequenceConfig(
        label="ones_and_zeros",
        length_in_clusters=4,
        weighted_clusters=[
            WeightedCluster(
                triggers=[1, 1, 1, 1],
                weight=1
            ),
            WeightedCluster(
                triggers=[0, 0, 0, 0],
                weight=1
            )
        ]
    )

    return RandomPatternConfig(
        max_polyphony=2,
        max_num_events_with_full_polyphony=2,
        random_sequence_configs=[
            ones_and_zeros, ones_and_zeros, ones_and_zeros, ones_and_zeros
        ]
    )


@pytest.fixture
def simple_pattern_dict():
    return {
        "triggers": {
            "BD": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            "SD": [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            "HH": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            "CH": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # empty
        }
    }


def test_pattern_from_dictionary(simple_pattern_dict):
    pattern = Pattern.from_dictionary(simple_pattern_dict)

    assert len(pattern.sequences) == 4
    assert set(pattern.get_labels()) == {"BD", "SD", "HH", "CH"}

    tensor = pattern.get_trigger_tensor()
    assert tensor.shape == (4, 16)
    assert tensor[0].tolist() == simple_pattern_dict["triggers"]["BD"]
    assert tensor[1].tolist() == simple_pattern_dict["triggers"]["SD"]
    assert tensor[2].tolist() == simple_pattern_dict["triggers"]["HH"]
    assert tensor[3].tolist() == simple_pattern_dict["triggers"]["CH"]


def test_augmentation_using_random_config_settings(simple_pattern_dict, ones_and_zeros_random_pattern_config):
    pattern = Pattern.from_dictionary(simple_pattern_dict)
    empty_sequence = pattern.sequences[3]

    assert empty_sequence.is_empty()

    # Apply filling method
    pattern.fill_empty_sequences_with_random(
        ones_and_zeros_random_pattern_config)

    assert pattern.valid_polyphony_requirements(
        ones_and_zeros_random_pattern_config.max_polyphony,
        ones_and_zeros_random_pattern_config.max_num_events_with_full_polyphony) == True
