
# Node structure for Huffman tree
class Node:

    def __init__(self, byte=None, freq=0):
        self.byte = byte  # Leaf node value (0–255), None for internal nodes
        self.freq = freq  # Frequency of the byte
        self.left = None  # Left child
        self.right = None  # Right child

    def __lt__(self, other):
        """Enable sorting nodes by frequency."""
        return self.freq < other.freq


# --- 2. TREE BUILDING LOGIC ---

def _build_frequency_map(data: bytes) -> dict:
    """Count frequency of each byte."""
    frequency_map = {}
    for byte_value in data:
        if byte_value in frequency_map:
            frequency_map[byte_value] += 1
        else:
            frequency_map[byte_value] = 1
    return frequency_map


def _build_huffman_tree(frequency_map: dict) -> Node | None:
    """Build Huffman tree by repeatedly merging lowest-frequency nodes."""
    nodes = []

    # Create initial leaf nodes
    for byte_value, frequency in frequency_map.items():
        nodes.append(Node(byte=byte_value, freq=frequency))

    if not nodes:
        return None

    # Merge nodes until one tree remains
    while len(nodes) > 1:
        nodes.sort()  # Sort by frequency
        n1 = nodes.pop(0)  # Smallest
        n2 = nodes.pop(0)  # Second smallest

        # Create parent node with combined frequency
        merged_node = Node(freq=n1.freq + n2.freq)
        merged_node.left = n1
        merged_node.right = n2

        nodes.append(merged_node)

    return nodes[0]  # Final root


def _generate_codes(node: Node, current_code: str = "", codes: dict = None) -> dict:
    """Traverse tree and assign binary codes to each byte."""
    if codes is None:
        codes = {}

    if node is None:
        return codes

    # Leaf node → assign code
    if node.byte is not None:
        codes[node.byte] = current_code or "0"  # Handle single-byte edge case
        return codes

    # Traverse left = 0
    _generate_codes(node.left, current_code + "0", codes)
    # Traverse right = 1
    _generate_codes(node.right, current_code + "1", codes)

    return codes


# --- 3. CUSTOM SERIALIZATION (Replaces JSON) ---

def _serialize_codes(codes: dict) -> bytes:
    """Serialize dictionary as bytes: (byte, code_length, code_string)."""
    serialized_parts = []

    for byte_value, code_string in codes.items():
        serialized_parts.append(bytes([byte_value]))  # Byte
        serialized_parts.append(bytes([len(code_string)]))  # Code length
        serialized_parts.append(code_string.encode('ascii'))  # Code bits as ASCII

    serialized_data = b''.join(serialized_parts)

    # Prefix with 4-byte length header
    length_prefix = len(serialized_data).to_bytes(4, 'big')
    return length_prefix + serialized_data


def deserialize_codes(serialized_data: bytes):
    """Deserialize dictionary from byte format."""
    codes = {}
    length_prefix = serialized_data[:4]  # Dictionary size
    dict_length = int.from_bytes(length_prefix, 'big')

    payload = serialized_data[4:4 + dict_length]

    i = 0
    while i < len(payload):
        byte_value = payload[i]  # Original byte
        i += 1

        code_length = payload[i]  # Length of code
        i += 1

        code_string = payload[i: i + code_length].decode('ascii')  # Code bits
        i += code_length

        codes[byte_value] = code_string

    return codes, serialized_data[4 + dict_length:]  # Return dictionary + remaining payload


# --- 4. PUBLIC COMPRESSION FUNCTION ---

def huffman_compress_dsa(data: bytes) -> tuple[bytes, bytes]:
    """Compress data using Huffman coding and return header + payload."""
    if not data:
        return b'', b''

    freq = _build_frequency_map(data)  # Frequency table
    root = _build_huffman_tree(freq)  # Huffman tree
    codes = _generate_codes(root)  # Byte→code mapping

    # Encode input to bitstring
    encoded_bits = "".join(codes[b] for b in data)

    # Pad to byte boundary
    padding = 8 - (len(encoded_bits) % 8)
    if padding == 8:
        padding = 0
    encoded_bits += '0' * padding

    # Convert bitstring to bytes
    padded_info = bytes([padding])  # Store padding size
    compressed_bytes = bytearray()
    for i in range(0, len(encoded_bits), 8):
        compressed_bytes.append(int(encoded_bits[i:i + 8], 2))

    compressed_payload = padded_info + bytes(compressed_bytes)

    # Serialize dictionary (header)
    serialized_codes = _serialize_codes(codes)

    return serialized_codes, compressed_payload


# --- 5. PUBLIC DECOMPRESSION FUNCTIONS ---

def _rebuild_tree_from_codes(codes: dict) -> Node:
    """Rebuild Huffman tree from serialized codes."""
    root = Node()

    for byte_val, code in codes.items():
        node = root
        for bit in code:
            if bit == '0':
                if not node.left:
                    node.left = Node()
                node = node.left
            else:
                if not node.right:
                    node.right = Node()
                node = node.right

        node.byte = byte_val  # Assign leaf byte
    return root


def huffman_decompress_dsa(compressed_payload: bytes, codes: dict) -> bytes:
    """Decompress Huffman-encoded payload using stored codes."""
    if not compressed_payload or not codes:
        return b''

    padding = compressed_payload[0]  # Read padding count
    encoded_bytes = compressed_payload[1:]  # Actual payload

    # Convert bytes to bitstring
    bit_string = ''
    for byte in encoded_bytes:
        bit_string += f"{byte:08b}"

    if padding:
        bit_string = bit_string[:-padding]  # Remove padding bits

    # Decode using Huffman tree
    root = _rebuild_tree_from_codes(codes)
    decoded = bytearray()
    node = root

    for bit in bit_string:
        if bit == '0':
            node = node.left
        else:
            node = node.right

        # Leaf node reached → append byte
        if node.byte is not None:
            decoded.append(node.byte)
            node = root  # Reset to root

    return bytes(decoded)
