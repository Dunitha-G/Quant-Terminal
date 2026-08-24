import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

# 1. Total TradingView Structural Overhaul (Force CSS Injection)
st.set_page_config(page_title="X-ALPHA // TERMINAL", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Block default padding margins to mimic full-bleed desktop monitor view */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; padding-left: 2rem !important; padding-right: 2rem !important; max-width: 100% !important; }
    .stApp { background-color: #131722; color: #d1d4dc; font-family: -apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, Ubuntu, sans-serif; }
    iframe { background-color: #131722 !important; }
    
    /* Header & Ticker Strips styling */
    .tv-header-container { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #2a2e39; padding-bottom: 10px; margin-bottom: 15px; }
    .tv-logo { font-size: 18px; font-weight: 700; letter-spacing: 1px; color: #2962ff !important; font-family: monospace; }
    .tv-ticker-pill { background: #1c2030; padding: 4px 10px; border-radius: 3px; font-size: 12px; border: 1px solid #2a2e39; font-weight: 600; color: #2962ff; }
    
    /* Custom High-Density Grid Cards */
    .tv-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 15px; }
    .tv-card { background: #1c2030; border: 1px solid #2a2e39; padding: 12px; border-radius: 4px; }
    .tv-label { font-size: 11px; color: #787b86; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .tv-value { font-size: 20px; font-weight: 700; color: #d1d4dc; font-family: monospace; }
    .tv-signal-buy { color: #089981 !important; font-weight: 700; }
    .tv-signal-sell { color: #f23645 !important; font-weight: 700; }
    .tv-signal-hold { color: #787b86 !important; font-weight: 700; }
    
    /* Clean up default Streamlit elements */
    div[data-testid="stSidebarCollapseButton"] { display: none; }
    .stExpander { border: 1px solid #2a2e39 !important; background: #1c2030 !important; border-radius: 4px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Hardcoded Live Asset Configurations (Eliminates messy sidebars to optimize terminal view)
asset_1 = "BTC-USD"
asset_2 = "GC=F"
lookback = 90

# 3. Fast Data Fetching Pipeline
@st.cache_data(ttl=300)
def get_tv_data(a1, a2, days):
    d1 = yf.download(a1, period=f"{days}d")["Close"]
    d2 = yf.download(a2, period=f"{days}d")["Close"]
    combined = pd.concat([d1, d2], axis=1).dropna()
    combined.columns = ['A1', 'A2']
    combined['Ratio'] = combined['A1'] / combined['A2']
    combined['ZScore'] = stats.zscore(combined['Ratio'])
    return combined

try:
    df = get_tv_data(asset_1, asset_2, lookback)
    current_ratio = df['Ratio'].iloc[-1]
    current_z = df['ZScore'].iloc[-1]
    
    # Calculate simple dynamic metrics for display matrix
    mean_ratio = df['Ratio'].mean()
    pct_dev = ((current_ratio - mean_ratio) / mean_ratio) * 100
    
    # Determine precise trading signals based on traditional boundary breaks
    if current_z > 2.0:
        sig_class = "tv-signal-sell"
        signal_text = "SHORT SPREAD (SELL ACTIVE)"
    elif current_z < -2.0:
        sig_class = "tv-signal-buy"
        signal_text = "LONG SPREAD (BUY ACTIVE)"
    else:
        sig_class = "tv-signal-hold"
        signal_text = "NEUTRAL / MEAN CONVERGING"

    # 4. Top Ribbon Navigation Bar Header
    st.markdown(f"""
        <div class="tv-header-container">
            <div>
                <span class="tv-logo">X-ALPHA // QUANT MATRIX</span>
                <span style="color:#787b86; margin-left:10px; font-size:12px;">CROSS-MARKET PROPRIETARY CORE</span>
            </div>
            <div class="tv-ticker-pill">📡 LIVE FEED: {asset_1} / {asset_2}</div>
        </div>
    """, unsafe_allow_html=True)

    # 5. Core High-Density TradingView Metric Blocks
    st.markdown(f"""
        <div class="tv-grid">
            <div class="tv-card">
                <div class="tv-label">Spread Exchange Ratio</div>
                <div class="tv-value">{current_ratio:.4f}</div>
            </div>
            <div class="tv-card">
                <div class="tv-label">Historical Mean Deviation</div>
                <div class="tv-value" style="color: {'#089981' if pct_dev >= 0 else '#f23645'}">{pct_dev:+.2f}%</div>
            </div>
            <div class="tv-card">
                <div class="tv-label">Normalized Volatility (Z-Score)</div>
                <div class="tv-value">{current_z:.2f} σ</div>
            </div>
            <div class="tv-card">
                <div class="tv-label">System Deployment Target</div>
                <div class="tv-value {sig_class}">{signal_text}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 6. Advanced Custom Plotly Engine (Emulating TradingView Line & Gradient Fills)
    fig = go.Figure()
    
    # Clean up dates format for crisp timeline view
    date_axis = df.index.strftime('%b %d')

    # Add primary strategy line with glowing configuration and transparent area shading
    fig.add_trace(go.Scatter(
        x=date_axis, y=df['ZScore'], name='Spread Z-Score',
        line=dict(color='#2962ff', width=2.5),
        fill='tozeroy', fillcolor='rgba(41, 98, 255, 0.04)',
        hoverinfo='x+y', mode='lines'
    ))
    
    # Sharp, clean limit boundary threshold lines matching trading screen overlays
    fig.add_trace(go.Scatter(x=date_axis, y=[2.0]*len(df), name='Upper Band (+2σ)', line=dict(color='#f23645', width=1, dash='dot'), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=date_axis, y=[-2.0]*len(df), name='Lower Band (-2σ)', line=dict(color='#089981', width=1, dash='dot'), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=date_axis, y=[0.0]*len(df), name='Mean Equilibrium', line=dict(color='#434651', width=1, dash='solid'), hoverinfo='none'))

    # Strict structural overhaul of chart workspace layout parameters
    fig.update_layout(
        height=480,
        margin=dict(l=0, r=0, t=10, b=0),
        template="plotly_dark",
        paper_bgcolor='#131722',
        plot_bgcolor='#131722',
        showlegend=False,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1c2030", font_size=12, font_family="monospace", bordercolor="#2a2e39"),
        xaxis=dict(
            showgrid=True, gridcolor='#202431', zeroline=False,
            tickfont=dict(color='#787b86', size=10), nticks=15,
            linecolor='#2a2e39', mirror=True
        ),
        yaxis=dict(
            showgrid=True, gridcolor='#202431', zeroline=False,
            side="right", tickfont=dict(color='#787b86', size=10),
            linecolor='#2a2e39', mirror=True, fixedrange=True
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

except Exception as e:
    st.error(f"Execution Halt: Data pipeline stream failed. Context: {e}")

# 7. Elite Math Explainer Segment (Sits cleanly below terminal fold)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🔬 CORE QUANTITATIVE METHODOLOGY (MATHEMATICAL VERIFICATION)"):
    st.write("""
    This quantitative terminal continuously captures market prices to run real-time statistical **mean-reversion pairs validation**. 
    Instead of tracing un-normalized historical values, pricing residuals are mapped directly via a rolling Gaussian distribution matrix:
    """)
    st.latex(r"Z_t = \frac{\left(\frac{P_{1,t}}{P_{2,t}}\right) - \mu_{\text{ratio}}}{\sigma_{\text{ratio}}}")
    st.write("""
    When our continuous tracking variable breaks outside the critical value bounds of **$\pm2.0\sigma$**, the pricing structure 
    enters a statistically anomalous domain ($p < 0.05$). Under the assumption of long-term cointegration, this indicates a clear structural asset mispricing setup 
    designed to yield risk-adjusted statistical alpha as values converge back toward historical parity.
    """)
