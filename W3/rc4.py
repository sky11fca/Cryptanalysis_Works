import os
import random
from collections import Counter


def ksa(key):
    key_len = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def prg(S, nr_bytes):
    i = 0
    j = 0
    keystream = bytearray()
    S_copy = list(S)
    for _ in range(nr_bytes):
        i = (i + 1) % 256
        j = (j + S_copy[i]) % 256
        S_copy[i], S_copy[j] = S_copy[j], S_copy[i]
        t = (S_copy[i] + S_copy[j]) % 256
        keystream.append(S_copy[t])
    return keystream


def encrypt(key, plaintext):
    S = ksa(key)
    keystream = prg(S, len(plaintext))
    return bytes(p ^ k for p, k in zip(plaintext, keystream))


def decrypt(key, ciphertext):
    return encrypt(key, ciphertext)


# Bias Confirmation of the Second Byte


def second_byte_bias_confirmation(nr_samples=100_000, key_len=16):
    second_bytes = []

    for _ in range(nr_samples):
        key = os.urandom(key_len)

        S = ksa(key)
        keystream = prg(S, 2)

        second_bytes.append(keystream[1])

    counts = Counter(second_bytes)
    zero_count = counts.get(0, 0)

    empirical_prob = zero_count / nr_samples

    uniform_prob = 1 / 256
    mantin_shamir_prob = 2 / 256

    print("\n--- Results ---")
    print(f"Total Samples: {nr_samples:,}")
    print(f"Occurrences of 0 at byte 2: {zero_count:,}")
    print(
        f"Empirical Probability:      {empirical_prob:.6f} ({
            empirical_prob * 100:.3f}%)"
    )
    print(f"Expected Uniform Prob:      {uniform_prob:.6f} ({uniform_prob * 100:.3f}%)")
    print(
        f"Mantin-Shamir Theoretical:  {mantin_shamir_prob:.6f} ({
            mantin_shamir_prob * 100:.3f}%)"
    )


# RC4 WEP implementation and FMS attack


def wep_ksa(iv, secret_key):
    full_key = bytearray(iv) + bytearray(secret_key)
    key_len = len(full_key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + full_key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def first_byte_prg(S):
    i = 0
    j = 0
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    t = (S[i] + S[j]) % 256
    return S[t]


def example_wep_packet(secret_key, iv):
    S = wep_ksa(iv, secret_key)
    first_byte = first_byte_prg(S)
    return first_byte


def fms_attack(secret_key, nr_packets=5000):
    votes = Counter()

    for _ in range(nr_packets):
        X = random.randint(0, 255)
        iv = bytes([3, 255, X])

        z = example_wep_packet(secret_key, iv)

        S = list(range(256))
        j = 0
        key = list(iv)

        # Step i = 0
        j = (j + S[0] + key[0]) % 256
        S[0], S[j] = S[j], S[0]

        # Step i = 1
        j = (j + S[1] + key[1]) % 256
        S[1], S[j] = S[j], S[1]

        # Step i = 2
        j = (j + S[2] + key[2]) % 256
        S[2], S[j] = S[j], S[2]

        try:
            s_inv_z = S.index(z)
            candidate_byte = (s_inv_z - j - S[3]) % 256
            votes[candidate_byte] += 1
        except ValueError:
            continue

    most_common_byte, frequency = votes.most_common(1)[0]
    print(
        f"[*] Attack complete. Winning byte: 0x{most_common_byte:02X} with {
            frequency
        } votes."
    )
    return most_common_byte


if __name__ == "__main__":
    plaintext = b"Sup Browskis! :3 My Enrique is shrinking at the moment"
    key = b"ENRIQUE"

    ciphertext = encrypt(key, plaintext)
    decrypted = decrypt(key, ciphertext)

    print(f"Plaintext:  {plaintext}")
    print(f"Ciphertext: {ciphertext.hex()}")
    print(f"Decrypted:  {decrypted}\n")

    second_byte_bias_confirmation(nr_samples=200_000)

    print("Begin The FMS attack")

    secret_key = b"\x42\xab\xcd\xef\x12"

    print(f"Target Secret Key (Hidden): {secret_key}")
    print(f"Actual First Byte:          0x{secret_key[0]:02X} ({secret_key[0]})")

    # Run attack to recover the first byte
    recovered_byte = fms_attack(secret_key, nr_packets=10000)

    print("\nResult Verification:")
    print(f"Recovered First Byte: 0x{recovered_byte:02X}")
    print(f"Match: {recovered_byte == secret_key[0]}")
