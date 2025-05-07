import pandas as pd

def parse_excel(file):
    df = pd.read_excel(file, header=None)

    keywords = {
        'revenue': ['revenue', 'total revenue'],
        'growth': ['growth', 'revenue growth'],
        'margin': ['ebitda margin', 'margin'],
        'wacc': ['wacc'],
        'terminal': ['terminal growth', 'terminal']
    }

    results = {}

    for row in df.itertuples():
        for key, words in keywords.items():
            if any(word.lower() in str(row[1]).lower() for word in words):
                results[key] = row[2]

    return results
