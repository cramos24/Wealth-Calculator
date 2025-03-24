import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import random
from PIL import Image
import base64
from io import BytesIO
import time

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
    <div style="display: flex; align-items: center; gap: 15px; padding-top: 20px; padding-bottom: 10px;">
        <img src="data:image/png;base64,{logo_base64}" width="60">
        <div style="line-height: 1.2;">
            <h2 style="margin: 0;">Compound Interest Calculator</h2>
            <p style="margin: 0; font-size: 16px;">Learn to build wealth with the power of compounding.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Global Spacing & Styling Tweaks ---
st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6 {
        margin-bottom: 0.2rem;
        margin-top: 0.5rem;
    }
    .stNumberInput, .stSelectbox, .stTextInput, .stDateInput, .stRadio, .stMarkdown p {
        margin-bottom: 0.3rem;
    }
    section.main > div {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    div.stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Calculator Inputs ---
st.info("Over the past 30 years, the average annual return of the S&P 500 has been approximately 10%. You can use this as a historical benchmark when estimating your interest rate.")

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
frequency_option = st.selectbox("Compound Frequency", ["Annually", "Quarterly", "Monthly", "Daily"], index=0)

# --- Calculate Button ---
calculate_clicked = st.button("Calculate")

if calculate_clicked:
    st.markdown("---", unsafe_allow_html=True)

    compound_per_year = {"Annually": 1, "Quarterly": 4, "Monthly": 12, "Daily": 365}[frequency_option]
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

    st.subheader("The Results Are In")
    st.markdown(f"In **{years} years**, you will have **${final_value:,.2f}**.")
    st.markdown("""
The chart below shows an estimate of how much your initial savings will grow over time, according to the interest rate and compounding schedule you specified.

Please remember that slight adjustments in any of those variables can affect the outcome. Reset the calculator and provide different figures to show different scenarios.
""")

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
    font=dict(family="Helvetica, Arial, sans-serif", size=16),
    height=400,
    autosize=True,
    margin=dict(l=10, r=10, t=40, b=30),
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    showlegend=True
    )

    fig.update_yaxes(tickprefix="$", tickformat=",.0f")

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Reduce spacing before CTA
    st.markdown(
        """
        <style>
        .cta-container {
            margin-top: 0.5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- CTA ---
    random.seed(time.time())
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
        <div class='cta-container' style='font-size: 22px; text-align: center;'>
            {random.choice(messages)}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # --- Next Steps ---
    st.markdown("---")
    with st.expander("🧭 Next Steps", expanded=False):
        st.markdown("""
1. **Set a Monthly Contribution Goal**  
   Even $50/month can grow significantly over time. Start small — just stay consistent.

2. **Explore Tax-Advantaged Accounts**  
   Consider a Roth IRA or 401(k) if available. These accounts help your investments grow tax-free or tax-deferred.

3. **Track Your Spending**  
   Use a budgeting app or spreadsheet to find extra money to invest.

4. **Keep Learning**  
   Read books like *The Psychology of Money* or *The Simple Path to Wealth*.

5. **Talk to a Financial Professional**  
   A licensed advisor can help tailor a plan based on your goals.
        """)