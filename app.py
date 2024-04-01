import pandas as pd
import streamlit as st
import io

# Set the page title and icon
st.set_page_config(
    page_title="Excel Chunking Tool",
    page_icon="📚", # You can replace "📚" with any emoji you prefer
    layout="centered",
    initial_sidebar_state="auto",
)

def main():
    st.title("Excel Chunking Tool 📚")

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])

    if uploaded_file:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)

        # Get chunk size from user input
        chunk_size = st.number_input("Enter chunk size:", min_value=1, value=40000)

        # Calculate the number of chunks
        num_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size != 0 else 0)

        # Split the DataFrame into chunks and offer download options for each chunk
        for i in range(num_chunks):
            start_index = i * chunk_size
            end_index = start_index + chunk_size if i < num_chunks - 1 else len(df)
            chunk = df.iloc[start_index:end_index]
            
            # Convert the chunk DataFrame to Excel format in memory
            excel_data = io.BytesIO()
            chunk.to_excel(excel_data, index=False)
            excel_data.seek(0)
            
            # Create a download button for the chunk
            st.download_button(
                label=f"Download chunk_{i + 1}.xlsx",
                data=excel_data,
                file_name=f"chunk_{i + 1}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

if __name__ == "__main__":
    main()
