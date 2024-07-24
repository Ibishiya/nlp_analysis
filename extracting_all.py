import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import csv
from PIL import Image
import re
import io

# Verify and display logo
logo_path = "/workspaces/nlp_analysis/logo-Vision2.png"  # Using raw string

# Set up Streamlit app
st.title("PDF and Image Text Extractor")
st.write("Upload your PDF or image files to extract text.")

try:
    st.image(logo_path, width=500)  # Adjust width as needed
except Exception as e:
    st.error(f"Error loading logo image: {str(e)}")

# File uploader
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
                text = pytesseract.image_to_string(img)

            else:
                st.warning(f"Skipping file: {uploaded_file.name} (not a PDF or supported image)")
                continue

            # Append text to output lists
            for line in text.splitlines():
                csv_output.append([line])

            txt_output.append(text)

            # Extract numbers above the user-defined threshold
            numbers_above_threshold.extend(extract_numbers_above_threshold(text, threshold))

            # Find lines with context if search term is provided
            if search_term:
                filtered_lines_with_context.extend(find_lines_with_context(text, search_term))

                # Filter lines with context based on threshold
                filtered_lines_above_threshold.extend(extract_numbers_from_lines(filtered_lines_with_context, threshold))

            st.success(f"Text from {uploaded_file.name} processed successfully.")

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")

    # Save results as TXT
    if st.button('Download TXT Results'):
        txt_data = "\n".join(txt_output)
        st.download_button(
            label="Download results as TXT",
            data=txt_data,
            file_name='results.txt',
            mime='text/plain'
        )

    # Save results as CSV
    if st.button('Download CSV Results'):
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerows(csv_output)
        st.download_button(
            label="Download results as CSV",
            data=csv_data.getvalue(),
            file_name='results.csv',
            mime='text/csv'
        )

    # Save numbers above threshold as CSV
    if st.button('Download Numbers Above Threshold'):
        numbers_csv_data = io.StringIO()
        writer = csv.writer(numbers_csv_data)
        writer.writerow(['Number'])  # Add header
        for num in numbers_above_threshold:
            writer.writerow([num])
        st.download_button(
            label="Download numbers above threshold as CSV",
            data=numbers_csv_data.getvalue(),
            file_name='numbers_above_threshold.csv',
            mime='text/csv'
        )

    # Save filtered lines with context as TXT
    if st.button('Download Filtered Lines With Context'):
        filtered_lines_data = "\n".join(filtered_lines_with_context)
        st.download_button(
            label="Download filtered lines with context as TXT",
            data=filtered_lines_data,
            file_name='filtered_lines_with_context.txt',
            mime='text/plain'
        )

    # Save filtered lines above threshold as TXT
    if st.button('Download Filtered Lines Above Threshold'):
        filtered_lines_above_threshold_data = "\n".join(filtered_lines_above_threshold)
        st.download_button(
            label="Download filtered lines above threshold as TXT",
            data=filtered_lines_above_threshold_data,
            file_name='filtered_lines_above_threshold.txt',
            mime='text/plain'
        )
