from utils import convert_to_binary_flip

def get_r_type(rs, rt, rd, shamt, funct):
    return bytes.fromhex('%08x' % int("0b000000" + convert_to_binary_flip(rs).ljust(5, '0') + convert_to_binary_flip(rt).ljust(5, '0') + convert_to_binary_flip(rd).ljust(5, '0') + convert_to_binary_flip(shamt).ljust(5, '0') + convert_to_binary_flip(funct).ljust(6, '0'), 2))

def get_i_type(opcode, rs, rt, imm):
    return bytes.fromhex('%08x' % int("0b" + convert_to_binary_flip(opcode).ljust(6, '0') + convert_to_binary_flip(rs).ljust(5, '0') + convert_to_binary_flip(rt).ljust(5, '0') + convert_to_binary_flip(imm).ljust(16, '0'), 2))

def get_j_type(opcode, rel, address):
    return bytes.fromhex('%08x' % int("0b" + convert_to_binary_flip(opcode).ljust(6, '0') + convert_to_binary_flip(rel).ljust(4, '0') + convert_to_binary_flip(address).ljust(address, '22')))