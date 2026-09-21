# DTMF Touch-Tone Signal Synthesizer and Spectral Decoder (DSP)

This project provides a comprehensive Discrete-Time Signal Processing (DSP) implementation of the **Dual-Tone Multi-Frequency (DTMF)** signaling protocol, widely known as telephone touch-tone. The repository includes end-to-end signal generation, spectral estimation (DTFT/FFT), and automated decoding pipelines implemented in both **Python** and **MATLAB**.

---

## 1. Theoretical Background & Mathematical Model

In standard telephone systems, pressing any keypad digit generates a composite acoustic signal formed by the superposition of two distinct sinusoids: a low-band frequency (row) and a high-band frequency (column)[cite: 1]. Under a continuous-to-discrete sampling rate of $8192\text{ Hz}$ ($F_s$), the discrete-time representation is governed by[cite: 1]:

$$d_k[n] = \sin(\omega_{row} \cdot n) + \sin(\omega_{col} \cdot n)$$

For instance, the signal corresponding to digit **5** is expressed as[cite: 1]:
$$d_5[n] = \sin(0.5906\,n) + \sin(1.0247\,n)$$

### Normalized Discrete Frequency Grid ($\text{rad/sample}$)

| Row / Column | $\omega_{col} = 0.9273$ | $\omega_{col} = 1.0247$ | $\omega_{col} = 1.1328$ |
| :--- | :---: | :---: | :---: |
| **$\omega_{row} = 0.5346$** | 1 | 2 | 3 |
| **$\omega_{row} = 0.5906$** | 4 | 5 | 6 |
| **$\omega_{row} = 0.6535$** | 7 | 8 | 9 |
| **$\omega_{row} = 0.7217$** | * | 0 | # |

---

## 2. Industrial Significance & Engineering Relevance

Although DTMF originated in early analog telephony, it remains an indispensable standard in modern telecommunications, aerospace, and embedded engineering:

1. **Immunity to Harmonics & Distortion:**
   * The frequencies were intentionally chosen to avoid harmonic relationships (no frequency is a multiple of another)[cite: 1].
   * This design prevents nonlinear line distortion or human speech from accidentally triggering command tones ("talk-off" phenomenon).

2. **Telephony & Automated IVR Systems:**
   * Every Interactive Voice Response (IVR) menu used in telecommunications, banking, and customer service relies on real-time DTMF decoding over audio channels.

3. **Critical Radio Communications (PMR / TETRA / Aerospace):**
   * Two-way radio communications use DTMF bursts for selective calling (Selcall), repeater access, and radio identification without requiring a digital data packet channel.

4. **Resource-Constrained Embedded Systems & IoT:**
   * In low-power microcontrollers (e.g., STM32, ARM Cortex-M), DTMF tone detection enables command-and-control over simple analog transceivers using lightweight algorithms like the Goertzel algorithm.

---

## 3. Architecture & Algorithmic Workflow

* **Dual-Tone Synthesis:** Dynamic parameter mapping converts key inputs into algebraic sinusoidal sums over discrete sample vectors[cite: 1].
* **Spectral Analysis (DTFT / FFT):** 2048-point zero-padded Fast Fourier Transform yields sharp frequency localization and high bin resolution.
* **Automated Decoder:** Band-segmented peak detectors inspect the sub-bands $[0.45, 0.80]\text{ rad}$ and $[0.85, 1.25]\text{ rad}$ independently, mapping Euclidean distances to the nearest valid keypad coordinate.

---

## 4. Getting Started

### Python Workflow
Dependencies: `numpy`, `matplotlib`
```bash
pip install numpy matplotlib
python dtmf_analyzer.py