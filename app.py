import streamlit as st
from openai import OpenAI
from dcf_logic import calculate_dcf
from input_parser import parse_excel
from export_builder import build_output_excel

st.set_page_config(page_title="GPT DCF Builder", layout="centered")
st.title("📊 GPT-Powered DCF Generator")

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    st.success("✅ File uploaded.")
    inputs = parse_excel(uploaded_file)

    # Validate required inputs
    required_keys = ['revenue', 'growth', 'margin', 'wacc', 'terminal']
    missing = [k for k in required_keys if k not in inputs]

    if missing:
        st.error(f"❌ Missing input(s): {', '.join(missing)}. Please check your Excel file labels.")
        st.stop()

    # Use parsed values with sliders for user confirmation
    st.subheader("📥 Confirm Inputs")
    revenue = st.number_input("Revenue", value=float(inputs['revenue']))
    growth = st.number_input("Growth Rate", value=float(inputs['growth']))
    margin = st.number_input("EBITDA Margin", value=float(inputs['margin']))
    wacc = st.number_input("WACC", value=float(inputs['wacc']))
    terminal = st.number_input("Terminal Growth Rate", value=float(inputs['terminal']))

    # Button to run DCF
    if st.button("Run DCF Valuation"):
        value = calculate_dcf(revenue, growth, margin, wacc, terminal)
        st.success(f"📈 Estimated DCF Valuation: ${value:,.2f}")

        # GPT-safe prompt
        prompt = (
            f"A company with ${revenue:,.0f} in revenue, "
            f"{growth*100:.1f}% revenue growth, "
            f"{margin*100:.1f}% EBITDA margin, "
            f"{wacc*100:.1f}% WACC, and "
            f"{terminal*100:.1f}% terminal growth. "
            f"Write a 3-sentence DCF valuation summary."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.choices[0].message.content
            st.subheader("🧠 GPT Valuation Summary")
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

        except Exception as e:
            st.error("❌ GPT API error. Please check your quota, key, and inputs.")
            st.code(str(e))

