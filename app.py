import streamlit as st
from database import add_trade, get_trades
from datetime import datetime

st.set_page_config(page_title="Trading Journal Pro", layout="wide")

st.title("📊 Trading Journal Pro v17 (AI Review System)")

# Load trades
trades = get_trades()

# =======================
# AI TRADE ANALYZER
# =======================
def analyze_trades(trades):

    insights = []

    if len(trades) < 5:
        return ["Not enough data yet. Add more trades for analysis."]

    pnl_list = [t[0] for t in trades]
    setup_list = [t[1] for t in trades]
    score_list = [t[3] for t in trades]

    avg_score = sum(score_list) / len(score_list)

    # 🧠 Quality insight
    if avg_score < 5:
        insights.append("⚠️ Low average trade quality. Focus on better setups, not more trades.")
    else:
        insights.append("✅ Good discipline level detected in your trading.")

    # 📊 High quality trades
    high_quality = [t for t in trades if t[3] >= 7]
    high_pnl = sum([t[0] for t in high_quality])

    insights.append(f"📊 Profit from high-quality trades: ${round(high_pnl, 2)}")

    # 📈 Setup performance
    breakout_pnl = sum([t[0] for t in trades if t[1] == "Breakout"])
    reversal_pnl = sum([t[0] for t in trades if t[1] == "Reversal"])
    trend_pnl = sum([t[0] for t in trades if t[1] == "Trend Following"])
    scalp_pnl = sum([t[0] for t in trades if t[1] == "Scalp"])

    best_setup = max(
        [("Breakout", breakout_pnl),
         ("Reversal", reversal_pnl),
         ("Trend", trend_pnl),
         ("Scalp", scalp_pnl)],
        key=lambda x: x[1]
    )

    insights.append(f"📈 Best performing setup: {best_setup[0]} (${round(best_setup[1], 2)})")

    # ⚠️ risk warning
    if max(pnl_list) > 100 and min(pnl_list) < -100:
        insights.append("⚠️ High volatility detected — reduce risk per trade.")

    return insights


# =======================
# SIDEBAR NAVIGATION
# =======================
menu = st.sidebar.selectbox(
    "Navigation",
    ["Add Trade", "Analytics", "Equity Curve", "AI Review"]
)

# =======================
# ADD TRADE PAGE
# =======================
if menu == "Add Trade":

    st.header("➕ Add New Trade")

    pnl = st.number_input("PnL ($)", step=1.0)

    setup = st.selectbox(
        "Setup Type",
        ["Breakout", "Reversal", "Trend Following", "Scalp"]
    )

    note = st.text_area("Trade Notes")

    score = st.slider(
        "Trade Quality Score (1 = bad, 10 = excellent)",
        1, 10, 5
    )

    if st.button("Save Trade"):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_trade(pnl, setup, note, score, timestamp)

        st.success("Trade saved!")

        trades = get_trades()

# =======================
# ANALYTICS PAGE
# =======================
elif menu == "Analytics":

    st.header("📊 Performance Analytics")

    if len(trades) > 0:

        pnl_list = [t[0] for t in trades]
        score_list = [t[3] for t in trades]

        total = len(pnl_list)
        wins = len([p for p in pnl_list if p > 0])
        win_rate = (wins / total) * 100
        total_pnl = sum(pnl_list)
        avg_score = sum(score_list) / len(score_list)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Trades", total)
        col2.metric("Win Rate %", round(win_rate, 2))
        col3.metric("Total PnL", round(total_pnl, 2))

        st.divider()

        st.subheader("🧠 Trade Quality")
        st.metric("Average Score", round(avg_score, 2))

        good = len([t for t in trades if t[3] >= 7])
        bad = len([t for t in trades if t[3] < 7])

        st.write("✅ Good Trades:", good)
        st.write("⚠️ Bad Trades:", bad)

    else:
        st.info("No trades yet.")

# =======================
# EQUITY CURVE PAGE
# =======================
elif menu == "Equity Curve":

    st.header("📈 Equity Curve + Risk")

    if len(trades) > 0:

        equity = []
        balance = 0
        peak = 0
        max_drawdown = 0

        for t in trades:
            pnl = t[0]

            balance += pnl
            equity.append(balance)

            if balance > peak:
                peak = balance

            drawdown = peak - balance

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        st.line_chart(equity)
        st.metric("Max Drawdown ($)", round(max_drawdown, 2))

    else:
        st.info("No data yet.")

# =======================
# AI REVIEW PAGE
# =======================
elif menu == "AI Review":

    st.header("🤖 AI Trade Review")

    insights = analyze_trades(trades)

    for i in insights:
        st.write(i)