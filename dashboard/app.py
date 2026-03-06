"""
GitOps Intelligence Platform - Professional Dashboard
Run: streamlit run dashboard/app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml_model.predict import predict_risk

st.set_page_config(
    page_title="GitOps Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

* { font-family: 'DM Sans', sans-serif !important; }
code, pre { font-family: 'DM Mono', monospace !important; }

/* ── App background ── */
[data-testid="stAppViewContainer"] {
    background: #f0f4f8;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1a1f2e !important;
    border-right: none;
    box-shadow: 4px 0 24px rgba(0,0,0,0.15);
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #cbd5e1 !important;
    font-size: 14px !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label {
    color: #94a3b8 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stSidebar"] p {
    color: #94a3b8 !important;
}
[data-testid="stSidebar"] h2 {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

/* ── Main content text ── */
h1 { color: #0f172a !important; font-weight: 700 !important; letter-spacing: -0.02em; }
h2 { color: #1e293b !important; font-weight: 600 !important; }
h3 { color: #1e293b !important; font-weight: 600 !important; }
p  { color: #475569 !important; }

/* ── Metric cards ── */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    border: 1px solid #e2e8f0;
    margin-bottom: 8px;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
.kpi-value { font-size: 2.2rem; font-weight: 700; margin: 6px 0 4px; line-height: 1; }
.kpi-label { font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 500; }
.kpi-sub   { font-size: 12px; color: #64748b; margin-top: 4px; }

/* ── Status banners ── */
.banner {
    border-radius: 12px;
    padding: 16px 22px;
    font-size: 15px;
    font-weight: 600;
    margin: 12px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.banner-safe     { background: #f0fdf4; border: 1.5px solid #86efac; color: #166534; }
.banner-moderate { background: #fffbeb; border: 1.5px solid #fcd34d; color: #92400e; }
.banner-risk     { background: #fef2f2; border: 1.5px solid #fca5a5; color: #991b1b; }

/* ── Section cards ── */
.section-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    border: 1px solid #e2e8f0;
    margin-bottom: 16px;
}

/* ── Page header ── */
.page-header {
    background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(26,31,46,0.2);
}
.page-header h1 { color: #ffffff !important; font-size: 2rem !important; margin: 0 !important; }
.page-header p  { color: #94a3b8 !important; margin: 6px 0 0 !important; font-size: 15px; }
.page-header .timestamp { color: #64748b !important; font-size: 13px; font-family: 'DM Mono'; }

/* ── Table styling ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── Streamlit metric override ── */
[data-testid="metric-container"] {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 12px !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; }

/* ── Divider ── */
hr { border-color: #e2e8f0 !important; margin: 20px 0 !important; }

/* ── Info/success boxes ── */
.stInfo    { background: #eff6ff !important; border-color: #93c5fd !important; color: #1e40af !important; }
.stSuccess { background: #f0fdf4 !important; border-color: #86efac !important; color: #166534 !important; }

/* ── Selectbox, slider labels ── */
.stSelectbox label, .stSlider label, .stRadio label, .stMultiSelect label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #374151 !important;
}

/* ── Caption ── */
.stCaption { color: #6b7280 !important; }
</style>
""", unsafe_allow_html=True)


