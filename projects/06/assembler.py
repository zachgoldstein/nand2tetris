import argparse
import re

DEBUG = False

parser = argparse.ArgumentParser(description='Assembler')
parser.add_argument('--filename')
parser.add_argument('--debug', action=argparse.BooleanOptionalAction)

args = parser.parse_args()
DEBUG = args.debug
if DEBUG:
    print(args.filename)


def convert_a_instruction(value: str) -> str:
    number_value = int(value[1:])
    binary_instruction = '{0:016b}'.format(number_value)
    if DEBUG:
        print(f'A-instr converting {value} to {binary_instruction}')
    return binary_instruction

# C-instruction lookup tables
comp_lookup = {
    "0":  "101010",
    "1":  "111111",
    "-1": "111010",
    "D":  "001100",
    "A":  "110000",
    "M":  "110000",
    "!D": "001101",
    "!A": "110001",
    "!M": "110001",
    "-D": "001111",
    "-A": "110011",
    "-M": "110011",
    "D+1":"011111",
    "A+1":"110111",
    "M+1":"110111",
    "D-1":"001110",
    "A-1":"110010",
    "M-1":"110010",
    "D+A":"000010",
    "D+M":"000010",
    "D-A":"010011",
    "D-M":"010011",
    "A-D":"000111",
    "M-D":"000111",
    "D&A":"000000",
    "D&M":"000000",
    "D|A":"010101",
    "D|M":"010101",
}

dest_lookup = {
    "null": "000",
    "M": "001",
    "D": "010",
    "DM": "011",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "ADM": "111"
}

jump_lookup = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

def get_a_bit(value:str) -> str:
    if "M" in value:
        if DEBUG:
            print(f"a bit for {value} is 1")
        return 1
    else:
        if DEBUG:
            print(f"a bit for {value} is 0")
        return 0

# example: "M=A-1;JTE"
def convert_c_instruction(value: str)-> str:
    if "=" not in value:
        value = f"null={value.split(';')[0]};{value.split(';')[1]}"
    if ";" not in value:
        value += ";null"
    if DEBUG:
        print(f"cleaned value to {value}")
    m = re.match(r'(.*)=(.*);(.*)', value)
    dest = dest_lookup[m.group(1)]
    comp = comp_lookup[m.group(2)]
    a_bit = get_a_bit(m.group(2))
    jump = jump_lookup[m.group(3)]
    binary_instruction = f"111{a_bit}{comp}{dest}{jump}"
    if DEBUG:
        print(m)
        print(f"comp:{comp}, dest:{dest}, jump:{jump}, a_bit:{a_bit}")
        print(f'C-instr converting {value} to {binary_instruction}')
    return binary_instruction

def detect_c_instruction(value: str)-> bool:
    if "=" in value or ";" in value:
        return True
    return False

def clean_data(data):
    output = []
    for line in data:
        lstripped = line.lstrip()
        # remove empty lines
        if lstripped == "":
            continue
        # remove lines that start with comment
        if lstripped[0:2] == "//":
            continue
        # remove comments at end of line
        if "//" in lstripped:
            lstripped = lstripped.split('//')[0]

        # strip newlines
        line_trimmed = lstripped.rstrip()
        output.append(line_trimmed)
    return output


def translate_to_binary(data):
    output = []
    for line in data:
        # detect if A-instruction
        if line[0:1] == "@":
            instr = convert_a_instruction(line)
            output.append(instr)
        elif detect_c_instruction(line):
            instr = convert_c_instruction(line)
            output.append(instr)
    return output

# Read in file
reader = open(args.filename)
input_data = []
try:
    # iterate over every line
    for line in reader:
        input_data.append(line)        
finally:
    reader.close()

symbol_table = {
    "R0":"0",
    "R1":"1",
    "R2":"2",
    "R3":"3",
    "R4":"4",
    "R5":"5",
    "R6":"6",
    "R7":"7",
    "R8":"8",
    "R9":"9",
    "R10":"10",
    "R11":"11",
    "R12":"12",
    "R13":"13",
    "R14":"14",
    "R15":"15",
    "SCREEN":"16384",
    "KBD":"24576",
    "SP":"0",
    "LCL":"1",
    "ARG":"2",
    "THIS":"3",
    "THAT":"4"
}

def first_pass(data):
    output = []
    for line in data:
        if line[0] == "@" and line[1:] in symbol_table:
            new_value = symbol_table[line[1:]]
            if DEBUG:
                print(f"first pass found symbol {line[1:]} -> {new_value}")
            line = f"@{new_value}"
        output.append(line)
    return output

def add_label_symbols(data, symbol_table):
    running_line_num = 0
    for line in data:
        if line[0] == "(" and line[-1] == ")":
            symbol_line_num = running_line_num
            symbol = line.replace('(','').replace(')','')
            if DEBUG:
                print(f"found label symbol: {symbol}, adding line:{symbol_line_num}")
            symbol_table[symbol] = symbol_line_num
        else:
            running_line_num += 1
    return symbol_table

def get_unique_mem_addr(symbol_table):
    for i in list(range(16,16383)):
        if i not in list(symbol_table.values()):
            return i

def add_variable_symbols(data, symbol_table):
    running_line_num = 0
    for line in data:
        if line[0] == "(" and line[-1] == ")":
            continue
        if line[0] == "@" and line[1:] not in symbol_table and not line[1:].isnumeric():
            unique_mem_addr = get_unique_mem_addr(symbol_table)
            if DEBUG:
                print(f"found var symbol {line[1:]}, using unique mem addr:{unique_mem_addr}")
            symbol_table[line[1:]] = unique_mem_addr
        running_line_num += 1
    return symbol_table

def replace_symbols(data, symbol_table):
    output = []
    for line in data:
        # skip pseudo lines
        if line[0] == "(" and line[-1] == ")":
            continue
        if line[0] == "@" and line[1:] in symbol_table:
            if DEBUG:
                print(f"found in symbol table, replacing {line} with @{symbol_table[line[1:]]}")
            output.append(f"@{symbol_table[line[1:]]}")
        else:
            output.append(line)
    return output

cleaned_data = clean_data(input_data)

# first pass, translate from symbol table
first_pass_data = first_pass(cleaned_data)
# second pass, translate user-defined symbols

# insert label symbols to symbol table
symbol_table = add_label_symbols(first_pass_data, symbol_table)
# insert variable symbols to symbol table
symbol_table = add_variable_symbols(first_pass_data, symbol_table)

if DEBUG:
    print(symbol_table)

# replace all symbols
replaced_data = replace_symbols(first_pass_data, symbol_table)

# translate output now...
binary_output = translate_to_binary(replaced_data)

for line in binary_output:
    print(line)

# write to file by just piping to file
# use diff to compare results