# assemble.py
# modified version of the mips-assembler-disassembler (original file name: assembler.py) by A-Hemdan https://github.com/A-Hemdan/mips-assembler-disassembler - downloaded on 12 February 2024

# My ISA:
#  move (and invert?)
#  add, subtract, and, nor, shift left arithmetic, shift right arithmetic, load word, store word
#  write immediate
#  bounce if not zero
#
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
#
#  Instruction types ('styles'):
#   0 A: op reg reg
#   1 B: op fun reg
#   2 C: op fun imm
#   3 D: op imm


from pyparsing import *
from bitstring import BitArray

# Helper conversion functions
def hex2bin(hex_str, n_bits):
    return bin(int(hex_str, 16))[2:].zfill(n_bits)

def dec2bin(dec, n_bits):
    if int(dec) < 0:
        dec = int(dec)
        b = BitArray(int=dec,length=n_bits)
        return b.bin
    else:
        return bin(int(dec))[2:].zfill(n_bits)

# MIPS Instruction Set hashtable
# style indicates the number of operands and their type as follows:-
# style : 0 -> operation reg,reg,reg
# style : 1 -> operation reg,reg,integer
# style : 2 -> operation reg
# style : 3 -> operation reg,integer
# style : 4 -> operation reg,intger(reg)
# style : 5 -> operation reg,reg,address

operations = {
    'mv' : {'format': 'R', 'opcode': 0, 'style': 0},
    'bz' : {'format': 'R', 'opcode': 1, 'style': 0},
    'ad' : {'format': 'R', 'opcode': 2, 'style': 1, 'funct': 0},
    'sb' : {'format': 'R', 'opcode': 2, 'style': 1, 'funct': 1},
    'an' : {'format': 'R', 'opcode': 2, 'style': 1, 'funct': 2},
    'nr' : {'format': 'R', 'opcode': 2, 'style': 1, 'funct': 3},
    'sl' : {'format': 'R', 'opcode': 2, 'style': 2, 'funct': 4},
    'sr' : {'format': 'R', 'opcode': 2, 'style': 2, 'funct': 5},
    'lw' : {'format': 'R', 'opcode': 2, 'style': 1, 'funct': 6},
    'sw' : {'format': 'R', 'opcode': 2, 'style': 1, 'funct': 7},
    'wi' : {'format': 'R', 'opcode': 3, 'style': 3}
}

valid_operations = operations.keys()

# Instruction type classification arrays
R0 = []
R1 = []
R2 = []
I1 = []
I3 = []
I4 = []
I5 = []
J  = []
# Add operations to respective instruction type array
for oper in valid_operations:
    current_oper = operations[oper]
    if current_oper['format'] == 'R':
        if current_oper['style'] == 0: R0.append(oper)
        if current_oper['style'] == 1: R1.append(oper)
        if current_oper['style'] == 2: R2.append(oper)
        
    if current_oper['format'] == 'I':
        if current_oper['style'] == 1: I1.append(oper)
        if current_oper['style'] == 3: I3.append(oper)
        if current_oper['style'] == 4: I4.append(oper)
        if current_oper['style'] == 5: I5.append(oper)
    
    if current_oper['format'] == 'J': J.append(oper) 


# Registers hashtable
regs = {}
regs['$zero']=0
regs['$at']=1
regs['$v0']=2
regs['$2']=2
regs['$v1']=3
for x in range(0,4):
    regs['$a%d'%x]= (x+4)
for x in range(0,8):
    regs['$t%d'%x]= (x+8)
    regs['$s%d'%x]= (x+16)
for y in range(8,10):
    regs['$t%d'%y]=(y+24)
for z in range(0,2):
    regs['$k%d'%z]=(z+26)
regs['$gp']=28
regs['$sp']=29
regs['$fp']=30
regs['$ra']=31
for s in range(0,31):
    regs['$%d'%s]=s
regs[''] = 0
    
valid_regs = list(regs.keys())
valid_regs.remove('')


# Setting grammer rules for parsing
identifier =  Word(alphas+"_",alphanums+"_")
reg = oneOf(valid_regs)
comma = Suppress(',')
number = Combine(Optional('-') + Word(nums))
EOL = OneOrMore(LineEnd())

