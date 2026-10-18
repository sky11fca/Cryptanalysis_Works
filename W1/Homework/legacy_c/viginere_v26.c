#include <ctype.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ALPHABET_SIZE 26
#define BUFFER_SIZE 8196
#define KEY_SIZE 256
#define CHAR_TO_INT(c) (c - 'A')
#define INT_TO_CHAR(i) (i + 'A')
#define IC_THRESHOLD 0.055f
#define MAX_KEY_LENGTH 20

static const float ENGLISH_FREQ[ALPHABET_SIZE] = {
    0.082f, 0.015f, 0.028f, 0.043f, 0.127f, 0.022f, 0.020f, 0.061f, 0.070f,
    0.002f, 0.008f, 0.040f, 0.024f, 0.067f, 0.075f, 0.019f, 0.001f, 0.060f,
    0.063f, 0.091f, 0.028f, 0.010f, 0.023f, 0.020f, 0.001f, 0.001f};

int preprocess(char *input, char *output) {
  int size = 0;
  for (int i = 0; input[i] != '\0'; i++) {
    if (isalpha(input[i])) {
      output[size++] = toupper(input[i]);
    }
  }

  output[size] = '\0';
  return size;
}

void encrypt(char *plaintext, char *key, char *ciphertext) {
  int key_size = strlen(key);

  for (int i = 0; plaintext[i] != '\0'; i++) {
    // ci = (pi + ki) MOD 26
    int result = CHAR_TO_INT(plaintext[i]) + CHAR_TO_INT(key[i % key_size]);
    ciphertext[i] = INT_TO_CHAR(result % ALPHABET_SIZE);
  }
  ciphertext[strlen(plaintext)] = '\0';
}

void decrypt(char *ciphertext, char *key, char *plaintext) {
  int key_size = strlen(key);
  for (int i = 0; ciphertext[i] != '\0'; i++) {
    // pi = (ci - ki) MOD 26
    int result = CHAR_TO_INT(ciphertext[i]) - CHAR_TO_INT(key[i % key_size]);
    if (result < 0) {
      result += ALPHABET_SIZE;
    }
    plaintext[i] = INT_TO_CHAR(result % ALPHABET_SIZE);
  }
  plaintext[strlen(ciphertext)] = '\0';
}

float ic(char *ciphertext, int offset, int step) {
  // computing the frequency array of all characters:

  int freq_arr[ALPHABET_SIZE] = {0};
  int n = 0;

  for (int i = offset; ciphertext[i] != '\0'; i += step) {
    freq_arr[CHAR_TO_INT(ciphertext[i])]++;
    n++;
  }
  if (n < 2)
    return 0.0f;
  float result = .0f;
  for (int i = 0; i < ALPHABET_SIZE; i++) {
    result += (float)(freq_arr[i] * (freq_arr[i] - 1)) / ((float)n * (n - 1));
  }
  return result;
}

float mic(char *ciphertext, int offset, int step, int s) {

  int freq_arr[ALPHABET_SIZE] = {0};
  int n = 0;

  for (int i = offset; ciphertext[i] != '\0'; i += step) {
    freq_arr[CHAR_TO_INT(ciphertext[i])]++;
    n++;
  }
  if (n == 0)
    return 0.0f;
  float result = .0f;

  for (int i = 0; i < ALPHABET_SIZE; i++) {
    result += ENGLISH_FREQ[i] *
              ((float)freq_arr[(i - s + ALPHABET_SIZE) % ALPHABET_SIZE] / n);
  }
  return result;
}

int find_key_length(char *ciphertext) {
  int len = strlen(ciphertext);
  int max_m = len < MAX_KEY_LENGTH * 150 ? len / 150 : MAX_KEY_LENGTH;
  for (int m = 1; m <= max_m; m++) {
    float sum = .0f;
    for (int j = 0; j < m; j++) {
      sum += ic(ciphertext, j, m);
    }
    float avg = sum / m;
    if (m > 1 && avg >= IC_THRESHOLD) {
      return m;
    }
  }
  return -1;
}

