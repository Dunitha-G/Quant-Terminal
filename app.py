import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# 1. Institutional Layout & CSS Core Engine Injection
st.set_page_config(page_title="ALPHA-MATRIX // TERMINAL", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Full-screen terminal dashboard layout */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; padding-left: 2rem !important; padding-right: 2rem !important; max-width: 100% !important; }
    .stApp { background-color: #0c0e15; color: #d1d4dc; font-family: -apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, sans-serif; }
    
    /* Header Bar Component Styling */
    .tv-header-container { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #2a2e39; padding-bottom: 12px; margin-bottom: 15px; }
    .tv-logo { font-size: 20px; font-weight: 700; letter-spacing: 1.5px; color: #2962ff !important; font-family: monospace; }
    .tv-status-badge { background: #1c2030; padding: 5px 12px; border-radius: 4px; font-size: 11px; border: 1px solid #2a2e39; font-weight: 600; color: #00e676; font-family: monospace; }
    
    /* Grid system layout definitions */
    .tv-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 15px; }
    .tv-card { background: #131722; border: 1px solid #2a2e39; padding: 14px; border-radius: 4px; }
    .tv-label { font-size: 11px; color: #787b86; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }
    .tv-value { font-size: 22px; font-weight: 700; color: #ffffff; font-family: monospace; }
    
    /* Dynamic signal color structures */
    .sig-buy { color: #089981 !important; }
    .sig-sell { color: #f23645 !important; }
    .sig-neutral { color: #787b86 !important; }
    
    /* Interactive Streamlit components visual overrides */
    .stDataFrame { border: 1px solid #2a2e39 !important; background-color: #131722 !important; border-radius: 4px; }
    div[data-testid="stSidebar"] { background-color: #131722 !important; border-right: 1px solid #2a2e39 !important; }
    .stSlider, .stSelectbox { color: #ffffff !important; }
    .stExpander { border: 1px solid #2a2e39 !important; background: #131722 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Institutional Structural Pairs Dictionary Definitions
PAIRS_CONFIG = {
    "Crypto Arbitrage (BTC / ETH)": {"a1": "BTC-USD", "a2": "ETH-USD", "desc": "Digital Gold vs Smart Contract Layer 1 Base"},
    "Precious Metals Spread (Gold / Silver)": {"a1": "GC=F", "a2": "SI=F", "desc": "Traditional Macro Hard Asset Safe Haven Spread"},
    "Global Energy Complex (Brent / WTI)": {"a1": "BZ=F", "a2": "CL=F", "desc": "North Sea Brent vs West Texas Intermediate Crude Pricing Deviation"},
    "Equity Benchmark Skew (S&P 500 / Nasdaq)": {"a1": "^GSPC", "a2": "^IXIC", "desc": "Broad Economic Baseline vs Heavily Concentrated Tech Growth"}
}

# 3. Sidebar Control Console Layout
st.sidebar.markdown("<h3 style='color:#2962ff !important; font-family:monospace; margin-bottom:0;'>🔧 CONFIG DESK</h3>", unsafe_allow_html=True)
st.sidebar.caption("Institutional Execution Strategy Interface")
st.sidebar.markdown("---")

selected_pair_label = st.sidebar.selectbox("🎯 Target Model Workspaces", list(PAIRS_CONFIG.keys()))
active_pair = PAIRS_CONFIG[selected_pair_label]

lookback_days = st.sidebar.slider("📅 Backtest Window Length (Days)", 30, 365, 120)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 System Target Summary")
st.sidebar.info(f"**Selected Strategy Domain:**\n{active_pair['desc']}\n\n**Assets Loaded:**\n{active_pair['a1']} // {active_pair['a2']}")

# 4. Multi-Asset Analytical Pipeline Core Engine
@st.cache_data(ttl=300)
def process_multi_asset_matrix(config_dict, days):
    matrix_rows = []
    
    # Pre-compile data streams for the global watch matrix overview
    for label, assets in config_dict.items():
        try:
            d1 = yf.download(assets['a1'], period=f"{days}d")["Close"]
            d2 = yf.download(assets['a2'], period=f"{days}d")["Close"]
            c = pd.concat([d1, d2], axis=1).dropna()
            c.columns = ['A1', 'A2']
            ratio = c['A1'] / c['A2']
            zscores = stats.zscore(ratio)
            
            cur_z = zscores.iloc[-1]
            status = "🚨 EXTREME DEV" if abs(cur_z) > 2.0 else "✓ PARITY"
            
            matrix_rows.append({
                "Strategy Class": label,
                "Primary Ticker": assets['a1'],
                "Secondary Ticker": assets['a2'],
                "Live Ratio": round(float(ratio.iloc[-1]), 4),
                "Z-Score Volatility": round(float(cur_z), 2),
                "System State": status
            })
        except:
            continue
            
    # Process dedicated full matrix dataframe history for active selection panel charts
    active_d1 = yf.download(active_pair['a1'], period=f"{days}d")["Close"]
    active_d2 = yf.download(active_pair['a2'], period=f"{days}d")["Close"]
    active_df = pd.concat([active_d1, active_d2], axis=1).dropna()
    active_df.columns = ['A1', 'A2']
    active_df['Ratio'] = active_df['A1'] / active_df['A2']
    active_df['ZScore'] = stats.zscore(active_df['Ratio'])
    
    return pd.DataFrame(matrix_rows), active_df

try:
    screener_df, history_df = process_multi_asset_matrix(PAIRS_CONFIG, lookback_days)
    
    # Derive core visualization states
    current_ratio = history_df['Ratio'].iloc[-1]
    current_z = history_df['ZScore'].iloc[-1]
    mean_ratio = history_df['Ratio'].mean()
    pct_deviation = ((current_ratio - mean_ratio) / mean_ratio) * 100
    
    if current_z > 2.0:
        signal_text, signal_class = "SHORT SPREAD (SELL)", "sig-sell"
    elif current_z < -2.0:
        signal_text, signal_class = "LONG SPREAD (BUY)", "sig-buy"
    else:
        signal_text, signal_class = "SYSTEM CONVERGING (HOLD)", "sig-neutral"

    # 5. Top Ribbon Navigation Bar Header Render
    st.markdown(f"""
        <div class="tv-header-container">
            <div>
                <span class="tv-logo">X-ALPHA // REALTIME DATA ENGINE</span>
                <span style="color:#787b86; margin-left:12px; font-size:12px; font-family:monospace;">MULTIVARIATE MATRIX</span>
            </div>
            <div class="tv-status-badge">🟢 COGNITIVE CLOUD NETWORKING LAYER ACTIVE</div>
        </div>
    """, unsafe_allow_html=True)

    # 6. Comprehensive Institutional Dashboard Ribbon Cards
    st.markdown(f"""
        <div class="tv-grid">
            <div class="tv-card">
                <div class="tv-label">Active Ratio [{active_pair['a1']}/{active_pair['a2']}]</div>
                <div class="tv-value">{current_ratio:.4f}</div>
            </div>
            <div class="tv-card">
                <div class="tv-label">Historical Mean Divergence</div>
                <div class="tv-value" style="color: {'#089981' if pct_deviation >= 0 else '#f23645'}">{pct_deviation:+.2f}%</div>
            </div>
            <div class="tv-card">
                <div class="tv-label">Statistical Volatility (Z-Score)</div>
                <div class="tv-value">{current_z:.2f} σ</div>
            </div>
            <div class="tv-card">
                <div class="tv-label">Automated System Flag Decision</div>
                <div class="tv-value {signal_class}">{signal_text}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 7. Dual-Pane Integrated Synchronized Visual Workspace (TradingView Screen Model)
    date_axis = history_df.index.strftime('%b %d')
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06, row_heights=[0.5, 0.5])
    
    # Top Panel Workspace: Raw Price Exchange Ratio Track Layer
    fig.add_trace(go.Scatter(
        x=date_axis, y=history_df['Ratio'], name='Exchange Price Ratio',
        line=dict(color='#2962ff', width=2),
        fill='tozeroy', fillcolor='rgba(41, 98, 255, 0.02)'
    ), row=1, col=1)
    fig.add_trace(go.Scatter(x=date_axis, y=[mean_ratio]*len(history_df), name='Mean Ratio Level', line=dict(color='#787b86', width=1, dash='dash')), row=1, col=1)
    
    # Bottom Panel Workspace: High-Density Statistical Z-Score Target Spread Layer
    fig.add_trace(go.Scatter(
        x=date_axis, y=history_df['ZScore'], name='Rolling Z-Score Deviation',
        line=dict(color='#00e676', width=2),
        fill='tozeroy', fillcolor='rgba(0, 230, 118, 0.02)'
    ), row=2, col=1)
    fig.add_trace(go.Scatter(x=date_axis, y=[2.0]*len(history_df), name='Upper Bound (+2σ)', line=dict(color='#f23645', width=1, dash='dot')), row=2, col=1)
    fig.add_trace(go.Scatter(x=date_axis, y=[-2.0]*len(history_df), name='Lower Bound (-2σ)', line=dict(color='#089981', width=1, dash='dot')), row=2, col=1)
    fig.add_trace(go.Scatter(x=date_axis, y=[0.0]*len(history_df), name='Zero Axis Parity', line=dict(color='#434651', width=1)), row=2, col=1)

    fig.update_layout(
        height=540,
        margin=dict(l=0, r=0, t=10, b=0),
        template="plotly_dark",
        paper_bgcolor='#0c0e15',
        plot_bgcolor='#0c0e15',
        showlegend=False,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#131722", font_size=12, font_family="monospace", bordercolor="#2a2e39")
    )
    
    # Format axes grids specifically to look like a hardware monitor terminal mesh
    fig.update_xaxes(showgrid=True, gridcolor='#1c2030', zeroline=False, tickfont=dict(color='#787b86', size=10), linecolor='#2a2e39')
    fig.update_yaxes(showgrid=True, gridcolor='#1c2030', zeroline=False, side="right", tickfont=dict(color='#787b86', size=10), linecolor='#2a2e39')
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

) 
