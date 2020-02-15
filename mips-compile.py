import sys
import json
import re
from utils import word_string_to_byte, byte_string_to_byte
from mips import get_i_type, get_j_type, get_r_type

def parse_by_section(f):
    current_section = None
    sections = {'.reg': [], '.data': [], '.main': []}

    with open(f, 'r') as handle:
        line = handle.readline()

        while line:
            # Remove comments
            if '//' in line:
                line = line[:line.index('//')]

            if not line.isspace():
                # Remove redundant spaces.
                line = re.sub(r'  +' , ' ', line.strip())
                
                # Split command according to spaces
                line_split = [x.lower() for x in line.split(' ')]

                # Gets opcode and trailing args
                opcode = line_split[0]
                operators = ''.join(line_split[1:])

                # If the opcode is a section, change section
                # Else insert code into section
                if opcode in sections.keys():
                    current_section = opcode
                else:
                    sections[current_section].append((opcode, operators))
                
            # Read next line
            line = handle.readline()
    
    return sections

if len(sys.argv) < 2:
    print("Usage: mips-compile.py FILE [OUTPUT]")
    exit()

opcode_dict = json.loads(open('./opcode-map.json', 'r').read())

output_file = "./build/out.bin"

if len(sys.argv) >= 3:
    output_file = sys.argv[2]

# Parse file

file_parsed_by_section = parse_by_section(sys.argv[1])

# Handles read data

queue = {x: b'' for x in file_parsed_by_section.keys()}

# Handle data section

sections_not_main = []

for (section, statements) in filter(lambda x: not x == '.map', file_parsed_by_section.items()):
    for statement in statements:
        sections_not_main.append((section, statement))

for (section, (opcode, operator)) in sections_not_main:
    if opcode == '.word':
        for n in operator.split(','):
            queue[section] += word_string_to_byte(n)
    elif opcode == '.byte':
        for n in operator.split(','):
            queue[section] += byte_string_to_byte(n)
    elif opcode == '.space':
        for _ in range(int(operator)):
            queue[section] += b'\x00'

# Handles main section
code_line_number = 1

for (opcode, operators) in file_parsed_by_section['.main']:
    opr = str(operators)
    opr = re.sub(r'\((.*?)\)', r',\1', opr)
    opr = opr.replace('r', '')
    opr = opr.split(',')

    if not opcode in opcode_dict:
        print("Unknown operator %s on line %d" % (opcode, code_line_number))
        exit()

    opcode_def = opcode_dict[opcode]

    form = dict(zip(opcode_def['format'], opr))

    if(opcode_def['type'].lower() == 'i'):
        queue['.main'] += get_i_type(opcode_def['opcode'], form['rs'], form['rt'], form['imm'])
    elif(opcode_def['type'].lower() == 'r'):
        queue['.main'] += get_r_type(form['rs'], form['rt'], form['rd'], form['shamt'] if 'shamt' in form else 0, opcode_def['funct'])
    elif(opcode_def['type'].lower() == 'j'):
        queue['.main'] += get_j_type(opcode_def['opcode'], form['rel'], form['address'])
            
    code_line_number += 1

# Writes file

with open(output_file, 'wb') as output_handle:
    output_handle.write(b'MIPS')
    output_handle.write(word_string_to_byte(len(queue['.reg'])))
    output_handle.write(word_string_to_byte(len(queue['.data'])))
    output_handle.write(word_string_to_byte(len(queue['.main'])))
    output_handle.write(queue['.reg'])
    output_handle.write(queue['.data'])
    output_handle.write(queue['.main'])