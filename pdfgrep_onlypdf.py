import streamlit as st
import subprocess
import os

# Function to run pdfgrep commands with error handling
def run_pdfgrep(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title('PDFgrep in Streamlit')

uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True)

if uploaded_files:
    # Save uploaded files to a writable directory
    save_path = '/tmp/uploaded_files'
    os.makedirs(save_path, exist_ok=True)
    
    file_paths = []
    for file in uploaded_files:
        file_path = os.path.join(save_path, file.name)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        file_paths.append(file_path)

    search_term = st.text_input("Search term")

    if search_term:
        st.text("Searching files...")
        for file_path in file_paths:
            st.write(f"Searching for '{search_term}' in {file_path}")
            
            # Search in the file
            command = f"pdfgrep -H '{search_term}' '{file_path}'"
            output = run_pdfgrep(command)
            
            st.text_area(f"Results for {file_path}", output)

    if st.button('Save Results'):
        st.text("Generating results file...")
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
