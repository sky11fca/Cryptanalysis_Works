#include <fcntl.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define ALPHABET_SIZE 26

typedef struct {
  char character;
  int count;
} CipherFreq;

int char_to_int(char c) { return c - 'A'; }

char int_to_char(int i) { return i + 'A'; }

void encrypt(char *plaintext, char *ciphertext, int size, char *key_alphabet) {
  for (int i = 0; i < size; i++) {
    ciphertext[i] = key_alphabet[char_to_int(plaintext[i])];
  }
  ciphertext[size] = '\0';
}

void find_top_unigraph(char *ciphertext, CipherFreq *freq_array) {
  // tally and sort by most frequent appearance

  // Tally Phase

  for (int i = 0; ciphertext[i] != '\0'; i++) {
    freq_array[char_to_int(ciphertext[i])].count++;
  }

  // Sorting

  for (int i = 0; i < ALPHABET_SIZE - 1; i++) {
    for (int j = i + 1; j < ALPHABET_SIZE; j++) {
      if (freq_array[i].count < freq_array[j].count) {
        CipherFreq aux = freq_array[i];
        freq_array[i] = freq_array[j];
        freq_array[j] = aux;
      }
    }
  }
}

char deduce_h(char *ciphertext, int size, char E_cipher, char T_cipher) {
  // Identifying PI(H), requied for finding PI(T), ? PI(E) for the THE trigraph

  // Tally only characters that appear in the middle of PI(T) and PI(E)
  int middle_tally[ALPHABET_SIZE] = {0};

  for (int i = 0; i <= size - 3; i++) {
    if (ciphertext[i] == T_cipher && ciphertext[i + 2] == E_cipher) {
      char middle = ciphertext[i + 1];
      middle_tally[middle - 'A']++;
    }
  }

  char H_cipher = '?';
  int max_cnt = 0;

  for (int i = 0; i < ALPHABET_SIZE; i++) {
    char candidate = 'A' + i;
    if (candidate != T_cipher && candidate != E_cipher) {
      if (middle_tally[i] > max_cnt) {
        max_cnt = middle_tally[i];
        H_cipher = 'A' + i;
      }
    }
  }

  return H_cipher;
}

char deduce_o(char *ciphertext, int size, char T_cipher, char H_cipher,
              char E_cipher) {
  // Identifying PI(O) required for finding the closest to TO digraph

  // Tally only characters that appear after PI(T)
  int after_tally[ALPHABET_SIZE] = {0};

  for (int i = 0; i <= size - 2; i++) {
    if (ciphertext[i] == T_cipher) {
      char after = ciphertext[i + 1];
      after_tally[after - 'A']++;
    }
  }

  char O_cipher = '?';
  int max_cnt = 0;

  for (int i = 0; i < ALPHABET_SIZE; i++) {
    char candidate = 'A' + i;
    if (candidate != H_cipher && candidate != T_cipher &&
        candidate != E_cipher) {
      if (after_tally[i] > max_cnt) {
        max_cnt = after_tally[i];
        O_cipher = 'A' + i;
      }
    }
  }

  return O_cipher;
}

void print_partial_text(char *ciphertext, char *keymap,
                        char *partially_decrypted) {

  for (int i = 0; ciphertext[i] != '\0'; i++) {
    char c = ciphertext[i];
    if (keymap[char_to_int(c)] != '.') {
      partially_decrypted[i] = keymap[char_to_int(c)];
    } else
      partially_decrypted[i] = '.';
  }
}

