```markdown
# Portfolio Monte Carlo Dashboard

A Streamlit dashboard for analyzing portfolio outcomes using Bayesian return assumptions and Monte Carlo simulation.

## Features

- Add and remove investment funds
- Define portfolio allocations
- Enter prior and historical return assumptions
- Combine assumptions using Bayesian weighting
- Simulate 1,000 to 10,000 possible outcomes
- Estimate:
  - Mean and median ending value
  - 5th-percentile value
  - Probability of loss
  - Probability of reaching a target range
- Analyze allocation sensitivity
- Export simulation results to CSV

## Technology

- Python
- Streamlit
- NumPy
- Pandas
- Plotly

## Run Locally

```bash
pip install streamlit numpy pandas plotly
streamlit run `app.py`
```

## Methodology

The dashboard:

1. Combines prior and historical return assumptions.
2. Adjusts returns and risk for the selected investment horizon.
3. Generates simulated fund returns.
4. Combines fund returns using portfolio weights.
5. Calculates the distribution of possible ending values.

## Limitations

- Historical inputs are entered manually.
- Fund correlations are not modeled.
- Returns use a normal distribution.
- Fees, taxes, inflation, and transaction costs are excluded.
- Results are estimates, not investment advice.

## Skills Demonstrated

This project demonstrates financial modeling, Bayesian estimation, Monte Carlo simulation, portfolio risk analysis, Python programming, data visualization, and interactive dashboard development.
```
