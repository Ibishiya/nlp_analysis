import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import csv
from PIL import Image
import re
import io

# Set up Streamlit app
st.title("PDF and Image Text Extractor")
st.write("Upload your PDF or image files to extract text.")

# Verify and display logo
logo_path = r"C:\Users\lenovo\Pictures\Davivienda-1024x597.png"  # Using raw string

# Try opening the image directly
try:
    logo_image = Image.open(logo_path)
    st.image(logo_image, width=200)  # Adjust width as needed
except Exception as e:
    st.error(f"Error loading logo image: {str(e)}")

# File uploader for debugging
uploaded_logo = st.file_uploader("Upload logo image for debugging", type=["png", "jpg", "jpeg"])
if uploaded_logo is not None:
    st.image(uploaded_logo, width=200)

# File uploader for PDF and image files
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

# Output lists
csv_output = []
txt_output = []
numbers_above_threshold = []
filtered_lines_with_context = []
filtered_lines_above_threshold = []

# Text Input for search term
search_term = st.text_input("Enter keyword or phrase to search for:")

# Number Input for threshold
threshold = st.number_input("Enter threshold value:", min_value=0, value=1000)

def extract_numbers_above_threshold(text, threshold):
    """Extract numbers greater than the given threshold from the text."""
    numbers = re.findall(r'\b\d+\b', text)
    return [int(num) for num in numbers if int(num) > threshold]

def find_lines_with_context(text, search_term, context=1):
    """Find lines containing the search term and their adjacent lines."""
    lines = text.splitlines()
    result = []
    for i, line in enumerate(lines):
        if search_term.lower() in line.lower():
            start = max(i - context, 0)
            end = min(i + context + 1, len(lines))
            result.extend(lines[start:end])
            result.append('---')  # Separator between different occurrences
    return result

def extract_numbers_from_lines(lines, threshold):
    """Extract numbers greater than the given threshold from the list of lines."""
    filtered_lines = []
    for line in lines:
        if any(int(num) > threshold for num in re.findall(r'\b\d+\b', line)):
            filtered_lines.append(line)
    return filtered_lines

# Process uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_type = uploaded_file.type
        
        try:
            if file_type == 'application/pdf':
                # Convert PDF to images
                images = convert_from_bytes(uploaded_file.read(), dpi=300, fmt='jpeg')

                # Extract text from images using OCR
                text = "".join(pytesseract.image_to_string(img) for img in images)

            elif file_type in ['image/png', 'image/jpeg', 'image/jpg']:
                # Open the image from bytes
                img = Image.open(uploaded_file)

                # Extract text from the image using OCR
                text = pytesserac
