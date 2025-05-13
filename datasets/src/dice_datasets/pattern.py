import json
import torch

from .sequence import RandomSequenceConfig, Sequence, Cluster
from dataclasses import dataclass
from random import shuffle
from torch import Tensor
from typing import List


@dataclass
class RandomPatternConfig:
    random_sequence_configs: List[RandomSequenceConfig]
    max_polyphony: int
    max_num_events_with_full_polyphony: int

    @staticmethod
    def from_dictionary(dict: dict):
        random_sequence_configs = [
            RandomSequenceConfig.from_dictionary(seq_config) for seq_config in dict['random_sequence_configs']
        ]

        # for readability purposes JSON has inverted order
        random_sequence_configs.reverse()

        return RandomPatternConfig(
            max_polyphony=dict['max_polyphony'],
            max_num_events_with_full_polyphony=dict['max_num_events_with_full_polyphony'],
            random_sequence_configs=random_sequence_configs
        )

    @staticmethod
    def from_json(path: str):
        with open(path, 'r') as file:
            dict_config = json.load(file)
            return RandomPatternConfig.from_dictionary(dict_config)


@dataclass
class Pattern:
    sequences: List[Sequence]

    def get_triggers(self):
        # Returns the triggers of pattern into one matrix
        return [sequence.get_triggers() for sequence in self.sequences]

    def get_labels(self):
        return [sequence.label for sequence in self.sequences]

    def get_trigger_tensor(self):
        # Returns the triggers of sequence into a 2D tensor
        tensors = [sequence.get_trigger_tensor()
                   for sequence in self.sequences]
        return torch.stack(tensors, dim=0)

    def valid_polyphony_requirements(self, max_polyphony: int, max_num_events_with_full_polyphony: int):
        return Pattern.tensor_valid_polyphony_requirements(
            self.get_trigger_tensor(),
            max_polyphony=max_polyphony,
            max_num_events_with_full_polyphony=max_num_events_with_full_polyphony
        )

    def fill_empty_sequences_with_random(self, config: RandomPatternConfig) -> None:
        if not self.valid_polyphony_requirements(
                config.max_polyphony, config.max_num_events_with_full_polyphony):
            return

        indexed_sequences = list(enumerate(self.sequences))
        shuffle(indexed_sequences)
        for i, sequence in indexed_sequences:
            if sequence.is_empty():
                # Replace with another random sequence
                empty_seq = sequence
                new_seq = Sequence.create_random(
                    config.random_sequence_configs[i])
                self.sequences[i] = new_seq
                # revert empty sequence if modifications exceed validation limits
                if not self.valid_polyphony_requirements(
                        config.max_polyphony, config.max_num_events_with_full_polyphony):
                    self.sequences[i] = empty_seq
                    return

    @staticmethod
    def tensor_valid_polyphony_requirements(pattern_tensor: Tensor, max_polyphony: int, max_num_events_with_full_polyphony: int):
        polyphony = torch.sum(pattern_tensor, dim=0)

        # 1. No timestep should exceed max polyphony
        if torch.any(polyphony > max_polyphony):
            return False

        # 2. Limit number of times full polyphony is reached
        full_polyphony_events = torch.sum(polyphony == max_polyphony).item()
        if full_polyphony_events > max_num_events_with_full_polyphony:
            return False

        return True

    @staticmethod
    def from_dictionary(dict_obj: dict):
        pattern_dict = dict_obj["triggers"]
        sequences = []

        for label, triggers in pattern_dict.items():
            # Wrap each trigger list in a single Cluster
            cluster = Cluster(triggers=triggers)
            sequence = Sequence(label=label, clusters=[cluster])
            sequences.append(sequence)

        return Pattern(sequences)

    @staticmethod
    def from_json(path: str):
        with open(path, 'r') as file:
            dict_obj = json.load(file)
            return Pattern.from_dictionary(dict_obj)
