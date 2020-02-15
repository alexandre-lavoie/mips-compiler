def word_string_to_byte(n):
    return bytes.fromhex('%02x' % (convert_hbi_str_to_integer(n) & 255)) + bytes.fromhex('%02x' % (convert_hbi_str_to_integer(n) >> 8))

def byte_string_to_byte(n):
    return bytes.fromhex('%02x' % convert_hbi_str_to_integer(n))

def convert_hbi_str_to_integer(n):
    if isinstance(n, int):
        return n

    if isinstance(n, str):
        if n[:2] == '0x':
            return int(n, 16)
        elif n[:2] == '0b':
            return int(n, 2)
        else:
            return int(n, 10)

    return int(n)

def convert_to_binary_flip(n):
    return str(bin(convert_hbi_str_to_integer(n))).split('b')[-1][::-1]