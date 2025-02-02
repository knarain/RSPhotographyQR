import os
import glob
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import qrcode
from PIL import Image

# Function to generate QR code
def generate_qr_code():
    data = entry_data.get()  # Get data from entry widget
    if data:
        try:
            # Create QR code object
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)  # Add data to QR code
            qr.make(fit=True)
            
            # Get selected color palette
            selected_palette = color_palettes[palette_combobox.get()]
            
            # Create QR code image with selected colors
            img = qr.make_image(fill_color=selected_palette[0], back_color=selected_palette[1])
            
            # Optionally embed an image in the QR code
            if with_image_var.get():
                image_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
                if image_file:
                    image = Image.open(image_file)
                    image = image.resize((100, 100))
                    img.paste(image, (img.size[0] // 2 - 50, img.size[1] // 2 - 50))
            
            # Save the QR code image
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                img.save(file_path)
                status_label.config(text="QR code generated successfully!", fg="green")
            else:
                status_label.config(text="QR code generation canceled", fg="red")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        status_label.config(text="Please enter data for QR code generation", fg="red")

# Function to select source folder for file moving
def select_source_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder_selected)

# Function to move files from source to destination folder
def move_files():
    source = source_entry.get()
    folder_name = folder_name_entry.get()
    file_format = file_format_var.get() if file_format_var.get() != "Other" else manual_format_entry.get()

    if not source or not folder_name or not file_format:
        status_label.config(text="Please provide source, folder name, and file format.")
        return

    destination = os.path.join(source, folder_name)
    os.makedirs(destination, exist_ok=True)

    allfiles = glob.glob(os.path.join(source, f"*{file_format}"))
    if not allfiles:
        status_label.config(text="No files found with the specified format.", fg="red")
        return

    num_files = len(allfiles)
    progress_step = 100 / num_files

    progress_bar['value'] = 0
    for idx, file_path in enumerate(allfiles, start=1):
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            dst_path = os.path.join(destination, f'{file_name}.{file_format[1:]}')
            shutil.move(file_path, dst_path)
            status_label.config(text=f"Moved {file_path} -> {dst_path}")
            progress_bar['value'] = idx * progress_step
            root.update()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while moving {file_path}: {e}")

# Function to show QR code generator frame
def show_qr_code_generator():
    qr_code_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    file_mover_frame.grid_forget()

# Function to show file mover frame
def show_file_mover():
    qr_code_frame.grid_forget()
    file_mover_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# GUI setup
root = tk.Tk()
root.title("QR Code and File Move")

# Color palettes for QR code generator
color_palettes = {
    "Black on White": ("black", "white"),
    "White on Black": ("white", "black"),
    "Red on Yellow": ("red", "yellow"),
    "Green on White": ("green", "white"),
    "Blue on White": ("blue", "white"),
    "Yellow on Black": ("yellow", "black"),
    "Purple on White": ("purple", "white"),
    "Orange on Black": ("orange", "black"),
    "Cyan on White": ("cyan", "white"),
    "Magenta on White": ("magenta", "white"),
    "Pink on Black": ("pink", "black"),
    "Brown on White": ("brown", "white"),
    # Add more color palettes as needed
}

# Main menu setup
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# QR code generator submenu
qr_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="QR Code Generator", menu=qr_menu)
qr_menu.add_command(label="Generate QR Code", command=show_qr_code_generator)

# File mover submenu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File Mover", menu=file_menu)
file_menu.add_command(label="Move Files", command=show_file_mover)

# QR Code Generator widgets
qr_code_frame = ttk.Frame(root, padding="10")

label_data = ttk.Label(qr_code_frame, text="Enter data for QR code:")
label_data.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_data = ttk.Entry(qr_code_frame, width=50)
entry_data.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

label_palette = ttk.Label(qr_code_frame, text="Select Color Palette:")
label_palette.grid(row=1, column=0, padx=10, pady=5, sticky="w")

palette_combobox = ttk.Combobox(qr_code_frame, values=list(color_palettes.keys()), state="readonly")
palette_combobox.current(0)
palette_combobox.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

with_image_var = tk.BooleanVar()
with_image_var.set(False)

with_image_check = ttk.Checkbutton(qr_code_frame, text="Embed Image", variable=with_image_var)
with_image_check.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="n")

button_generate = ttk.Button(qr_code_frame, text="Generate QR Code", command=generate_qr_code)
button_generate.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# File Mover widgets
file_mover_frame = ttk.Frame(root, padding="10")

source_label = ttk.Label(file_mover_frame, text="Source Path:")
source_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
source_entry = ttk.Entry(file_mover_frame, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=5)
source_button = ttk.Button(file_mover_frame, text="Browse", command=select_source_folder)
source_button.grid(row=0, column=2, padx=5, pady=5)

folder_name_label = ttk.Label(file_mover_frame, text="Folder Name:")
folder_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
folder_name_entry = ttk.Entry(file_mover_frame, width=50)
folder_name_entry.grid(row=1, column=1, padx=10, pady=5)

file_format_label = ttk.Label(file_mover_frame, text="File Format:")
file_format_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
file_format_var = tk.StringVar(file_mover_frame)
file_format_combobox = ttk.Combobox(file_mover_frame, textvariable=file_format_var, width=20, state="readonly")
file_format_combobox['values'] = (
    ".ARW", ".JPG", ".PNG", ".JPEG", ".TIFF", ".BMP", ".GIF", ".HEIC", ".ICO", 
    ".IM", ".MSP", ".PCX", ".PPM", ".SGI", ".SPIDER", ".TGA", ".WEBP", "Other"
)
file_format_combobox.grid(row=2, column=1, padx=10, pady=5)
file_format_combobox.current(0)

manual_format_label = ttk.Label(file_mover_frame, text="Manual Format:")
manual_format_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
manual_format_entry = ttk.Entry(file_mover_frame, width=20)
manual_format_entry.grid(row=3, column=1, padx=10, pady=5)

# Enable manual format entry if "Other" is selected
def set_manual_format(*args):
    if file_format_var.get() == "Other":
        manual_format_entry.config(state="normal")
        manual_format_entry.delete(0, tk.END)
    else:
        manual_format_entry.config(state="disabled")

file_format_var.trace_add("write", set_manual_format)

move_button = ttk.Button(file_mover_frame, text="Move Files", command=move_files)
move_button.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

progress_frame = ttk.Frame(file_mover_frame)
progress_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

progress_label = ttk.Label(progress_frame, text="Progress:")
progress_label.pack(side="left", padx=5)

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
progress_bar.pack(side="left", fill="x", expand=True, padx=5)

status_label = ttk.Label(file_mover_frame, text="", foreground="green")
status_label.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# Initially hide file mover frame
file_mover_frame.grid_forget()

root.mainloop()
