# QuietArchive

*A minimal, open-source sanctuary for calming vintage audio — crafted with the care of old artisans, shaped by modern signal wisdom.*

QuietArchive restores recordings that carry the dust of time: cassette hiss, room hum, brittle highs, uneven dynamics. Its purpose is simple:
**to let old sound breathe again.**

---

## ✨ Features

* **Spectral-gate denoising** to soften steady tape hiss
* **High-pass cleaning** to remove rumble and mechanical drift
* **Low-pass smoothing** to tame harsh high frequencies
* **Gentle dynamics control** for a calm and even presence
* **Optional warmth & reverb** to revive the ambience of forgotten rooms
* **Peak normalization** for consistent loudness
* Works fully **offline**, built with **open-source DSP tools**

---

## 📦 Installation

QuietArchive uses standard Python libraries:

```bash
pip install numpy scipy soundfile librosa noisereduce pysndfx
```

Optional (for advanced users):

```bash
pip install torch torchaudio
```

---

## 🛠 Usage

Process any vintage audio file:

```bash
python calm_audio.py input.wav output_calm.wav \
  --sr 22050 \
  --denoise_strength 0.6 \
  --lowpass 8000 \
  --reverb
```

### Key Arguments

* `--sr` — target sample rate (default 22050)
* `--denoise_strength` — 0–1, higher values remove more hiss
* `--lowpass` — cutoff frequency to soften the high end
* `--reverb` — enable analog-style warmth and subtle ambience

---

## 🌿 Philosophy

QuietArchive follows a timeless sequence, inspired by traditional restoration craft: ( a vibe coded project ) 

1. **Stabilize** the recording
2. **Lift away** the rumble of the world below
3. **Sweep aside** the endless hiss of time
4. **Smooth** the brittle edges
5. **Balance** the voice of the piece
6. **Normalize** its presence
7. **Revive** — gently — the atmosphere it once lived in

Each step serves the same purpose:
**to let the soul of the recording speak without strain.**

---

## 📁 Project Structure

```
QuietArchive/
 ├── calm_audio.py
 ├── README.md
 └── examples/
```

---

## 🤝 Contributions

Pull requests are welcome. QuietArchive is shaped with respect for both tradition and the forward path of audio research. If you add a feature, keep it **minimal**, **transparent**, and **gentle**.

---

## ⚖️ License

MIT License — free to use, adapt, and share.

---

## 🕯 Closing Note

Recordings from the past carry stories etched in noise.
QuietArchive does not erase their age —
it **lets their age rest peacefully**,
so the voice beneath may rise with calm clarity.
