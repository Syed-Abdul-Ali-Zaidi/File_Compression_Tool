*************** File Compression Tool *************** 

A lightweight Python-based File Compression Tool that compresses and decompresses files using a hybrid approach of Run-Length Encoding (RLE) followed by Huffman Coding.
The project includes a simple and user-friendly CustomTkinter GUI for easy file selection and processing.

📁 Project Structure:
<br>
-> rle.py       - Run-Length Encoding compression and decompression logic
<br>
-> huffman.py   - Huffman encoding and decoding logic
<br>
-> process.py   - Integrates RLE and Huffman for full compression/decompression
<br>
-> main.py      - Main application file with CustomTkinter GUI

✨ Features:
<br>

-> Hybrid compression using RLE → Huffman Encoding.
<br>
-> Accurate and lossless decompression.
<br>
-> Simple, clean, and interactive GUI.
<br>
-> Modular and well-structured codebase.
<br>
-> Easy to understand and maintain.

🛠️ Requirements:
<br>

-> Python 3.x.
<br>
-> customtkinter.
<br>
-> Install CustomTkinter library using:  pip install customtkinter
<br>

▶️ Usage:
<br>

-> Run the application using:  python main.py

🖥️ GUI Functionality:
<br>

-> Using the graphical interface, you can:
<br>
    * Select a file and compress it.
    <br>
    * Save the generated compressed file.
    <br>
    * Select a compressed file and decompress it.
    <br>
    * View status messages and file paths during processing.

⚙️ How It Works:
<br>

The input file is first processed using Run-Length Encoding (RLE) to reduce repeating patterns.
The RLE output is further compressed using Huffman Coding.
During decompression, the process is reversed to perfectly restore the original file.

📌 Notes

* This project demonstrates the practical implementation of lossless compression algorithms.
* This project also serves as a Powerful Encrypter and Decrypter.
* Intended for educational and academic purposes.# File_Compression_Tool
* File Compression Tool using Run-Length Encoding (RLE) and Huffman Encoding to reduce file size efficiently.
