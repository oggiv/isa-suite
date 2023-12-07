// emulate.c
// Usage: emulate BINARY

/*
  move (and invert?)
  add, subtract, and, nor, shift left arithmetic, shift right arithmetic, load word, store word
  write immediate
  bounce if not zero

  mv 00 reg reg - move - copy value from second register to first register
  bz 01 reg reg - bounce if not zero - jump to the address in the first register if the value in the second register is not zero
  ad 10 000 reg - add - add the value of the accumulator and the value of the register and store the sum in the accumulator
  sb 10 001 reg - subtract - subtract the value of the accumulator with the value of the register and store the difference in the accumulator
  an 10 010 reg - and - logical bitwise and the value in the accumulator and the value in the register and store the result in the accumulator
  nr 10 011 reg - nor - logical bitwise nor the value in the accumulator and the value in the register and store the result in the accumulator
  sl 10 100 imm - shift left arithmetic - arithmetically shift the value in the accumulator to the left by the amount given by the immediate value and store the result in the accumulator
  sr 10 101 imm - shift right arithmetic - arithmetically shift the value in the accumulator to the right by the amount given by the immediate value and store the result in the accumulator
  lw 10 110 reg - load word - fetch the value in memory at the address which is the value in the register, and store it in the accumulator
  sw 10 111 reg - store word - store the value of the accumulator in memory on the address that is the value of the register
  wi 11 imm     - write immediate - store the unsigned immediate value in the accumulator
*/

#include <stdio.h>

int main(int argc, char const *argv[])
{

  // manually inputing binaries for testing
  unsigned char testProgram[] = {
    0b11000110, // put 6 in a
    0b00001000, // copy reg[a] to reg[1]
    0b00010001  // copy reg[1] to reg[2]
  };

  // every position in reg is a CPU register
  signed char reg[8];

  // PC keeps track of which instruction the program is on
  unsigned int programCounter;

  // run the program
  unsigned char inputByte;
  unsigned int opCode;
  for (programCounter = 0; programCounter < sizeof(testProgram); programCounter++) {

    inputByte = testProgram[programCounter];
    unsigned int opCode = (inputByte & 0b11000000) >> 6;

    int imm;
    int arg1 = (inputByte & 0b00111000) >> 3;
    int arg2 = (inputByte & 0b00000111);

    switch (opCode) {
      case 0b00: // move
        // copy value from the arg2 register to the arg1 register
        reg[arg1] = reg[arg2];
        break;

      case 0b01: // bounce if not zero
        // jump to the address in the first register if the value in the second register is not zero
        if (reg[arg2] != 0) {
          programCounter = reg[arg1];
        }
        break;

      case 0b10: // functional operations
        // code
        break;

      case 0b11: // write immediate
        // code
        imm = arg1 | arg2;
        reg[0] = imm;
        break;

      default: // unknown opcode
        break;
    }
  }

  printf("PC: %d\n", programCounter);
  printf("Registers\n");
  printf(" $a %d\n", reg[0]);
  printf(" $1 %d\n", reg[1]);
  printf(" $2 %d\n", reg[2]);
  printf(" $3 %d\n", reg[3]);
  printf(" $4 %d\n", reg[4]);
  printf(" $5 %d\n", reg[5]);
  printf(" $6 %d\n", reg[6]);
  printf(" $7 %d\n", reg[7]);

  return 0;
}