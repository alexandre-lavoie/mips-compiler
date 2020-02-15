import sys
import json
import re

def con2binflip(n):
    s = ""

    if n[:2] == '0x':
        s = str(bin(int(n, 16)))
    elif n[:2] == '0b':
        s = n
    else:
        s = str(bin(int(n, 10)))

    return s.split('b')[-1][::-1]

def get_r_type(rs, rt, rd, shamt, funct):
    return bytes.fromhex('%08x' % int("0b000000" + con2binflip(rs).ljust(5, '0') + con2binflip(rt).ljust(5, '0') + con2binflip(rd).ljust(5, '0') + con2binflip(shamt).ljust(5, '0') + con2binflip(funct).ljust(6, '0'), 2))

def get_i_type(opcode, rs, rt, imm):
    return bytes.fromhex('%08x' % int("0b" + con2binflip(opcode).ljust(6, '0') + con2binflip(rs).ljust(5, '0') + con2binflip(rt).ljust(5, '0') + con2binflip(imm).ljust(16, '0'), 2))

def get_j_type(opcode, rel, address):
    return bytes.fromhex('%08x' % int("0b" + con2binflip(opcode).ljust(6, '0') + con2binflip(rel).ljust(4, '0') + con2binflip(address).ljust(address, '22')))

if len(sys.argv) < 2:
    print("Usage: mips-compile.py FILE [OUTPUT]")
    exit()

opcode_dict = json.loads(open('./opcode-map.json', 'r').read())

output_file = "./build/out.bin"

if len(sys.argv) >= 3:
    output_file = sys.argv[2]

with open(sys.argv[1], 'r') as input_handle:
    with open(output_file, 'wb') as output_handle:
        line = input_handle.readline()

        line_number = 1

        while line:
            line = re.sub(r'  +' , ' ', line.strip())

            if '//' in line:
                line = line[:line.index('//')]

            line_split = [x.lower() for x in line.split(' ')]

            opcode = line_split[0]
            operators = ''.join(line_split[1:])

            operators = re.sub(r'\((.*?)\)', r',\1', operators)
            operators = operators.replace('r', '')
            operators = operators.split(',')

            if not opcode in opcode_dict:
                print("Unknown operator %s on line %d" % (opcode, line_number))
                exit()
            
            opcode_def = opcode_dict[opcode]

            form = dict(zip(opcode_def['format'], operators))
            
            if(opcode_def['type'].lower() == 'i'):
                output_handle.write(get_i_type(opcode_def['opcode'], form['rs'], form['rt'], form['imm']))
            elif(opcode_def['type'].lower() == 'r'):
                output_handle.write(get_r_type(form['rs'], form['rt'], form['rd'], form['shamt'], opcode_def['funct']))
            elif(opcode_def['type'].lower() == 'j'):
                output_handle.write(get_j_type(opcode_def['opcode'], form['rel'], form['address']))
            
            line_number += 1
            line = input_handle.readline()