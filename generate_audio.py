import wave
import struct
import math
import random
import os

out_dir = r"T:\Project\Phim\mytv4u_flutter\assets\easter\sfx"
os.makedirs(out_dir, exist_ok=True)

def generate_wav(filename, samples, sample_rate=44100):
    path = os.path.join(out_dir, filename)
    with wave.open(path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for s in samples:
            s_clamped = max(-1.0, min(1.0, s))
            wav_file.writeframesraw(struct.pack("<h", int(s_clamped * 32767.0)))

sr = 44100

# 1. Heartbeat
heartbeat = []
for i in range(sr * 2):
    t = i / sr
    env1 = math.exp(-10 * t) if t < 0.5 else 0
    env2 = math.exp(-10 * (t - 0.3)) if t >= 0.3 else 0
    val = math.sin(2 * math.pi * 50 * t) * (env1 + env2)
    heartbeat.append(val)
generate_wav("heartbeat.wav", heartbeat, sr)

# 2. Swoosh
swoosh = []
for i in range(int(sr * 1.5)):
    t = i / sr
    env = math.sin(math.pi * (t / 1.5))
    swoosh.append(random.uniform(-1, 1) * env * 0.5)
for i in range(1, len(swoosh)):
    swoosh[i] = swoosh[i]*0.2 + swoosh[i-1]*0.8
generate_wav("swoosh.wav", swoosh, sr)

# 3. Thwip
thwip = []
for i in range(int(sr * 0.5)):
    t = i / sr
    env = math.exp(-15 * t)
    thwip.append(random.uniform(-1, 1) * env * 0.8)
for i in range(1, len(thwip)):
    thwip[i] = (thwip[i] - thwip[i-1]) * 0.8
generate_wav("thwip.wav", thwip, sr)

print("Generated SFX files successfully!")
