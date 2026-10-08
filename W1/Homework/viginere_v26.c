#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ALPHABET_SIZE 26
#define BUFFER_SIZE 1024
#define KEY_SIZE 256
#define CHAR_TO_INT(c) (c - 'A')
#define INT_TO_CHAR(i) (i + 'A')

void encrypt(char *plaintext, char *key, char *ciphertext) {
  int key_size = strlen(key);

  for (int i = 0; plaintext[i] != '\0'; i++) {
    // ci = (pi + ki) MOD 26
    int result = CHAR_TO_INT(plaintext[i]) + CHAR_TO_INT(key[i % key_size]);
    if (result < 0) {
      result = 26 - result;
    }
    ciphertext[i] = INT_TO_CHAR(result % ALPHABET_SIZE);
  }
}

int main(void) {
  int fd = open("./example.txt", O_RDONLY);
  if (fd == -1) {
    perror("open");
    exit(EXIT_FAILURE);
  }

  int buff_size = lseek(fd, 0, SEEK_END);
  lseek(fd, 0, SEEK_SET);

  char buffer[BUFFER_SIZE];
  memset(buffer, BUFFER_SIZE, sizeof(char));

  if (read(fd, buffer, buff_size) == -1) {
    perror("read");
    exit(EXIT_FAILURE);
  }

  close(fd);

  buffer[buff_size - 1] = '\0';
  buff_size--;

  char key[KEY_SIZE];
  memset(key, KEY_SIZE, sizeof(char));

  printf("Insert a Key: ");
  fgets(key, KEY_SIZE, stdin);

  int n = strlen(key);
  key[n - 1] = '\0';

  printf("Plain Text:\n%s\n", buffer);
  printf("Key: %s\n", key);

  char ciphertext[buff_size];
  memset(ciphertext, buff_size, sizeof(char));

  encrypt(buffer, key, ciphertext);
  ciphertext[buff_size] = '\0';

  printf("Ciphertext:\n%s\n", ciphertext);
}
