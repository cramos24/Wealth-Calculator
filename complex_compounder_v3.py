import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import random
from PIL import Image
import base64
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(page_title="Wealth Calculator", layout="centered")

# --- Convert Logo Image to Base64 ---
def pil_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode()

# --- Load and Display Logo + Title ---
logo = Image.open("futurefundedlogo.png")
logo_base64 = pil_to_base64(logo)

st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{logo_base64}" width="60" style="margin-right: 15px;">
        <div>
            <h2 style="margin-bottom: 0;">Compound Interest Calculator</h2>
            <p style="margin-top: 2px;">Learn to build wealth with the power of compounding.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Info Box ---
st.info("Over the past 30 years, the average annual return of the S&P 500 has been approximately 10%. You can use this as a historical benchmark when estimating your interest rate.")

# --- Inputs ---
st.markdown("#### Initial Investment")
st.caption("This is the first step to building long-term wealth.")
initial = st.number_input("Initial Investment *", min_value=0.0, value=0.0, step=100.0, format="%.2f")

st.markdown("#### Monthly Contribution")
st.caption("Consistent contributions accelerate your path to financial freedom.")
monthly = st.number_input("Monthly Contribution", value=0.0, step=10.0, format="%.2f")

st.markdown("#### Investment Duration")
st.caption("Time in the market beats timing the market. The longer you invest, the more you benefit from compounding.")
years = st.number_input("Length of Time in Years *", min_value=1, value=1, step=1)

st.markdown("#### Expected Annual Return")
st.caption("Estimate your average return based on historical performance or market assumptions.")
interest = st.number_input("Estimated Interest Rate *", min_value=0.0, value=0.0, step=0.1, format="%.2f")

st.markdown("#### Interest Rate Variance")
st.caption("Explore how different return rates can impact your investment outcomes.")
range_offset = st.number_input("Interest Rate Variance Range", min_value=0.0, value=0.0, step=0.1, format="%.2f")

st.markdown("#### Compound Frequency")
st.caption("More frequent compounding can enhance your long-term gains.")
frequency_option = st.radio("Compound Frequency", ["Annually", "Quarterly", "Monthly", "Daily"])

frequency_map = {
    "Annually": 1,
    "Quarterly": 4,
    "Monthly": 12,
    "Daily": 365
}

# --- Calculate Button Centered ---
st.markdown(
    """
    <style>
        div.stButton > button {
            display: block;
            margin: 0 auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Calculate"):
    st.markdown("---")
    st.subheader("The Results Are In")

    st.write(f"Initial Investment: **${initial:,.2f}**")
    st.write(f"Monthly Contribution: **${monthly:,.2f}**")

    compound_per_year = frequency_map[frequency_option]
    year_range = range(0, years + 1)
    df = pd.DataFrame()

    if range_offset == 0:
        rates = [interest]
        labels = [f"Future Value ({interest:.2f}%)"]
        colors = ["#0066cc"]
    else:
        rates = [interest - range_offset, interest, interest + range_offset]
        labels = [f"Variance Below ({rates[0]:.2f}%)", f"Future Value ({rates[1]:.2f}%)", f"Variance Above ({rates[2]:.2f}%)"]
        colors = ["#ff4b4b", "#0066cc", "#4b8aff"]

    for i, rate in enumerate(rates):
        r = rate / 100
        values = []
        for t in year_range:
            future_val = initial * (1 + r / compound_per_year) ** (compound_per_year * t)
            if r > 0:
                contribution_val = monthly * (((1 + r / compound_per_year) ** (compound_per_year * t) - 1) / (r / compound_per_year))
            else:
                contribution_val = monthly * t * compound_per_year
            total = future_val + contribution_val
            values.append(total)
        df[labels[i]] = values

    df.insert(0, "Year", year_range)
    df["Total Contributions"] = [initial + monthly * t * compound_per_year for t in year_range]

    final_value = df[labels[len(labels)//2]].iloc[-1]
    st.markdown(f"In **{years} years**, you could have **${final_value:,.2f}** based on your inputs.")

    fig = go.Figure()
    for i, label in enumerate(labels):
        fig.add_trace(go.Scatter(x=df["Year"], y=df[label], mode='lines+markers', name=label, line=dict(color=colors[i])))

    fig.add_trace(go.Scatter(x=df["Year"], y=df["Total Contributions"], mode='lines+markers', name="Total Contributions", line=dict(color="green", dash='dot')))

    fig.update_layout(
        title="Total Savings Over Time",
        xaxis_title="Year",
        yaxis_title="US Dollars",
        legend_title="Scenario",
        plot_bgcolor="white",
        font=dict(family="Helvetica, Arial, sans-serif", size=18),
        height=700,
        margin=dict(l=20, r=20, t=50, b=40),
        showlegend=True
    )

    fig.update_yaxes(tickprefix="$", tickformat=",.0f")

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # CTA Quote
messages = [
    "Let’s change your financial future, one dollar at a time.",
    "The best time to invest was yesterday. The next best time is today.",
    "Start small. Stay consistent. Let compounding do the heavy lifting.",
    "Your future self will thank you for the steps you take today.",
    "Big dreams start with small, consistent contributions.",
    "Wealth isn't built overnight. It's built with purpose, patience, and persistence.",
    "No amount is too small to begin. Just begin.",
    "Turn time into your greatest asset. Start investing today."
]
st.markdown("---")
st.markdown(
    f"""
    <div class='cta-container' style='font-size: 22px; text-align: center; margin-top: 20px;'>
        {random.choice(messages)}
    </div>
    """,
    unsafe_allow_html=True
)