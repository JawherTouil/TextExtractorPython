Text Extractor
A fun little side project designed to help with my daily work of extracting text or code snippets from images. This tool simplifies the process of converting image-based text into editable text, making it especially useful for learning, studying, and streamlining workflows.

Features
Extract text from images using Tesseract OCR or EasyOCR (toggleable).
Clean and simple interface built with Tkinter.
Clipboard-style history of extracted text during the session.
Temporary storage of extracted text that clears after restarting the tool.
Screenshot support (paste directly from clipboard).
Clear functionality for removing text from the interface without affecting clipboard history.
Requirements
Before running the project, ensure you have the following installed:

Python 3.10+
Download and install Python from python.org.

Pillow (Python Imaging Library fork)
Install it via pip:

bash
Copy code
pip install Pillow
Pytesseract (Python wrapper for Tesseract OCR)
Install it via pip:

bash
Copy code
pip install pytesseract
Tesseract OCR (Standalone tool)
Download and install Tesseract OCR from tesseract-ocr/tesseract GitHub releases.
During installation:

Choose the desired language files (e.g., English).
Add Tesseract to your system PATH.
EasyOCR (Optional for OCR)
If you want to use EasyOCR as an alternative to Tesseract:

bash
Copy code
pip install easyocr
PyInstaller (For packaging into an .exe)
Optional: If you want to generate a standalone .exe version of the project:

bash
Copy code
pip install pyinstaller
Setup Instructions
1. Clone the Repository
bash
Copy code
git clone https://github.com/jojotwil/TextExtractorPython
cd TextExtractor
2. Install Required Python Packages
bash
Copy code
pip install -r requirements.txt
If requirements.txt is missing, manually install the following:

bash
Copy code
pip install Pillow pytesseract easyocr
3. Ensure Tesseract OCR is Installed
Verify Tesseract OCR is installed and accessible from the command line:

bash
Copy code
tesseract --version
If not recognized, add the Tesseract installation directory to your system PATH.

4. Run the Application
Run the script directly with:

bash
Copy code
python text_extractor.py
Optional: Create an Executable
If you'd like to create a standalone .exe for easier distribution:

bash
Copy code
pyinstaller --onefile text_extractor.py
The .exe file will be located in the dist/ folder.

How It Works
Upload an Image: Use the Open File button to select an image or paste a screenshot directly from the clipboard.
Extract Text: The tool processes the image using Tesseract OCR or EasyOCR (toggle between them) and displays the text in the text box.
Clipboard History: View and reuse previous extractions during the same session from the history sidebar.
Clear Functionality: Remove all extracted text from the interface while preserving clipboard history until the application is closed or restarted.
Why I Built This
This project started as a simple way to streamline my daily workflow. When studying or learning, I often come across screenshots or images containing text or code. Manually retyping this information was a hassle, so I built this tool to make the process easier, faster, and more enjoyable.

Planned Improvements
Add support for extracting text from multiple images simultaneously.
Integrate language auto-detection for multilingual text extraction.
Provide options for saving extracted text to files.
Improve the UI design for a more modern look.
License
This project is free to use for personal and educational purposes. Feel free to contribute and suggest improvements!

