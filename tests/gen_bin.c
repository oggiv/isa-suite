// test.c lol

#include <stdio.h>
#include <stdint.h>

int main(int argc, char const *argv[]) {

  uint8_t program[] = {
    /*0b11000111,
    0b11000100,
    0b11000101,
    0b11011100*/
    0xc4,
    0xc7,
    0xdc
    //0xc5
  };

  if (sizeof(program) % 2 == 1) {

  }

  FILE* fd = fopen("test.bin", "wb");
  fwrite(program, sizeof(uint8_t), sizeof(program), fd);
  fclose(fd);
  return 0;
}