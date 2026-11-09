IP = [
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    60,
    52,
    44,
    36,
    28,
    20,
    12,
    4,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    64,
    56,
    48,
    40,
    32,
    24,
    16,
    8,
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
]

IP_INV = [
    40,
    8,
    48,
    16,
    56,
    24,
    64,
    32,
    39,
    7,
    47,
    15,
    55,
    23,
    63,
    31,
    38,
    6,
    46,
    14,
    54,
    22,
    62,
    30,
    37,
    5,
    45,
    13,
    53,
    21,
    61,
    29,
    36,
    4,
    44,
    12,
    52,
    20,
    60,
    28,
    35,
    3,
    43,
    11,
    51,
    19,
    59,
    27,
    34,
    2,
    42,
    10,
    50,
    18,
    58,
    26,
    33,
    1,
    41,
    9,
    49,
    17,
    57,
    25,
]

E = [
    32,
    1,
    2,
    3,
    4,
    5,
    4,
    5,
    6,
    7,
    8,
    9,
    8,
    9,
    10,
    11,
    12,
    13,
    12,
    13,
    14,
    15,
    16,
    17,
    16,
    17,
    18,
    19,
    20,
    21,
    20,
    21,
    22,
    23,
    24,
    25,
    24,
    25,
    26,
    27,
    28,
    29,
    28,
    29,
    30,
    31,
    32,
    1,
]

P = [
    16,
    7,
    20,
    21,
    29,
    12,
    28,
    17,
    1,
    15,
    23,
    26,
    5,
    18,
    31,
    10,
    2,
    8,
    24,
    14,
    32,
    27,
    3,
    9,
    19,
    13,
    30,
    6,
    22,
    11,
    4,
    25,
]

S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]

PC1 = [
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    60,
    52,
    44,
    36,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    28,
    20,
    12,
    4,
]

PC2 = [
    14,
    17,
    11,
    24,
    1,
    5,
    3,
    28,
    15,
    6,
    21,
    10,
    23,
    19,
    12,
    4,
    26,
    8,
    16,
    7,
    27,
    20,
    13,
    2,
    41,
    52,
    31,
    37,
    47,
    55,
    30,
    40,
    51,
    45,
    33,
    48,
    44,
    49,
    39,
    56,
    34,
    53,
    46,
    42,
    50,
    36,
    29,
    32,
]

ROUNDS_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Helper Functions


def permute(bits: int, table: list[int], in_len: int) -> int:
    res = 0
    for pos in table:
        bit = (bits >> (in_len - pos)) & 1
        res = (res << 1) | bit
    return res


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big")


def int_to_bytes(n: int, length: int = 8) -> bytes:
    return n.to_bytes(length, byteorder="big")


# Key scheduler algorithm


def generate_round_keys(key_64: int) -> list[int]:
    pc1_val = permute(key_64, PC1, 64)
    c = (pc1_val >> 28) & 0x0FFFFFFF
    d = pc1_val & 0x0FFFFFFF

    subkeys = []
    for shift in ROUNDS_SHIFTS:
        c = ((c << shift) | (c >> (28 - shift))) & 0x0FFFFFFF
        d = ((d << shift) | (d >> (28 - shift))) & 0x0FFFFFFF
        cd = (c << 28) | d
        subkeys.append(permute(cd, PC2, 56))
    return subkeys


# DES Encryption and Decryption


def des_f(r_32: int, k_48: int) -> int:
    """DES Feistel f-function: Expansion -> XOR Key -> S-Boxes -> Permutation P."""
    expanded = permute(r_32, E, 32) ^ k_48
    sbox_out = 0

    for i in range(8):
        # Extract 6-bit chunk
        chunk = (expanded >> (42 - 6 * i)) & 0x3F
        row = ((chunk & 0x20) >> 4) | (chunk & 0x01)
        col = (chunk >> 1) & 0x0F
        val = S_BOXES[i][row][col]
        sbox_out = (sbox_out << 4) | val

    return permute(sbox_out, P, 32)


def des_process_block(block_64: int, subkeys: list[int]) -> int:
    """Atomic block processing through Initial Permutation, 16 rounds, and Inverse IP."""
    permuted = permute(block_64, IP, 64)
    left = (permuted >> 32) & 0xFFFFFFFF
    right = permuted & 0xFFFFFFFF

    for k in subkeys:
        new_right = left ^ des_f(right, k)
        left = right
        right = new_right

    # Inverted order of halves before final permutation: (R16, L16)
    pre_output = (right << 32) | left
    return permute(pre_output, IP_INV, 64)


