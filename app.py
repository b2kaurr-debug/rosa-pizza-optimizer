import numpy as np
import pandas as pd
import streamlit as st
from starter import ZONES, TIME_BLOCKS, COSTS, delivery_times

st.set_page_config(page_title="Rosa's Pizza — Delivery Promise Optimizer", page_icon="🍕")

st.title("🍕 Rosa's Pizza — Delivery Promise Optimizer")
st.write(
    "Pick a zone and time block, set the range of promised delivery times to test, "
    "and adjust the cost assumptions if you'd like. Click **Find best promise** to "
    "see the recommendation and how net profit changes across the range."
)

# --- Ported from rosa_analysis.ipynb (Part II) ---
# Keep this logic identical to the notebook's cost_per_late_order / best_promise
# functions so the app and the notebook always agree.

def cost_per_late_order(costs):
    """Total cost to Rosa of a single late order: the refund paid directly,
    plus the profit lost to churn (churned orders * profit margin per order)."""
    return costs["refund"] + costs["churn"] * costs["margin"]


def best_promise(zone, time_block, promises, costs):
    """Return (best_promise, best_net_profit, all_results) for a zone/time
    block, searching over the candidate `promises`.

    Net profit = (orders * profit margin per order)
                 - (late orders * cost per late order)
    """
    cost_late = cost_per_late_order(costs)
    margin = costs["margin"]

    best_p, best_profit = None, -np.inf
    all_results = []

    for p in promises:
        times = delivery_times(zone, time_block, p, seed=1)
        n_orders = len(times)
        n_late = int((times > p).sum())
        net_profit = n_orders * margin - n_late * cost_late

        all_results.append(
            {"Promise (min)": p, "Orders": n_orders, "Late orders": n_late, "Net profit ($)": net_profit}
        )

        if net_profit > best_profit:
            best_p, best_profit = p, net_profit

    return best_p, best_profit, all_results


# --- UI ---

col1, col2 = st.columns(2)
with col1:
    zone = st.selectbox("Zone", ZONES)
with col2:
    time_block = st.selectbox("Time block", TIME_BLOCKS)

st.subheader("Range of promised delivery times to try")
c1, c2, c3 = st.columns(3)
with c1:
    low = st.number_input("Minimum (min)", min_value=5, max_value=120, value=5, step=5)
with c2:
    high = st.number_input("Maximum (min)", min_value=5, max_value=120, value=50, step=5)
with c3:
    step = st.number_input("Step (min)", min_value=1, max_value=30, value=5, step=1)

st.subheader("Cost assumptions")
st.caption("Defaults are pulled from the starter package's COSTS dictionary.")
c4, c5, c6 = st.columns(3)
with c4:
    margin = st.number_input("Profit margin per order ($)", value=float(COSTS.get("margin", COSTS.get("MARGIN", 5.0))), step=0.5)
with c5:
    churn = st.number_input("Orders lost per late order (churn)", value=float(COSTS.get("churn", COSTS.get("CHURN", 2.0))), step=0.1)
with c6:
    refund = st.number_input("Refund per late order ($)", value=float(COSTS.get("refund", COSTS.get("REFUND", 10.0))), step=0.5)
custom_costs = {"margin": margin, "churn": churn, "refund": refund}

if st.button("Find best promise", type="primary"):
    if high < low or step < 1:
        st.error("Please choose a valid range (maximum ≥ minimum, step ≥ 1).")
    else:
        promises = list(range(int(low), int(high) + 1, int(step)))
        best_p, best_profit, results = best_promise(zone, time_block, promises, custom_costs)

        st.success(f"Recommended promise for **{zone} / {time_block}**: **{best_p} minutes**")
        st.metric("Net profit at recommended promise", f"${best_profit:,.2f}")

        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.line_chart(df.set_index("Promise (min)")["Net profit ($)"])

        if best_p in (promises[0], promises[-1]):
            st.info(
                "The best promise found sits at the edge of your range — try "
                "widening the range to make sure you're not missing a better option."
            )
