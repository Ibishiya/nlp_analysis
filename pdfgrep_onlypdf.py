import streamlit as st
import subprocess
import os
import pandas as pd
import sweetviz as sv

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

results = []  # Initialize results outside the conditional block

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
            
            # Append results to the list
            results.append({
                'file_path': file_path,
                'search_term': search_term,
                'output': output
            })

    if st.button('Save Results'):
        st.text("Generating results files...")
        # Save as text file
        all_results_txt = "\n".join([f"Results for {result['file_path']}:\n{result['output']}'" for result in results])
        txt_file_path = '/tmp/results.txt'
        with open(txt_file_path, 'w') as f:
            f.write(all_results_txt)
        
        # Save as csv file
        df = pd.DataFrame(results)
        csv_file_path = '/tmp/results.csv'
        df.to_csv(csv_file_path, index=False)

        # Provide download buttons
        st.download_button(
            label="Download results as TXT",
            data=open(txt_file_path, 'r').read(),
            file_name='results.txt'
        )
        
        st.download_button(
            label="Download results as csv",
            data=open(csv_file_path_file_path, 'rb').read(),
            file_name='results.csv'
        )

    if results and st.button('Generate EDA Report'):
        st.text("Generating EDA report...")
        df = pd.DataFrame(results)
        eda_report = sv.analyze(df)
        eda_report_file = '/tmp/eda_report.html'
        eda_report.show_html(eda_report_file, open_browser=False)

        st.download_button(
            label="Download EDA Report",
            data=open(eda_report_file, 'r').read(),
            file_name='eda_report.html'
        )
