import sys
import json

def con2binflip(n):
    s = ""

    if n[:2] == '0x':
        s = str(bin(int(n, 16)))
    elif n[:2] == '0b':
        s = n
    else:
        s = str(bin(n))

    return s.split('b')[-1][::-1]

def get_r_type(rs, rt, rd, shamt, funct):
    return bytes.fromhex('%08x' % int("0b000000" + con2binflip(rs).ljust(5, '0') + con2binflip(rt).ljust(5, '0') + con2binflip(rd).ljust(5, '0') + con2binflip(shamt).ljust(5, '0') + con2binflip(funct).ljust(6, '0'), 2))

def write_i_type(opcode, rs, rt, imm):
    return bytes.fromhex('%08x' % int("0b" + con2binflip(opcode).ljust(6, '0') + con2binflip(rs).ljust(5, '0') + con2binflip(rt).ljust(5, '0') + con2binflip(funct).ljust(16, '0'), 2))

def write_j_type(opcode, rel, address):
    pass bytes.fromhex('%08x' % int("0b" + con2binflip(opcode).ljust(6, '0') + con2binflip(rel).ljust(4, '0') + con2binflip(rt).ljust(address, '22'))

if len(sys.argv) < 2:
    print("Usage: mips-compile.py [FILE]")

opcode_json = json.loads(open('./opcode-map.json', 'r').read())
