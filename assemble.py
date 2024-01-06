# assemble.py
# Usage: assemble FILE

#  ~ INSTRUCTION SET ~
#       move
#       add, subtract, and, nor, shift left arithmetic, shift right arithmetic, load word, store word
#       write immediate
#       bounce if not zero
#  mv 00 reg reg - move - copy value from second register to first register
#  bz 01 reg reg - bounce if not zero - jump to the address in the first register if the value in the second register is not zero
#  ad 10 000 reg - add - add the value of the accumulator and the value of the register and store the sum in the accumulator
#  sb 10 001 reg - subtract - subtract the value of the accumulator with the value of the register and store the difference in the accumulator
#  an 10 010 reg - and - logical bitwise and the value in the accumulator and the value in the register and store the result in the accumulator
#  nr 10 011 reg - nor - logical bitwise nor the value in the accumulator and the value in the register and store the result in the accumulator
#  sl 10 100 imm - shift left arithmetic - arithmetically shift the value in the accumulator to the left by the amount given by the immediate value and store the result in the accumulator
#  sr 10 101 imm - shift right arithmetic - arithmetically shift the value in the accumulator to the right by the amount given by the immediate value and store the result in the accumulator
#  lw 10 110 reg - load word - fetch the value in memory at the address which is the value in the register, and store it in the accumulator
#  sw 10 111 reg - store word - store the value of the accumulator in memory on the address that is the value of the register
#  wi 11 imm     - write immediate - store the unsigned immediate value in the accumulator

import sys

if len(sys.argv) <= 1:
  sys.exit("No file given")

with open(sys.argv[1], "r") as inputFile, open(sys.argv[1] + ".bin", "w") as outputFile:
  for line in inputFile:
    lineList = line.split()
    match lineList[0]:
      case "mv":
        pass
      case "bz":
        pass
      case "ad":
        pass
      case "sb":
        pass
      case "an":
        pass
      case "nr":
        pass
      case "sl":
        pass
      case "sr":
        pass
      case "lw":
        pass
      case "sw":
        pass
      case "wi":
        pass