# ── Demo deployment history ───────────────────────────────────
@st.cache_data(ttl=60)
def get_deployment_history(n=40):
    random.seed(42)
    records = []
    base_time = datetime.now()
    for i in range(n):
        m = {
            "files_changed":          random.randint(1, 45),
            "lines_added":            random.randint(1, 750),
            "lines_deleted":          random.randint(0, 300),
            "hour_of_day":            random.randint(0, 23),
            "day_of_week":            random.randint(0, 6),
            "days_since_last_deploy": random.randint(0, 20),
            "recent_failures":        random.randint(0, 4),
            "test_pass_rate":         round(random.uniform(0.6, 1.0), 2),
            "is_main_branch":         random.randint(0, 1),
            "num_contributors":       random.randint(1, 8),
        }
        result = predict_risk(m)
        ts = base_time - timedelta(hours=i * 4)
        records.append({
            "Timestamp":  ts.strftime("%Y-%m-%d %H:%M"),
            "Commit":     f"#{random.randint(1000, 9999)}",
            "Branch":     random.choice(["main", "feature/auth", "fix/bug-123", "develop"]),
            "Risk Score": result["risk_score"],
            "Status":     result["status"],
            "Files":      m["files_changed"],
            "Test Rate":  f"{m['test_pass_rate']:.0%}",
        })
    return pd.DataFrame(records)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 GitOps Intelligence")
    st.markdown("<p style='font-size:12px;margin-top:-8px'>AI-Powered DevOps Platform</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🎮 Simulate Deployment")
    sim_type = st.radio(
        "",
        ["Normal Deploy", "✅ Safe Deploy", "🚨 Risky Deploy"],
        index=0,
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### ⚙️ Parameters")

    defaults = {
        "Normal Deploy":    (8,  120, 0.92, "Wed", 14, 1),
        "✅ Safe Deploy":   (3,  45,  0.99, "Tue", 10, 0),
        "🚨 Risky Deploy":  (45, 750, 0.60, "Fri", 18, 4),
    }
    df_files, df_lines, df_test, df_day, df_hour, df_fail = defaults[sim_type]

    files    = st.slider("Files Changed",    1, 50,   df_files)
    lines    = st.slider("Lines Added",      1, 800,  df_lines)
    test_rt  = st.slider("Test Pass Rate", 0.5, 1.0,  df_test)
    day      = st.selectbox("Day of Week",
                            ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                            index=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].index(df_day))
    hour     = st.slider("Hour of Day",     0, 23,   df_hour)
    failures = st.slider("Recent Failures", 0, 5,    df_fail)

    st.markdown("---")
    st.markdown("### 📍 Navigation")
    page = st.radio("",
                    ["📊 Dashboard", "📈 Analytics", "📋 History", "🤖 AI Review"],
                    label_visibility="collapsed")

# ── Risk calculation ──────────────────────────────────────────
day_map = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}
current_metrics = {
    "files_changed":          files,
    "lines_added":            lines,
    "lines_deleted":          int(lines * 0.3),
    "hour_of_day":            hour,
    "day_of_week":            day_map[day],
    "days_since_last_deploy": 3,
    "recent_failures":        failures,
    "test_pass_rate":         test_rt,
    "is_main_branch":         1,
    "num_contributors":       3,
}
risk_result = predict_risk(current_metrics)
risk_score  = risk_result["risk_score"]
status      = risk_result["status"]

# Colors for light theme
if status == "SAFE":
    color = "#16a34a"; badge_bg = "#dcfce7"; badge_text = "#166534"
elif status == "MODERATE":
    color = "#d97706"; badge_bg = "#fef3c7"; badge_text = "#92400e"
else:
    color = "#dc2626"; badge_bg = "#fee2e2"; badge_text = "#991b1b"


