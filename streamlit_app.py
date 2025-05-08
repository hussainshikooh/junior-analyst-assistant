import streamlit as st
import os
from openai import OpenAI
from dcf_logic import calculate_dcf
from input_parser import parse_excel
from export_builder import build_output_excel

st.set_page_config(page_title="GPT DCF Builder", layout="centered")
st.title("📊 GPT-Powered DCF Generator")

# GPT is temporarily disabled to isolate the Axios error
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    st.success("✅ File uploaded.")
    inputs = parse_excel(uploaded_file)

    # ✅ Validate required inputs
    required_keys = ['revenue', 'growth', 'margin', 'wacc', 'terminal']
    missing = [k for k in required_keys if k not in inputs]

    if missing:
        st.error(f"❌ Missing input(s): {', '.join(missing)}. Please check your Excel file.")
        st.stop()

    # Confirm and allow edits
    st.subheader("📥 Confirm Inputs")
    revenue = st.number_input("Revenue", value=float(inputs['revenue']))
    growth = st.number_input("Growth Rate", value=float(inputs['growth']))
    margin = st.number_input("EBITDA Margin", value=float(inputs['margin']))
    wacc = st.number_input("WACC", value=float(inputs['wacc']))
    terminal = st.number_input("Terminal Growth Rate", value=float(inputs['terminal']))

    if st.button("Run DCF Valuation"):
        value = calculate_dcf(revenue, growth, margin, wacc, terminal)
        st.success(f"📈 Estimated DCF Valuation: ${value:,.2f}")

        # 🔁 GPT replaced with fallback summary
        summary = (
            f"This is a placeholder summary. Revenue: ${revenue:,.0f}, "
            f"Growth: {growth*100:.1f}%, Margin: {margin*100:.1f}%, "
            f"WACC: {wacc*100:.1f}%, Terminal Growth: {terminal*100:.1f}%."
        )

        st.subheader("🧠 Valuation Summary")
        st.write(summary)

        file_name = build_output_excel("Company", value, {
            'Revenue': revenue,
            'Growth Rate': growth,
            'EBITDA Margin': margin,
            'WACC': wacc,
            'Terminal Growth Rate': terminal
        }, summary)

        with open(file_name, "rb") as file:
            st.download_button("📥 Download Excel Model", file, file_name)
