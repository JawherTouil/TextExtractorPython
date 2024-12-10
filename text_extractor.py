import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import pyperclip
from PIL import ImageGrab
import easyocr  # Import EasyOCR
import numpy as np

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your path

# Global variables
history = []
current_image = None
use_easyocr = False

def paste_screenshot():
    """Handles pasted screenshots and processes them."""
    global current_image
    try:
        image = ImageGrab.grabclipboard()
        if image:
            current_image = image
            display_image(image)
            extract_text_from_image(image)
        else:
            messagebox.showwarning("No Image", "No image found in clipboard. Paste a valid screenshot.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def display_image(image):
    """Displays the pasted image in the GUI."""
    img = image.resize((300, 200))
    tk_image = ImageTk.PhotoImage(img)
    image_label.config(image=tk_image)
    image_label.image = tk_image

def preprocess_image(image):
    """Preprocesses the image for better OCR accuracy."""
    import cv2
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return Image.fromarray(gray)

def extract_text_from_image(image):
    """Extracts text from the given image using the selected OCR method."""
    global use_easyocr
    try:
        processed_image = preprocess_image(image)

        if use_easyocr:
            reader = easyocr.Reader(['en'])
            results = reader.readtext(np.array(processed_image))
            text = "\n".join([res[1] for res in results])
        else:
            text = pytesseract.image_to_string(processed_image)

        if text.strip():
            extracted_text.insert(tk.END, text)
            history.append(text)
            update_history_sidebar()
        else:
            messagebox.showinfo("No Text", "No text found in the image!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while extracting text: {e}")

def update_history_sidebar():
    """Updates the clipboard history sidebar."""
    history_list.delete(0, tk.END)
    for idx, text in enumerate(history, start=1):
        history_list.insert(tk.END, f"Item {idx}")

def clear_all():
    """Clears the current text and image while preserving clipboard history."""
    extracted_text.delete(1.0, tk.END)
    image_label.config(image="")
    image_label.image = None

def copy_from_history(event):
    """Copies selected text from the history to the clipboard."""
    try:
        selected_index = history_list.curselection()
        if selected_index:
            selected_text = history[selected_index[0]]
            pyperclip.copy(selected_text)
            messagebox.showinfo("Copied", "Text copied to clipboard!")
        else:
            messagebox.showwarning("No Selection", "Please select an item to copy.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def toggle_ocr_method():
    """Toggles between Tesseract and EasyOCR."""
    global use_easyocr
    use_easyocr = not use_easyocr
    ocr_label.config(text=f"OCR Method: {'EasyOCR' if use_easyocr else 'Tesseract'}")

# GUI setup
app = ttk.Window(themename="solar") #  1- solar 
app.title("Text Extractor")
app.geometry("1000x650")

# Left section
left_frame = ttk.Frame(app, padding=10)
left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

image_label = ttk.Label(left_frame, text="Paste a screenshot here", bootstyle=SECONDARY, width=40)
image_label.pack(pady=10)

extracted_text = ttk.Text(left_frame, height=10, width=50)
extracted_text.pack(pady=10)

btn_clear = ttk.Button(left_frame, text="Clear", bootstyle=DANGER, command=clear_all)
btn_clear.pack(pady=5)

ocr_label = ttk.Label(left_frame, text="OCR Method: Tesseract", bootstyle=INFO)
ocr_label.pack(pady=5)
btn_toggle_ocr = ttk.Button(left_frame, text="Toggle OCR", bootstyle=SUCCESS, command=toggle_ocr_method)
btn_toggle_ocr.pack(pady=5)

# Right section
right_frame = ttk.Frame(app, padding=10)
right_frame.pack(side=RIGHT, fill=Y, padx=10, pady=10)

history_label = ttk.Label(right_frame, text="Clipboard History", bootstyle=INFO)
history_label.pack()

history_list = tk.Listbox(right_frame, height=20, width=30)
history_list.pack(pady=10)
history_list.bind("<Double-Button-1>", copy_from_history)

# Paste shortcut
app.bind("<Control-v>", lambda event: paste_screenshot())

app.mainloop()
