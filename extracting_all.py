# Install necessary libraries
#!apt-get install -y poppler-utils
#!apt-get install -y tesseract-ocr
#!pip install pytesseract pdf2image pypdf2 openpyxl Pillow streamlit

# Import libraries
import streamlit as st
from pdf2image import convert_from_path
import pytesseract
import os
import csv
from PIL import Image

# Set up Streamlit app
st.title("PDF and Image Text Extractor")
st.write("Upload your PDF or image files to extract text.")

# File uploader
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

# Process uploaded files
if uploaded_files:
    output_csv_file = "all_data.csv"
    output_txt_file = "all_data.txt"

    with open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile_csv, \
         open(output_txt_file, 'w', encoding='utf-8') as outfile_txt:

        writer = csv.writer(outfile_csv)

        for uploaded_file in uploaded_files:
            file_path = os.path.join("/content", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if uploaded_file.name.lower().endswith('.pdf'):
                # Handle PDF files
                try:
                    # Convert PDF to images
                    images = convert_from_path(file_path, dpi=300, fmt='jpeg')

                    # Extract text from images using OCR
                    text = ""
                    for img in images:
                        text += pytesseract.image_to_string(img)

                    # Append text to the output CSV
                    for line in text.splitlines():
                        writer.writerow([line])

                    # Append text to the output TXT
                    outfile_txt.write(text)

                    st.success(f"Text from {uploaded_file.name} appended to output files.")

                except PyPDF2.errors.PdfReadError:
                    st.error(f"Error: {uploaded_file.name} is not a valid PDF.")

            elif uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Handle image files
                try:
                    # Open the image
                    img = Image.open(file_path)

                    # Extract text from the image using OCR
                    text = pytesseract.image_to_string(img)

                    # Append text to the output CSV
                    for line in text.splitlines():
                        writer.writerow([line])

                    # Append text to the output TXT
                    outfile_txt.write(text)

                    st.success(f"Text from {uploaded_file.name} appended to output files.")

                except IOError:
                    st.error(f"Error: Unable to open image {uploaded_file.name}.")

            else:
                st.warning(f"Skipping file: {uploaded_file.name} (not a PDF or supported image)")

    st.write("Process completed. Check the output files for the extracted text.")
