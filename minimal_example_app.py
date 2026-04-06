"""
ProcessSigma — Minimal Example Dashboard
Standalone Streamlit app. No database required.
Run: streamlit run minimal_example_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math
from pathlib import Path

st.set_page_config(
    page_title="ProcessSigma — Minimal Example",
    page_icon="⚡",
    layout="wide"
)

# ── Helpers ──────────────────────────────────────────────────
def dpmo_to_sigma(dpmo: float) -> float:
    if dpmo <= 0:       return 6.0
    if dpmo >= 999999:  return 0.5
    if dpmo >= 500000:  return 1.5
    if dpmo >= 308538:  return 2.0
    if dpmo >= 66807:   return 3.0
    if dpmo >= 6210:    return 4.0
    if dpmo >= 233:     return 5.0
    x = 29.37 - 2.221 * math.log(dpmo)
    return round(0.8406 + math.sqrt(max(0, x)), 2)

def classify_sigma(sigma: float) -> str:
    if sigma >= 6: return "🏆 World Class"
    if sigma >= 5: return "✅ Excellent"
    if sigma >= 4: return "🟡 Good"
    if sigma >= 3: return "🟠 Attention"
    return "🔴 Critical"

COLUMNS_MAP = {
    "Order Id": "order_id",
    "order date (DateOrders)": "order_date",
    "shipping date (DateOrders)": "ship_date",
    "Days for shipment (scheduled)": "days_scheduled",
    "Days for shipping (real)": "days_real",
    "Delivery Status": "delivery_status",
    "Late_delivery_risk": "late_delivery_risk",
    "Order Region": "order_region",
    "Order Country": "order_country",
    "Category Name": "category_name",
}

@st.cache_data
def load_and_process(file) -> pd.DataFrame:
    df = pd.read_csv(file, encoding="latin1")
    df = df[[c for c in COLUMNS_MAP if c in df.columns]].rename(columns=COLUMNS_MAP)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["delay_days"] = df["days_real"] - df["days_scheduled"]
    df["is_late"]    = df["delay_days"] > 0
    df["damage_flag"] = False
    df["return_flag"] = False
    df["period"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df = df.dropna(subset=["order_id", "order_date", "delay_days"])
    df = df.drop_duplicates(subset=["order_id"])
    return df

@st.cache_data
def generate_synthetic(n=500) -> pd.DataFrame:
    np.random.seed(42)
    regions    = ["NORTH AMERICA","SOUTH AMERICA","EUROPE","ASIA","OCEANIA"]
    categories = ["Electronics","Clothing","Sports","Home","Food"]
    df = pd.DataFrame({
        "order_id":       range(10001, 10001 + n),
        "order_date":     pd.date_range("2022-01-01", periods=n, freq="12h"),
        "days_scheduled": np.random.randint(3, 7, n),
        "days_real":      np.random.randint(2, 9, n),
        "delivery_status": np.random.choice(
            ["Late delivery","Advance shipping","Shipping on time"], n, p=[0.57, 0.20, 0.23]),
        "order_region":   np.random.choice(regions, n),
        "order_country":  np.random.choice(["USA","Brazil","Germany","Japan","Australia"], n),
        "category_name":  np.random.choice(categories, n),
        "damage_flag":    False,
        "return_flag":    False,
    })
    df["delay_days"] = df["days_real"] - df["days_scheduled"]
    df["is_late"]    = df["delay_days"] > 0
    df["period"]     = df["order_date"].dt.to_period("M").dt.to_timestamp()
    return df

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.image(
    "https://img.shields.io/badge/ProcessSigma-Delivery%20Intelligence-1F4E79?style=for-the-badge",
    use_column_width=True
)
st.sidebar.title("⚡ ProcessSigma")
st.sidebar.caption("Minimal Example — No database required")
st.sidebar.markdown("---")

data_source = st.sidebar.radio(
    "Data Source",
    ["📂 Upload CSV", "🔄 Use Synthetic Data"]
)

df = None

if data_source == "📂 Upload CSV":
    uploaded = st.sidebar.file_uploader(
        "Upload template_injecao.csv",
        type=["csv", "xlsx"]
    )
    if uploaded:
        df = load_and_process(uploaded)
        st.sidebar.success(f"✅ {len(df):,} orders loaded")
    else:
        st.sidebar.info("Download the template below and upload your data.")
        template_path = Path("data/template_injecao.csv")
        if template_path.exists():
            with open(template_path, "rb") as f:
                st.sidebar.download_button(
                    "📥 Download Template CSV",
                    f, "template_injecao.csv", "text/csv"
                )
else:
    df = generate_synthetic()
    st.sidebar.success("✅ 500 synthetic orders ready")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**ProcessSigma Framework**
[GitHub](https://github.com/moises-rb) |
[Full Project](https://github.com/moises-rb/process-sigma-framework) |
[Connect or Contact](https://www.linkedin.com/in/moisesrsjr/)
                    
*Six Sigma + Data Engineering + Process Mining*
""")

