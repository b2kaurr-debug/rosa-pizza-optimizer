---
name: notebook-to-streamlit
description: Port the analysis functions from the Rosa's Pizza notebook (rosa_analysis.ipynb) into the Streamlit app (app.py), keeping the business logic identical.
---

# notebook-to-streamlit

When asked to build or update the Streamlit app for the Rosa's Pizza project,
treat the functions already written and tested in `rosa_analysis.ipynb` as the
source of truth for business logic — do not re-derive the formulas from
scratch.

## Functions to port

- `cost_per_late_order(costs)` — refund + churn * margin
- `best_promise(zone, time_block, promises, costs)` — searches a list of
  candidate promises and returns the one with the highest net profit, where
  `net profit = orders * margin - late_orders * cost_per_late_order`

## Steps

1. Read the corresponding cells in `rosa_analysis.ipynb` (Part II.a and II.b).
2. Reproduce the functions in `app.py` with the same parameter names and the
   same formulas — do not change the math.
3. Call `delivery_times(zone, time_block, promise, seed=1)` (same fixed seed as
   the notebook) so app results are reproducible and match the notebook.
4. Wire the ported functions to Streamlit widgets:
   - `st.selectbox` for zone and time block (from `ZONES` / `TIME_BLOCKS`)
   - `st.number_input` for the promise range (min, max, step) and for the cost
     assumptions (margin, churn, refund), defaulted from `COSTS`
   - `st.button` to trigger the search and display the recommended promise
5. Do not hardcode zone/time-block names or cost figures anywhere in `app.py` —
   always read them from the `starter` package or from the widget values, so
   the app stays correct if the underlying data changes.