int main(void) {
  int fd;
  if ((fd = open("./example.txt", O_RDONLY)) == -1) {
    perror("open");
    exit(1);
  }

  int buff_size = lseek(fd, 0, SEEK_END);
  lseek(fd, 0, SEEK_SET);

  char buffer[buff_size];
  memset(buffer, 0, buff_size);

  if (read(fd, buffer, buff_size) == -1) {
    perror("read");
    exit(1);
  }

  close(fd);

  buffer[buff_size - 1] = '\0';
  buff_size--;

  printf("Our plaintext:\n%s\n", buffer);

  // Generating a random Aplhabet Permutation

  struct timespec ts;
  timespec_get(&ts, TIME_UTC);

  srand(ts.tv_sec ^ ts.tv_nsec);

  char key_alphabet[ALPHABET_SIZE + 1];
  memset(key_alphabet, 0, ALPHABET_SIZE);

  for (int i = 0; i < ALPHABET_SIZE; i++) {
    key_alphabet[i] = 'A' + i;
  }
  key_alphabet[ALPHABET_SIZE] = '\0';

  // Scramble

  for (int i = ALPHABET_SIZE - 1; i > 0; i--) {
    int j = rand() % (i + 1);

    char aux = key_alphabet[i];
    key_alphabet[i] = key_alphabet[j];
    key_alphabet[j] = aux;
  }

  printf("Permutated Alphabet Key: %s\n", key_alphabet);

  // Encrypting
  char ciphertext[buff_size];
  encrypt(buffer, ciphertext, buff_size, key_alphabet);

  printf("Our ciphertext:\n%s\n", ciphertext);

  // Cryptanalysis

  // First we find the most common digit
  CipherFreq *freq_array = malloc(ALPHABET_SIZE * sizeof(CipherFreq));
  memset(freq_array, 0, ALPHABET_SIZE * sizeof(CipherFreq));

  // Initializing the freq aray:

  for (int i = 0; i < ALPHABET_SIZE; i++) {
    freq_array[i].character = 'A' + i;
    freq_array[i].count = 0;
  }

  find_top_unigraph(ciphertext, freq_array);

  printf("| CHAR | FREQ |\n");
  for (int i = 0; i < ALPHABET_SIZE; i++) {
    printf("| %c | %d |\n", freq_array[i].character, freq_array[i].count);
  }

  // Then we analyse appearance of the trigraph THE
  const char E_cipher = freq_array[0].character;
  const char T_cipher = freq_array[1].character;

  printf("Most Likely character to be E is: %c\n", E_cipher);
  printf("Most Likely character to be T is: %c\n", T_cipher);

  char H_cipher = deduce_h(ciphertext, buff_size, E_cipher, T_cipher);
  printf("Most Likely character to be H is: %c\n", H_cipher);

  // Then analyse the appearance of digraph TO
  char O_cipher = deduce_o(ciphertext, buff_size, T_cipher, H_cipher, E_cipher);
  printf("Most Likely character to be O is: %c\n", O_cipher);

  // Last we make a assumption of finding the shifting key and partially break
  // the cipher

  char assumpted_keymap[ALPHABET_SIZE + 1];
  for (int i = 0; i < ALPHABET_SIZE; i++) {
    assumpted_keymap[i] = '.';
  }
  assumpted_keymap[ALPHABET_SIZE] = '\0';

  // Adding the discovered key bits
  assumpted_keymap[char_to_int(E_cipher)] = 'E';
  assumpted_keymap[char_to_int(T_cipher)] = 'T';
  assumpted_keymap[char_to_int(H_cipher)] = 'H';
  assumpted_keymap[char_to_int(O_cipher)] = 'O';

  printf("Assumpted Keymapping: %s\n", assumpted_keymap);

  // Partially Decrypting the cipher

  char partially_decrypted[buff_size];

  print_partial_text(ciphertext, assumpted_keymap, partially_decrypted);

  partially_decrypted[buff_size] = '\0';

  printf("Our Plaintext:\n%s\n", partially_decrypted);

  // Other statistics:

  int correct_characters = 0, deciphered_characters = 0;

  for (int i = 0; partially_decrypted[i] != 0; i++) {
    if (partially_decrypted[i] != '.') {
      deciphered_characters++;
    }

    if (partially_decrypted[i] == buffer[i]) {
      correct_characters++;
    }
  }

  printf("Deciphered characters: %d\n", deciphered_characters);
  printf("Correct Decryption: %d\n", correct_characters);

  // counting correct occurences of THE
  int the_occurences = 0;

  for (int i = 0; i <= buff_size - 3; i++) {
    if (partially_decrypted[i] == 'T' && partially_decrypted[i + 1] == 'H' &&
        partially_decrypted[i + 2] == 'E') {
      if (partially_decrypted[i] == buffer[i] &&
          partially_decrypted[i + 1] == buffer[i + 1] &&
          partially_decrypted[i + 2] == buffer[i + 2]) {
        the_occurences++;
      }
    }
  }

  printf("Correct occurences of THE: %d\n", the_occurences);

  // counting occurences of TO

  int to_occurences = 0;

  for (int i = 0; i <= buff_size - 2; i++) {
    if (partially_decrypted[i] == 'T' && partially_decrypted[i + 1] == 'O') {
      if (partially_decrypted[i] == buffer[i] &&
          partially_decrypted[i + 1] == buffer[i + 1]) {
        to_occurences++;
      }
    }
  }

  printf("Correct occurences of TO: %d\n", to_occurences);
  free(freq_array);
  return 0;
}
