
import streamlit as st
import math

st.title("Impermanent Loss Calculator")

st.markdown("Enter price data and liquidity amounts to calculate IL")

with st.form("il_form"):
    st.subheader("Asset A (e.g., ETH)")
    price_a_entry = st.number_input("Entry Price of Asset A (USD)", value=3000.0)
    price_a_now = st.number_input("Current Price of Asset A (USD)", value=3500.0)
    deposit_token_a = st.number_input("Amount of Asset A Deposited", value=1.0)

    st.subheader("Asset B (e.g., BTC)")
    price_b_entry = st.number_input("Entry Price of Asset B (USD)", value=60000.0)
    price_b_now = st.number_input("Current Price of Asset B (USD)", value=62000.0)
    deposit_token_b = st.number_input("Amount of Asset B Deposited", value=0.05)

    submitted = st.form_submit_button("Calculate IL")

if submitted:
    value_entry = deposit_token_a * price_a_entry + deposit_token_b * price_b_entry
    ratio_entry = price_a_entry / price_b_entry
    ratio_now = price_a_now / price_b_now
    price_ratio = ratio_now / ratio_entry

    il_percent = 1 - (2 * math.sqrt(price_ratio) / (1 + price_ratio))
    value_now_hodl = deposit_token_a * price_a_now + deposit_token_b * price_b_now
    total_lp_value = value_entry * (2 * math.sqrt(price_ratio) / (1 + price_ratio))
    il_dollars = value_now_hodl - total_lp_value

    st.subheader("Result")
    st.metric("Impermanent Loss (%)", f"{round(il_percent * 100, 4)}%")
    st.metric("HODL Value Now ($)", f"${round(value_now_hodl, 2)}")
    st.metric("LP Value Now ($)", f"${round(total_lp_value, 2)}")
    st.metric("IL ($)", f"${round(il_dollars, 2)}")
