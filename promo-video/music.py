"""Generate a royalty-free ambient pad (music.wav) matching the 33s promo timeline."""
import numpy as np, wave

SR, DUR = 44100, 33.0
t = np.arange(int(SR * DUR)) / SR
hz = lambda n: 440 * 2 ** ((n - 69) / 12)  # MIDI -> Hz

# Am - F - C - G - Am, chord changes roughly on scene cuts
chords = [(0, [57, 64, 69, 72]), (4.9, [53, 60, 65, 69]), (8.9, [48, 55, 64, 67]),
          (15.6, [55, 62, 67, 71]), (21.4, [53, 60, 69, 72]), (26.4, [57, 64, 69, 76])]
pad = np.zeros_like(t)
for i, (start, notes) in enumerate(chords):
    end = chords[i + 1][0] if i + 1 < len(chords) else DUR
    env = np.clip((t - start + 0.8) / 1.6, 0, 1) * np.clip((end + 0.8 - t) / 1.6, 0, 1)
    env = np.sin(env * np.pi / 2) ** 2
    for n in notes:
        f = hz(n)
        for det in (-0.12, 0.0, 0.12):  # detuned voices for warmth
            ff = f * 2 ** (det / 12)
            pad += env * (np.sin(2*np.pi*ff*t) + 0.25*np.sin(4*np.pi*ff*t) + 0.08*np.sin(6*np.pi*ff*t))
pad *= 1 + 0.15 * np.sin(2 * np.pi * 0.2 * t)

# soft bell arpeggio from the services scene onward
bell = np.zeros_like(t)
arp = [69, 72, 76, 79, 76, 72]
step = 0.55
for k, st in enumerate(np.arange(8.9, DUR - 1.5, step)):
    chord = [c for s, c in chords if s <= st][-1]
    f = hz(chord[k % len(chord)] + 12)
    m = t >= st
    tt = t[m] - st
    bell[m] += np.exp(-tt * 3.2) * (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*f*2.01*tt))

# deep sub on the hook for tension
sub = np.sin(2*np.pi*hz(45)*t) * np.clip(1 - t / 5, 0, 1) * 0.6

mix = pad / np.abs(pad).max() * 0.55 + bell / max(np.abs(bell).max(), 1e-9) * 0.18 + sub * 0.35
# simple stereo: slight delay on the right channel, plus a feedback echo on bells
L = mix.copy()
R = np.roll(mix, int(SR * 0.012))
echo = np.zeros_like(bell); d = int(SR * 0.33)
for g in (0.4, 0.2, 0.1):
    echo[d:] += bell[:-d] * g; d += int(SR * 0.33)
echo = echo / max(np.abs(bell).max(), 1e-9) * 0.18
L += np.roll(echo, 0); R += np.roll(echo, int(SR * 0.05))
fade = np.clip(t / 1.2, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1)
st = np.stack([L * fade, R * fade], axis=1)
st = st / np.abs(st).max() * 0.85
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print('wrote music.wav')
