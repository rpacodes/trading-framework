import streamlit as st
from datetime import datetime
import os

from database import init_db, add_trade, get_trades, reset_all_trades

init_db()

st.set_page_config(page_title="Trading Journal", layout="wide")

# ======================
# LOGO
# ======================
if os.path.exists("logo.png"):
    st.image("logo.png", width=120)

st.title("📊 Trading Journal")

trades = get_trades()

# ======================
# SIDEBAR
# ======================
menu = st.sidebar.radio("Menu", ["Dashboard", "Add Trade", "Analytics"])

filter_type = st.sidebar.selectbox("Filter", ["All", "Wins", "Losses"])

# ======================
# FILTER
# ======================
def filter_trades(trades):
    out = []

    for t in trades:
        pnl = float(t[0])

        if filter_type == "Wins" and pnl <= 0:
            continue
        if filter_type == "Losses" and pnl > 0:
            continue

        out.append(t)

    return out

filtered = filter_trades(trades)

# ======================
# DASHBOARD
# ======================
if menu == "Dashboard":

    st.header("Overview")

    if filtered:

        pnl_list = [float(t[0]) for t in filtered]

        wins = len([p for p in pnl_list if p > 0])
        losses = len([p for p in pnl_list if p <= 0])

        total = len(pnl_list)
        winrate = (wins / total) * 100 if total else 0

        st.metric("Trades", total)
        st.metric("Win Rate", f"{winrate:.2f}%")

        st.divider()

        for i, t in enumerate(filtered, 1):

            pnl, setup, note, link, day, time = t

            status = "WIN" if float(pnl) > 0 else "LOSS"

            st.write(f"### {status} Trade {i}")
            st.write(f"PnL: {pnl}")
            st.write(f"Setup: {setup}")
            st.write(f"Day: {day}")
            st.write(f"Note: {note}")

            if link:
                st.markdown(f"[TradingView Link]({link})")

    else:
        st.info("No trades found")

# ======================
# ADD TRADE
# ======================
elif menu == "Add Trade":

    st.header("Add Trade")

    pnl = st.number_input("PnL")
    setup = st.selectbox("Setup", ["Breakout", "Reversal", "Trend", "Scalp"])
    day = st.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri"])
    note = st.text_area("Notes")
    link = st.text_input("TradingView Link")

    if st.button("Save"):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_trade(pnl, setup, note, link, day, timestamp)

        st.success("Saved!")
        st.rerun()

# ======================
# ANALYTICS
# ======================
elif menu == "Analytics":

    st.header("Analytics")

    if filtered:

        pnl_list = [float(t[0]) for t in filtered]

        win_rate = len([p for p in pnl_list if p > 0]) / len(pnl_list) * 100

        st.metric("Win Rate", f"{win_rate:.2f}%")

    else:
        st.info("No data")