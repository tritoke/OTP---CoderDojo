#!/usr/bin/env python
import random
import binascii

# seed the random number generator so we get the same result each time
### maybe get them to generate the seed from a password
### if they get through everything really fast
random.seed(42)

def generate_pad(message: bytes) -> bytes:
    """
    Generates the One Time Pad (OTP) to be used for encrypting the message.

    Arguments:
    message: bytes - the message to generate a pad for

    Returns:
    bytes - the randomly generated pad as a hex string

    i.e. a pad of [0x01, 0x02, 0xFE] would be b"0102FE"

    this is done to make printing the pad / encrypted data easier
    """

    # store the padding data in a list while we create it
    # this lets us append easily which is harder with a bytes object
    pad = []
    for i in range(len(message)):
        # for each character of the message add a new random number
        # between 0 and 255 for each character in the input
        pad.append(random.randint(0, 255))

    # convert the pad to bytes and then to its hex representation
    return binascii.hexlify(bytes(pad))

def encrypt(message: bytes, pad: bytes) -> bytes:
    """
    Performs the encryption between the message and pad.

    Arguments:
    message: bytes - the message to encrypt, raw bytes not in hex
    pad: bytes - the pad to encrypt with, hex form

    Returns: bytes - the encrypted message
    """
    
    # take the pad out of hex form
    pad = binascii.unhexlify(pad)

    # make sure the message and pad are the same length
    assert len(message) == len(pad)

    encrypted = []
    for m, p in zip(message, pad):
        # iterate through the message and pad taking the
        # exclusive or of each pair of bytes in the message and pad
        encrypted.append(m ^ p)

    # return the encrypted message in hex form
    return binascii.hexlify(bytes(encrypted))

def decrypt(encrypted, pad):
    """
    Performs the encryption between the message and pad.

    Arguments:
    encrypted: bytes - the encrypted text to decrypt, hex form
    pad:       bytes - the pad to decrypt with, hex form

    Returns: bytes - the decrypted message
    """
    # take the encrypted text out of hex form
    # so that it can be processed by encrypt
    encrypted = binascii.unhexlify(encrypted)
    
    # re-use the encrypt function to decrypt the message
    ### interesting point, the pad and encrypted text can actually
    ### be swapped here to have the same effect as XOR is commutative
    decrypted = encrypt(encrypted, pad)

    # return the decrypted message as raw bytes
    return binascii.unhexlify(decrypted)


message = input("Enter the message to encrypt: ")

# encode message into a bytes object
message = message.encode()

# generate the pad and encrypt the message
pad = generate_pad(message)
encrypted = encrypt(message, pad)

# decrypt the message again with the pad
decrypted = decrypt(encrypted, pad)

# print everything out
print(f"Original message:  {message.decode()}")
print(f"One Time Pad:      {pad.decode()}")
print(f"Encrypted message: {encrypted.decode()}")
print(f"Decrypted message: {decrypted.decode()}")

assert message == decrypted
