import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up Streamlit app with custom styling
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for better styling
st.markdown(
    """
    <style>
        body {
            background-color: #f7f9fc;
        }
        .main {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 16px;
            font-weight: bold;
        }
        .stFileUploader {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #ddd;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with styling
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📊 Data Sweeper</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Effortlessly clean, visualize, and convert your datasets!</p>", unsafe_allow_html=True)

# Sidebar for file upload
st.sidebar.header("📂 Upload Your Files")
uploaded_files = st.sidebar.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

# Process files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file based on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.sidebar.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # File Info
        st.markdown(f"### 📂 File: {file.name}")
        st.write(f"**📏 Size:** {file.size / 1024:.2f} KB")

        # Preview Data
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning
        st.subheader("🛠 Data Cleaning Options")
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"🚀 Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed!")

        with col2:
            if st.button(f"🩺 Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing Values Filled!")

        # Column Selection
        st.subheader("📌 Select Columns to Keep")
        selected_columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Chart for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion
        st.subheader("🔄 Convert File Format")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                new_file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download button with better UI
            st.download_button(
                label=f"📥 Download {new_file_name}",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type
            )

st.sidebar.success("✅ All files processed successfully!")
