---
layout: home
title: /dice
---

![DICE GitHub Banner](./assets/images/github-banner-black-600.png)

**DICE** is a tool designed for advanced manipulation of musical patterns using a custom-trained machine learning model based on diffusion architectures.

Rather than focusing on outright generation, DICE refines, transforms, and reinterprets existing patterns in real time while preserving the original musical features.

Built specifically for the Max/MSP environment as a max external, and embedded into a MIDI Transformation Tool for Ableton, it enables seamless integration into both live performance and studio workflows.

---

<div style="text-align: center; margin-top: 2em;">
  <video width="600" controls>
    <source src="./assets/videos/dice_test.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>

---

# Functionalities

Focusing on a minimal user experience, the goal of this tool is to bridge the gap between deterministic pattern manipulation and stochastic processes, allowing for a controlled but flexible approach to reshaping musical materials while limiting any form of bias related to style and genre.

## **Pattern Manipulation through Diffusion**

DICE employs a diffusion-based architecture to iteratively refine and reshape input patterns. This approach ensures that transformations retain musical coherence while introducing new structural possibilities.

## **Real-Time Interaction**

Designed for Ableton users, DICE responds instantly to user adjustments, enabling dynamic manipulation of musical sequences within a Max patch. Parameters like `threshold`, `noiseLevel`, and `seed` provide granular control over the transformation process.

## **Matrix-Based Input**

The system operates on a 16x16 matrix input, allowing users to define initial states that DICE can then expand upon, invert, or alter based on diffusion steps and user-defined parameters.

## **Integration with Max/MSP and Max for Live**

Fully compatible with Max/MSP and Max for Live, DICE can be embedded into existing workflows or used as a standalone tool.

---

# Ethical Considerations

# **Custom Dataset Use**

DICE is trained on a purpose-built synthetic dataset, ensuring that it does not rely on copyrighted or external musical material.

# **Transparency in Manipulation**

The diffusion-based architecture allows users to trace how patterns evolve through each manipulation stage, offering clarity in how changes occur. Every transformation depends only from the current set of parameters and input notes, so that generations on same states will give consistent results.

# **User-Driven Control**

Emphasizing the musician's role as the primary creative agent, DICE ensures that its manipulations serve the artist’s intent, rather than imposing algorithmic biases, while offering a minimal user interface.
