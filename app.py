import streamlit as st
import os
from datetime import datetime

from database import (
    init_db,
    add_trade,
    get_trades,
    reset_all_trades
)

# =======================
# INIT
# =======================
init_db()

st.set_page_config(page_title="Trading Journal", layout="wide")

# =======================
# LOGO
# =======================
logo_path = "logo.png"

if os.path.isfile(logo_path):
    st.image(logo_path, width=120)

# =======================
# HEADER
# =======================
st.title("Precision Market Academy")
st.caption("📊 Trading Journal")

trades = get_trades()

# =======================
# SIDEBAR
# =======================
st.sidebar.title("Filters")

menu = st.sidebar.radio(
    "Module",
    ["Dashboard", "Add Trade", "Analytics", "Equity Curve", "AI Review"]
)

filter_type = st.sidebar.selectbox(
    "Filter",
    ["All", "Wins", "Losses"]
)

# =======================
# RESET
# =======================
st.sidebar.markdown("### Reset Data")

confirm = st.sidebar.checkbox("Confirm delete all trades")

if st.sidebar.button("Reset Trades"):
    if confirm:
        reset_all_trades()
        st.rerun()
    else:
        st.error("Confirm first")

# =======================
# FILTER LOGIC
# =======================
def apply_filters(trades):

    out = []

    for t in trades:
        pnl = float(t[0])

        if filter_type == "Wins" and pnl <= 0:
            continue
        if filter_type == "Losses" and pnl > 0:
            continue

        out.append(t)

    return out

filtered_trades = apply_filters(trades)

# =======================
# DASHBOARD (TRADINGVIEW STYLE)
# =======================
if menu == "Dashboard":

    st.header("📊 Trade Dashboard")

    if filtered_trades:

        pnl_list = [float(t[0]) for t in filtered_trades]

        wins = len([p for p in pnl_list if p > 0])
        losses = len([p for p in pnl_list if p <= 0])

        total = len(pnl_list)
        win_rate = (wins / total) * 100 if total else 0
        total_pnl = sum(pnl_list)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Trades", total)
        col2.metric("Win Rate", f"{win_rate:.1f}%")
        col3.metric("Wins/Losses", f"{wins}/{losses}")
        col4.metric("PnL", f"${total_pnl:.2f}")

        st.divider()

        st.subheader("📈 Trade Journal")

        for i, t in enumerate(filtered_trades, 1):

            pnl, setup, note, tv_link, day, timestamp = t
            pnl = float(pnl)

            status = "🟢 WIN" if pnl > 0 else "🔴 LOSS"

            with st.expander(f"{status} Trade #{i} | ${pnl}"):

                st.markdown(f"""
**Setup:** {setup}  
**Day:** {day}  
**Time:** {timestamp}  

📝 **Note:**  
{note}
""")

                if tv_link:
                    st.markdown(f"🔗 [Open TradingView Chart]({tv_link})")

    else:
        st.info("No trades found.")

# =======================
# ADD TRADE
# =======================
elif menu == "Add Trade":

    st.header("➕ Add Trade")

    pnl = st.number_input("PnL", step=1.0)

    setup = st.selectbox(
        "Setup",
        ["Breakout", "Reversal", "Trend", "Scalp"]
    )

    day = st.selectbox(
        "Day",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    note = st.text_area("Notes")

    tv_link = st.text_input("TradingView Link")

    if st.button("Save Trade"):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_trade(pnl, setup, note, tv_link, day, timestamp)

        st.success("Trade saved!")

        st.rerun()

# =======================
# ANALYTICS
# =======================
elif menu == "Analytics":

    st.header("📊 Analytics")

    if filtered_trades:

        pnl_list = [float(t[0]) for t in filtered_trades]

        wins = [p for p in pnl_list if p > 0]
        losses = [p for p in pnl_list if p <= 0]

        total = len(pnl_list)
        win_rate = (len(wins) / total) * 100 if total else 0

        gross_profit = sum(wins)
        gross_loss = abs(sum(losses)) if losses else 0

        profit_factor = gross_profit / gross_loss if gross_loss != 0 else float("inf")

        expectancy = sum(pnl_list) / total if total else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Win Rate", f"{win_rate:.2f}%")
        col2.metric("Profit Factor", round(profit_factor, 2))
        col3.metric("Expectancy", round(expectancy, 2))

    else:
        st.info("No trades found.")

# =======================
# EQUITY CURVE
# =======================
elif menu == "Equity Curve":

    st.header("📈 Equity Curve")

    if filtered_trades:

        balance = 0
        equity = []
        peak = 0
        max_dd = 0

        for t in filtered_trades:
            pnl = float(t[0])
            balance += pnl
            equity.append(balance)

            peak = max(peak, balance)
            max_dd = max(max_dd, peak - balance)

        st.line_chart(equity)
        st.metric("Max Drawdown", f"${max_dd:.2f}")

    else:
        st.info("No data")

# =======================
# AI REVIEW (FIXED + REAL INSIGHT)
# =======================
elif menu == "AI Review":

    st.header("🤖 AI Insights")

    if len(filtered_trades) == 0:
        st.warning("No trades available.")

    else:

        pnl_list = [float(t[0]) for t in filtered_trades]

        wins = [p for p in pnl_list if p > 0]
        losses = [p for p in pnl_list if p <= 0]

        total = len(pnl_list)

        win_rate = (len(wins) / total) * 100 if total else 0
        avg_pnl = sum(pnl_list) / total if total else 0

        best_trade = max(filtered_trades, key=lambda x: float(x[0]))
        worst_trade = min(filtered_trades, key=lambda x: float(x[0]))

        st.subheader("📊 Performance Summary")

        st.write(f"• Win Rate: **{win_rate:.2f}%**")
        st.write(f"• Average PnL: **${avg_pnl:.2f}**")
        st.write(f"• Total Trades: **{total}**")

        st.divider()

        st.subheader("🏆 Best Trade")

        st.success(f"""
PnL: ${best_trade[0]}  
Setup: {best_trade[1]}  
Day: {best_trade[4]}  
Note: {best_trade[2]}
""")

        st.subheader("❌ Worst Trade")

        st.error(f"""
PnL: ${worst_trade[0]}  
Setup: {worst_trade[1]}  
Day: {worst_trade[4]}  
Note: {worst_trade[2]}
""")

        st.divider()

        st.subheader("🧠 Insight")

        if win_rate > 60:
            st.success("Strong system. Focus on scaling execution.")
        elif win_rate >= 45:
            st.warning("Decent system. Improve entry precision.")
        else:
            st.error("Weak system. Review strategy and discipline.")