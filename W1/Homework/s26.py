"""
Substitution cipher Cryptanalysis (S(26))

1. First we analyse the unigraphs: In the english alphabet,
most frequent letter is E, the second most frequent letter is T,
with that information, we find the 2 most frequent letters in the ciphertext
that would be pi(E) and pi(T)

2. Trigraph analysis: Given pi(E) and pi(T), we find the most frequent
character that would be pi(H), this allows finding ciphertext equivalent of
the trigraph THE

3. Digraph analysis: Knowing equivalent of TH,
we can also deduce the TO equivalent

4. We follow finding based of digraphs,
multigraphs in finding permutation equivalent of: N, I, R, A, S, G, D, F. L

5. In case of Multigraphs (L), a special tally mechanism is imposed

6. Partial decryption:
We can partially deduce the permutation and decipher the text.

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


def tally_pattern(ciphertext: str, before: list, after: list) -> dict:
    tally = {c: 0 for c in string.ascii_uppercase}
    lb, la = len(before), len(after)

    if lb + la == 0:
        return tally
    for i in range(len(ciphertext) - lb - la):
        if ciphertext[i : i + lb] == "".join(before) and ciphertext[
            i + lb + 1 : i + lb + 1 + la
        ] == "".join(after):
            tally[ciphertext[i + lb]] += 1
    return tally


def deduce_from_pattern(
    ciphertext: str, before: list, after: list, excluded: set
) -> tuple:
    tally = tally_pattern(ciphertext, before, after)
    best, best_count = "?", 0
    for c in string.ascii_uppercase:
        if c not in excluded and tally[c] > best_count:
            best, best_count = c, tally[c]
    return best, best_count


def tally_doubled_after(ciphertext: str, before: list) -> dict:
    tally = {c: 0 for c in string.ascii_uppercase}
    lb = len(before)
    for i in range(len(ciphertext) - lb - 2):
        if (
            ciphertext[i : i + lb] == "".join(before)
            and ciphertext[i + lb] == ciphertext[i + lb + 1]
        ):
            tally[ciphertext[i + lb]] += 1
    return tally


def run_rules(ciphertext: str, e_cipher: str, t_cipher: str):

    keymap = {e_cipher: "E", t_cipher: "T"}
    log = [
        ("E", e_cipher, "unigraph rank 1 or 2 (English: E)", 0),
        ("T", t_cipher, "unigraph rank 1 or 2 (English: T)", 0),
    ]

    def excluded():
        return set(keymap.keys())

    def add(plain, cipher, evidence, count):
        if cipher == "?":
            return
        keymap[cipher] = plain
        log.append((plain, cipher, evidence, count))

    T_c, E_c = t_cipher, e_cipher

    # Finding H
    c, n = deduce_from_pattern(ciphertext, [T_c], [E_c], excluded())
    add("H", c, "middle of trigraph T?E (THE)", n)
    H_c = next((k for k, v in keymap.items() if v == "H"), None)

    # Finding O
    c, n = deduce_from_pattern(ciphertext, [T_c], [], excluded())
    add("O", c, "letter after digraph T? (TO)", n)

    # Finding N
    c, n = deduce_from_pattern(ciphertext, [E_c], [T_c], excluded())
    add("N", c, "middle of trigraph E?T (ENT)", n)
    N_c = next((k for k, v in keymap.items() if v == "N"), None)

    # Finding I
    c, n = deduce_from_pattern(ciphertext, [], [N_c], excluded())
    add("I", c, "letter before digraph ?N (IN)", n)
    I_c = next((k for k, v in keymap.items() if v == "I"), None)

    # Finding R
    c, n = deduce_from_pattern(ciphertext, [], [E_c], excluded())
    add("R", c, "letter before digraph ?E (RE)", n)
    R_c = next((k for k, v in keymap.items() if v == "R"), None)

    # Finding A
    H_c = next((k for k, v in keymap.items() if v == "H"), None)
    c, n = deduce_from_pattern(ciphertext, [T_c, H_c], [], excluded())
    add("A", c, "letter after trigraph TH? (THA)", n)
    A_c = next((k for k, v in keymap.items() if v == "A"), None)

    # Finding S
    c, n = deduce_from_pattern(ciphertext, [E_c], [], excluded())
    add("S", c, "letter after digraph E? (ES)", n)
    S_c = next((k for k, v in keymap.items() if v == "S"), None)

    # Finding G
    c, n = deduce_from_pattern(ciphertext, [I_c, N_c], [], excluded())
    add("G", c, "letter after trigraph IN? (ING)", n)

    # Finding D
    c, n = deduce_from_pattern(ciphertext, [A_c, N_c], [], excluded())
    add("D", c, "letter after trigraph AN? (AND)", n)

    # Finding O
    O_c = next((k for k, v in keymap.items() if v == "O"), None)
    c, n = deduce_from_pattern(ciphertext, [], [O_c], excluded())
    add("F", c, "letter before digraph ?O (OF)", n)

    # Finding L
    tally = tally_doubled_after(ciphertext, [A_c])
    best, best_count = "?", 0
    for ch in string.ascii_uppercase:
        if ch not in excluded() and tally[ch] > best_count:
            best, best_count = ch, tally[ch]
    add("L", best, "doubled pair after multigraph A?? (ALL)", best_count)

    return keymap, log


def decrypt(ciphertext: str, keymap: dict) -> str:
    """pi = RPI(ci) if RPI(ci).isalpha() else '.'"""
    return "".join(keymap.get(c, ".") for c in ciphertext)


def verify_multigraphs(ciphertext: str, keymap: dict):
    plain_to_cipher = {v: k for k, v in keymap.items()}
    multigraphs = [
        "THE",
        "ENT",
        "ING",
        "AND",
        "TION",
        "THAT",
        "ALL",
        "ATION",
        "THERE",
        "WITHIN",
    ]
    results = []
    for mg in multigraphs:
        if all(ch in plain_to_cipher for ch in mg):
            image = "".join(plain_to_cipher[ch] for ch in mg)
            count = ciphertext.count(image)
            results.append((mg, image, count))
    return results


def score_keymap(ciphertext: str, keymap: dict) -> int:
    plain_to_cipher = {v: k for k, v in keymap.items()}
    total = 0
    for mg in ["THE", "ENT", "ING", "AND"]:
        if all(ch in plain_to_cipher for ch in mg):
            image = "".join(plain_to_cipher[ch] for ch in mg)
            total += ciphertext.count(image)
    return total


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

    hypotheses = [
        (freq[0][0], freq[1][0]),  # E = rank 1, T = rank 2
        (freq[1][0], freq[0][0]),
    ]  # E = rank 2, T = rank 1

    # Run the cascade for the first hypothesis; if the alternative
    # scores better on multigraph evidence, keep that instead.
    e_c, t_c = hypotheses[0]
    keymap, log = run_rules(ciphertext, e_c, t_c)
    best_score = score_keymap(ciphertext, keymap)
    print(f"hypothesis E={e_c}, T={t_c}: multigraph evidence = {best_score}")

    e_c, t_c = hypotheses[1]
    alt_keymap, alt_log = run_rules(ciphertext, e_c, t_c)
    alt_score = score_keymap(ciphertext, alt_keymap)
    print(f"hypothesis E={e_c}, T={t_c}: multigraph evidence = {alt_score}")
    if alt_score > best_score:
        keymap, log = alt_keymap, alt_log

    print("\nDeduction log:")
    print("| PLAIN | CIPHER | EVIDENCE | COUNT |")
    for plain, cipher, evidence, count in log:
        print(f"| {plain} | {cipher} | {evidence} | {count} |")

    print(
        f"\nAssumpted Keymapping: "
        f"{''.join(keymap.get(c, '.') for c in string.ascii_uppercase)}"
    )

    # Partially decrypting the cipher
    partially_decrypted = decrypt(ciphertext, keymap)
    print(f"Partially Decrypted Text:\n{partially_decrypted}")

    # Multigraph verification
    print("\nMultigraph verification (found in ciphertext):")
    print("| PLAIN MULTIGRAPH | CIPHER IMAGE | COUNT |")
    for mg, image, count in verify_multigraphs(ciphertext, keymap):
        print(f"| {mg} | {image} | {count} |")

    # Statistics
    deciphered = sum(1 for c in partially_decrypted if c != ".")
    correct = sum(1 for i, c in enumerate(partially_decrypted) if c == plaintext[i])
    known = len(keymap)
    correct_deductions = sum(
        1 for c_cipher, p in keymap.items() if key_alphabet[p] == c_cipher
    )

    print(f"\nDeciphered characters: {deciphered}")
    print(f"Correct Decryption: {correct}")
    print(f"Key components deduced: {known}/26 ({correct_deductions} correct)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
