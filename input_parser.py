import pandas as pd

def parse_excel(file):
    df = pd.read_excel(file, header=None)

    keywords = {
        'revenue': ['revenue', 'total revenue'],
        'growth': ['growth', 'revenue growth'],
        'margin': ['margin', 'ebitda margin'],
        'wacc': ['wacc', 'wacc estimate', 'discount rate'],
        'terminal': ['terminal', 'terminal growth', 'terminal rate']
    }

    results = {}

    for _, row in df.iterrows():
        if pd.isna(row[0]) or pd.isna(row[1]):
            continue

        label = str(row[0]).lower().strip()
        value = row[1]

        for key, options in keywords.items():
            if any(k in label for k in options):
                try:
                    results[key] = float(value)
                except:
                    pass

    return results
