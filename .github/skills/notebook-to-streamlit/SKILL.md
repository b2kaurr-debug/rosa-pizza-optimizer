---
name: notebook-to-streamlit
description: Port analysis functions from rosa_analysis.ipynb into app.py while preserving core business logic.
---

# notebook-to-streamlit

When updating the Streamlit application for the Rosa's Pizza project, treat the validated functions in `rosa_analysis.ipynb` as the source of truth for business logic.

## Core Functions

- `cost_per_late_order(costs)` — computes total cost as `refund + churn * margin`.
- `best_promise(zone, time_block, promises, costs)` — evaluates candidate promises to maximize net profit (`orders * margin - late_orders * cost_per_late_order`).

## Implementation Guidelines

1. Reference Parts II.a and II.b of `rosa_analysis.ipynb` to ensure parity.
2. Maintain identical parameter signatures and mathematical formulations.
3. Utilize `delivery_times(zone, time_block, promise, seed=1)` to ensure reproducibility matching the notebook.
4. Bind functions to Streamlit controls:
   - `st.selectbox` for zones and time blocks sourced from `ZONES` and `TIME_BLOCKS`.
   - `st.number_input` for promise ranges and cost parameters (`margin`, `churn`, `refund`), initialized from `COSTS`.
   - `st.button` execution triggers for optimization outputs.
5. Avoid hardcoding domain values; dynamically reference the `starter` package or widget inputs.
