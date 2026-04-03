import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io

# ─────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Financial Statement Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background-color: #07111d; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #0d1b2a 100%);
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] * { color: #c9d6e3 !important; }

.dash-title { font-size:1.9rem; font-weight:700; color:#ffffff; letter-spacing:-0.02em; line-height:1.2; }
.dash-sub   { font-size:0.88rem; color:#5a7a99; margin-top:4px; margin-bottom:24px; }
.accent     { color:#3b9eff; }

.kpi-card {
    background: linear-gradient(135deg, #0d1b2a, #112240);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 20px 16px 16px 16px;
    text-align: center;
    position: relative; overflow: hidden;
}
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.kpi-blue::before   { background: linear-gradient(90deg,#1a6bb5,#3b9eff); }
.kpi-green::before  { background: linear-gradient(90deg,#00804d,#00e68a); }
.kpi-yellow::before { background: linear-gradient(90deg,#b07d00,#f39c12); }
.kpi-red::before    { background: linear-gradient(90deg,#8b1a1a,#e74c3c); }
.kpi-purple::before { background: linear-gradient(90deg,#5b2d8e,#9b59b6); }

.kpi-title { font-size:0.7rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#7a99bb; margin-bottom:6px; }
.kpi-value { font-size:1.9rem; font-weight:700; line-height:1; margin-bottom:2px; }
.kpi-blue .kpi-value   { color:#3b9eff; }
.kpi-green .kpi-value  { color:#00e68a; }
.kpi-yellow .kpi-value { color:#f39c12; }
.kpi-red .kpi-value    { color:#e74c3c; }
.kpi-purple .kpi-value { color:#9b59b6; }
.kpi-sub   { font-size:0.72rem; color:#566f8a; margin-top:4px; }
.kpi-delta { font-size:0.75rem; margin-top:6px; font-weight:500; }
.delta-up   { color:#00e68a; }
.delta-down { color:#e74c3c; }
.delta-flat { color:#f39c12; }

.section-title {
    font-size:1.05rem; font-weight:700; color:#e0eaf4;
    border-left:4px solid #3b9eff;
    padding-left:12px; margin:28px 0 14px 0;
    letter-spacing:0.02em;
}

.insight-box {
    background:#0d1b2a; border-left:3px solid #3b9eff;
    border-radius:0 8px 8px 0; padding:12px 16px; margin:6px 0;
    color:#b0c8e0; font-size:0.84rem; line-height:1.7;
}
.insight-box.green  { border-left-color:#00e68a; }
.insight-box.yellow { border-left-color:#f39c12; }
.insight-box.red    { border-left-color:#e74c3c; }

.verdict-box {
    background: linear-gradient(135deg,#0d1b2a,#0a1628);
    border:1px solid #1e3a5f; border-radius:12px;
    padding:20px 24px; margin:12px 0;
}
.verdict-title { font-size:1rem; font-weight:700; color:#e0eaf4; margin-bottom:10px; }
.verdict-body  { font-size:0.85rem; color:#b0c8e0; line-height:1.75; }

.ratio-table { width:100%; border-collapse:collapse; font-size:0.82rem; }
.ratio-table th {
    background:#0d1b2a; color:#7a99bb; font-weight:600;
    font-size:0.7rem; letter-spacing:0.08em; text-transform:uppercase;
    padding:10px 14px; border-bottom:1px solid #1e3a5f; text-align:left;
}
.ratio-table td { padding:9px 14px; border-bottom:1px solid #0d1b2a; color:#c9d6e3; }
.ratio-table tr:hover td { background:#0d1b2a; }
.chip { display:inline-block; padding:2px 9px; border-radius:20px; font-size:0.68rem; font-weight:600; }
.chip-g { background:rgba(0,230,138,0.13); color:#00e68a; }
.chip-r { background:rgba(231,76,60,0.13);  color:#e74c3c; }
.chip-y { background:rgba(243,156,18,0.13); color:#f39c12; }

hr.div { border:none; border-top:1px solid #1e3a5f; margin:24px 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SAMPLE DATA — Saudi Aramco style
# ─────────────────────────────────────────
SAMPLE_DATA = {
    "Year":               [2019, 2020, 2021, 2022, 2023],
    "Revenue":            [329784, 229766, 400394, 535184, 440959],
    "COGS":               [138512,  98234, 157832, 194321, 172483],
    "Operating_Expenses": [ 42312,  38104,  49832,  56123,  51234],
    "Net_Income":         [ 88200,  49017, 110024, 161100, 121270],
    "Assets":             [510400, 501100, 576000, 665000, 701000],
    "Liabilities":        [198100, 201300, 228000, 266500, 298400],
    "Equity":             [312300, 299800, 348000, 398500, 402600],
}

# ─────────────────────────────────────────
# RATIO ENGINE
# ─────────────────────────────────────────
def compute_ratios(df):
    r = pd.DataFrame()
    r["Year"]         = df["Year"]
    r["Gross_Margin"] = ((df["Revenue"] - df["COGS"]) / df["Revenue"] * 100).round(2)
    r["Net_Margin"]   = (df["Net_Income"] / df["Revenue"] * 100).round(2)
    r["OpEx_Ratio"]   = (df["Operating_Expenses"] / df["Revenue"] * 100).round(2)
    r["ROA"]          = (df["Net_Income"] / df["Assets"] * 100).round(2)
    r["ROE"]          = (df["Net_Income"] / df["Equity"] * 100).round(2)
    r["Debt_Equity"]  = (df["Liabilities"] / df["Equity"]).round(2)
    r["Asset_Turn"]   = (df["Revenue"] / df["Assets"]).round(2)
    r["Current_Ratio"]= ((df["Assets"] - df["Liabilities"]) / df["Liabilities"]).round(2)
    return r

def yoy(series):
    """YoY % change for latest year."""
    if len(series) < 2:
        return None
    prev, curr = series.iloc[-2], series.iloc[-1]
    if prev == 0:
        return None
    return round((curr - prev) / abs(prev) * 100, 1)

def trend_label(series):
    delta = yoy(series)
    if delta is None:
        return "—", "delta-flat"
    if delta > 0:
        return f"▲ {delta}% YoY", "delta-up"
    elif delta < 0:
        return f"▼ {abs(delta)}% YoY", "delta-down"
    else:
        return "→ Flat", "delta-flat"

# ─────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────
BG, CARD, GRID = "#07111d", "#0d1b2a", "#1e3a5f"
BLUE, GREEN, YELLOW, RED, PURPLE = "#3b9eff", "#00e68a", "#f39c12", "#e74c3c", "#9b59b6"

def base_layout(title="", height=280):
    return dict(
        paper_bgcolor=BG, plot_bgcolor=CARD,
        font=dict(family="Inter", color="#c9d6e3", size=11),
        title=dict(text=title, font=dict(size=12, color="#c9d6e3"), x=0.01, y=0.97),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickcolor="#566f8a"),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickcolor="#566f8a"),
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        height=height,
        showlegend=True,
    )

# ─────────────────────────────────────────
# AI INSIGHTS ENGINE
# ─────────────────────────────────────────
def generate_insights(df, ratios, company):
    years = df["Year"].tolist()
    rev   = df["Revenue"].tolist()
    ni    = df["Net_Income"].tolist()
    nm    = ratios["Net_Margin"].tolist()
    gm    = ratios["Gross_Margin"].tolist()
    roe   = ratios["ROE"].tolist()
    roa   = ratios["ROA"].tolist()
    de    = ratios["Debt_Equity"].tolist()

    rev_cagr = ((rev[-1]/rev[0])**(1/(len(years)-1))-1)*100 if rev[0] > 0 else 0
    ni_cagr  = ((ni[-1]/ni[0])**(1/(len(years)-1))-1)*100  if ni[0]  > 0 and ni[-1] > 0 else 0

    best_margin_yr  = years[nm.index(max(nm))]
    worst_margin_yr = years[nm.index(min(nm))]
    de_trend = "rising" if de[-1] > de[0] else "falling"
    roe_trend = "improving" if roe[-1] > roe[0] else "declining"

    nm_latest  = nm[-1]
    gm_latest  = gm[-1]
    roe_latest = roe[-1]
    roa_latest = roa[-1]
    de_latest  = de[-1]

    insights = {
        "revenue": {
            "title": "Revenue & Profitability",
            "color": "green" if rev_cagr > 5 else ("yellow" if rev_cagr > 0 else "red"),
            "body": (
                f"{company} grew revenue at a {rev_cagr:.1f}% CAGR over the {len(years)}-year period, "
                f"from {rev[0]:,.0f}K to {rev[-1]:,.0f}K. "
                f"Net income followed a {'positive' if ni_cagr > 0 else 'negative'} trajectory "
                f"({ni_cagr:.1f}% CAGR), with peak profitability in {best_margin_yr} "
                f"(net margin: {max(nm):.1f}%) and a trough in {worst_margin_yr} "
                f"(net margin: {min(nm):.1f}%). "
                f"{'Revenue growth outpaced cost growth, signalling pricing power.' if gm[-1] > gm[0] else 'Gross margin compression suggests rising input costs or pricing pressure.'}"
            )
        },
        "efficiency": {
            "title": "Asset Efficiency & Returns",
            "color": "green" if roe_latest > 15 else ("yellow" if roe_latest > 8 else "red"),
            "body": (
                f"Return on Equity stands at {roe_latest:.1f}% (latest year), "
                f"{'a strong result indicating high shareholder value creation' if roe_latest > 15 else 'moderate — room to improve capital deployment'}. "
                f"ROE is {roe_trend} over the review period. "
                f"Return on Assets of {roa_latest:.1f}% reflects "
                f"{'efficient asset utilisation' if roa_latest > 10 else 'moderate asset productivity — management may consider asset optimisation'}. "
                f"The gap between ROE and ROA indicates leverage is "
                f"{'amplifying returns meaningfully' if (roe_latest - roa_latest) > 5 else 'not significantly magnifying equity returns'}."
            )
        },
        "costs": {
            "title": "Cost Structure & Margins",
            "color": "green" if gm_latest > 40 else ("yellow" if gm_latest > 25 else "red"),
            "body": (
                f"Gross margin of {gm_latest:.1f}% indicates "
                f"{'strong pricing power and cost control' if gm_latest > 40 else 'moderate cost discipline'}. "
                f"Net margin of {nm_latest:.1f}% after operating expenses and taxes "
                f"{'compares favourably with industry peers' if nm_latest > 15 else 'suggests overhead costs are eroding gross profits significantly'}. "
                f"{'The gap between gross and net margin is within an acceptable range.' if (gm_latest - nm_latest) < 20 else 'A large gross-to-net margin gap warrants scrutiny of operating expense line items.'}"
            )
        },
        "leverage": {
            "title": "Leverage & Balance Sheet Risk",
            "color": "green" if de_latest < 0.8 else ("yellow" if de_latest < 1.5 else "red"),
            "body": (
                f"Debt-to-Equity ratio of {de_latest:.2f}x is "
                f"{'conservative and reflects a strong balance sheet' if de_latest < 0.8 else ('moderate — manageable but warrants monitoring' if de_latest < 1.5 else 'elevated — liabilities significantly exceed equity, raising solvency risk')}. "
                f"Leverage is {de_trend} over the review period, "
                f"{'which is a positive signal' if de_trend == 'falling' else 'which should be monitored closely alongside interest coverage'}. "
                f"{'The company retains significant equity buffer against creditors.' if de_latest < 1 else 'Management should prioritise debt reduction or equity reinforcement to reduce financial risk.'}"
            )
        },
        "verdict": (
            f"{company} shows "
            f"{'strong overall financial health' if (nm_latest > 15 and roe_latest > 15 and de_latest < 1) else 'mixed financial signals requiring selective improvement'}. "
            f"{'Profitability metrics are solid with consistent margin performance.' if nm_latest > 10 else 'Margin improvement should be a strategic priority.'} "
            f"{'Capital efficiency is high, with ROE well above the cost of equity threshold.' if roe_latest > 15 else 'Capital efficiency needs attention — ROE is below typical investor return expectations.'} "
            f"{'The balance sheet is conservatively structured.' if de_latest < 1 else 'Leverage risk is the primary concern for credit and equity stakeholders.'} "
            f"Overall trajectory: {'positive — the company is generating strong returns and managing costs effectively.' if (rev_cagr > 0 and ni_cagr > 0 and roe_latest > 10) else 'cautionary — management should focus on margin recovery and balance sheet discipline.'}"
        )
    }
    return insights

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Financial Analyzer")
    st.markdown("---")

    data_source = st.radio(
        "Data Source",
        ["Use Saudi Aramco Sample Data", "Upload My Own CSV"],
        index=0
    )

    uploaded_file = None
    company_name  = "Saudi Aramco"

    if data_source == "Upload My Own CSV":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        company_name  = st.text_input("Company Name", value="My Company")
        st.markdown("""
**Required CSV columns:**
`Year`, `Revenue`, `COGS`,
`Operating_Expenses`, `Net_Income`,
`Assets`, `Liabilities`, `Equity`

*(figures in thousands)*
        """)
    else:
        company_name = "Saudi Aramco"

    st.markdown("---")
    show_raw = st.checkbox("Show Raw Data Table", value=False)
    show_methodology = st.checkbox("Show Ratio Formulas", value=False)
    st.markdown("---")
    st.caption("Financial Statement Analyzer\nBuilt by BaqarW-tech · 2024")

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
try:
    if data_source == "Upload My Own CSV" and uploaded_file:
        df = pd.read_csv(uploaded_file)
        required = ["Year","Revenue","COGS","Operating_Expenses","Net_Income","Assets","Liabilities","Equity"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            st.error(f"Missing columns: {', '.join(missing)}")
            st.stop()
        df = df.sort_values("Year").reset_index(drop=True)
    elif data_source == "Upload My Own CSV" and not uploaded_file:
        st.info("👈 Upload a CSV file to begin analysis, or switch to the sample data.")
        st.stop()
    else:
        df = pd.DataFrame(SAMPLE_DATA)
        company_name = "Saudi Aramco"

    ratios   = compute_ratios(df)
    insights = generate_insights(df, ratios, company_name)
    years    = df["Year"].tolist()

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div class="dash-title">📊 <span class="accent">{company_name}</span> — Financial Intelligence Report</div>
<div class="dash-sub">
    Automated ratio analysis · AI-powered insights · {years[0]}–{years[-1]} · Figures in SAR thousands
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# KPI STRIP
# ─────────────────────────────────────────
kpis = [
    ("Net Margin",    f"{ratios['Net_Margin'].iloc[-1]:.1f}%",    "Profitability after all costs",  *trend_label(ratios['Net_Margin']),   "kpi-blue"),
    ("ROE",           f"{ratios['ROE'].iloc[-1]:.1f}%",           "Return on shareholders' equity", *trend_label(ratios['ROE']),          "kpi-green"),
    ("ROA",           f"{ratios['ROA'].iloc[-1]:.1f}%",           "Return on total assets",         *trend_label(ratios['ROA']),          "kpi-yellow"),
    ("Gross Margin",  f"{ratios['Gross_Margin'].iloc[-1]:.1f}%",  "Revenue minus COGS",             *trend_label(ratios['Gross_Margin']), "kpi-purple"),
    ("Debt / Equity", f"{ratios['Debt_Equity'].iloc[-1]:.2f}x",   "Leverage ratio",                 *trend_label(ratios['Debt_Equity']),  "kpi-red"),
]

cols = st.columns(5)
for col, (title, value, sub, delta, delta_cls, card_cls) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card {card_cls}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
            <div class="kpi-delta {delta_cls}">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# CHART ROW 1 — Revenue & Margins
# ─────────────────────────────────────────
st.markdown('<div class="section-title">📈 Revenue, Profitability & Margin Trends</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=years, y=df["Revenue"], name="Revenue",
        marker_color=f"rgba(59,158,255,0.7)",
        hovertemplate="<b>%{x}</b><br>Revenue: %{y:,.0f}K<extra></extra>"
    ), secondary_y=False)
    fig.add_trace(go.Bar(
        x=years, y=df["Net_Income"], name="Net Income",
        marker_color=f"rgba(0,230,138,0.7)",
        hovertemplate="<b>%{x}</b><br>Net Income: %{y:,.0f}K<extra></extra>"
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=years, y=ratios["Net_Margin"], name="Net Margin %",
        line=dict(color=YELLOW, width=2.5, dash="dot"),
        mode="lines+markers", marker=dict(size=6, color=YELLOW),
        hovertemplate="<b>%{x}</b><br>Net Margin: %{y:.1f}%<extra></extra>"
    ), secondary_y=True)
    layout = base_layout("Revenue vs Net Income + Net Margin %", 300)
    layout["yaxis2"] = dict(gridcolor=GRID, zerolinecolor=GRID, tickcolor="#566f8a",
                             title="%", ticksuffix="%", showgrid=False)
    layout["barmode"] = "group"
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=years, y=ratios["Gross_Margin"], name="Gross Margin",
        line=dict(color=BLUE, width=2.5), mode="lines+markers",
        marker=dict(size=6, color=BLUE),
        fill='tonexty' if False else None,
        hovertemplate="<b>%{x}</b><br>Gross Margin: %{y:.1f}%<extra></extra>"
    ))
    fig2.add_trace(go.Scatter(
        x=years, y=ratios["Net_Margin"], name="Net Margin",
        line=dict(color=GREEN, width=2.5), mode="lines+markers",
        marker=dict(size=6, color=GREEN),
        hovertemplate="<b>%{x}</b><br>Net Margin: %{y:.1f}%<extra></extra>"
    ))
    fig2.add_trace(go.Scatter(
        x=years, y=ratios["OpEx_Ratio"], name="OpEx Ratio",
        line=dict(color=RED, width=2, dash="dot"), mode="lines+markers",
        marker=dict(size=5, color=RED),
        hovertemplate="<b>%{x}</b><br>OpEx Ratio: %{y:.1f}%<extra></extra>"
    ))
    layout2 = base_layout("Margin Profile (%)", 300)
    layout2["yaxis"]["ticksuffix"] = "%"
    fig2.update_layout(**layout2)
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────
# CHART ROW 2 — Returns & Leverage
# ─────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=years, y=ratios["ROE"], name="ROE %",
        line=dict(color=PURPLE, width=2.5), mode="lines+markers",
        marker=dict(size=6, color=PURPLE),
        fill="tozeroy",
        fillcolor="rgba(155,89,182,0.08)",
        hovertemplate="<b>%{x}</b><br>ROE: %{y:.1f}%<extra></extra>"
    ))
    fig3.add_trace(go.Scatter(
        x=years, y=ratios["ROA"], name="ROA %",
        line=dict(color=YELLOW, width=2.5), mode="lines+markers",
        marker=dict(size=6, color=YELLOW),
        fill="tozeroy",
        fillcolor="rgba(243,156,18,0.06)",
        hovertemplate="<b>%{x}</b><br>ROA: %{y:.1f}%<extra></extra>"
    ))
    # Reference line at 15% (good ROE benchmark)
    fig3.add_hline(y=15, line_dash="dot", line_color="#566f8a", line_width=1,
                   annotation_text="15% benchmark", annotation_font_size=9,
                   annotation_font_color="#566f8a", annotation_position="top right")
    layout3 = base_layout("ROE vs ROA (%)", 300)
    layout3["yaxis"]["ticksuffix"] = "%"
    fig3.update_layout(**layout3)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    de_colors = [GREEN if v < 0.8 else (YELLOW if v < 1.5 else RED) for v in ratios["Debt_Equity"]]
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=years, y=ratios["Debt_Equity"], name="D/E Ratio",
        marker_color=de_colors,
        hovertemplate="<b>%{x}</b><br>D/E: %{y:.2f}x<extra></extra>"
    ))
    fig4.add_hline(y=1.0, line_dash="dot", line_color=RED, line_width=1.5,
                   annotation_text="1.0x danger line", annotation_font_size=9,
                   annotation_font_color=RED, annotation_position="top right")
    layout4 = base_layout("Debt-to-Equity Ratio (x)", 300)
    layout4["showlegend"] = False
    fig4.update_layout(**layout4)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# FULL RATIO TABLE
# ─────────────────────────────────────────
st.markdown('<div class="section-title">📋 Complete Ratio Dashboard</div>', unsafe_allow_html=True)

header_row = "<tr>" + "".join(
    f"<th>{'Indicator' if i==0 else y}</th>"
    for i, y in enumerate(["Indicator"] + years)
) + "</tr>"

ratio_defs = [
    ("Gross Margin %",  "Gross_Margin", "%",  lambda v: "chip-g" if v>40 else ("chip-y" if v>25 else "chip-r")),
    ("Net Margin %",    "Net_Margin",   "%",  lambda v: "chip-g" if v>15 else ("chip-y" if v>5  else "chip-r")),
    ("OpEx Ratio %",    "OpEx_Ratio",   "%",  lambda v: "chip-g" if v<15 else ("chip-y" if v<25 else "chip-r")),
    ("ROA %",           "ROA",          "%",  lambda v: "chip-g" if v>10 else ("chip-y" if v>5  else "chip-r")),
    ("ROE %",           "ROE",          "%",  lambda v: "chip-g" if v>15 else ("chip-y" if v>8  else "chip-r")),
    ("Debt / Equity",   "Debt_Equity",  "x",  lambda v: "chip-g" if v<0.8 else ("chip-y" if v<1.5 else "chip-r")),
    ("Asset Turnover",  "Asset_Turn",   "x",  lambda v: "chip-g" if v>0.7 else ("chip-y" if v>0.4 else "chip-r")),
]

data_rows = ""
for label, col, unit, color_fn in ratio_defs:
    cells = f"<td><b>{label}</b></td>"
    for val in ratios[col].tolist():
        chip = color_fn(val)
        fmt  = f"{val:.1f}{unit}" if unit == "%" else f"{val:.2f}{unit}"
        cells += f'<td><span class="chip {chip}">{fmt}</span></td>'
    data_rows += f"<tr>{cells}</tr>"

st.markdown(f"""
<table class="ratio-table">
    <thead>{header_row}</thead>
    <tbody>{data_rows}</tbody>
</table>
""", unsafe_allow_html=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# AI INSIGHTS
# ─────────────────────────────────────────
st.markdown('<div class="section-title">🧠 AI-Powered Financial Intelligence</div>', unsafe_allow_html=True)

col_l, col_r = st.columns(2)
sections = list(insights.items())
left_sections  = [s for s in sections if s[0] != "verdict"][:2]
right_sections = [s for s in sections if s[0] != "verdict"][2:]

for (key, data) in left_sections:
    with col_l:
        st.markdown(f"""
        <div class="insight-box {data['color']}">
            <b>{data['title']}</b><br>{data['body']}
        </div>
        """, unsafe_allow_html=True)

for (key, data) in right_sections:
    with col_r:
        st.markdown(f"""
        <div class="insight-box {data['color']}">
            <b>{data['title']}</b><br>{data['body']}
        </div>
        """, unsafe_allow_html=True)

# Overall verdict
st.markdown(f"""
<div class="verdict-box">
    <div class="verdict-title">⚖️ Overall Analyst Verdict — {company_name}</div>
    <div class="verdict-body">{insights['verdict']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# WATERFALL — Net Income Bridge
# ─────────────────────────────────────────
st.markdown('<div class="section-title">🌊 Net Income Waterfall — Latest Year</div>', unsafe_allow_html=True)

latest = df.iloc[-1]
bridge_labels  = ["Revenue", "Cost of Goods Sold", "Gross Profit", "Operating Expenses", "Operating Income", "Net Income"]
gross_profit   = latest["Revenue"] - latest["COGS"]
op_income      = gross_profit - latest["Operating_Expenses"]
other_costs    = op_income - latest["Net_Income"]

bridge_values  = [latest["Revenue"], -latest["COGS"], gross_profit,
                  -latest["Operating_Expenses"], op_income, latest["Net_Income"]]
bridge_measure = ["absolute", "relative", "total", "relative", "total", "total"]
bridge_colors  = [BLUE, RED, GREEN, RED, YELLOW, GREEN]

fig_wf = go.Figure(go.Waterfall(
    name="Income Bridge",
    orientation="v",
    measure=bridge_measure,
    x=bridge_labels,
    y=bridge_values,
    connector=dict(line=dict(color=GRID, width=1)),
    increasing=dict(marker=dict(color=GREEN)),
    decreasing=dict(marker=dict(color=RED)),
    totals=dict(marker=dict(color=BLUE)),
    text=[f"{v:,.0f}K" for v in bridge_values],
    textposition="outside",
    textfont=dict(color="#c9d6e3", size=10),
    hovertemplate="<b>%{x}</b><br>%{y:,.0f}K<extra></extra>"
))

layout_wf = base_layout(f"Income Bridge — {latest['Year']:.0f}", 320)
layout_wf["showlegend"] = False
fig_wf.update_layout(**layout_wf)
st.plotly_chart(fig_wf, use_container_width=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────
st.markdown('<div class="section-title">📥 Export</div>', unsafe_allow_html=True)

ec1, ec2 = st.columns(2)
with ec1:
    csv_buf = io.StringIO()
    export_df = ratios.copy()
    export_df.columns = ["Year","Gross Margin %","Net Margin %","OpEx Ratio %","ROA %","ROE %","D/E Ratio","Asset Turnover","Current Ratio"]
    export_df.to_csv(csv_buf, index=False)
    st.download_button(
        "⬇️ Download Ratio Report (CSV)",
        data=csv_buf.getvalue().encode("utf-8"),
        file_name=f"{company_name.replace(' ','_')}_ratios.csv",
        mime="text/csv",
        use_container_width=True
    )
with ec2:
    report_lines = [
        f"FINANCIAL INTELLIGENCE REPORT — {company_name}",
        f"Period: {years[0]}–{years[-1]}",
        "=" * 60, "",
    ]
    for key, data in insights.items():
        if key == "verdict":
            report_lines += ["", "OVERALL VERDICT", "-"*40, data, ""]
        else:
            report_lines += [data["title"].upper(), "-"*40, data["body"], ""]
    report_text = "\n".join(report_lines)
    st.download_button(
        "⬇️ Download Insights Report (TXT)",
        data=report_text.encode("utf-8"),
        file_name=f"{company_name.replace(' ','_')}_insights.txt",
        mime="text/plain",
        use_container_width=True
    )

# ─────────────────────────────────────────
# RAW DATA & METHODOLOGY
# ─────────────────────────────────────────
if show_raw:
    st.markdown('<hr class="div">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗃️ Raw Financial Data</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

if show_methodology:
    st.markdown('<hr class="div">', unsafe_allow_html=True)
    with st.expander("📐 Ratio Formulas & Interpretation Guide"):
        st.markdown("""
| Ratio | Formula | Benchmark |
|---|---|---|
| Gross Margin % | (Revenue − COGS) / Revenue × 100 | >40% = strong |
| Net Margin % | Net Income / Revenue × 100 | >15% = strong |
| OpEx Ratio % | Operating Expenses / Revenue × 100 | <15% = lean |
| ROA % | Net Income / Total Assets × 100 | >10% = efficient |
| ROE % | Net Income / Equity × 100 | >15% = strong |
| Debt / Equity | Total Liabilities / Equity | <0.8x = conservative |
| Asset Turnover | Revenue / Total Assets | >0.7x = productive |

**Colour coding:** 🟢 Strong &nbsp; 🟡 Moderate &nbsp; 🔴 Needs attention
        """)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#2a4a6a; font-size:0.75rem; margin-top:32px; padding-bottom:20px;">
    Financial Statement Analyzer · Built by BaqarW-tech ·
    AI insights are generated from ratio analysis and do not constitute financial advice
</div>
""", unsafe_allow_html=True)
