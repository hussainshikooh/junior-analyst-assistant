import streamlit as st
import openai
from dcf_logic import calculate_dcf
from input_parser import parse_excel
from export_builder import build_output_excel

st.title("GPT-Powered DCF Generator")

openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file:
    st.success("File uploaded successfully.")
    inputs = parse_excel(uploaded_file)

    st.subheader("Review and Confirm Extracted Inputs")
    revenue = st.number_input("Revenue", value=float(inputs.get('revenue', 100000000)))
    growth = st.number_input("Growth Rate", value=float(inputs.get('growth', 0.1)))
    margin = st.number_input("EBITDA Margin", value=float(inputs.get('margin', 0.2)))
    wacc = st.number_input("WACC", value=float(inputs.get('wacc', 0.1)))
    terminal = st.number_input("Terminal Growth", value=float(inputs.get('terminal', 0.03)))

    if st.button("Run DCF"):
        value = calculate_dcf(revenue, growth, margin, wacc, terminal)
        st.success(f"Estimated DCF Valuation: ${value:,.2f}")

        prompt = f"Company with ${revenue} in revenue, {growth*100}% growth, {margin*100}% margin, {wacc*100}% WACC, and {terminal*100}% terminal growth. Write a valuation summary."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content
        st.write("GPT Summary:")
        st.write(summary)

        file_name = build_output_excel("Company", value, {
            'Revenue': revenue,
            'Growth Rate': growth,
            'EBITDA Margin': margin,
            'WACC': wacc,
            'Terminal Growth Rate': terminal
        }, summary)

        with open(file_name, "rb") as file:
            st.download_button("Download Excel Model", file, file_name)
