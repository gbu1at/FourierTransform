import numpy as np
import soundfile as sf
import sys



_, encoded_audio_path = sys.argv
header_length = 32

_, sr = sf.read(encoded_audio_path)

encoded, _ = sf.read(encoded_audio_path, dtype='int16')

extracted_header_bits = []
for i in range(header_length):
    bit = encoded[i] & 1
    extracted_header_bits.append(int(bit))

secret_length_decoded = 0
for i in range(header_length):
    secret_length_decoded = (secret_length_decoded << 1) | extracted_header_bits[i]


extracted_secret_bits = []
for i in range(header_length, header_length + secret_length_decoded):
    bit = encoded[i] & 1
    extracted_secret_bits.append(bit)

extracted_secret_bytes = []
for i in range(0, len(extracted_secret_bits), 8):
    byte_bits = extracted_secret_bits[i:i+8]
    if len(byte_bits) < 8:
        byte_bits += [0] * (8 - len(byte_bits))
    byte = 0
    for bit in byte_bits:
        byte = (byte << 1) | bit
    extracted_secret_bytes.append(byte)

decoded_secret = np.frombuffer(bytes(extracted_secret_bytes), dtype=np.int16)

decoded_secret_path = "decoded_secret.wav"
sf.write(decoded_secret_path, decoded_secret, sr)
print(f"Декодированное секретное аудио сохранено по пути: {decoded_secret_path}")