import base64


def convert_payload(payload):
    decoded_bytes = base64.b64decode(payload)
    
    # Expected payload is exactly 1 byte
    byte = decoded_bytes[0]
    
    # Extract the first 3 bits (type)
    # Example:
    # Original byte:  10110110
    # Right shift 5:  00000101
    type_bits = byte >> 5
    type = str(type_bits)
    
    # Extract the remaining 5 bits (value)
    # Mask with 0b11111 to get last 5 bits
    # Example:
    # Original byte:  10110110
    #            AND  00011111
    #            --------------
    #                 00010110
    value_bits = byte & 0b11111
    value = int(value_bits)
    
    return type, value