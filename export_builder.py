import pandas as pd

def build_output_excel(company, valuation, inputs, summary):
    # Extract inputs
    revenue = inputs['Revenue']
    growth = inputs['Growth Rate']
    margin = inputs['EBITDA Margin']
    wacc = inputs['WACC']
    terminal = inputs['Terminal Growth Rate']

    # Projections for 5 years
    projections = []
    for year in range(1, 6):
        rev = revenue * ((1 + growth) ** year)
        ebitda = rev * margin
        d_and_a = ebitda * 0.1
        ebit = ebitda - d_and_a
        taxes = ebit * 0.35
        tax_adjusted_ebit = ebit - taxes
        capex = 1000000
        nwc_change = 500000
        unlevered_fcf = tax_adjusted_ebit + d_and_a - capex - nwc_change
        discount_factor = (1 + wacc) ** year
        discounted_fcf = unlevered_fcf / discount_factor

        projections.append({
            'Year': f'Year {2024 + year}',
            'Revenue': round(rev),
            'EBITDA': round(ebitda),
            'D&A': round(d_and_a),
            'EBIT': round(ebit),
            'Taxes': round(taxes),
            'UFCF': round(unlevered_fcf),
            'Discount Factor': round(discount_factor, 4),
            'Discounted UFCF': round(discounted_fcf)
        })

    df_proj = pd.DataFrame(projections)

    # Terminal value
    final_fcf = projections[-1]['UFCF']
    terminal_value = final_fcf * (1 + terminal) / (wacc - terminal)
    discounted_terminal = terminal_value / ((1 + wacc) ** 5)

    # Total value
    total_dcf = df_proj['Discounted UFCF'].sum() + discounted_terminal

    # Summary sheet
    df_inputs = pd.DataFrame.from_dict(inputs, orient='index', columns=['Value'])
    df_summary = pd.DataFrame([summary], columns=['GPT Valuation Summary'])

    # Terminal value and final valuation
    df_valuation = pd.DataFrame({
        'Item': ['Sum of Discounted UFCFs', 'Discounted Terminal Value', 'Total DCF Valuation'],
        'Value': [df_proj['Discounted UFCF'].sum(), discounted_terminal, total_dcf]
    })

    file_path = f"/mnt/data/{company}_DCF_Model.xlsx"
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df_inputs.to_excel(writer, sheet_name='Inputs')
        df_proj.to_excel(writer, sheet_name='DCF Projection', index=False)
        df_valuation.to_excel(writer, sheet_name='Valuation Summary', index=False)
        df_summary.to_excel(writer, sheet_name='GPT Summary', index=False)

    return file_path

