import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Upload Test")

st.title("📄 Excel File Upload & Preview")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=None)
        st.success("✅ File uploaded and parsed successfully!")
        st.dataframe(df)
    except Exception as e:
        st.error("❌ Error reading Excel file:")
        st.code(str(e))
