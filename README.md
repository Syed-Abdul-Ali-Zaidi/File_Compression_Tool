File Compression Tool

A lightweight Python-based File Compression Tool that compresses and decompresses files using a hybrid approach of Run-Length Encoding (RLE) followed by Huffman Coding.
The project includes a simple and user-friendly CustomTkinter GUI for easy file selection and processing.

📁 Project Structure
rle.py        - Run-Length Encoding compression and decompression logic
huffman.py   - Huffman encoding and decoding logic
process.py   - Integrates RLE and Huffman for full compression/decompression
main.py      - Main application file with CustomTkinter GUI

✨ Features

Hybrid compression using RLE → Huffman Encoding

Accurate and lossless decompression

Simple, clean, and interactive GUI

Modular and well-structured codebase

Easy to understand and maintain

🛠️ Requirements

Python 3.x

customtkinter

Install CustomTkinter using:

pip install customtkinter

▶️ Usage

Run the application using:

python main.py

🖥️ GUI Functionality

Using the graphical interface, you can:

Select a file and compress it

Save the generated compressed file

Select a compressed file and decompress it

View status messages and file paths during processing

⚙️ How It Works

The input file is first processed using Run-Length Encoding (RLE) to reduce repeating patterns.

The RLE output is further compressed using Huffman Coding.

During decompression, the process is reversed to perfectly restore the original file.

👥 Group Members

Muhammad Faiz Alam (CS-24128)

Syed Abdul Ali Zaidi (CS-24131)

📌 Notes

This project demonstrates the practical implementation of lossless compression algorithms.

Intended for educational and academic purposes.# File_Compression_Tool
File Compression Tool using Run-Length Encoding (RLE) and Huffman Encoding to reduce file size efficiently.
