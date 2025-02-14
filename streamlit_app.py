import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os
import traceback

# Verify and display logo
logo_path = "./logo-Vision2.png"  # Using raw string
try:
    st.image(logo_path, width=700)  # Adjust width as needed
except Exception as e:
    st.error(f"Error loading logo image: {str(e)}")
    
# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        return f"Failed to extract text from PDF: {str(e)}"

# Function to extract text from image
def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Failed to extract text from image: {str(e)}"

# Streamlit UI
st.title('PDF and Image Text Extraction in Streamlit')

uploaded_files = st.file_uploader("Choose PDF or Image files", accept_multiple_files=True, type=['pdf', 'jpg', 'jpeg', 'png'])

if uploaded_files:
    try:
        save_path = '/tmp/uploaded_files'
        os.makedirs(save_path, exist_ok=True)
    except Exception as e:
        st.error(f"Failed to create save directory: {str(e)}")

    file_paths = []
    for file in uploaded_files:
        try:
            file_path = os.path.join(save_path, file.name)
            with open(file_path, 'wb') as f:
                f.write(file.read())
            file_paths.append(file_path)
        except Exception as e:
            st.error(f"Failed to save file {file.name}: {str(e)}")

    search_term = st.text_input("Search term")

    if search_term:
        st.text("Processing files...")
        for file_path in file_paths:
            try:
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.pdf']:
                    st.write(f"Searching for '{search_term}' in PDF: {file_path}")
                    text = extract_text_from_pdf(file_path)
                elif ext in ['.jpg', '.jpeg', '.png']:
                    st.write(f"Searching for '{search_term}' in Image: {file_path}")
                    text = extract_text_from_image(file_path)
                else:
                    st.write(f"Unsupported file type: {file_path}")
                    text = ""
                
                # Search in the extracted text
                search_results = [line for line in text.split('\n') if search_term.lower() in line.lower()]
                result_text = "\n".join(search_results) if search_results else "No matches found."
                st.text_area(f"Results for {file_path}", result_text)
            except Exception as e:
                st.error(f"Failed to process file {file_path}: {str(e)}")

    if st.button('Save Results'):
        try:
            st.text("Generating results file...")
            all_results = ""
            for file_path in file_paths:
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.pdf']:
                    text = extract_text_from_pdf(file_path)
                elif ext in ['.jpg', '.jpeg', '.png']:
                    text = extract_text_from_image(file_path)
                else:
                    text = ""
                
                search_results = [line for line in text.split('\n') if search_term.lower() in line.lower()]
                result_text = "\n".join(search_results) if search_results else "No matches found."
                
                all_results += f"\nResults for {file_path}:\n{result_text}"
            
            with open('results.txt', 'w') as f:
                f.write(all_results)
            
            st.download_button(
                label="Download results",
                data=open('results.txt', 'r').read(),
                file_name='results.txt'
            )
        except Exception as e:
            st.error(f"Failed to save results: {str(e)}")