# ════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ════════════════════════════════════════════════════════════
if "Dashboard" in page:

    # Header card
    st.markdown(f"""
    <div class="page-header">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
                <h1>🚀 GitOps Release Intelligence</h1>
                <p>AI-Powered Deployment Risk Platform — Real-time monitoring & prediction</p>
            </div>
            <div style="text-align:right">
                <div class="timestamp">{datetime.now().strftime('%d %b %Y')}</div>
                <div class="timestamp">{datetime.now().strftime('%H:%M')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Status banner
    if status == "SAFE":
        st.markdown(f'<div class="banner banner-safe">🟢 DEPLOYMENT STATUS: SAFE — Auto-deploy is ready! &nbsp;<strong>Risk Score: {risk_score}%</strong></div>', unsafe_allow_html=True)
    elif status == "MODERATE":
        st.markdown(f'<div class="banner banner-moderate">🟡 DEPLOYMENT STATUS: MODERATE — Deploy carefully. &nbsp;<strong>Risk Score: {risk_score}%</strong></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="banner banner-risk">🔴 PIPELINE BLOCKED — HIGH RISK detected! &nbsp;<strong>Risk Score: {risk_score}%</strong> — Manual approval required</div>', unsafe_allow_html=True)

    st.markdown(f"<p style='color:#64748b;font-size:14px;margin-bottom:20px'>💡 {risk_result['recommendation']}</p>", unsafe_allow_html=True)

    # KPI Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Risk Score</div><div class="kpi-value" style="color:{color}">{risk_score}%</div><div class="kpi-sub">{status}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Files Changed</div><div class="kpi-value" style="color:#2563eb">{files}</div><div class="kpi-sub">in this commit</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Lines Added</div><div class="kpi-value" style="color:#16a34a">+{lines}</div><div class="kpi-sub">lines of code</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Test Pass Rate</div><div class="kpi-value" style="color:#7c3aed">{test_rt:.0%}</div><div class="kpi-sub">test coverage</div></div>', unsafe_allow_html=True)
    with c5:
        fc = "#dc2626" if failures >= 3 else "#16a34a"
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Recent Failures</div><div class="kpi-value" style="color:{fc}">{failures}</div><div class="kpi-sub">last 5 deploys</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gauge + Line chart
    col_g, col_l = st.columns([2, 3])

    with col_g:
        st.markdown("#### 🎯 Risk Gauge")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            number={'font': {'color': color, 'size': 52, 'family': 'DM Sans'}, 'suffix': '%'},
            title={'text': "Deployment Risk Score", 'font': {'color': '#475569', 'size': 14}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#94a3b8',
                         'tickfont': {'color': '#64748b', 'size': 11}},
                'bar': {'color': color, 'thickness': 0.28},
                'bgcolor': '#f8fafc',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 30],   'color': '#f0fdf4'},
                    {'range': [30, 60],  'color': '#fffbeb'},
                    {'range': [60, 100], 'color': '#fef2f2'}
                ],
                'threshold': {
                    'line': {'color': '#ef4444', 'width': 2},
                    'thickness': 0.75, 'value': 60
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='white',
            font_color='#0f172a',
            height=290,
            margin=dict(t=40, b=10, l=20, r=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_l:
        st.markdown("#### 📈 Risk Score History — Last 40 Deployments")
        df_hist = get_deployment_history()
        fig_line = px.line(
            df_hist, x='Timestamp', y='Risk Score', color='Branch',
            template='plotly_white',
            color_discrete_sequence=['#2563eb', '#16a34a', '#d97706', '#7c3aed']
        )
        fig_line.add_hline(y=60, line_dash='dash', line_color='#ef4444',
                           annotation_text="Risk Threshold (60%)",
                           annotation_font_color='#ef4444',
                           annotation_font_size=11)
        fig_line.update_layout(
            paper_bgcolor='white', plot_bgcolor='#f8fafc',
            height=290,
            legend=dict(font=dict(color='#374151', size=11),
                        bgcolor='white', bordercolor='#e2e8f0', borderwidth=1),
            xaxis=dict(tickfont=dict(color='#6b7280', size=10),
                       gridcolor='#f1f5f9', linecolor='#e2e8f0'),
            yaxis=dict(tickfont=dict(color='#6b7280', size=10),
                       gridcolor='#f1f5f9', linecolor='#e2e8f0',
                       range=[0, 100]),
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # Feature importance + pie
    col_fi, col_pie = st.columns(2)

    with col_fi:
        st.markdown("#### 🧠 What Makes Deployments Risky?")
        try:
            fi = pd.read_csv('data/feature_importance.csv').head(8)
            fig_bar = px.bar(
                fi, x='importance', y='feature', orientation='h',
                template='plotly_white',
                color='importance',
                color_continuous_scale=['#dbeafe', '#3b82f6', '#1d4ed8']
            )
            fig_bar.update_layout(
                paper_bgcolor='white', plot_bgcolor='#f8fafc',
                height=300, showlegend=False,
                xaxis=dict(gridcolor='#f1f5f9', tickfont=dict(color='#6b7280')),
                yaxis=dict(tickfont=dict(color='#374151', size=12)),
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        except Exception:
            st.info("Run `python ml_model/train.py` to see feature importance")

    with col_pie:
        st.markdown("#### 📊 Risk Distribution")
        df_hist2 = get_deployment_history()
        sc = df_hist2['Status'].value_counts().reset_index()
        sc.columns = ['Status', 'Count']
        fig_pie = px.pie(
            sc, values='Count', names='Status',
            color='Status',
            color_discrete_map={
                'SAFE':      '#16a34a',
                'MODERATE':  '#d97706',
                'HIGH_RISK': '#dc2626'
            },
            template='plotly_white',
            hole=0.45
        )
        fig_pie.update_traces(textfont=dict(color='white', size=13))
        fig_pie.update_layout(
            paper_bgcolor='white',
            height=300,
            legend=dict(font=dict(color='#374151', size=12),
                        bgcolor='white'),
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ════════════════════════════════════════════════════════════
elif "Analytics" in page:
    st.markdown("""
    <div class="page-header">
        <h1>📈 Deep Analytics</h1>
        <p>Deployment trends, risk patterns, and branch-level insights</p>
    </div>
    """, unsafe_allow_html=True)

    df_hist = get_deployment_history()
    total   = len(df_hist)
    safe    = len(df_hist[df_hist['Status'] == 'SAFE'])
    blocked = len(df_hist[df_hist['Status'] == 'HIGH_RISK'])
    avg_r   = df_hist['Risk Score'].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Deployments</div><div class="kpi-value" style="color:#2563eb">{total}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Safe Deploys</div><div class="kpi-value" style="color:#16a34a">{safe}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">High Risk Blocked</div><div class="kpi-value" style="color:#dc2626">{blocked}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Avg Risk Score</div><div class="kpi-value" style="color:#d97706">{avg_r:.1f}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Risk Score Over Time")
    fig = px.scatter(
        df_hist, x='Timestamp', y='Risk Score',
        color='Status', size='Files',
        color_discrete_map={'SAFE':'#16a34a','MODERATE':'#d97706','HIGH_RISK':'#dc2626'},
        template='plotly_white', height=380
    )
    fig.add_hline(y=60, line_dash='dash', line_color='#ef4444')
    fig.update_layout(paper_bgcolor='white', plot_bgcolor='#f8fafc',
                      xaxis=dict(gridcolor='#f1f5f9'),
                      yaxis=dict(gridcolor='#f1f5f9'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Average Risk Score by Branch")
    branch_avg = df_hist.groupby('Branch')['Risk Score'].mean().reset_index()
    fig2 = px.bar(
        branch_avg, x='Branch', y='Risk Score',
        color='Risk Score',
        color_continuous_scale=['#bbf7d0', '#fde68a', '#fca5a5'],
        template='plotly_white', text='Risk Score'
    )
    fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside',
                       textfont=dict(color='#374151'))
    fig2.update_layout(paper_bgcolor='white', plot_bgcolor='#f8fafc',
                       xaxis=dict(tickfont=dict(color='#374151')),
                       yaxis=dict(gridcolor='#f1f5f9'))
    st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE: HISTORY
# ════════════════════════════════════════════════════════════
elif "History" in page:
    st.markdown("""
    <div class="page-header">
        <h1>📋 Deployment History</h1>
        <p>Complete log of all deployments with risk scores and status</p>
    </div>
    """, unsafe_allow_html=True)

    df_hist = get_deployment_history()
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        sf = st.multiselect("Filter by Status",
                            ["SAFE","MODERATE","HIGH_RISK"],
                            default=["SAFE","MODERATE","HIGH_RISK"])
    with col_f2:
        bf = st.multiselect("Filter by Branch",
                            df_hist['Branch'].unique().tolist(),
                            default=df_hist['Branch'].unique().tolist())

    filtered = df_hist[(df_hist['Status'].isin(sf)) & (df_hist['Branch'].isin(bf))]

    def highlight_status(val):
        return {
            'SAFE':      'color:#166534;font-weight:600;background:#dcfce7;border-radius:4px',
            'MODERATE':  'color:#92400e;font-weight:600;background:#fef3c7;border-radius:4px',
            'HIGH_RISK': 'color:#991b1b;font-weight:600;background:#fee2e2;border-radius:4px'
        }.get(val, '')

    def highlight_score(val):
        if val >= 60: return 'color:#dc2626;font-weight:600'
        if val >= 30: return 'color:#d97706;font-weight:600'
        return 'color:#16a34a;font-weight:600'

    styled = filtered.style \
        .applymap(highlight_status, subset=['Status']) \
        .applymap(highlight_score,  subset=['Risk Score'])

    st.dataframe(styled, use_container_width=True, hide_index=True, height=480)
    st.caption(f"Showing {len(filtered)} of {len(df_hist)} deployments")


# ════════════════════════════════════════════════════════════
# PAGE: AI REVIEW
# ════════════════════════════════════════════════════════════
elif "AI Review" in page:
    st.markdown("""
    <div class="page-header">
        <h1>🤖 AI Code Review</h1>
        <p>Paste a git diff and get an instant AI-powered security & quality review</p>
    </div>
    """, unsafe_allow_html=True)

    sample_diff = '''diff --git a/app.py b/app.py
@@ -10,6 +10,12 @@ def login(username, password):
+    query = f"SELECT * FROM users WHERE username=\'{username}\'"
+    result = db.execute(query)
+    if result and result['password'] == password:
+        token = str(random.random())
+        return token'''

    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.markdown("#### Paste your Git Diff:")
        code_input = st.text_area("", value=sample_diff, height=240,
                                  label_visibility="collapsed")
        if st.button("🔍 Review with AI", type="primary", use_container_width=True):
            with st.spinner("Analyzing code..."):
                from llm_services.code_reviewer import review_with_gemini
                review = review_with_gemini(code_input)
            st.markdown("#### 📝 Review Result:")
            st.markdown(f"""
<div style="background:white;border:1.5px solid #e2e8f0;border-left:4px solid #2563eb;
border-radius:12px;padding:24px;color:#1e293b;line-height:1.8;font-size:14px">
{review}
</div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown("#### 📝 Auto Release Notes:")
        st.markdown("<p style='color:#64748b;font-size:13px'>Generate professional release notes from your recent git commits automatically.</p>", unsafe_allow_html=True)
        if st.button("⚡ Generate Release Notes", use_container_width=True):
            with st.spinner("Generating..."):
                from llm_services.release_notes import generate_release_notes
                notes = generate_release_notes()
            st.markdown(f"""
<div style="background:white;border:1.5px solid #e2e8f0;border-left:4px solid #16a34a;
border-radius:12px;padding:20px;color:#1e293b;line-height:1.8;font-size:13px">
{notes}
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 💡 What AI Reviews For:")
        items = ["🔒 SQL Injection & Security flaws",
                 "🐛 Logic bugs & edge cases",
                 "⚡ Performance bottlenecks",
                 "✅ Code quality & best practices",
                 "📝 Auto-generated release notes"]
        for item in items:
            st.markdown(f"<p style='color:#374151;font-size:13px;margin:4px 0'>{item}</p>",
                        unsafe_allow_html=True)