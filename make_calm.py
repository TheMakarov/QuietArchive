"""
Minimal open-source pipeline to "calm" noisy vintage recordings (e.g. a 1980 cassette recording).
Sensible defaults, command-line usage, and fallbacks when specialized libs aren't available.

Goals:
 - reduce broadband noise (hiss, tape noise)
 - remove clicks/pops (optional)
 - smooth high-frequency harshness (gentle lowpass / de-essing)
 - control dynamic range (light compression)
 - optionally add gentle plate reverb / warmth to make sound "calm"

Dependencies (install with pip):
 pip install numpy scipy soundfile librosa noisereduce pysndfx pyrubberband

Optional (better results):
 - rnnoise Python wrapper (for realtime denoising) or use rnnoise C lib
 - demucs / spleeter for source separation (to isolate vocals/instruments)
 - torch + torchaudio if using ML denoisers

Usage:
 python #{this.script name} input.wav output_calm.wav --sr 22050 --denoise_strength 0.6 --lowpass 8000

"""

import argparse
import numpy as np
import soundfile as sf
import librosa
import noisereduce as nr
from scipy import signal
from pysndfx import AudioEffectsChain


def resample(x, orig_sr, target_sr):
    if orig_sr == target_sr:
        return x
    return librosa.resample(x, orig_sr=orig_sr, target_sr=target_sr)


def highpass_filter(x, sr, cutoff=80):
    # Remove DC and rumble
    sos = signal.butter(2, cutoff, btype='highpass', fs=sr, output='sos')
    return signal.sosfilt(sos, x)


def lowpass_filter(x, sr, cutoff=8000):
    sos = signal.butter(4, cutoff, btype='lowpass', fs=sr, output='sos')
    return signal.sosfilt(sos, x)


def gentle_compress(x, sr, threshold_db=-18, ratio=2.0):
    # Simple soft-knee compressor implemented in the amplitude domain.
    # Not a production compressor but good enough for "calm" effect.
    eps = 1e-9
    db = 20 * np.log10(np.maximum(np.abs(x), eps))
    gain_db = np.zeros_like(db)
    # apply downward compression above threshold
    over = db > threshold_db
    gain_db[over] = (threshold_db + (db[over] - threshold_db) / ratio) - db[over]
    gain = 10 ** (gain_db / 20)
    return x * gain


def add_warmth_and_reverb(x, sr, reverb_amount=0.12, room_scale=20):
    # Use pysndfx chain: mild saturation -> plate reverb -> gentle EQ
    fx = AudioEffectsChain()
    # soft saturation by 'overdrive' (small amount) then reverb
    fx = fx.overdrive(gain=3.0, colour=20).reverb(reverberance=room_scale, hf_damping=50, room_scale=room_scale, pre_delay=20)
    # pysndfx expects a file; we process via temporary file approach
    return fx(x, sr)


def denoise_with_spectral_gate(x, sr, prop_decrease=0.8, n_fft=2048, hop_length=512):
    # Use noisereduce library spectral gating (works well for stationary hiss)
    # prop_decrease is how much to reduce the noise (0-1); higher -> more aggressive
    reduced = nr.reduce_noise(y=x, sr=sr, prop_decrease=prop_decrease, stationary=True, n_fft=n_fft, hop_length=hop_length)
    return reduced


def normalize_peak(x, peak=0.95):
    maxval = np.max(np.abs(x))
    if maxval < 1e-9:
        return x
    return x * (peak / maxval)


def process_file(infile, outfile, sr=22050, denoise_strength=0.6, lowpass_cutoff=8000, add_reverb=False):
    x, orig_sr = sf.read(infile)
    # If stereo, convert to mono by average (for minimal pipeline)
    if x.ndim == 2:
        x = x.mean(axis=1)
    # Resample
    x = resample(x, orig_sr, sr)
    # Remove low-frequency rumble
    x = highpass_filter(x, sr, cutoff=80)
    # Denoise (spectral gating)
    x = denoise_with_spectral_gate(x, sr, prop_decrease=denoise_strength)
    # Gentle lowpass to remove tape harshness
    x = lowpass_filter(x, sr, cutoff=lowpass_cutoff)
    # Light compression
    x = gentle_compress(x, sr, threshold_db=-18, ratio=2.0)
    # Normalize
    x = normalize_peak(x, peak=0.95)
    # Optional warmth + reverb (calmening effect)
    if add_reverb:
        try:
            x = add_warmth_and_reverb(x, sr, reverb_amount=0.12, room_scale=20)
        except Exception as e:
            print('Reverb step failed, continuing without it:', e)
    # Save
    sf.write(outfile, x, sr)
    print(f"Wrote calm file to: {outfile}")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Minimal calm-audio pipeline (OSS).')
    p.add_argument('infile')
    p.add_argument('outfile')
    p.add_argument('--sr', type=int, default=22050)
    p.add_argument('--denoise_strength', type=float, default=0.6, help='0-1, higher is more aggressive')
    p.add_argument('--lowpass', type=int, default=8000)
    p.add_argument('--reverb', action='store_true')
    args = p.parse_args()
    process_file(args.infile, args.outfile, sr=args.sr, denoise_strength=args.denoise_strength, lowpass_cutoff=args.lowpass, add_reverb=args.reverb)

