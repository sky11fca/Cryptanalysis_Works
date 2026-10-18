"""
Substitution cipher Cryptanalysis (S(26))

1. First we analyse the unigraphs: In the english alphabet, most frequent letter is E, the second most frequent letter is T, with that information, we find the 2 most frequent letters in the ciphertext that would be pi(E) and pi(T)

2. Trigraph analysis: Given pi(E) and pi(T), we find the most frequent character that would be pi(H), this allows finding ciphertext equivalent of the trigraph THE

3. Digraph analysis: Knowing equivalent of TH, we can also deduce the TO equivalent

4. Partial decryption: We can partially deduce the permutation and decipher the text.

"""

import random
import string
import sys

ALPHABET_SIZE = 26


def char_to_int(c: str) -> int:
    return ord(c) - ord("A")


def int_to_char(i: int) -> str:
    return chr(i + ord("A"))


def preprocess(buffer: str) -> str:
    return "".join(c.upper() for c in buffer if c.isalpha())


def encrypt(plaintext: str, key_alpha: dict) -> str:
    """ci = PI(pi)"""
    return "".join(key_alpha[c] for c in plaintext)


def find_top_unigraphs(ciphertext: str):
    """Finding the top 2 unigraphs of the ciphertext"""
    counts = {
        c: 0 for c in string.ascii_uppercase
    }  # <- string.ascii_upercase: Special string of UPPER CASE characters
    for c in ciphertext:
        counts[c] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def deduce_h(ciphertext: str, e_cipher: str, t_cipher: str) -> str:
    """Finding the pi(H)"""
    tally_middle = {c: 0 for c in string.ascii_uppercase}
    for i in range(len(ciphertext) - 2):
        if ciphertext[i] == t_cipher and ciphertext[i + 2] == e_cipher:
            tally_middle[ciphertext[i + 1]] += 1

    best, best_cnt = "?", 0

    for c in string.ascii_uppercase:
        if c not in (t_cipher, e_cipher) and tally_middle[c] > best_cnt:
            best = c
            best_cnt = tally_middle[c]

    return best


def deduce_o(ciphertext: str, e_cipher: str, t_cipher: str, h_cipher: str) -> str:
    """Finding the pi(O)"""
    tally_second = {c: 0 for c in string.ascii_uppercase}
    for i in range(len(ciphertext) - 1):
        if ciphertext[i] == t_cipher:
            tally_second[ciphertext[i + 1]] += 1

    best, best_cnt = "?", 0

    for c in string.ascii_uppercase:
        if c not in (t_cipher, e_cipher, h_cipher) and tally_second[c] > best_cnt:
            best = c
            best_cnt = tally_second[c]

    return best


def decrypt(ciphertext: str, keymap: dict) -> str:
    """pi = PI(ci) if PI(ci).isalpha() else '.'"""
    return "".join(keymap.get(c, ".") for c in ciphertext)


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "./example.txt"
    try:
        with open(path, "r") as f:
            buffer = f.read()
    except OSError as e:
        print(f"open: {e}")
        return 1

    plaintext = preprocess(buffer)

    print(f"our plaintext:\n{plaintext}")

    permutated = list(string.ascii_uppercase)
    random.shuffle(permutated)
    key_alphabet = dict(zip(string.ascii_uppercase, permutated))

    print(f"Permuteted alphabet: {''.join(permutated)}")

    # encrypting

    ciphertext = encrypt(plaintext, key_alphabet)
    print(f"Out ciphertext:\n{ciphertext}")

    # Finding the ciphertext frequency:

    freq = find_top_unigraphs(ciphertext)

    print("| CHAR | COUNT |")
    for c, n in freq:
        print(f"| {c} | {n} |")

    e_cipher = freq[0][0]
    t_cipher = freq[1][0]

    h_cipher = deduce_h(ciphertext, e_cipher, t_cipher)
    o_cipher = deduce_o(ciphertext, e_cipher, t_cipher, h_cipher)

    keymap = {}
    keymap[e_cipher] = "E"
    keymap[t_cipher] = "T"
    keymap[h_cipher] = "H"
    keymap[o_cipher] = "O"

    print(
        f"Assumped Keymap: {
            ''.join(keymap.get(c, '.') for c in string.ascii_uppercase)
        }"
    )

    partialy_decrypted = decrypt(ciphertext, keymap)
    print(f"Our ciphertext\n{partialy_decrypted}")

    deciphered = sum(1 for c in partialy_decrypted if c != ".")
    correct = sum(1 for i, c in enumerate(partialy_decrypted) if c == plaintext[i])

    print(f"Deciphered {deciphered} characters")
    print(f"with {correct} correct guesses")

    return 0


if __name__ == "__main__":
    sys.exit(main())
