import os
from tkinter import filedialog
import customtkinter as ctk
from process import encode, decode
import threading

def file_dialog():
    """Open file dialog to select a file for compression or decompression."""

    global file_path
    if current_mode == "compress":
        file_path = filedialog.askopenfilename(title="Select file to compress")
    else:
        # Only allow our custom extension for decompression
        file_path = filedialog.askopenfilename(title="Select file to Decompress",filetypes=[("Compressed Files","*.usa")])

    if file_path:
        file_entry.delete(0, "end")
        file_entry.insert(0, file_path)
    validate_file_path()


def folder_dialog():
    """Open folder dialog to select destination folder."""

    global folder_path
    folder_path = filedialog.askdirectory(title="Select destination folder")
    if folder_path:
        folder_entry.delete(0, "end")
        folder_entry.insert(0, folder_path)
    validate_folder_path()


def validate_file_path(event=None):
    """Validate the selected file path and display error messages if invalid."""

    global file_path
    file_path = file_entry.get().strip()

    if not os.path.isfile(file_path):
        file_error_label.configure(text="Invalid File Path. Please provide a valid file.")
        if folder_frame.winfo_ismapped():
            folder_frame.pack_forget()
    elif current_mode == "decompress" and not file_path.lower().endswith(".usa"):
        file_error_label.configure(text="Invalid file type. Please select a .usa file for decompression.")
        if folder_frame.winfo_ismapped():
            folder_frame.pack_forget()
    else:
        file_error_label.configure(text="")  # clear error
        if not folder_frame.winfo_ismapped():
            folder_frame.pack(padx=2, pady=15)

    update_start_button()



def validate_folder_path(event=None):
    """Validate the selected folder path and display error messages if invalid."""

    global folder_path
    folder_path = folder_entry.get().strip()
    if os.path.isdir(folder_path):
        folder_error_label.configure(text="")
    else:
        folder_error_label.configure(text="Invalid Folder Path. Please provide a valid folder.")
    update_start_button()

def update_start_button():
    """Enable the start button only if both file and folder paths are valid."""

    filepath = file_entry.get().strip()
    folderpath = folder_entry.get().strip()

    if os.path.isfile(filepath) and os.path.isdir(folderpath):
        start_btn.configure(state="normal")
    else:
        start_btn.configure(state="disabled")

def set_mode(mode):
    """Switch between compression and decompression modes in the UI."""

    global current_mode
    current_mode = mode

    undo_details_labels() # clear previous process details

    if mode == "compress":
        file_label.configure(text="Select File to Compress:")
        start_btn.configure(text="Start Compression")
    else:
        file_label.configure(text="Select File to Decompress:")
        start_btn.configure(text="Start Decompression")

def make_compressed_filename(filename):
    """Generate a compressed file name with .usa extension."""

    name, ext = os.path.splitext(filename)
    ext = ext[1:]
    return f'{name}_{ext}.usa'

def recover_original_filename(filepath):
    """Recover original file name from the compressed .usa file."""

    filename = os.path.basename(filepath)  # filename is with our extension
    filename = os.path.splitext(filename)[0]  # our extension removed

    if '_' in filename:
        # split only at the last '_', in case somehow others exist
        name, ext = filename.rsplit('_', 1)
        return f"{name}.{ext}"
    else:
        # fallback: no hidden extension
        return filename


def process():
    """Perform compression or decompression and update process_result."""

    global process_result
    update_progress(0.05)  # update progress bar

    if current_mode == "compress":
        update_progress(0.2)  # update progress bar
        with open(file_path, "rb") as f:
            original_data = f.read()
        update_progress(0.4)  # update progress bar

        compressed_data, rle_used = encode(original_data)

        update_progress(0.8)

        file_name = os.path.basename(file_path)
        file_name = make_compressed_filename(file_name)
        destination_path = os.path.join(folder_path, file_name)

        with open(destination_path, "wb") as f:
            f.write(bytes([1 if rle_used else 0]))
            f.write(compressed_data)

        update_progress(0.9)

        # store results for later use by update_labels()
        process_result = {
            "status": "Compressed Successfully!",
            "original_size": len(original_data),
            "compressed_size": len(compressed_data),
            "decompressed_size":None,
            "destination_path": destination_path,
            "rle_used": rle_used,
        }

    else:  # decompress mode
        update_progress(0.05)  # update progress bar

        with open(file_path, "rb") as f:
            rle_flag = f.read(1)[0]
            rle_used = bool(rle_flag)
            compressed_data = f.read()

        update_progress(0.4)  # update progress bar

        original_data = decode(compressed_data, rle_used)

        update_progress(0.6)  # update progress bar

        file_name = recover_original_filename(file_path)
        destination_path = os.path.join(folder_path, file_name)

        with open(destination_path, "wb") as f:
            f.write(original_data)

        update_progress(0.9)  # update progress bar

        process_result = {
            "status": "Decompressed Successfully!",
            "original_size": len(compressed_data),
            "decompressed_size":len(original_data),
            "compressed_size": None,
            "destination_path": destination_path
        }
    # full complete
    update_progress(1.0)  # update progress bar

