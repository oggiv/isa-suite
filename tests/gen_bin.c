// gen_bin.c
/* this test outputs a binary file "test.bin" containing
   the values in the array "program". */

#include <stdio.h>
#include <stdint.h>

int main(int argc, char const *argv[]) {

  uint8_t program[] = {
    0b11000111,
    0xc7,
    0xdc
  };

  FILE* fd = fopen("test.bin", "wb");
  fwrite(program, sizeof(uint8_t), sizeof(program), fd);
  fclose(fd);
  return 0;
}