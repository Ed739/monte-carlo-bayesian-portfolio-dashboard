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
1. Bayesian blend — Each fund's prior (μ, σ) and historical estimate (μ, σ) are combined via a precision-weighted Normal–Normal update. The lower-variance input dominates. If disabled, the prior is used as-is.

2. Horizon scaling — 3-month inputs are projected to H months: mean scales linearly (× H/3), SD scales by √(H/3).

3. Monte Carlo — N independent Normal draws per fund (uncorrelated across funds).

4. Portfolio return — Weighted sum of fund returns, allocations normalised to 100 %.

5. Outcome — Vend = V0(1 + r). Reports mean, median, 5th percentile, P(in target range), P(loss), and ±5 pp allocation sensitivity.

## Key assumptions: Normal returns, zero inter-fund correlation, square-root-of-time scaling, single-period compounding, static parameters. Suitable for scenario comparison, not precise probability estimates.

## Limitations

- Historical inputs are entered manually.
- Fund correlations are not modeled.
- Returns use a normal distribution.
- Fees, taxes, inflation, and transaction costs are excluded.
- Results are estimates, not investment advice.

## Skills Demonstrated

This project demonstrates financial modeling, Bayesian estimation, Monte Carlo simulation, portfolio risk analysis, Python programming, data visualization, and interactive dashboard development.
```
