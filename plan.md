Plan: Custom 3-Month Portfolio Monte Carlo Dashboard (HK$9,999 Cap)

Problem statement
- Build a single-file interactive app (app.py) that estimates 3-month portfolio return and risk for a user-constructed multi-fund portfolio using Bayesian-informed priors and Monte Carlo simulation.
- Data for listed funds comes only from Yahoo Finance via the yfinance library. Bank-specific/manual funds are modelled as Manual and rely on user priors.

Overall approach
- Implement the app as a Streamlit single-page app (default recommendation). Alternatively can implement in Plotly Dash if requested.
- UI: dynamic fund list with add/remove, inputs for name, ticker, data source (Yahoo/Manual), allocation %, prior mean & sd (3-month), and per-fund controls.
- Data: for Yahoo funds, fetch adjusted close history via yfinance (max available, e.g. 5y). Compute overlapping 3-month returns (approximated by 63 trading days) and derive mean_hist and sd_hist. For Manual funds, derive mean_hist = prior_mean - 0.2% and sd_hist = prior_sd (documented in code).
- Bayesian blending: implement precision-weighted normal-normal combine when "Blend priors with historical data" is checked. Display formula in the help section.
- Monte Carlo: sample per-fund 3-month returns from Normal(mean, sd) using prior or posterior params. Compute portfolio return using user allocations (normalise if sum != 100% and display a warning). Compute end values and decision metrics (P(V_end > 9999), mean, median, 5th percentile, P(loss)). Provide histogram/density plots for end value and return, mark lines and shaded regions.
- Sensitivity: show P(V_end > 9999) for nearby total amounts (±200, ±100) and allow a simple allocation sensitivity for one fund (±5% reallocations).
- Performance: use NumPy vectorised sampling. Support 1k/5k/10k sims and ensure app remains responsive.

Key files/components to produce/modify
- app.py (single file, top-level comments with requirements and run instructions)
- plan.md (this file) — saved to session workspace

Important UI text (must appear in the app)
- "Fund data for listed ETFs/mutual funds is fetched from Yahoo Finance via yfinance." 
- "Bank-specific funds (e.g. HSBC internal fund codes) are not available via free public APIs and must be modelled as 'Manual'."
- Display the Bayesian formula in plain text.

Assumptions and notes
- 3-month return is computed as return over ~63 trading days; overlapping windows are used when historical data length permits.
- For Manual funds no external calls are made; a conservative shrinkage mean_hist = prior_mean - 0.2% is used (documented in code/help).
- Allocation percentages will be normalised to sum to 100% if they do not; the UI will warn the user and state normalization behaviour.

Todos (high-level)
- create-app-skeleton: Create Streamlit app skeleton, layout, metadata, top help text and default example funds.
- implement-fund-ui: Implement dynamic fund list UI (add/remove rows, inputs for all required fields).
- implement-data-fetch: Add yfinance fetch, compute overlapping 3-month historical returns, mean_hist and sd_hist.
- implement-priors-and-bayesian: Implement prior handling, the precision-weighted posterior calculation, and documentation of formula.
- implement-montecarlo: Implement vectorised Monte Carlo with selectable N (1k/5k/10k), sampling, portfolio aggregation, and metrics computation.
- implement-visuals: Create end-value and return distributions using Plotly, with required annotations and shading.
- implement-sensitivity: Add nearby-amount sensitivity and simple allocation perturbation for a marked fund.
- testing-and-performance: Test with up to 10k sims, several funds; ensure runtime is acceptable and add small progress indicator.
- docs-and-deliverables: Top-of-file comments with requirements and run instructions, and final user-facing help text.

Deliverable
- Single file app.py runnable via: streamlit run app.py
- Top comments listing required packages: streamlit, numpy, plotly, yfinance and pip install instructions.

Next steps
- Implement app.py according to todos above.

Open Anaconda Prompt (search for it in the Start menu) or activate your base environment in PowerShell:
conda activate base

Install Streamlit (if not already installed in this environment):
conda install -c conda-forge streamlit

Note: Using conda-forge is recommended for the most up-to-date packages.
Navigate to your script's folder:
cd c:\Users\edmon\.copilot\session-state\3df1ca44-ac31-4f69-8bed-aeb7ca3c6370

Run the app:
streamlit run app.py