import numpy as np
import soundfile as sf
import sys


def to_int16(audio):
    if audio.dtype != np.int16:
        return np.int16(audio * 32767)
    return audio

def bits_to_int(bits):
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return value

_, carrier_path, secret_path = sys.argv

carrier, sr = sf.read(carrier_path)
if carrier.ndim == 2:
    carrier = carrier.mean(axis=1)
carrier = to_int16(carrier)

secret, sr_secret = sf.read(secret_path)
if secret.ndim == 2:
    secret = secret.mean(axis=1)
secret = to_int16(secret)


if sr != sr_secret:
    raise ValueError("Частоты дискретизации у файлов должны совпадать!")

carrier = to_int16(carrier)
secret = to_int16(secret)


secret_bytes = secret.tobytes()
secret_bits = np.unpackbits(np.frombuffer(secret_bytes, dtype=np.uint8))
num_secret_bits = len(secret_bits)


header_length = 32
total_bits_needed = header_length + num_secret_bits

if total_bits_needed > len(carrier):
    raise ValueError("Несущий файл слишком короткий для данного секретного сообщения.")


secret_length_array = np.array([num_secret_bits], dtype='>u4')
secret_length_bytes = secret_length_array.tobytes()
secret_length_bits = np.unpackbits(np.frombuffer(secret_length_bytes, dtype=np.uint8))

assert len(secret_length_bits) == header_length


encoded_carrier = np.copy(carrier)


for i in range(header_length):
    bit = secret_length_bits[i]
    encoded_carrier[i] = (encoded_carrier[i] & ~1) | bit


for i in range(num_secret_bits):
   encoded_carrier[header_length + i] = (encoded_carrier[header_length + i] & ~1) | secret_bits[i]


encoded_audio_path = "AUDIO/encoded_audio.wav"
sf.write(encoded_audio_path, encoded_carrier, sr)
print(f"Закодированный аудиофайл сохранён по пути: {encoded_audio_path}")
