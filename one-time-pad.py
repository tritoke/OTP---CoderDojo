#!/usr/bin/env python
import random
import binascii

random.seed(42)

def generate_pad(message):
    pad = []
    for i in range(len(message)):
        pad.append(random.randint(0, 255))

    return binascii.hexlify(bytes(pad))

def encrypt(message, pad):
    pad = binascii.unhexlify(pad)

    encrypted = []
    for m, p in zip(message, pad):
        encrypted.append(m ^ p)

    return binascii.hexlify(bytes(encrypted))

def decrypt(encrypted, pad):
    encrypted = binascii.unhexlify(encrypted)
    
    decrypted = encrypt(encrypted, pad)

    return binascii.unhexlify(decrypted)

message = b"Hi my name is Sam and this is a message!"

pad = generate_pad(message)
encrypted = encrypt(message, pad)

decrypted = decrypt(encrypted, pad)

print(f"Original message:  {message}")
print(f"One Time Pad:      {pad}")
print(f"Encrypted message: {encrypted}")
print(f"Decrypted message: {decrypted}")
