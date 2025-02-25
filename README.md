# DICE

![DICE GitHub Banner](./docs/assets/images/github-banner.png)

[Download Page](https://github.com/eilseq/Dice/releases)

## Diffusion Network for MIDI Transformation

**DICE** is a tool designed for advanced manipulation of musical patterns using a custom-trained machine learning model based on diffusion architectures.

Rather than focusing on outright generation, DICE refines, transforms, and reinterprets existing patterns in real time while preserving the original musical features.

Built specifically for the Max/MSP environment as a max external, and embedded into a MIDI Transformation Tool for Ableton, it enables seamless integration into both live performance and studio workflows.

### Functionalities

Focusing on a minimal user experience, the goal of this tool is to bridge the gap between deterministic pattern manipulation and stochastic processes, allowing for a controlled but flexible approach to reshaping musical materials while limiting any form of bias related to style and genre.

- **Pattern Manipulation through Diffusion**  
  DICE employs a diffusion-based architecture to iteratively refine and reshape input patterns. This approach ensures that transformations retain musical coherence while introducing new structural possibilities.

- **Real-Time Interaction**  
  Designed for Ableton users, DICE responds instantly to user adjustments, enabling dynamic manipulation of musical sequences within a Max patch. Parameters like `threshold`, `noiseLevel`, and `seed` provide granular control over the transformation process.

- **Matrix-Based Input**  
  The system operates on a 16x16 matrix input, allowing users to define initial states that DICE can then expand upon, invert, or alter based on diffusion steps and user-defined parameters.

- **Integration with Max/MSP and Max for Live**  
  Fully compatible with Max/MSP and Max for Live, DICE can be embedded into existing workflows or used as a standalone tool.

### Ethical Considerations

- **Custom Dataset Use**  
  DICE is trained on a purpose-built synthetic dataset, ensuring that it does not rely on copyrighted or external musical material.

- **Transparency in Manipulation**  
  The diffusion-based architecture allows users to trace how patterns evolve through each manipulation stage, offering clarity in how changes occur. Every transformation depends only from the current set of parameters and input notes, so that generations on same states will give consistent results.

- **User-Driven Control**  
  Emphasizing the musician's role as the primary creative agent, DICE ensures that its manipulations serve the artist’s intent, rather than imposing algorithmic biases, while offering a minimal user interface.

---

## Getting Started

### Installation

1. **Download DICE**  
   Access the [Releases](https://github.com/eilseq/Dice/releases) section to download the external.

2. **Open Ableton Project and Follow Lesson**  
   The bundle comes with an Ableton Live project containing examples of DICE use and accurate documentation on how to generate clips and install the tool globally.

### Basic Usage

1. **Input a 16x16 Matrix**  
   Like any other Ableton Live's MIDI Transformation Tool, create clip and select notes to provide structured input data to the model. This release is designed specifically for drum patterns, so it will act upon the first bar of notes in the conventionla drum rack range (additional info in Ableton Lesson).

2. **Adjust Parameters**

   - `threshold`: Controls the cutoff for pattern retention or alteration.
   - `noiseLevel`: Determines the intensity of stochastic perturbations during diffusion.
   - `seed`: Sets the random seed for consistent results across sessions.

3. **Trigger Pattern Manipulation**  
   The tool provides a minimal user interface provided under clip view. Every control will trigger a MIDI transformation based on selected notes. Observe how the input pattern is transformed based on the configured diffusion settings.

---

## License

DICE is provided under an **All Rights Reserved** license. While musicians are free to use it for commercial music and audio asset creation, redistribution or modification of the source code requires explicit permission. Full license details can be found in the [LICENSE](./LICENSE.md).
