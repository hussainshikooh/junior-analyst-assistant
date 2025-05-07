import pandas as pd

def build_output_excel(company, valuation, inputs, summary):
    df_inputs = pd.DataFrame.from_dict(inputs, orient='index', columns=['Value'])
    df_summary = pd.DataFrame([summary], columns=['GPT Valuation Summary'])

    with pd.ExcelWriter(f"{company}_DCF_Model.xlsx", engine='openpyxl') as writer:
        df_inputs.to_excel(writer, sheet_name='Inputs')
        pd.DataFrame([['Estimated Valuation', valuation]]).to_excel(writer, sheet_name='Valuation')
        df_summary.to_excel(writer, sheet_name='GPT Summary')

    return f"{company}_DCF_Model.xlsx"