def des_encrypt_block(plaintext_bytes: bytes, key_bytes: bytes) -> bytes:
    """Encrypts an 8-byte block using DES."""
    subkeys = generate_round_keys(bytes_to_int(key_bytes))
    ct_int = des_process_block(bytes_to_int(plaintext_bytes), subkeys)
    return int_to_bytes(ct_int, 8)


def des_decrypt_block(ciphertext_bytes: bytes, key_bytes: bytes) -> bytes:
    """Decrypts an 8-byte block using DES (reversed subkeys)."""
    subkeys = generate_round_keys(bytes_to_int(key_bytes))
    subkeys.reverse()
    pt_int = des_process_block(bytes_to_int(ciphertext_bytes), subkeys)
    return int_to_bytes(pt_int, 8)


# The 2DES algorithm


def double_des_encrypt(pt: bytes, k1: bytes, k2: bytes) -> bytes:
    """2DES encryption: C = E_k2(E_k1(M))."""
    return des_encrypt_block(des_encrypt_block(pt, k1), k2)


def double_des_decrypt(ct: bytes, k1: bytes, k2: bytes) -> bytes:
    """2DES decryption: M = D_k1(D_k2(C))."""
    return des_decrypt_block(des_decrypt_block(ct, k2), k1)


# The MiTM Attack


def set_odd_parity_byte(b: int) -> int:
    """Sets the least significant bit so that the byte has odd parity."""
    # Count bits in the top 7 bits
    b_7 = b & 0xFE
    parity = bin(b_7).count("1") % 2
    # If number of 1s is even, set LSB to 1; if odd, set LSB to 0
    return b_7 if parity == 1 else (b_7 | 1)


def make_parity_key(b: int) -> bytes:
    """Creates an 8-byte DES key of the form yyyyyyyy with valid odd parity."""
    p_byte = set_odd_parity_byte(b)
    return bytes([p_byte] * 8)


def mitm_attack_2des(pairs: list[tuple[bytes, bytes]]) -> tuple[bytes, bytes] | None:
    m0, c0 = pairs[0]
    lookup_table: dict[bytes, list[bytes]] = {}

    # Iterate through the 128 distinct 7-bit values (all valid odd-parity bytes)
    parity_keys = [make_parity_key(b << 1) for b in range(128)]

    for k1 in parity_keys:
        mid = des_encrypt_block(m0, k1)
        lookup_table.setdefault(mid, []).append(k1)

    for k2 in parity_keys:
        mid_target = des_decrypt_block(c0, k2)
        if mid_target in lookup_table:
            for k1 in lookup_table[mid_target]:
                if all(double_des_encrypt(m, k1, k2) == c for m, c in pairs[1:]):
                    return k1, k2
    return None


if __name__ == "__main__":
    print("=== 1. Validating Single DES with FIPS-46 Test Vector ===")
    pt = bytes.fromhex("0123456789ABCDEF")
    key = bytes.fromhex("133457799BBCDFF1")
    expected_ct = bytes.fromhex("85E813540F0AB405")

    encrypted = des_encrypt_block(pt, key)
    decrypted = des_decrypt_block(encrypted, key)

    print(f"Plaintext : {pt.hex().upper()}")
    print(f"Key       : {key.hex().upper()}")
    print(f"Ciphertext: {encrypted.hex().upper()}")
    print(f"Expected  : {expected_ct.hex().upper()}")
    assert encrypted == expected_ct, "DES Encryption test vector failed!"
    assert decrypted == pt, "DES Decryption test vector failed!"
    print("[+] DES encryption & decryption verified.\n")

    print("=== 2. Testing Meet-in-the-Middle Attack on 2DES ===")
    import os

    # Secret keys of form yyyyyyyy
    secret_k1 = make_parity_key(0x4A)
    secret_k2 = make_parity_key(0x9B)

    # Generate 3 known plaintext-ciphertext pairs
    known_pairs = []
    for _ in range(3):
        m = os.urandom(8)
        c = double_des_encrypt(m, secret_k1, secret_k2)
        known_pairs.append((m, c))

    print(f"Target Secret k1: {secret_k1.hex().upper()}")
    print(f"Target Secret k2: {secret_k2.hex().upper()}")

    recovered = mitm_attack_2des(known_pairs)
    if recovered:
        rec_k1, rec_k2 = recovered
        print(f"Found k1        : {rec_k1.hex().upper()}")
        print(f"Found k2        : {rec_k2.hex().upper()}")
        assert recovered == (secret_k1, secret_k2)
        print("[+] Meet-in-the-middle attack recovered both keys successfully.")
    else:
        print("[-] MITM Attack failed to find keys.")
