import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import csv
from PIL import Image
import io
import re

# Set up Streamlit app
st.title("PDF and Image Text Extractor")
st.write("Upload your PDF or image files to extract text.")

# File uploader
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

# Output lists
csv_output = []
txt_output = []
numbers_above_threshold = []
filtered_lines = []

# Number Input for threshold
threshold = st.number_input("Enter threshold value:", min_value=0, value=1000)

# Text Input for search term
search_term = st.text_input("Enter keyword or phrase to search for:")

def extract_numbers_above_threshold(text, threshold):
    """Extract numbers greater than the given threshold from the text."""
    numbers = re.findall(r'\b\d+\b', text)
    return [int(num) for num in numbers if int(num) > threshold]

def find_lines_containing_search_term(text, search_term):
    """Find and return lines containing the search term."""
    return [line for line in text.splitlines() if search_term.lower() in line.lower()]

# Process uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_type = uploaded_file.type
        
        if file_type == 'application/pdf':
            # Handle PDF files
            try:
                # Convert PDF to images
                images = convert_from_bytes(uploaded_file.read(), dpi=300, fmt='jpeg')

                # Extract text from images using OCR
                text = ""
                for img in images:
                    text += pytesseract.image_to_string(img)

                # Append text to output lists
                for line in text.splitlines():
                    csv_output.append([line])

                txt_output.append(text)

                # Extract numbers above the user-defined threshold
                numbers_above_threshold.extend(extract_numbers_above_threshold(text, threshold))

                # Find lines containing the search term
                if search_term:
                    filtered_lines.extend(find_lines_containing_search_term(text, search_term))

                st.success(f"Text from {uploaded_file.name} processed successfully.")

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")

        elif file_type in ['image/png', 'image/jpeg', 'image/jpg']:
            # Handle image files
            try:
                # Open the image from bytes
                img = Image.open(uploaded_file)

                # Extract text from the image using OCR
                text = pytesseract.image_to_string(img)

                # Append text to output lists
                for line in text.splitlines():
                    csv_output.append([line])

                txt_output.append(text)

                # Extract numbers above the user-defined threshold
                numbers_above_threshold.extend(extract_numbers_above_threshold(text, threshold))

                # Find lines containing the search term
                if search_term:
                    filtered_lines.extend(find_lines_containing_search_term(text, search_term))

                st.success(f"Text from {uploaded_file.name} processed successfully.")

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")

        else:
            st.warning(f"Skipping file: {uploaded_file.name} (not a PDF or supported image)")

    # Save results as TXT
    if st.button('Download TXT Results'):
        txt_file_path = '/tmp/results.txt'
        with open(txt_file_path, 'w') as f:
            f.write("\n".join(txt_output))
        st.download_button(
            label="Download results as TXT",
            data=open(txt_file_path, 'r').read(),
            file_name='results.txt'
        )

    # Save results as CSV
    if st.button('Download CSV Results'):
        csv_file_path = '/tmp/results.csv'
        with open(csv_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_output)
        st.download_button(
            label="Download results as CSV",
            data=open(csv_file_path, 'r').read(),
            file_name='results.csv'
        )

    # Save numbers above threshold as CSV
    if st.button('Download Numbers Above Threshold'):
        numbers_csv_file_path = '/tmp/numbers_above_threshold.csv'
        with open(numbers_csv_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Number'])  # Add header
            for num in numbers_above_threshold:
                writer.writerow([num])
        st.download_button(
            label="Download numbers above threshold as CSV",
            data=open(numbers_csv_file_path, 'r').read(),
            file_name='numbers_above_threshold.csv'
        )

    # Save filtered lines containing the search term as TXT
    if st.button('Download Filtered Lines'):
        filtered_lines_file_path = '/tmp/filtered_lines.txt'
        with open(filtered_lines_file_path, 'w') as f:
            f.write("\n".join(filtered_lines))
        st.download_button(
            label="Download filtered lines as TXT",
            data=open(filtered_lines_file_path, 'r').read(),
            file_name='filtered_lines.txt'
        )
