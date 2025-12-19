
def rle_compress(original : bytes):
    """Run_Length_Encoding Compression"""

    # If input is empty, return empty bytes
    if not original:
        return b''

    results = bytearray()   # To store the compressed output
    current_run_byte = original[:1] # Start with the first byte
    run_length = 1  # Initial count of the first byte

    # Loop through the rest of the bytes
    for i in range(1,len(original)):
        current_byte = original[i:i+1]
        # Check if current byte is same as the last one and count < 255
        if current_byte == current_run_byte and run_length < 255: # can't store bytes more than 255
            run_length += 1 # Update  the run length
        else:
            # Append the byte and its run length to results
            results.extend(current_run_byte)
            results.extend(bytes(run_length))
            # Start new run
            current_run_byte = current_byte
            run_length = 1

    # Add the last byte run to results
    results.extend(current_run_byte)
    results.extend(bytes(run_length))

    # If compression didn't reduce size, return original
    if len(results) > len(original):
        return original, False

    # Return compressed data and True indicating compression succeeded
    return bytes(results), True

def rle_decompress(compressed_text):
    """Run_Length_Encoding Decompression"""

    # If input is empty, return empty bytes
    if not compressed_text:
        return b''

    results = bytearray()   # To store the decompressed output

    # Process each pair of byte and count
    for i in range(0,len(compressed_text),2):
        byte = compressed_text[i:i+1]   # The actual byte
        run_length = compressed_text[i+1]   # How many times to repeat it

        results.extend(byte * run_length)   # Repeat the byte and add to output

    return bytes(results)   # Convert to immutable bytes before returning