# 📊 Financial Statement Analyzer — Python & AI Insights

> Upload any company's financials and get automated ratio analysis, dynamic multi-chart dashboards, an AI-generated analyst report, and a net income waterfall bridge — all in one interactive app.


# Live Demo

![Streamlit App](https://financial-statement-analyzer-python-ai-insights-h6vvqm8jsetwcw.streamlit.app/) 
---


## 🎯 What This App Does

Most financial analysis tools either require expensive software (Bloomberg, FactSet) or produce static outputs. This app does neither — it's a fully interactive, browser-based financial intelligence platform that:

- **Ingests** any company's financials via CSV upload
- **Calculates** 8 key ratios across profitability, efficiency, returns, and leverage
- **Visualises** trends across 4 interactive Plotly chart panels with hover tooltips
- **Renders** a colour-coded ratio dashboard with RAG (Red/Amber/Green) benchmarking
- **Generates** a 4-section AI-powered analyst narrative from the actual data values
- **Builds** a net income waterfall bridge showing the path from Revenue to Net Income
- **Exports** a ratio CSV and a full insights report as downloadable files

---

## 📌 Ratios Calculated

| Ratio | Formula | What It Measures |
|---|---|---|
| Gross Margin % | (Revenue − COGS) / Revenue | Pricing power & production efficiency |
| Net Margin % | Net Income / Revenue | Overall bottom-line profitability |
| OpEx Ratio % | Operating Expenses / Revenue | Cost discipline |
| ROA % | Net Income / Total Assets | Asset productivity |
| ROE % | Net Income / Equity | Shareholder value creation |
| Debt / Equity | Total Liabilities / Equity | Leverage & solvency risk |
| Asset Turnover | Revenue / Total Assets | Revenue generation per asset dollar |
| Current Ratio | (Assets − Liabilities) / Liabilities | Short-term liquidity |

---

## 🧠 AI Insights Engine

The app auto-generates a structured analyst report with four sections:

1. **Revenue & Profitability** — CAGR, peak/trough margin years, pricing power signals
2. **Asset Efficiency & Returns** — ROE vs ROA gap, leverage amplification analysis
3. **Cost Structure** — Gross-to-net margin gap, overhead burden assessment
4. **Leverage & Balance Sheet Risk** — D/E trend, solvency risk flags
5. **Overall Analyst Verdict** — Directional assessment with actionable language

All commentary is dynamically generated from the uploaded data — not templated filler.

---

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| Web Framework | Streamlit |
| Charts | Plotly (Graph Objects + Subplots) |
| Data Processing | Pandas, NumPy |
| Styling | Custom CSS (Inter font, dark theme) |
| Deployment | Streamlit Cloud |

---

## 📂 Project Structure

```
Financial-Statement-Analyzer/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── aramco_sample_financials.csv    # Sample input data (Saudi Aramco 2019–2023)
└── README.md                       # This file
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/BaqarW-tech/Financial-Statement-Analyzer-Python-AI-Insights.git
cd Financial-Statement-Analyzer-Python-AI-Insights
pip install -r requirements.txt
streamlit run app.py
```

---

## 📋 CSV Format

Your file must include these 8 columns (figures in thousands):

```
Year, Revenue, COGS, Operating_Expenses, Net_Income, Assets, Liabilities, Equity
2019, 329784, 138512, 42312, 88200, 510400, 198100, 312300
2020, 229766,  98234, 38104, 49017, 501100, 201300, 299800
```

---

## 📈 Sample Output — Saudi Aramco

| Indicator | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|
| Net Margin % | 26.7% | 21.3% | 27.5% | 30.1% | 27.5% |
| ROE % | 28.2% | 16.4% | 31.6% | 40.4% | 30.1% |
| ROA % | 17.3% | 9.8% | 19.1% | 24.2% | 17.3% |
| D/E Ratio | 0.63x | 0.67x | 0.66x | 0.67x | 0.74x |

---

## 👤 About

**Author:** Muhammad Baqar Wagan
**Focus:** Financial analysis, economic research, and data-driven reporting targeting finance roles in KSA — including Big Four consulting, Islamic Development Bank, and Vision 2030-aligned institutions.

This project demonstrates applied skills in Python financial modelling, interactive dashboard development, automated report generation, and analytical communication — the core skills demanded in financial analysis roles across the Saudi market.

---

## ⚠️ Disclaimer

AI-generated insights are based on ratio analysis and directional trends. They do not constitute investment or financial advice. Sample data is for demonstration purposes only.

---

## 📄 License

MIT License — free to use with attribution.
