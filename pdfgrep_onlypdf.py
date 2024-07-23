import streamlit as st
import subprocess
import os

# Function to run pdfgrep commands
def run_pdfgrep(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

# Streamlit UI
st.title('PDFgrep in Streamlit')

uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True)

if uploaded_files:
    # Save uploaded files to /content directory
    file_paths = []
    for file in uploaded_files:
        file_path = os.path.join('/content', file.name)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        file_paths.append(file_path)

    search_term = st.text_input("Search term")

    if search_term:
        # Search in all uploaded files
        for file_path in file_paths:
            st.write(f"Searching for '{search_term}' in {file_path}")
            
            # Example command to search for term in a single file
            command = f"pdfgrep -H '{search_term}' '{file_path}'"
            output = run_pdfgrep(command)
            
            st.text_area(f"Results for {file_path}", output)

    if st.button('Save Results'):
        # Example command to search for term in all uploaded files and save results
        all_results = ""
        for file_path in file_paths:
            command = f"pdfgrep '{search_term}' '{file_path}'"
            output = run_pdfgrep(command)
            all_results += f"\nResults for {file_path}:\n{output}"
        
        with open('results.txt', 'w') as f:
            f.write(all_results)
        
        st.download_button(
            label="Download results",
            data=open('results.txt', 'r').read(),
            file_name='results.txt'
        )
