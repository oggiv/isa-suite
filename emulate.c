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
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define ACC 0
#define DATA_WIDTH 16
#define MAX_INSTRUCTIONS 100

int main(int argc, char const *argv[])
{
  bool readFile = false;

  // calloc initializes every cell to 0
  int16_t* RAM = (int16_t*) calloc(2^DATA_WIDTH, sizeof(int16_t));
  if (RAM == NULL) {
    perror("Error allocating RAM");
    return 1;
  }

  int instructionsRead = 0;

  if (0 < argc) {
    for (int i = 0; i < argc; i++) {
      if (argv[i][0] == '-') {
        // flag option
        // not implemented yet
      }
      else {
        // input binary file
        readFile = true;
        FILE* fd = fopen(argv[i], "r");
        if (fd == NULL) {
          perror("Error opening file");
          return 1;
        }
        //instructionsRead = fread(RAM, sizeof(uint16_t), MAX_INSTRUCTIONS, fd);
        fclose(fd);
      }
    }
  }

  // every position in reg is a CPU register
  int16_t reg[8];
  for (int i = 0; i < sizeof(reg); i++) {
    reg[i] = 0;
  }

  // PC keeps track of which instruction the program is on
  uint16_t programCounter;

  // run the program
  uint8_t inputByte;
  unsigned int opCode;
  int imm;
  int arg1;
  int arg2;
  for (programCounter = 0; programCounter < instructionsRead; programCounter++) {

    if (programCounter % 2 == 0) {
      inputByte = (uint8_t) RAM[programCounter] & 0xFF;
    }
    else {
      inputByte = (uint8_t) RAM[programCounter] >> 8;
    }

    opCode = (inputByte & 0b11000000) >> 6;
    arg1 = (inputByte & 0b00111000) >> 3;
    arg2 = (inputByte & 0b00000111);

    switch (opCode) {
      case 0b00: // move
        // copy value from the arg2 register to the arg1 register
        reg[arg1] = reg[arg2];
        break;
      case 0b01: // bounce if not zero
        // jump to the address in the first register if the value in the second register is not zero
        if (reg[arg2] != 0) {
          programCounter = reg[arg1]; // !!! should there be a -1 as well?
        }
        break;
      case 0b10: // functional operations
        // read arg1 to determine operation
        switch (arg1) {
          case 0b000: // add
          // add the value of the accumulator and the value of the register and store the sum in the accumulator
          reg[ACC] = reg[ACC] + reg[arg2];
          break;
        case 0b001: // subtract
          // subtract the value of the accumulator with the value of the register and store the difference in the accumulator
          reg[ACC] = reg[ACC] - reg[arg2];
          break;
        case 0b010: // and
          // logical bitwise and the value in the accumulator and the value in the register and store the result in the accumulator
          reg[ACC] = reg[ACC] & reg[arg2];
          break;
        case 0b011: // nor
          // logical bitwise nor the value in the accumulator and the value in the register and store the result in the accumulator
          reg[ACC] = ~(reg[ACC] | reg[arg2]);
          break;
        case 0b100: // shift left arithmetic
          // arithmetically shift the value in the accumulator to the left by the amount given by the immediate value and store the result in the accumulator
          reg[ACC] = reg[ACC] << arg2;
          break;
        case 0b101: // shift right arithmetic
          // arithmetically shift the value in the accumulator to the right by the amount given by the immediate value and store the result in the accumulator
          reg[ACC] = reg[ACC] >> arg2;
          break;
        case 0b110: // load word
          // fetch the value in memory at the address which is the value in the register, and store it in the accumulator
          reg[ACC] = RAM[reg[arg2]];
          break;
        case 0b111: // store word
          // store the value of the accumulator in memory on the address that is the value of the register
          RAM[reg[arg2]] = reg[ACC];
          break;
        default:
          // invalid funct somehow
          break;
        }
        break;
      case 0b11: // write immediate
        // store the unsigned immediate value in the accumulator
        imm = (arg1 << 3) | arg2;
        reg[ACC] = imm;
        break;
      default: // unknown opcode
        break;
    }
  }

  printf("PC: %d\n", programCounter);
  printf("Registers\n");
  printf(" $a %d\n", reg[ACC]);
  printf(" $1 %d\n", reg[1]);
  printf(" $2 %d\n", reg[2]);
  printf(" $3 %d\n", reg[3]);
  printf(" $4 %d\n", reg[4]);
  printf(" $5 %d\n", reg[5]);
  printf(" $6 %d\n", reg[6]);
  printf(" $7 %d\n\n", reg[7]);

  char userInput[DATA_WIDTH / 4];
  int charsEntered = 0;
  int inspectAddress = 0;

  while (1) {
    scanf("%s", userInput);
    for (int i = 0; i < (DATA_WIDTH / 4); i++) {
      if ('0' <= userInput[i] && userInput[i] <= '9') {
        printf("%c", userInput[i]);
        inspectAddress *= 16;
        inspectAddress += userInput[i] - '0';
        charsEntered++;
      }
      if ('a' <= userInput[i] && userInput[i] <= 'f') {
        printf("%c", userInput[i] - ('a' - 'A'));
        inspectAddress *= 16;
        inspectAddress += 10 + userInput[i] - 'a';
        charsEntered++;
      }
      if (userInput[i] == 'q') {
        free(RAM);
        return 0;
      }
    }
    printf(" : %d\n", RAM[inspectAddress]);
    inspectAddress = 0;
    charsEntered = 0;
  }

  free(RAM);
  return 0;
}