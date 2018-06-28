from dicts import CHECK


'''
Parses a serial line with a checksum value at the end
Returns dictionary with status, valid, calculated, checksum
Returns valid = False if checksum bad
'''


def parse(line=''):
    CHECKSUM = CHECK.SUM
    # Remvove newline
    sentence = line.rstrip('\n\r')
    # Retrieve data excluding checksum
    data = sentence[1:-3]
    # Retreive checksum value
    checksum = sentence[-2:]
    # Start xor checksum calculation at 0
    data_check = 0
    # For each character do a xor with previous
    for c in data:
        data_check ^= ord(c)
    # Add a '0x' to the front of the checksum
    hex_checksum = '0x'+checksum.lower()
    # Convert to hex
    hex_data = format(data_check, '#04x')
    if hex_data == hex_checksum:
        CHECKSUM['valid'] = True
        CHECKSUM['status'] = '[OK]'
    else:
        CHECKSUM['valid'] = False
        CHECKSUM['status'] = '[Fail]'
    CHECKSUM['calculated'] = hex_data
    CHECKSUM['checksum'] = hex_checksum
    return(CHECKSUM)


if __name__ == '__main__':
    CHECKSUM = parse(
        '$GPGGA,024106,3321.9308,S,11537.59819,E,1,21,1.0,-8.313,M,-30.9,M,,*63')
    print(CHECKSUM)
