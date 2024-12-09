import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import pytesseract
import pyperclip
from PIL import ImageGrab
import easyocr  # Import EasyOCR
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global variables
history = []  # To store history of extracted texts
current_image = None  # To store the current image
use_easyocr = False  # Toggle between Tesseract and EasyOCR

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
        # Preprocess image for better results
        processed_image = preprocess_image(image)

        if use_easyocr:
            # EasyOCR Extraction
            reader = easyocr.Reader(['en'])
            results = reader.readtext(np.array(processed_image))
            text = "\n".join([res[1] for res in results])
        else:
            # Tesseract Extraction
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
    # Clear the text displayed in the GUI
    extracted_text.delete(1.0, tk.END)
    # Remove the image from the display
    image_label.config(image="")
    image_label.image = None
    # Preserve the history and clipboard
    #messagebox.showinfo("Clear", "Display cleared! Clipboard history preserved.")

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
app = tk.Tk()
app.title("Text Extractor")
app.geometry("600x400")

# Left section (Image and text display)
left_frame = tk.Frame(app)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Image display
image_label = tk.Label(left_frame, text="Paste a screenshot here", width=40, height=10, bg="lightgray")
image_label.pack(pady=10)

# Text display area
extracted_text = tk.Text(left_frame, height=10, width=50)
extracted_text.pack(pady=10)

# Clear button
btn_clear = tk.Button(left_frame, text="Clear", command=clear_all)
btn_clear.pack()

# OCR Toggle Button
ocr_label = tk.Label(left_frame, text="OCR Method: Tesseract")
ocr_label.pack()
btn_toggle_ocr = tk.Button(left_frame, text="Toggle OCR", command=toggle_ocr_method)
btn_toggle_ocr.pack()

# Right section (Clipboard history)
right_frame = tk.Frame(app)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

history_label = tk.Label(right_frame, text="Clipboard History")
history_label.pack()

history_list = tk.Listbox(right_frame, height=20, width=20)
history_list.pack(pady=10)
history_list.bind("<Double-Button-1>", copy_from_history)

# Shortcut to paste
app.bind("<Control-v>", lambda event: paste_screenshot())

app.mainloop()
