import streamlit as st
from openai import OpenAI
from dcf_logic import calculate_dcf
from input_parser import parse_excel
from export_builder import build_output_excel

st.set_page_config(page_title="GPT DCF Builder", layout="centered")
st.title("📊 GPT-Powered DCF Generator")

# ✅ NEW OpenAI client (v1 syntax)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    st.success("✅ File uploaded.")
    inputs = parse_excel(uploaded_file)

    st.subheader("📥 Confirm Inputs")
    revenue = st.number_input("Revenue", value=float(inputs.get('revenue', 100_000_000)))
    growth = st.number_input("Growth Rate", value=float(inputs.get('growth', 0.1)))
    margin = st.number_input("EBITDA Margin", value=float(inputs.get('margin', 0.2)))
    wacc = st.number_input("WACC", value=float(inputs.get('wacc', 0.1)))
    terminal = st.number_input("Terminal Growth", value=float(inputs.get('terminal', 0.03)))

    if st.button("Run DCF Valuation"):
        value = calculate_dcf(revenue, growth, margin, wacc, terminal)
        st.success(f"DCF Valuation: ${value:,.2f}")

        # ✅ GPT summary with v1 client
        prompt = (
            f"A company with ${revenue} in revenue, {growth*100:.1f}% growth, "
            f"{margin*100:.1f}% EBITDA margin, {wacc*100:.1f}% WACC, and "
            f"{terminal*100:.1f}% terminal growth. Write a short DCF valuation summary."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.choices[0].message.content
            st.markdown("### 🧠 GPT Valuation Summary")
            st.write(summary)

            # Excel output
            file_name = build_output_excel("Company", value, {
                'Revenue': revenue,
                'Growth Rate': growth,
                'EBITDA Margin': margin,
                'WACC': wacc,
                'Terminal Growth': terminal
            }, summary)

            with open(file_name, "rb") as file:
                st.download_button("📥 Download Excel Model", file, file_name)

        except Exception as e:
            st.error(f"GPT error: {e}")
