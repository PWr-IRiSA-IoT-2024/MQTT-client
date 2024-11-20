import base64


TYPES = {
    '0': 'CO2',
    '1': 'VOC',
    '2': 'Temperature',
    '3': 'Humidity'
}


def convert_payload(payload):
    decoded_bytes = base64.b64decode(payload)
    
    # Expected payload is exactly 1 byte
    byte = decoded_bytes[0]
    
    # Extract the first 3 bits (type)
    # Example:
    # Original byte:  10110110
    # Right shift 5:  00000101
    type_bits = byte >> 5
    type = TYPES.get(str(type_bits), 'UNKNOWN_TYPE')
    
    # Extract the remaining 5 bits (value)
    # Mask with 0b11111 to get last 5 bits
    # Example:
    # Original byte:  10110110
    #            AND  00011111
    #            --------------
    #                 00010110
    value_bits = byte & 0b11111
    value = int(value_bits)

    if type is 'Temperature':
        value = (value / 2) + 16

    if type is 'Humidity':
        value = (value * 2) + 20
    
    return type, value