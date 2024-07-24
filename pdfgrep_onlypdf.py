# Save results as TXT
if st.button('Download TXT Results'):
    txt_file_path = '/tmp/results.txt'
    with open(txt_file_path, 'w') as f:
        f.write("\n".join(txt_output))
    with open(txt_file_path, 'r') as f:
        st.download_button(
            label="Download results as TXT",
            data=f.read(),
            file_name='results.txt'
        )

# Save results as CSV
if st.button('Download CSV Results'):
    csv_file_path = '/tmp/results.csv'
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_output)
    with open(csv_file_path, 'r') as f:
        st.download_button(
            label="Download results as CSV",
            data=f.read(),
            file_name='results.csv'
        )

# Sweetviz report
if excel_file:
    try:
        df = pd.read_excel(excel_file)
        st.write("Generating Sweetviz report...")
        report = sv.analyze(df)
        eda_report_file = '/tmp/eda_report.html'
        report.show_html(eda_report_file, open_browser=False)
        with open(eda_report_file, 'r') as f:
            st.download_button(
                label="Download EDA Report",
                data=f.read(),
                file_name='eda_report.html'
            )
    except Exception as e:
        st.error(f"Error generating Sweetviz report: {str(e)}")
