import streamlit as st
import subprocess
import os
import pandas as pd
import sweetviz as sv

# Verify and display logo
logo_path = "/workspaces/nlp_analysis/logo-Vision2.png"  # Using raw string
try:
    st.image(logo_path, width=700)  # Adjust width as needed
except Exception as e:
    st.error(f"Error loading logo image: {str(e)}")
    
# Function to run pdfgrep commands with error handling
def run_pdfgrep(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title('PDFgrep in Streamlit')
results = []  # Initialize results outside the conditional block

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
        results = []
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
        all_results_txt = "\n".join([f"Results for {result['file_path']}:\n{result['output']}" for result in results])
        txt_file_path = '/tmp/results.txt'
        with open(txt_file_path, 'w') as f:
            f.write(all_results_txt)
        
        # Save as CSV file
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
            label="Download results as CSV",
            data=open(csv_file_path, 'r').read(),
            file_name='results.csv'
        )

    if results and st.button('Generate EDA Report'):
        st.text("Generating EDA report...")
        df = pd.DataFrame(results)
        eda_report = sv.analyze(df)
        eda_report_file = '/tmp/eda_report.html'
        eda_report.show_html(eda_report_file, open_browser=False)

        st.download_button(
            label="Download Report",
            data=open(eda_report_file, 'r').read(),
            file_name='eda_report.html'
        )

# Sweetviz analysis section
st.write("Upload an Excel file to perform Sweetviz EDA:")
excel_file = st.file_uploader("Choose an Excel file", type=['xls', 'xlsx'])

if excel_file:
    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(excel_file)
        df['valor inicial'] = pd.to_numeric(df['valor inicial'], errors='coerce')
        df['valor final'] = pd.to_numeric(df['valor final'], errors='coerce')
        df['fecha inicial'] = df['fecha inicial'].astype(str)
        df['fecha final'] = df['fecha inicial'].astype(str)
        # Generate Sweetviz report
        st.write("Generating Sweetviz report...")
        report = sv.analyze(df)
        eda_report_file = '/tmp/eda_report.html'
        report.show_html(eda_report_file, open_browser=False)

        st.success("EDA report generated successfully.")
        
        # Provide download button for Sweetviz report
        st.download_button(
            label="Download EDA Report",
            data=open(eda_report_file, 'r').read(),
            file_name='eda_report.html'
        )

    except Exception as e:
        st.error(f"Error generating Sweetviz report: {str(e)}")