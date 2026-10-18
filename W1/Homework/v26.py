"""
Viginere cipher cryptanalysis (V(26))

1. Computing the key length:
- for each coset y_{m, j}, the Index of Coincidence must be apporximatly equal to 0.065
    Index of Coincidence:
    IC(alpha) = sum_i f_i(f_i - 1) / (n(n-1)

2. Deducing the key:
    -for each coset j, we find s such that the mutual IC of the text and message shifted y_{m,j} with s is aproximately equal to 0.065
    - Then k_j = (26 - s) mod 26

3. Chi-square scores for multiple m instances  to pich the best m
"""

import string
import sys

ALPHABET_SIZE = 26
IC_THRESHOLD = 0.055
MAX_KEY_LENGTH = 20
MIN_CHARS_PER_COSET = 150
MIN_CHARS_PER_COSET_KEY = 50
MIC_EPSILON = 0.001

# English letter frequencies p_0 ... p_25
ENGLISH_FREQ = [
    0.082,
    0.015,
    0.028,
    0.043,
    0.127,
    0.022,
    0.020,
    0.061,
    0.070,
    0.002,
    0.008,
    0.040,
    0.024,
    0.067,
    0.075,
    0.019,
    0.001,
    0.060,
    0.063,
    0.091,
    0.028,
    0.010,
    0.023,
    0.020,
    0.001,
    0.001,
]

CHAR_TO_INT = {c: i for i, c in enumerate(string.ascii_uppercase)}
INT_TO_CHAR = string.ascii_uppercase


def preprocess(buffer: str) -> str:
    return "".join(c.upper() for c in buffer if c.isalpha())


def encrypt(plaintext: str, key: str) -> str:
    m = len(key)
    return "".join(
        INT_TO_CHAR[(CHAR_TO_INT[p] + CHAR_TO_INT[key[i % m]]) % ALPHABET_SIZE]
        for i, p in enumerate(plaintext)
    )


def decrypt(ciphertext: str, key: str) -> str:
    m = len(key)
    return "".join(
        INT_TO_CHAR[(CHAR_TO_INT[c] - CHAR_TO_INT[key[i % m]]) % ALPHABET_SIZE]
        for i, c in enumerate(ciphertext)
    )


def coset_frequency(ciphertext: str, offset: int, step: int):
    freq = [0] * ALPHABET_SIZE
    n = 0
    for i in range(offset, len(ciphertext), step):
        freq[CHAR_TO_INT[ciphertext[i]]] += 1
        n += 1
    return freq, n


def ic(ciphertext: str, offset: int, step: int) -> float:
    freq, n = coset_frequency(ciphertext, offset, step)
    if n < 2:
        return 0.0
    return sum(f * (f - 1) for f in freq) / (n * (n - 1))


def mic(ciphertext: str, offset: int, step: int, s: int) -> float:
    freq, n = coset_frequency(ciphertext, offset, step)
    if n < 2:
        return 0.0

    return sum(
        ENGLISH_FREQ[i] * freq[(i - s) % ALPHABET_SIZE] / n
        for i in range(ALPHABET_SIZE)
    )


def find_key_length(ciphertext: str) -> int:
    length = len(ciphertext)
    max_m = length // MIN_CHARS_PER_COSET
    max_m = min(max_m, MAX_KEY_LENGTH)

    for m in range(1, max_m + 1):
        avg = sum(ic(ciphertext, j, m) for j in range(m)) / m
        if m > 1 and avg >= IC_THRESHOLD:
            return m
    return -1


def find_key_for_length(ciphertext: str, m: int):
    """MIC test for a fixed candidate length m: for each coset j pick the
    shift s maximizing MIC, then k_j = (26 - s) mod 26.
    Returns (key, average peak MIC over the m cosets)."""
    key = []
    total = 0.0
    for j in range(m):
        best_s, best_value = 0, -1.0
        for s in range(ALPHABET_SIZE):
            value = mic(ciphertext, j, m, s)
            if value > best_value:
                best_s, best_value = s, value
        key.append(INT_TO_CHAR[(ALPHABET_SIZE - best_s) % ALPHABET_SIZE])
        total += best_value
    return "".join(key), total / m


def find_full_key(ciphertext: str, m: int) -> str:
    """Handle keys built from a shorter period, e.g. ABABABABAA or
    ABCABCABCABA.

    The IC test returns the smallest m whose cosets look like English
    (IC ~= 0.065). If the real key is an exact repetition of a shorter
    word (ABABAB...), that minimal m already decrypts everything
    correctly - the longer original is information-theoretically
    unrecoverable, since it produces the very same ciphertext.

    But if the real key only *almost* repeats (ABABABABAA,
    ABCABCABCABA), the cosets of the minimal m are mixtures: mostly one
    key letter plus a few contaminating letters. The MIC test then
    returns the majority letter and the deviating positions stay wrong.

    Remedy, using only the MIC: try every multiple of m as candidate
    length. A candidate whose cosets are pure English-like text peaks at
    MIC ~= 0.065; a mixed coset peaks lower. Keep the smallest candidate
    whose average peak MIC is within MIC_EPSILON of the best.
    """
    length = len(ciphertext)
    candidates = []

    M = m
    while M <= MAX_KEY_LENGTH and length // M >= MIN_CHARS_PER_COSET_KEY:
        cand_key, avg = find_key_for_length(ciphertext, M)
        candidates.append((M, cand_key, avg))
        M += m

    if not candidates:
        return ""

    best_avg = max(avg for _, _, avg in candidates)
    for _, cand_key, avg in candidates:  # candidates are in increasing M
        if avg >= best_avg - MIC_EPSILON:
            return cand_key
    return candidates[0][1]


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "./example.txt"
    try:
        with open(path, "r") as f:
            buffer = f.read()
    except OSError as e:
        print(f"open: {e}", file=sys.stderr)
        return 1

    # Preprocessing
    plaintext = preprocess(buffer)

    key = preprocess(input("Insert a Key: "))

    print(f"Plain Text:\n{plaintext}")
    print(f"Key: {key}")

    ciphertext = encrypt(plaintext, key)
    print(f"Ciphertext:\n{ciphertext}")

    key_len = find_key_length(ciphertext)
    if key_len == -1:
        print(f"Key not found", file=sys.stderr)
        return 1
    print(f"Effective key length: {key_len}")

    recovered_key = find_full_key(ciphertext, key_len)
    print(f"Potential key length {len(recovered_key)}")
    print(f"the key: {recovered_key}")

    decrypted = decrypt(ciphertext, recovered_key)

    print(f"Our Plaintext:\n{decrypted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