Label = identifier.setResultsName("label") + Suppress(":")
reg_rs = reg.setResultsName('rs')
reg_rt = reg.setResultsName('rt')
reg_rd = reg.setResultsName('rd')
imm_value = number.setResultsName('imm')
addr = identifier.setResultsName("address")

R_format = (oneOf(R0).setResultsName('operation') + White() + reg_rd + comma + reg_rs + comma + reg_rt) ^\
           (oneOf(R1).setResultsName('operation') + White() + reg_rd + comma + reg_rt + comma + number.setResultsName('shamt')) ^\
           (oneOf(R2).setResultsName('operation') + White() + reg_rs)

I_format = (oneOf(I1).setResultsName('operation') + White() + reg_rt + comma + reg_rs + comma + imm_value) ^\
           (oneOf(I3).setResultsName('operation') + White() + reg_rt + comma + imm_value) ^\
           (oneOf(I4).setResultsName('operation') + White() + reg_rt + comma + imm_value + Suppress('(') + reg_rs + Suppress(')')) ^\
           (oneOf(I5).setResultsName('operation') + White() + reg_rs + comma + reg_rt + comma + addr)

J_format = oneOf(J).setResultsName('operation') + White() + addr

Instruction =   ((Label) + (R_format ^ I_format ^ J_format)) ^\
                (Label) ^ (R_format ^ I_format ^ J_format) ^ EOL.setResultsName('EOL')

Instruction.ignore(pythonStyleComment)

# Reading and Parsing assembly input file
print('Welcome to MIPS Assembler v1.00')
print('You should input a text file containing MIPS assembly code.')
print("Your machine code will be in 'mcode_file.txt' text file while Hex code will be printed on console. ")
filename = input('Please enter the assembly text file name (e.g. assembly.txt) or path: ')
init_address = input('Please enter the initial address of your assembly code in hexadecimal: ')

with open(filename, 'r') as assembly_file:
    Memory = []
    Labels = {}

    line_address = int(init_address,16)
    for line in assembly_file:
        current_inst = Instruction.parseString(line)
        if len(current_inst) == 0: 
            continue
        if current_inst[0] == '\n': 
            continue
        Memory.append(current_inst)
        if not current_inst.label == '':
            if not current_inst.operation == '':
                Labels[current_inst.label] = line_address
            else :  
                Labels[current_inst.label] = line_address
                continue
        line_address += 4

# Assembling the parsed code
with open('mcode_file.txt','w') as mcode_file: # opening the output file !!! As a text file !?!?
    PC = int(init_address,16)   #converting PC to decimal for ease of use to be used in arithmatic operations
    for inst in Memory:
        if inst.operation == '':
            continue
        op = operations[inst.operation]
        PC += 4
        
        if op['format'] == 'R':
            opcode = op['opcode']
            funct = op['funct']
            if inst.shamt == not '': shamt = inst.shamt
            else: shamt = 0
            rs_code = regs[inst.rs]
            rt_code = regs[inst.rt]
            rd_code = regs[inst.rd]
            inst_mcode = hex2bin(opcode,6) + dec2bin(rs_code,5) + dec2bin(rt_code,5) + dec2bin(rd_code,5) +\
                         dec2bin(shamt,5) + hex2bin(funct,6)
            mcode_file.write(inst_mcode + '\n')
            print(hex(int(inst_mcode,2)))
            
        if op['format'] == 'I':
            opcode = op['opcode']
            rs_code = regs[inst.rs]
            rt_code = regs[inst.rt]
            if inst.imm == not '': imm = inst.imm
            else:
                address = Labels[inst.address]
                imm = (address - PC)/4
            inst_mcode = hex2bin(opcode,6) + dec2bin(rs_code,5) + dec2bin(rt_code,5) + dec2bin(imm,16)
            mcode_file.write(inst_mcode + '\n')
            print(hex(int(inst_mcode,2)))
            
        if op['format'] == 'J':
            opcode = op['opcode']
            address = Labels[inst.address]
            address = dec2bin(address,32)
            address = address[4:]
            address = int(address,2)
            address = address/4
            address = dec2bin(address,26)
            inst_mcode = hex2bin(opcode,6) + address
            mcode_file.write(inst_mcode + '\n')
            print(hex(int(inst_mcode,2)))