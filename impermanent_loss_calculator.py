import streamlit as st
import math

st.title("Impermanent Loss Calculator")

st.markdown("Choose input method and enter asset prices or ratios")

# Переключатель режима ввода
mode = st.radio("Choose Input Mode:", ["Individual USD Prices", "Price Ratio (Asset A / Asset B)"])

with st.form("il_form"):
    if mode == "Individual USD Prices":
        st.subheader("Asset A (e.g., ETH)")
        price_a_entry = st.number_input("Entry Price of Asset A (USD)", min_value=0.0, format="%.2f", value=None, placeholder="2600.0")
        price_a_now = st.number_input("Current Price of Asset A (USD)", min_value=0.0, format="%.2f", value=None, placeholder="2600.0")

        st.subheader("Asset B (e.g., BTC)")
        price_b_entry = st.number_input("Entry Price of Asset B (USD)", min_value=0.0, format="%.4f", value=None, placeholder="100000.0")
        price_b_now = st.number_input("Current Price of Asset B (USD)", min_value=0.0, format="%.4f", value=None, placeholder="100000.0")

    else:
        st.subheader("Price Ratio Mode (Asset A / Asset B)")
        ratio_entry = st.number_input("Entry Price Ratio (A/B)", min_value=0.0, format="%.3f", value=None, placeholder="0.02")
        ratio_now = st.number_input("Current Price Ratio (A/B)", min_value=0.0, format="%.3f", value=None, placeholder="0.03")

        # Приводим к совместимому виду для расчётов
        price_a_entry = 1.0
        price_b_entry = 1.0 / ratio_entry
        price_a_now = 1.0
        price_b_now = 1.0 / ratio_now

    st.subheader("Liquidity Provided")
    deposit_token_a = st.number_input("Amount of Asset A Deposited", min_value=0.0, format="%.4f", value=None, placeholder="1.0")
    deposit_token_b = st.number_input("Amount of Asset B Deposited", min_value=0.0, format="%.4f", value=None, placeholder="0.05")

    submitted = st.form_submit_button("Calculate IL")

if submitted:
    # Считаем изначальную стоимость портфеля
    value_entry = deposit_token_a * price_a_entry + deposit_token_b * price_b_entry

    # Отношения цен
    ratio_entry = price_a_entry / price_b_entry
    ratio_now = price_a_now / price_b_now
    price_ratio = ratio_now / ratio_entry

    # IL формула
    il_percent = 1 - (2 * math.sqrt(price_ratio) / (1 + price_ratio))

    # Если просто держал
    value_now_hodl = deposit_token_a * price_a_now + deposit_token_b * price_b_now

    # LP стоимость после изменения цен
    total_lp_value = value_entry * (2 * math.sqrt(price_ratio) / (1 + price_ratio))
    il_dollars = value_now_hodl - total_lp_value

    st.subheader("Result")
    st.metric("Impermanent Loss (%)", f"{round(il_percent * 100, 4)}%")
    st.metric("HODL Value Now ($)", f"${round(value_now_hodl, 2)}")
    st.metric("LP Value Now ($)", f"${round(total_lp_value, 2)}")
    st.metric("IL ($)", f"${round(il_dollars, 2)}")