# ── Main ──────────────────────────────────────────────────────
st.title("⚡ ProcessSigma — Delivery Intelligence")
st.markdown("**Minimal Example** — Six Sigma indicators from a single CSV file. No database required.")
st.markdown("---")

if df is None:
    st.info("👈 Upload your CSV or select synthetic data from the sidebar to get started.")
    st.markdown("""
    ### What this dashboard demonstrates

    | Layer | What it does |
    |-------|-------------|
    | 🥉 Bronze | Raw data ingestion — preserved as-is |
    | 🥈 Silver | Cleaning, deduplication, delay calculation |
    | 🥇 Gold | OTD%, DPMO, Sigma Level aggregated by period and region |

    **Run the full notebook** for step-by-step explanation:
    ```bash
    jupyter notebook minimal_example.ipynb
    ```
    """)
    st.stop()

# ── Filter ────────────────────────────────────────────────────
regions_all = sorted(df["order_region"].dropna().unique().tolist())
regions_sel = st.sidebar.multiselect("Filter by Region", regions_all, default=regions_all)
df_f = df[df["order_region"].isin(regions_sel)] if regions_sel else df

# ── KPIs ──────────────────────────────────────────────────────
total_orders  = len(df_f)
total_late    = int(df_f["is_late"].sum())
global_otd    = round((total_orders - total_late) / total_orders * 100, 2) if total_orders else 0
global_dpmo   = round(total_late / total_orders * 1_000_000, 2) if total_orders else 0
global_sigma  = dpmo_to_sigma(global_dpmo)
classification = classify_sigma(global_sigma)
mean_delay    = round(df_f["delay_days"].mean(), 2)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Orders",   f"{total_orders:,}")
col2.metric("OTD Global",     f"{global_otd}%",
            delta=f"{round(global_otd - 95, 1)}% vs target",
            delta_color="normal")
col3.metric("Sigma Level",    f"{global_sigma}σ")
col4.metric("DPMO",           f"{global_dpmo:,.0f}")
col5.metric("Classification", classification)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 SPC — P-Chart", "🔬 Six Sigma Analysis"])

