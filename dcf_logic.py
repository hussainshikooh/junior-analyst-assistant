def calculate_dcf(revenue, growth_rate, margin, wacc, terminal_growth, years=5):
    cash_flows = []
    for year in range(1, years + 1):
        future_revenue = revenue * ((1 + growth_rate) ** year)
        ebitda = future_revenue * margin
        discounted = ebitda / ((1 + wacc) ** year)
        cash_flows.append(discounted)

    terminal_value = cash_flows[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    terminal_discounted = terminal_value / ((1 + wacc) ** years)
    total_valuation = sum(cash_flows) + terminal_discounted
    return round(total_valuation, 2)
