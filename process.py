from  rle import rle_compress,rle_decompress
from huffman import huffman_compress_dsa,deserialize_codes,huffman_decompress_dsa


def encode(data):
    """
        Compress the input data using RLE first, then Huffman encoding.

        Returns:
            compressed_data: bytes object containing the final compressed data
            rle_used: boolean indicating whether RLE was effective

    """

    # First compress with RLE
    rle_compressed, rle_used = rle_compress(data)
    # Then compress with Huffman and get header + payload
    serialized_codes_header, compressed_payload = huffman_compress_dsa(rle_compressed)

    # Combine header and payload
    compressed_data = serialized_codes_header + compressed_payload

    # Return the final compressed data and whether RLE was used
    return compressed_data,rle_used

def decode(data,rle_used):
    """
        Decompress data that was compressed with encode().

        Args:
            data: bytes object of compressed data
            rle_used: boolean indicating if RLE was applied during encoding

        Returns:
            decompressed_data: original uncompressed bytes
    """

    # Separate Huffman header from payload
    deserialized_codes, payload_from_file = deserialize_codes(data)
    # Decompress Huffman
    huffman_decomp = huffman_decompress_dsa(payload_from_file, deserialized_codes)
    # If RLE was used, decompress it
    if rle_used:
        decompressed_data = rle_decompress(huffman_decomp)
    else:
        decompressed_data = huffman_decomp

    # Return the fully decompressed data
    return decompressed_data
