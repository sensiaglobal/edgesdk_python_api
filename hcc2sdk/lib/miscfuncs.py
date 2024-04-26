#
# Mario Torre - 12/19/2023
#
import logging
import struct

def text_to_log_level (str):
    if str=="INFO":
        return logging.INFO
    if str=="DEBUG":
        return logging.DEBUG
    if str=="WARN":
        return logging.WARN
    if str=="ERROR":
        return logging.ERROR
    return logging.DEBUG

def double_to_bin(value):
    [d] = struct.unpack(">Q", struct.pack(">d", value))
    return d

def bin_to_double(value):
    [d] = struct.unpack(">d", struct.pack(">Q", value))
    return d

def float_to_bin(value):
    [d] = struct.unpack(">L", struct.pack(">f", value))
    #[d] = struct.unpack(">l", struct.pack(">f", value))
    return d

def bin_to_float(value):
    [d] = struct.unpack(">f", struct.pack(">L", value))
    #[d] = struct.unpack(">f", struct.pack(">l", value))
    return d

def int_to_bin(value):
    [d] = struct.unpack(">L", struct.pack(">l", value))
    return d

def hex_to_bin(value):
    d = int(value, 16)
    return d

def split_int_16(value):
    rtn = []
    a = (value >> 16) & 0xffff
    b = value & 0xffff
    rtn.append(a)
    rtn.append(b)
    return rtn

def split_int_16_double(value):
    rtn = []
    a = (value >> 48) & 0xffff
    b = (value >> 32) & 0xffff
    c = (value >> 16) & 0xffff
    d = value & 0xffff
    rtn.append(a)
    rtn.append(b)
    rtn.append(c)
    rtn.append(d)
    return rtn

def merge_int_16_to_32(value_array):
    return ((value_array[0] & 0xffff) << 16) + (value_array[1] & 0xffff)

def hex_string_array_to_int(rxb):
    return [ int(rxb[i], 16) for i in range(len(rxb))]

def convert_int_array_to_one_string_separated(array, prefix, sep):
    rtn = sep
    for val in array:
        rtn += format(val, '02x') + sep
    return prefix + ": " + rtn

def convert_binary_string_to_byte_array(txb):
    byte_str_array = []
    for i in range (0, len(txb),2):
        byte_str_array.append(txb[i] + txb[i+1])
    return hex_string_array_to_int(byte_str_array)

def setup_parameter(value, min):
        if ( value < min):
            return min
        return value


def swap_word_bytes(val, ws, bs):
            
    v = val.to_bytes(4,'little')
    a=0; b=0; c=0; d=0
    
    if (not ws and not bs):
        a=0; b=1; c=2; d=3
    elif (not ws and bs):
        a=1; b=0; c=3; d=2
    elif (ws and not bs):
        a=2; b=3; c=0; d=1
    else:
        a=3; b=2; c=1; d=0;                

    rtn2 = [ v[a], v[b], v[c], v[d] ]
    return int.from_bytes(rtn2, 'little')

def swap_word_bytes_double(val, ws, bs):
            
    v = val.to_bytes(8,'little')
    a=0; b=0; c=0; d=0; e=0; f=0; g=0; h=0
    
    if (not ws and not bs):
        a=0; b=1; c=2; d=3; e=4; f=5; g=6; h=7
    elif (not ws and bs):
        a=1; b=0; c=3; d=2; e=5; f=4; g=7; h=6
    elif (ws and not bs):
        a=2; b=3; c=0; d=1; e=6; f=7; g=4; h=5
    else:
        a=7; b=6; c=5; d=4; e=3; f=2; g=1; h=0;                

    rtn2 = [ v[a], v[b], v[c], v[d], v[e], v[f], v[g], v[h] ]
    return int.from_bytes(rtn2, 'little')

def convert_unsigned_to_signed(value, size):
    num_bits = (size << 4) - 1
    if (value & (1 << num_bits)) != 0:
        value = value - (1 << num_bits)
        value = -value
    return value