def update_labels():
    """Update the UI labels and progress info after process completes."""

    global process_result
    result = process_result

    process_label0.pack(anchor="w", padx=15)

    progressbar.pack(pady=1)
    # Updating progress bar label
    process_label0.configure(text="Completed!")

    process_label1.configure(text=result["status"])
    process_label1.pack(anchor="w", padx=15)

    process_label2.configure(text=f'Original Size:           {round(result["original_size"]/1024,2)} KB')
    process_label2.pack(anchor="w", padx=15)

    if result["decompressed_size"] is None:
        process_label3.configure(text=f'Compressed Size:    {round(result["compressed_size"]/1024,2)} KB')
        process_label3.pack(anchor="w", padx=15)

        efficiency = round((100 - (result["compressed_size"] / result["original_size"]) * 100),2)
        process_label4.configure(text=f"Efficiency: {efficiency}% space saved!")
        process_label4.pack(anchor="w", padx=15)

    else:
        process_label3.configure(text=f'Decompressed Size: {round(result["decompressed_size"] / 1024, 2)} KB')
        process_label3.pack(anchor="w", padx=15)

def undo_details_labels():
    """Hide all process-related labels and progress bar."""

    process_label0.pack_forget()
    progressbar.pack_forget()
    process_label1.pack_forget()
    process_label2.pack_forget()
    process_label3.pack_forget()
    process_label4.pack_forget()

def disable_all_buttons():
    """Disable all interactive buttons to prevent user input during processing."""

    start_btn.configure(state="disabled")
    compression_button.configure(state="disabled")
    decompression_button.configure(state="disabled")
    browse_file_btn.configure(state="disabled")
    browse_folder_btn.configure(state="disabled")
    start_btn.configure(state="disabled")

def enable_all_buttons():
    """Enable all buttons after process is complete."""

    start_btn.configure(state="normal")
    compression_button.configure(state="normal")
    decompression_button.configure(state="normal")
    browse_file_btn.configure(state="normal")
    browse_folder_btn.configure(state="normal")
    start_btn.configure(state="normal")

def update_progress(value):
    """Update the progress bar value on the main UI thread."""

    app.after(0, lambda: progressbar.set(value))

def start_process():
    """Start compression/decompression in a separate thread to keep UI responsive."""

    try:
        progressbar.set(0)

        undo_details_labels()  # Erasing previous process details if written

        # Disable all buttons before starting the process
        disable_all_buttons()

        process_label0.pack(anchor="w", padx=15, pady=1)
        progressbar.pack(pady=2)
        process_label0.configure(text="Processing...")

        def run_and_update():
            try:
                process()  # compression/decompression logic
                # Schedule UI update + re-enable buttons back on the main thread
                app.after(0, update_labels)
                app.after(0, enable_all_buttons)
            except Exception as e:
                print("Error in thread:", e)
                app.after(0, enable_all_buttons)  # re-enable even if there's an error

        # Run in background thread to keep UI responsive
        thread = threading.Thread(target=run_and_update, daemon=True)
        thread.start()
    except Exception as e:
        process_label1.configure(text=f"Error: {str(e)}", text_color="red")


# ---------------- MAIN UI ----------------
ctk.set_appearance_mode("system") # Use system theme (light/dark)
LABEL_FONT = ("Segoe UI", 13)
TITLE_FONT = ("Segoe UI Semibold", 15)
ENTRY_FONT = ("Segoe UI", 12)


app = ctk.CTk()
app.geometry("600x580+400+70")  # Window size and position
app.title("File Compression Tool")
app.minsize(height=580, width= 600)

# Footer at the bottom
footer = ctk.CTkLabel(app, text= "© 2025  File Compression Tool  •  RLE & Huffman  •  Developed by Asim & Co.",font= ("Segoe UI",11),text_color= "#777777")
footer.pack(side="bottom", pady=1)

