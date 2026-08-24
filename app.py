import streamlit as st
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
from scipy import stats

# 1. Institutional Dark Mode Terminal Configuration
st.set_page_config(page_title="CrossAlpha || Quant Terminal", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #E0E6ED; }
    h1, h2, h3, h4 { font-family: 'Courier New', monospace; color: #00E676 !important; }
    div.stButton > button:first-child { background-color: #7C4DFF; color: white; border-radius: 4px; border: none; }
    .stMetric { background-color: #171E2E; padding: 15px; border-radius: 6px; border: 1px solid #232E44; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 CROSS-ALPHA STATISTICAL ARBITRAGE TERMINAL")
st.caption("Institutional Risk & Cointegration Metric Engine // Deployed via iPad Cloud Infrastructure")

# 2. Sidebar Terminal Controls
st.sidebar.header("🔧 System Configurations")
st.sidebar.markdown("Modify tickers using standard Yahoo Finance formatting (e.g., `BTC-USD`, `GC=F`, `^FTSE`).")
asset_1 = st.sidebar.text_input("Primary Asset Ticker", "BTC-USD")
asset_2 = st.sidebar.text_input("Secondary Asset Ticker", "GC=F")
lookback = st.sidebar.slider("Historical Lookback (Days)", 30, 365, 90)

# 3. Quantitative Processing Pipeline
@st.cache_data
def fetch_and_calculate(a1, a2, days):
    data1 = yf.download(a1, period=f"{days}d")["Close"]
    data2 = yf.download(a2, period=f"{days}d")["Close"]
    
    # Structural alignment
    # Structural alignment
import pandas as pd
combined = pd.concat([data1, data2], axis=1).dropna()
combined.columns = ['A1', 'A2']

    combined['ZScore'] = stats.zscore(combined['Ratio'])
    return combined

try:
    df = fetch_and_calculate(asset_1, asset_2, lookback)
    current_z = df['ZScore'].iloc[-1]
    
    # 4. Institutional Metric Analytics Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='stMetric'>", unsafe_allow_html=True)
        st.metric(label=f"Current {asset_1}/{asset_2} Ratio", value=f"{df['Ratio'].iloc[-1]:.4f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stMetric'>", unsafe_allow_html=True)
        if abs(current_z) > 2.0:
            st.metric(label="Statistical Z-Score Status", value=f"{current_z:.2f}", delta="⚠️ ANOMALY DETECTED", delta_color="inverse")
        else:
            st.metric(label="Statistical Z-Score Status", value=f"{current_z:.2f}", delta="✓ STABLE EQUILIBRIUM")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='stMetric'>", unsafe_allow_html=True)
        condition = "EXECUTE ARBITRAGE" if abs(current_z) > 2.0 else "HOLD / NO SIGNAL"
        st.metric(label="Engine Trading Signal", value=condition)
        st.markdown("</div>", unsafe_allow_html=True)

    # 5. Interactive Time-Series Charts
    st.subplots_adjust()
    st.subheader("📈 Real-Time Rolling Deviation Matrix")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['ZScore'], name='Rolling Z-Score', line=dict(color='#00E676', width=2)))
    fig.add_trace(go.Scatter(x=df.index, y=[2]*len(df), name='Upper Threshold (+2σ)', line=dict(color='#FF1744', dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=[-2]*len(df), name='Lower Threshold (-2σ)', line=dict(color='#FF1744', dash='dash')))
    
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#232E44')
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Data Connection Error: Please verify ticker symbols on Yahoo Finance. System Output: {e}")

# 6. Elite Communication Section (The Tutor Edge)
st.subheader("🧠 Mathematical Modeling Framework")
with st.expander("Deconstruct the Econometric Framework Used Here"):
    st.write("""
    This quantitative terminal models historical price series to isolate alpha spreads using a normalized statistical **Z-score framework**:
    """)
    st.latex(r"Z_t = \frac{R_t - \mu_R}{\sigma_R}")
    st.write("""
    Where $R_t$ is the asset price ratio at time $t$, $\mu_R$ represents the historical sample mean, and $\sigma_R$ represents the sample standard deviation. 
    When the absolute value of $Z_t$ breaks past our **$\pm2.0\sigma$ boundary thresholds**, the system rejects the random walk null hypothesis. This flags a statistically 
    significant pricing divergence, indicating a high-probability mean-reversion trading setup.
    """)

