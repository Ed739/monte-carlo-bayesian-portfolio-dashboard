"""
Custom Portfolio Monte Carlo Dashboard

Required packages:
  streamlit, numpy, pandas, plotly

Install:
  pip install streamlit numpy pandas plotly

Run:
  streamlit run app.py

Notes:
- Historical return inputs are entered manually for each fund.
- This single-file Streamlit app allows a user to add any number of funds, set priors, enter historical return statistics, blend with historical data using a precision-weighted normal-normal Bayesian update, run Monte Carlo simulations (1k/5k/10k), and visualise the distribution of end values and portfolio returns.
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math import sqrt

st.set_page_config(page_title="Custom Portfolio Monte Carlo Dashboard", layout="wide")

# --- Helper functions ---

def precision_weighted_update(prior_mean, prior_sd, hist_mean, hist_sd):
    # enforce minimum sd to avoid divide-by-zero
    eps = 1e-6
    prior_sd = max(prior_sd, eps)
    hist_sd = max(hist_sd, eps)
    prior_var = prior_sd ** 2
    hist_var = hist_sd ** 2
    post_var = 1.0 / (1.0 / prior_var + 1.0 / hist_var)
    post_mean = (prior_mean / prior_var + hist_mean / hist_var) * post_var
    post_sd = sqrt(post_var)
    return post_mean, post_sd


# --- Session state: funds management ---
if 'funds' not in st.session_state:
    # default example funds
    st.session_state.funds = [
        {
            'name': 'Money Market Proxy',
            'ticker': 'MM',
            'source': 'Manual historical data',
            'alloc': 30.0,
            'prior_mean': 0.2,
            'prior_sd': 0.2,
            'hist_mean': 0.25,
            'hist_sd': 0.35
        },
        {
            'name': 'Global Bond Fund',
            'ticker': 'GB',
            'source': 'Manual historical data',
            'alloc': 40.0,
            'prior_mean': 0.5,
            'prior_sd': 2.0,
            'hist_mean': 0.8,
            'hist_sd': 2.5
        },
        {
            'name': 'Equity Growth Fund',
            'ticker': 'EQ',
            'source': 'Manual historical data',
            'alloc': 30.0,
            'prior_mean': 3.0,
            'prior_sd': 8.0,
            'hist_mean': 4.5,
            'hist_sd': 9.0
        }
    ]


# Utilities for adding/removing funds

def add_fund():
    st.session_state.funds.append({
        'name': 'New Fund',
        'ticker': '',
        'source': 'Manual historical data',
        'alloc': 0.0,
        'prior_mean': 0.0,
        'prior_sd': 1.0,
        'hist_mean': 0.0,
        'hist_sd': 1.0
    })


def remove_fund(idx: int):
    if 0 <= idx < len(st.session_state.funds):
        st.session_state.funds.pop(idx)


# --- App layout ---
st.title("Custom Portfolio Monte Carlo Dashboard")

st.markdown(
    "This dashboard estimates the expected return and risk of a custom multi-fund portfolio over a user-defined horizon using Bayesian-informed priors and Monte Carlo simulation. Results are estimates, not guarantees."
)
st.info("Historical return statistics are entered manually for each fund, so you can model any investment without depending on external market data providers.")

with st.expander("How Bayesian blending works (click to expand)"):
    st.markdown("""
    If "Blend priors with historical data" is enabled, a precision-weighted normal-normal update is used:

    posterior_mean = (prior_mean / prior_var + hist_mean / hist_var) / (1/prior_var + 1/hist_var)

    posterior_var = 1 / (1/prior_var + 1/hist_var)

    where prior_var = prior_sd^2 and hist_var = hist_sd^2.

    If blending is disabled, the user priors are used directly.
    """)

# Controls column
controls_col, output_col = st.columns([1, 2])

with controls_col:
    st.header("Portfolio inputs")
    total_amount = st.number_input("Total investment amount (HKD)", min_value=0.0, value=9900.0, step=100.0, format="%.2f")
    horizon_months = st.number_input("Time horizon (months)", min_value=0.1, value=3.0, step=0.5, format="%.1f")
    sim_count = st.selectbox("Number of Monte Carlo simulations", options=[1000, 5000, 10000], index=0)
    blend = st.checkbox("Blend priors with historical data (Bayesian update)", value=True)
    target_lower = st.number_input("Target range lower bound (HKD)", min_value=0.0, value=9500.0, step=100.0, format="%.2f")
    target_upper = st.number_input("Target range upper bound (HKD)", min_value=0.0, value=11000.0, step=100.0, format="%.2f")
    if target_lower > target_upper:
        st.error("Target range lower bound must be less than or equal to the upper bound.")
        st.stop()

    st.markdown("---")
    st.subheader("Funds in portfolio")
    st.button("Add fund", on_click=add_fund)

    # Editable fund rows
    for idx, fund in enumerate(st.session_state.funds):
        st.markdown(f"**Fund {idx+1}**")
        c1, c2 = st.columns([2, 1])
        name = c1.text_input("Fund name", value=fund['name'], key=f"name_{idx}")
        ticker = c2.text_input("Label / identifier", value=fund.get('ticker',''), key=f"ticker_{idx}")
        alloc = st.number_input("Allocation %", min_value=0.0, max_value=100.0, value=float(fund.get('alloc',0.0)), key=f"alloc_{idx}")
        pm, psd = st.columns(2)
        prior_mean = pm.number_input("Prior mean (3-month %)", value=float(fund.get('prior_mean',0.0)), key=f"prior_mean_{idx}")
        prior_sd = psd.number_input("Prior sd (3-month %)", min_value=0.0001, value=float(fund.get('prior_sd',1.0)), key=f"prior_sd_{idx}")

        hist_m, hist_s = st.columns(2)
        hist_mean = hist_m.number_input("Enter historical mean (3-month %)", value=float(fund.get('hist_mean', prior_mean)), key=f"hist_mean_{idx}")
        hist_sd = hist_s.number_input("Enter historical sd (3-month %)", min_value=0.0001, value=float(fund.get('hist_sd', prior_sd)), key=f"hist_sd_{idx}")

        remove = st.button("Remove", key=f"remove_{idx}")
        if remove:
            remove_fund(idx)
            st.experimental_rerun()

        # write back to session_state
        st.session_state.funds[idx]['name'] = name
        st.session_state.funds[idx]['ticker'] = ticker
        st.session_state.funds[idx]['source'] = 'Manual historical data'
        st.session_state.funds[idx]['alloc'] = alloc
        st.session_state.funds[idx]['prior_mean'] = prior_mean
        st.session_state.funds[idx]['prior_sd'] = prior_sd
        st.session_state.funds[idx]['hist_mean'] = hist_mean
        st.session_state.funds[idx]['hist_sd'] = hist_sd

    st.markdown("---")
    st.caption("Warning: If allocations do not sum to 100%, weights will be normalised proportionally so they sum to 100% for the simulation.")
    st.caption("The chosen horizon scales the per-fund return assumptions from the displayed 3-month priors to the requested time period.")

    st.subheader("Sensitivity options")
    riskiest_idx = None
    if len(st.session_state.funds) > 0:
        riskiest_name = st.selectbox("Select a fund to test ±5% allocation sensitivity", options=[f"{i+1}: {f['name']}" for i,f in enumerate(st.session_state.funds)])
        riskiest_idx = int(riskiest_name.split(":")[0]) - 1


# --- Prepare data and run simulation ---
with output_col:
    st.header("Simulation & results")

    funds = st.session_state.funds
    n = len(funds)

    if n == 0:
        st.warning("No funds in the portfolio. Add funds to simulate.")
        st.stop()

    # gather arrays
    names = [f['name'] for f in funds]
    sources = [f['source'] for f in funds]
    tickers = [f['ticker'] for f in funds]
    allocs = np.array([float(f.get('alloc',0.0)) for f in funds], dtype=float)
    prior_means = np.array([float(f.get('prior_mean',0.0))/100.0 for f in funds], dtype=float)  # convert % to decimal
    prior_sds = np.array([float(f.get('prior_sd',1.0))/100.0 for f in funds], dtype=float)
    horizon_days = max(1, int(round(float(horizon_months) * 21.0)))
    horizon_scale = float(horizon_months) / 3.0
    horizon_scale_sd = sqrt(horizon_scale)

    # Normalize allocations to sum to 1
    alloc_sum = allocs.sum()
    if alloc_sum <= 0:
        st.error("Allocations must sum to > 0. Please set positive allocations.")
        st.stop()
    norm_weights = allocs / alloc_sum
    if abs(alloc_sum - 100.0) > 1e-9:
        st.warning(f"Allocations sum to {alloc_sum:.2f}%. They will be normalised to sum to 100% for the simulation.")

    # Historical stats are manually provided by the user for each fund.
    hist_means = np.zeros(n)
    hist_sds = np.zeros(n)
    hist_rows = []
    for i in range(n):
        hist_mean = float(funds[i].get('hist_mean', prior_means[i])) / 100.0
        hist_sd = float(funds[i].get('hist_sd', prior_sds[i])) / 100.0
        hist_means[i] = hist_mean
        hist_sds[i] = hist_sd
        hist_rows.append({'fund': names[i], 'label': tickers[i], 'hist_mean_pct': hist_mean*100, 'hist_sd_pct': hist_sd*100, 'n_obs': 'manual'})

    hist_df = pd.DataFrame(hist_rows)

    # Compute posterior or use priors, then scale from the 3-month inputs to the requested horizon
    if blend:
        post_means = np.zeros(n)
        post_sds = np.zeros(n)
        for i in range(n):
            pm, psd = precision_weighted_update(prior_means[i], prior_sds[i], hist_means[i], hist_sds[i])
            post_means[i] = pm
            post_sds[i] = psd
        base_means = post_means
        base_sds = post_sds
    else:
        base_means = prior_means
        base_sds = prior_sds

    use_means = base_means * horizon_scale
    use_sds = base_sds * horizon_scale_sd

    # Display table of fund priors / historical / posteriors
    df_display = pd.DataFrame({
        'Fund': names,
        'Label': tickers,
        'Source': ['Manual historical data'] * n,
        'Alloc % (input)': allocs,
        'Prior mean (3m, %)': (prior_means*100).round(3),
        'Prior sd (3m, %)': (prior_sds*100).round(3),
        'Hist mean (3m, %)': (hist_means*100).round(3),
        'Hist sd (3m, %)': (hist_sds*100).round(3),
        'Use mean (3m, %)': (use_means*100).round(3),
        'Use sd (3m, %)': (use_sds*100).round(3)
    })

    st.subheader("Per-fund priors, historical stats, and values used for simulation")
    st.caption(f"Simulation horizon: {horizon_months:.1f} months (~{horizon_days} trading days)")
    st.dataframe(df_display)

    # Run Monte Carlo simulation
    st.subheader("Monte Carlo simulation")
    run_sim = st.button("Run simulation")

    if run_sim:
        with st.spinner("Running Monte Carlo..."):
            # sample returns for each fund: shape (sim_count, n)
            rng = np.random.default_rng()
            sims = rng.normal(loc=use_means, scale=use_sds, size=(sim_count, n))  # decimals
            # compute portfolio return per sim
            port_returns = sims.dot(norm_weights)  # shape (sim_count,)
            end_values = total_amount * (1.0 + port_returns)

            # Metrics
            prob_in_range = float(((end_values >= target_lower) & (end_values <= target_upper)).mean())
            prob_below_range = float((end_values < target_lower).mean())
            prob_above_range = float((end_values > target_upper).mean())
            mean_end = float(end_values.mean())
            median_end = float(np.median(end_values))
            p5_end = float(np.percentile(end_values, 5))
            p95_end = float(np.percentile(end_values, 95))
            prob_loss = float((end_values < total_amount).mean())

            # Display key metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric(label=f"P({target_lower:,.0f} <= V_end <= {target_upper:,.0f})", value=f"{prob_in_range*100:.2f}%")
            col2.metric(label="Mean end value (HKD)", value=f"{mean_end:,.2f}")
            col3.metric(label="Median end value (HKD)", value=f"{median_end:,.2f}")
            col4.metric(label="5th percentile end value (HKD)", value=f"{p5_end:,.2f}")
            col5.metric(label="P(loss) (V_end < initial)", value=f"{prob_loss*100:.2f}%")

            # End value distribution plot
            fig_ev = px.histogram(end_values, nbins=100, marginal='box', histnorm=None, labels={'value':'End value (HKD)'}, title='Distribution of portfolio end values (HKD)')
            fig_ev.update_traces(marker_color='lightblue')
            # add vertical lines
            fig_ev.add_vline(x=total_amount, line_dash='dash', line_color='black', annotation_text='Initial amount', annotation_position='top left')
            fig_ev.add_vline(x=target_lower, line_dash='dash', line_color='orange', annotation_text='Range lower', annotation_position='top left')
            fig_ev.add_vline(x=target_upper, line_dash='dash', line_color='green', annotation_text='Range upper', annotation_position='top right')
            fig_ev.add_shape(type="rect", x0=target_lower, x1=target_upper, y0=0, y1=1, xref='x', yref='paper', fillcolor='rgba(0,128,0,0.08)', line_width=0)

            st.plotly_chart(fig_ev, use_container_width=True)

            # Portfolio return distribution plot (in %)
            fig_r = px.histogram(port_returns*100.0, nbins=100, marginal='box', labels={'value':'Portfolio return (%)'}, title='Portfolio return distribution (%)')
            fig_r.update_traces(marker_color='lightgreen')
            fig_r.add_vline(x=port_returns.mean()*100.0, line_dash='dash', line_color='black', annotation_text='Mean', annotation_position='top left')
            fig_r.add_vline(x=np.median(port_returns)*100.0, line_dash='dash', line_color='blue', annotation_text='Median', annotation_position='top right')
            st.plotly_chart(fig_r, use_container_width=True)

            # Range sensitivity around the user-selected bounds
            range_df = pd.DataFrame({
                'Scenario': ['Lower -200', 'Lower -100', 'Selected lower', 'Selected upper', 'Upper +100', 'Upper +200'],
                'Lower bound (HKD)': [target_lower - 200.0, target_lower - 100.0, target_lower, target_lower, target_lower, target_lower],
                'Upper bound (HKD)': [target_upper, target_upper, target_upper, target_upper, target_upper + 100.0, target_upper + 200.0],
            })
            range_df['P(in range)'] = [float(((end_values >= row['Lower bound (HKD)']) & (end_values <= row['Upper bound (HKD)'])).mean()) for _, row in range_df.iterrows()]
            st.subheader('Probability in nearby ranges')
            st.table(range_df[['Scenario', 'Lower bound (HKD)', 'Upper bound (HKD)', 'P(in range)']].style.format({'Lower bound (HKD)': '{:,.2f}', 'Upper bound (HKD)': '{:,.2f}', 'P(in range)': '{:.3f}'}))

            st.caption(f"For the selected range: below = {prob_below_range*100:.2f}%, in range = {prob_in_range*100:.2f}%, above = {prob_above_range*100:.2f}%.")

            # Allocation sensitivity for selected riskiest fund (+/-5%)
            if riskiest_idx is not None and 0 <= riskiest_idx < n:
                delta = 0.05  # 5 percentage points absolute (i.e. 5% of portfolio)
                current_alloc = norm_weights.copy()
                # increase
                inc_alloc = current_alloc.copy()
                inc_alloc[riskiest_idx] = inc_alloc[riskiest_idx] + delta
                # renormalise (if sum >1, scale others proportionally)
                if inc_alloc.sum() <= 0:
                    inc_alloc = current_alloc
                else:
                    inc_alloc = np.maximum(inc_alloc, 0)
                    inc_alloc = inc_alloc / inc_alloc.sum()
                # decrease
                dec_alloc = current_alloc.copy()
                dec_alloc[riskiest_idx] = max(dec_alloc[riskiest_idx] - delta, 0.0)
                if dec_alloc.sum() <= 0:
                    dec_alloc = current_alloc
                else:
                    dec_alloc = np.maximum(dec_alloc, 0)
                    dec_alloc = dec_alloc / dec_alloc.sum()

                prob_base = float(((end_values >= target_lower) & (end_values <= target_upper)).mean())
                # recompute with inc and dec quickly using same sims
                ev_inc = total_amount * (1.0 + (sims.dot(inc_alloc)))
                ev_dec = total_amount * (1.0 + (sims.dot(dec_alloc)))
                prob_inc = float(((ev_inc >= target_lower) & (ev_inc <= target_upper)).mean())
                prob_dec = float(((ev_dec >= target_lower) & (ev_dec <= target_upper)).mean())

                st.subheader(f"Allocation sensitivity for '{names[riskiest_idx]}' (±5% absolute)")
                st.write(f"Base probability in range: {prob_base*100:.2f}%")
                st.write(f"If this fund +5% (rebalanced), probability in range: {prob_inc*100:.2f}%")
                st.write(f"If this fund -5% (rebalanced), probability in range: {prob_dec*100:.2f}%")

            # Download CSV of simulation summary
            sim_summary = pd.DataFrame({
                'portfolio_return': port_returns,
                'end_value': end_values,
                'in_selected_range': (end_values >= target_lower) & (end_values <= target_upper)
            })
            csv = sim_summary.to_csv(index=False).encode('utf-8')
            st.download_button(label='Download raw simulation results (csv)', data=csv, file_name='simulation_results.csv', mime='text/csv')

    else:
        st.info('Adjust inputs and click "Run simulation" to compute results.')

# Footer / Help
st.markdown('---')
st.markdown('Hints: Use realistic prior and historical sd values for your chosen horizon. Historical statistics are input directly by the user and are blended with your priors using the Bayesian update above.')

# End
