import pandas as pd

def parse_excel(file):
    df = pd.read_excel(file, header=None)

    keywords = {
        'revenue': ['revenue', 'total revenue'],
        'growth': ['growth', 'revenue growth'],
        'margin': ['ebitda margin', 'margin'],
        'wacc': ['wacc', 'weighted average cost'],
        'terminal': ['terminal growth', 'terminal', 'long-term growth']
    }

    results = {}

    for _, row in df.iterrows():
        if pd.isna(row[0]) or pd.isna(row[1]):
            continue

        label = str(row[0]).lower().strip()
        value = row[1]

        for key, words in keywords.items():
            if any(word in label for word in words):
                results[key] = float(value)

    return results