void find_key(char *ciphertext, int m, char *key) {
  for (int j = 0; j < m; j++) {
    int best_s = 0;
    float best_mic = -1.0f;
    for (int s = 0; s < ALPHABET_SIZE; s++) {
      float value = mic(ciphertext, j, m, s);
      if (value > best_mic) {
        best_mic = value;
        best_s = s;
      }
    }
    key[j] = INT_TO_CHAR((ALPHABET_SIZE - best_s) % ALPHABET_SIZE);
  }
  key[m] = '\0';
}

float chi_squared(char *text) {
  int freq_arr[ALPHABET_SIZE] = {0};
  int n = 0;
  for (int i = 0; text[i] != '\0'; i++) {
    freq_arr[CHAR_TO_INT(text[i])]++;
    n++;
  }
  float result = .0f;
  for (int i = 0; i < ALPHABET_SIZE; i++) {
    float expected = ENGLISH_FREQ[i] * n;
    float diff = freq_arr[i] - expected;
    result += diff * diff / expected;
  }
  return result;
}

int find_full_key(char *ciphertext, int m, char *best_key) {
  int len = strlen(ciphertext);
  float best_score = 1e9f;

  char cand_key[KEY_SIZE];
  char decrypted[BUFFER_SIZE];

  for (int M = m; M <= MAX_KEY_LENGTH && len / M >= 150; M += m) {
    find_key(ciphertext, M, cand_key);
    decrypt(ciphertext, cand_key, decrypted);

    float score = chi_squared(decrypted);
    printf("candidate length %2d, key %-20s chi squared = %.1f\n", M, cand_key,
           score);

    if (score < best_score) {
      best_score = score;
      strcpy(best_key, cand_key);
    }
  }
  return strlen(best_key);
}

int main(void) {
  int fd = open("./example.txt", O_RDONLY);
  if (fd == -1) {
    perror("open");
    exit(EXIT_FAILURE);
  }

  int buff_size = lseek(fd, 0, SEEK_END);
  lseek(fd, 0, SEEK_SET);

  if (buff_size < 0 || buff_size >= BUFFER_SIZE) {
    fprintf(stderr, "File too large\n");
    close(fd);
    exit(EXIT_FAILURE);
  }

  char buffer[BUFFER_SIZE] = {0};

  if (read(fd, buffer, buff_size) == -1) {
    perror("read");
    exit(EXIT_FAILURE);
  }

  close(fd);
  buffer[buff_size] = '\0';

  // preprocessing

  char preprocessed_plaintext[buff_size];
  int plaintext_size = preprocess(buffer, preprocessed_plaintext);

  char key[KEY_SIZE] = {0};
  printf("Insert a Key: ");
  fgets(key, KEY_SIZE, stdin);
  int n = strlen(key);
  if (key[n - 1] == '\n')
    key[n - 1] = '\0';
  preprocess(key, key);

  printf("Plain Text:\n%s\n", preprocessed_plaintext);
  printf("Key: %s\n", key);

  char ciphertext[plaintext_size + 1];
  encrypt(preprocessed_plaintext, key, ciphertext);
  printf("Ciphertext:\n%s\n", ciphertext);

  int key_len = find_key_length(ciphertext);
  if (key_len == -1) {
    fprintf(stderr, "Key not found\n");
    exit(EXIT_FAILURE);
  }
  printf("Effective key length: %d\n", key_len);
  char recovered_key[KEY_SIZE];
  find_full_key(ciphertext, key_len, recovered_key);

  printf("Potential key length: %zu\n", strlen(recovered_key));
  printf("Recovered key: %s\n", recovered_key);

  char decrypted[plaintext_size + 1];
  decrypt(ciphertext, recovered_key, decrypted);
  printf("Decrypted Text:\n%s\n", decrypted);

  return EXIT_SUCCESS;
}
