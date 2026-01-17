import ctypes

def qlog_checksum(data: bytes) -> int:
    low = 0
    high = 0

    for b in data:
        high = (high + b) & 0xFFFFFFFF
        low = (low + (~b & 0xFFFFFFFF)) & 0xFFFFFFFF
    
    return ((high & 0xFFFFFFFF) << 32) | (low & 0xFFFFFFFF)


def dat_checksum(data: bytes) -> int:
    high = 0
    low = 0

    count = len(data) // 2

    for i in range(count):
        # Read big-endian u16
        v = (data[2*i] << 8) | data[2*i + 1]

        high += (v & 0xFFFF)
        low  += (~v & 0xFFFF)

    return ((high & 0xFFFF) << 16) | (low & 0xFFFF)


def ctype_limits(c_int_type):
    signed = c_int_type(-1).value < c_int_type(0).value
    bit_size = ctypes.sizeof(c_int_type) * 8
    signed_limit = 2 ** (bit_size - 1)
    return (-signed_limit, signed_limit - 1) if signed else (0, 2 * signed_limit - 1)