# ── TAB 1: Overview ───────────────────────────────────────────
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Lead Time Deviation Distribution")
        fig1 = px.histogram(
            df_f, x="delay_days", nbins=20,
            labels={"delay_days": "Deviation (days)"},
            color_discrete_sequence=["#4fc3f7"]
        )
        fig1.add_vline(
            x=0,
            line_dash="dash",
            line_color="red",
            annotation_text="Zero deviation (on-time)",
            annotation_position="top left"
        )
        fig1.add_vline(
            x=df_f["delay_days"].mean(),
            line_dash="dot",
            line_color="orange",
            annotation_text=f"Mean: {df_f['delay_days'].mean():.2f}d",
            annotation_position="top right"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("OTD (%) by Region")
        otd_reg = df_f.groupby("order_region").agg(
            total=("order_id","count"), late=("is_late","sum")
        ).reset_index()
        otd_reg["otd_pct"] = round(
            (otd_reg["total"] - otd_reg["late"]) / otd_reg["total"] * 100, 2)
        otd_reg = otd_reg.sort_values("otd_pct")

        fig2 = px.bar(
            otd_reg, x="otd_pct", y="order_region", orientation="h",
            labels={"otd_pct": "OTD (%)", "order_region": "Region"},
            color="otd_pct",
            color_continuous_scale=["red","yellow","green"],
            range_color=[40, 100]
        )
        fig2.add_vline(x=95, line_dash="dash", line_color="green",
                       annotation_text="Target 95%")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Monthly OTD Trend")
    monthly_otd = df_f.groupby("period").agg(
        total=("order_id","count"), on_time=(
            "is_late", lambda x: (~x).sum())
    ).reset_index()
    monthly_otd["otd_pct"] = round(
        monthly_otd["on_time"] / monthly_otd["total"] * 100, 2)

    fig3 = px.line(
        monthly_otd, x="period", y="otd_pct",
        markers=True,
        labels={"period":"Period","otd_pct":"OTD (%)"},
        color_discrete_sequence=["#4fc3f7"]
    )
    fig3.add_hline(y=95, line_dash="dash", line_color="green",
                   annotation_text="Target 95%")
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 2: P-Chart ────────────────────────────────────────────
with tab2:
    st.subheader("P-Chart — Monthly Defect Rate")
    st.caption("Statistical Process Control: is the process stable?")

    monthly = df_f.groupby("period").agg(
        total=("order_id","count"), late=("is_late","sum")
    ).reset_index()
    monthly["prop"] = monthly["late"] / monthly["total"]

    p_bar = monthly["late"].sum() / monthly["total"].sum()
    monthly["ucl"] = p_bar + 3 * np.sqrt(
        p_bar * (1 - p_bar) / monthly["total"])
    monthly["lcl"] = (p_bar - 3 * np.sqrt(
        p_bar * (1 - p_bar) / monthly["total"])).clip(lower=0)
    monthly["out"] = (monthly["prop"] > monthly["ucl"]) | \
                     (monthly["prop"] < monthly["lcl"])

    fig_p = go.Figure()
    fig_p.add_trace(go.Scatter(
        x=monthly["period"], y=monthly["ucl"],
        mode="lines", name="UCL",
        line=dict(color="red", dash="dash")))
    fig_p.add_trace(go.Scatter(
        x=monthly["period"], y=monthly["lcl"],
        mode="lines", name="LCL",
        line=dict(color="red", dash="dash"),
        fill="tonexty", fillcolor="rgba(255,0,0,0.05)"))
    fig_p.add_trace(go.Scatter(
        x=monthly["period"], y=monthly["prop"],
        mode="lines+markers", name="Defect Rate",
        line=dict(color="#4fc3f7"),
        marker=dict(size=9,
            color=["red" if v else "#4fc3f7" for v in monthly["out"]])
    ))
    fig_p.add_hline(y=p_bar, line_color="white",
                    annotation_text=f"CL = {p_bar:.3f} ({p_bar*100:.1f}%)")

    out_count = monthly["out"].sum()
    fig_p.update_layout(
        title=f"P-Chart | {out_count} point(s) out of control",
        xaxis_title="Period", yaxis_title="Proportion of Defects"
    )
    st.plotly_chart(fig_p, use_container_width=True)

    if out_count == 0:
        st.success("✅ Process is STATISTICALLY STABLE — no special causes detected.")
        st.info(f"However, the center line ({p_bar*100:.1f}% defect rate) may still be above your target.")
    else:
        st.warning(f"⚠️ {out_count} point(s) out of control — special causes present. Investigate flagged periods.")

# ── TAB 3: Six Sigma ──────────────────────────────────────────
with tab3:
    st.subheader("Six Sigma Indicators")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.subheader("Sigma Level Evolution")
        gold_sigma_rows = []
        for period, grp in df_f.groupby("period"):
            opps    = len(grp)
            defects = int(grp["is_late"].sum() + grp["damage_flag"].sum() +
                         grp["return_flag"].sum())
            dpmo    = round(defects / opps * 1_000_000, 2)
            sigma   = dpmo_to_sigma(dpmo)
            gold_sigma_rows.append({
                "period": period, "dpmo": dpmo, "sigma_level": sigma
            })
        gs = pd.DataFrame(gold_sigma_rows)

        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(
            x=gs["period"], y=gs["sigma_level"],
            mode="lines+markers", name="Sigma Level",
            line=dict(color="#4fc3f7", width=2)
        ))
        fig_s.add_hrect(y0=0, y1=3, fillcolor="red",    opacity=0.07, line_width=0)
        fig_s.add_hrect(y0=3, y1=4, fillcolor="orange", opacity=0.07, line_width=0)
        fig_s.add_hrect(y0=4, y1=5, fillcolor="yellow", opacity=0.07, line_width=0)
        fig_s.add_hrect(y0=5, y1=6, fillcolor="green",  opacity=0.07, line_width=0)
        fig_s.add_hline(y=4, line_dash="dash", line_color="green",
                        annotation_text="Target 4σ")
        fig_s.update_layout(
            yaxis=dict(range=[0, 6.5]),
            xaxis_title="Period", yaxis_title="Sigma Level (σ)"
        )
        st.plotly_chart(fig_s, use_container_width=True)

    with col_s2:
        st.subheader("Six Sigma Reference")
        ref = pd.DataFrame({
            "Sigma": ["6σ","5σ","4σ","3σ","2σ","1.5σ"],
            "DPMO":  ["3.4","233","6,210","66,807","308,538","500,000+"],
            "OTD":   ["99.9997%","99.98%","99.4%","93.3%","69.1%","< 50%"],
            "Class": ["World Class","Excellent","Good ✓","Attention","Poor","Critical"]
        })
        st.dataframe(ref, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Your Process")
        st.markdown(f"""
        | Indicator | Value | Target |
        |-----------|-------|--------|
        | OTD | **{global_otd}%** | >= 95% |
        | DPMO | **{global_dpmo:,.0f}** | <= 6,210 |
        | Sigma Level | **{global_sigma}σ** | >= 4.0σ |
        | Classification | **{classification}** | Good or above |
        """)

st.markdown("---")
st.caption(
    "ProcessSigma Framework — Minimal Example | "
    "Full project: https://github.com/moises-rb/process-sigma-framework"
)
