---
layout: page
title: /getting-started
---

# Getting Started

---

## Installation

### **Download DICE**

Access the [Releases](https://github.com/eilseq/Dice/releases) section to download DICE.

### **Open Ableton Project and Follow Lesson**

The bundle includes an Ableton Live project with examples and further documentation. It requires Ableton Live 12.

---

## Basic Usage

### **Input a 16x16 Matrix**

Like any other Ableton Live's MIDI Transformation Tool, create clip and select notes to provide structured input data to the model. This release is designed specifically for drum patterns, so it will act upon the first bar of notes in the conventionla drum rack range (additional info in Ableton Lesson).

### **Adjust Parameters**

- `threshold`: Controls the cutoff for pattern retention or alteration.
- `noiseLevel`: Intensity of stochastic perturbations during diffusion.
- `seed`: Sets the random seed for consistent results across sessions.

### **Trigger Pattern Manipulation**

The tool provides a minimal user interface provided under clip view. Every control will trigger a MIDI transformation based on selected notes. Observe how the input pattern is transformed based on the configured diffusion settings.