# ---------- TOP FRAME (Mode Selection) ----------
frame1 = ctk.CTkFrame(app, width=450, height=50, fg_color="light grey")
frame1.pack(pady=5)

current_mode = "compress" # default MODE
file_path = ""
folder_path = ""
process_result = {}

# Mode selection buttons
compression_button = ctk.CTkButton(frame1, text="Compress",command=lambda: set_mode("compress"),font= TITLE_FONT)
compression_button.pack(side="left", padx=10, pady=10)

decompression_button = ctk.CTkButton(frame1, text="Decompress",command=lambda: set_mode("decompress"),font= TITLE_FONT)
decompression_button.pack(side="right", padx=10, pady=10)

# ---------- MIDDLE SECTION (File & Folder Selection) ----------
sec_frame = ctk.CTkFrame(app, width=585, height=335, fg_color="light grey")
sec_frame.pack()
sec_frame.pack_propagate(False)

# --- File Selection Frame ---
file_frame = ctk.CTkFrame(sec_frame, width=581, height=120, fg_color="white")
file_frame.pack(padx=2, pady=15)
file_frame.pack_propagate(False)

file_label = ctk.CTkLabel(file_frame, text="Select File to Compress:",font= LABEL_FONT)
file_label.pack(anchor="w", padx=15, pady=10)

# Inner frame for entry + browse button
file_input_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
file_input_frame.pack(fill="x", padx=3)

file_entry = ctk.CTkEntry(file_input_frame, placeholder_text="Type or browse file path...",font= ENTRY_FONT)
file_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
file_entry.bind("<KeyRelease>", validate_file_path)

browse_file_btn = ctk.CTkButton(file_input_frame, text="Browse",font=("Arial",13,'bold'), width=100, command=file_dialog)
browse_file_btn.pack(side="right")

# File error label
file_error_label = ctk.CTkLabel(file_frame, text="", text_color="red", anchor="w", justify="left")
file_error_label.pack(fill="x", padx=15, pady=(5, 5))

# --- Folder Selection Frame (hidden initially) ---
folder_frame = ctk.CTkFrame(sec_frame, width=581, height=120, fg_color="white")
folder_frame.pack_propagate(False)

folder_label = ctk.CTkLabel(folder_frame, text="Select Destination Folder:",font= LABEL_FONT)
folder_label.pack(anchor="w", padx=15, pady=10)

# Inner frame for folder entry + browse button
folder_input_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
folder_input_frame.pack(fill="x", padx=3)

folder_entry = ctk.CTkEntry(folder_input_frame, placeholder_text="Type or browse folder path...",font = ENTRY_FONT)
folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
folder_entry.bind("<KeyRelease>", validate_folder_path)

browse_folder_btn = ctk.CTkButton(folder_input_frame, text="Browse",font=("Arial",13,'bold'), width=100, command=folder_dialog)
browse_folder_btn.pack(side="right")

# Folder error label
folder_error_label = ctk.CTkLabel(folder_frame, text="", text_color="red", anchor="w", justify="left")
folder_error_label.pack(fill="x", padx=15, pady=(5, 5))

# Start button for compression/decompression
start_btn = ctk.CTkButton(sec_frame,text = "Start Compression",state="disabled",font=TITLE_FONT,command=start_process)
start_btn.pack(side = "bottom",pady = 5)

# ---------- DETAILS SECTION (Progress & Info) ----------
detail_frame = ctk.CTkFrame(app,width=585, height=155, fg_color="light grey")
detail_frame.pack(pady=5)
detail_frame.pack_propagate(False)

# Labels & progress bar (hidden initially
process_label0 = ctk.CTkLabel(detail_frame, text='Processing...',font= LABEL_FONT)
progressbar = ctk.CTkProgressBar(detail_frame, width=560, progress_color="#00B894",corner_radius=5)
progressbar.set(0)

process_label1 = ctk.CTkLabel(detail_frame, text= '',font=("Segoe UI", 13,'bold'))
process_label2 = ctk.CTkLabel(detail_frame,text= '',font= LABEL_FONT)
process_label3 = ctk.CTkLabel(detail_frame,text= '',font= LABEL_FONT)
process_label4 = ctk.CTkLabel(detail_frame,text= '',font= LABEL_FONT)

# Start the GUI main loop
app.mainloop()

