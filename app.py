"""
╔══════════════════════════════════════════════════════════════════════╗
║          STUDENT PERFORMANCE KPI DASHBOARD — app.py                 ║
║          Tech: Python · Streamlit · Plotly                          ║
║          Auth: admin / admin123 (hardcoded demo)                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduMetrics · Student Performance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --surface2:  #1e2633;
    --accent:    #58a6ff;
    --accent2:   #3fb950;
    --warn:      #f78166;
    --muted:     #8b949e;
    --text:      #e6edf3;
    --border:    #30363d;
    --radius:    12px;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.block-container { padding: 1.5rem 2rem 2rem !important; }
h1,h2,h3,h4 { font-family: 'Space Mono', monospace; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── KPI Cards ── */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform .18s, box-shadow .18s;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(88,166,255,.15);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.kpi-label { font-size: .75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .3rem; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 1.9rem; font-weight: 700; color: var(--text); line-height: 1; }
.kpi-sub   { font-size: .75rem; color: var(--muted); margin-top: .3rem; }
.kpi-icon  { position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); font-size: 2rem; opacity:25; }

/* ── Section header ── */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: var(--accent);
    border-left: 3px solid var(--accent);
    padding-left: .75rem;
    margin: 1.8rem 0 1rem;
    letter-spacing: .04em;
    text-transform: uppercase;
}

/* ── Chart containers ── */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
}

/* ── Login card ── */
.login-wrap {
    max-width: 400px;
    margin: 6vh auto;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 3rem 2.5rem;
    box-shadow: 0 20px 60px rgba(0,0,0,.5);
}
.login-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    text-align: center;
    margin-bottom: .3rem;
    background: linear-gradient(135deg, #58a6ff, #3fb950);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.login-sub { text-align: center; color: var(--muted); font-size: .85rem; margin-bottom: 2rem; }

/* ── Streamlit metric override ── */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
}
[data-testid="metric-container"]::before {
    content: '';
    display: block;
    height: 3px;
    background: linear-gradient(90deg, #58a6ff, #3fb950);
    margin: -1rem -1rem .8rem;
    border-radius: var(--radius) var(--radius) 0 0;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #58a6ff22, #3fb95022) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    transition: all .15s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #58a6ff44, #3fb95044) !important;
    transform: translateY(-1px);
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* ── DataTable ── */
.stDataFrame { border-radius: var(--radius) !important; overflow: hidden; }

/* ── Alerts ── */
.stAlert { border-radius: var(--radius) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Logo bar ── */
.logo-bar {
    display: flex; align-items: center; gap: .6rem;
    font-family: 'Space Mono', monospace; font-size: 1.1rem;
    padding: .8rem 0 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
}
.logo-dot { width: 10px; height: 10px; border-radius: 50%;
    background: linear-gradient(135deg, #58a6ff, #3fb950); display: inline-block; }
/* 🔥 Hide the clear (X) button in multiselect */
[data-baseweb="tag"] button {
    display: none !important;
}

/* Hide dropdown clear icon */
[data-baseweb="select"] svg {
    display: none !important;
}
            
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
VALID_CREDENTIALS = {"admin": "admin123"}
SUBJECTS   = ["Mathematics", "Science", "English", "History", "Geography",
               "Computer Science", "Physics", "Chemistry", "Biology", "Economics"]
CLASSES    = ["9", "10", "11", "12"]
GENDERS    = ["Male", "Female"]
GRADE_MAP  = {"A (85–100)": (85, 100), "B (70–84)": (70, 84),
              "C (50–69)": (50, 69), "D (<50)": (0, 49)}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#e6edf3"),
    margin=dict(l=20, r=20, t=40, b=20),
    showlegend=True,
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#30363d"),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d"),
)
ACCENT_SEQ = ["#58a6ff", "#3fb950", "#f78166", "#d2a8ff", "#ffa657",
              "#79c0ff", "#56d364", "#ff7b72"]

# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
def init_state():
    defaults = {
        "authenticated": False,
        "username": "",
        "students": pd.DataFrame(columns=[
            "ID", "Timestamp", "Name", "Class", "Gender", "Subject", "Score", "Attendance"
        ]),
        "edit_id": None,
        "next_id": 1,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def get_grade(score):
    if score >= 85: return "A"
    if score >= 70: return "B"
    if score >= 50: return "C"
    return "D"

def compute_kpis(df):
    if df.empty:
        return {}
    
    df = df.copy()
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df["Attendance"] = pd.to_numeric(df["Attendance"], errors="coerce")

    total_students = df["Name"].nunique()
    total_records  = len(df)
    total_subjects = df["Subject"].nunique()
    avg_score      = df["Score"].mean()
    avg_attendance = df["Attendance"].mean()
    pass_count     = (df["Score"] >= 40).sum()
    fail_count     = total_records - pass_count
    pass_pct       = pass_count / total_records * 100
    top_score      = df["Score"].max()
    low_score      = df["Score"].min()

    class_avg = df.groupby("Class")["Score"].mean().round(1).to_dict()
    gender_avg = df.groupby("Gender")["Score"].mean().round(1).to_dict()

    df["Grade"] = df["Score"].apply(get_grade)
    grade_dist = df["Grade"].value_counts().to_dict()

    return dict(
        total_students=total_students, total_records=total_records,
        total_subjects=total_subjects, avg_score=round(avg_score, 1),
        avg_attendance=round(avg_attendance, 1), pass_count=pass_count,
        fail_count=fail_count, pass_pct=round(pass_pct, 1),
        top_score=top_score, low_score=low_score,
        class_avg=class_avg, gender_avg=gender_avg, grade_dist=grade_dist,
    )

def add_student(name, cls, gender, subject, score, attendance):
    new_row = {
        "ID": st.session_state.next_id,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Name": name, "Class": cls, "Gender": gender,
        "Subject": subject, "Score": score, "Attendance": attendance,
    }
    st.session_state.students = pd.concat(
        [st.session_state.students, pd.DataFrame([new_row])], ignore_index=True
    )
    st.session_state.next_id += 1

def delete_student(row_id):
    st.session_state.students = st.session_state.students[
        st.session_state.students["ID"] != row_id
    ].reset_index(drop=True)

# ─── LOGIN PAGE ───────────────────────────────────────────────────────────────
def login_page():
    st.markdown("""
    <div class="login-wrap">
        <div class="login-title">🎓 EduMetrics</div>
        <div class="login-sub">Student Performance Intelligence Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    # Centre the form
    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        st.markdown("### Sign In")
        username = st.text_input("👤  Username", placeholder="admin")
        password = st.text_input("🔒  Password", type="password", placeholder="admin123")

        if st.button("Login →", use_container_width=True):
            if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌  Invalid credentials. Try **admin / admin123**")

        st.caption("Demo credentials: `admin` / `admin123`")

# ─── SIDEBAR — DATA ENTRY ────────────────────────────────────────────────────
def sidebar_entry():
    with st.sidebar:
        # Logo
        st.markdown('<div class="logo-bar"><span class="logo-dot"></span> EduMetrics</div>',
                    unsafe_allow_html=True)

        st.markdown("### ➕ Add Student Record")

        with st.form("entry_form", clear_on_submit=True):
            name       = st.text_input("Student Name", placeholder="e.g. Priya Sharma")
            cls        = st.selectbox("Class", CLASSES)
            gender     = st.selectbox("Gender", GENDERS)
            subject    = st.selectbox("Subject", SUBJECTS)
            score      = st.number_input("Score (0–100)", min_value=0, max_value=100, value=75)
            attendance = st.number_input("Attendance % (0–100)", min_value=0, max_value=100, value=85)
            submitted  = st.form_submit_button("✅ Submit Record", use_container_width=True)

            if submitted:
                if not name.strip():
                    st.error("Please enter a student name.")
                else:
                    add_student(name.strip(), cls, gender, subject, score, attendance)
                    st.success(f"✅ Record added for **{name}**")

        st.divider()

        # Quick stats in sidebar
        df = st.session_state.students
        if not df.empty:
            st.markdown("### 📊 Quick Stats")
            st.metric("Total Records", len(df))
            st.metric("Avg Score", f"{df['Score'].mean():.1f}")
            st.metric("Pass Rate", f"{(df['Score'] >= 40).mean()*100:.1f}%")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.students = pd.DataFrame(columns=[
                    "ID", "Timestamp", "Name", "Class", "Gender", "Subject", "Score", "Attendance"
                ])
                st.session_state.next_id = 1
                st.rerun()
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()

# ─── KPI CARDS ────────────────────────────────────────────────────────────────
def kpi_cards(kpis):
    st.markdown('<div class="section-header">📌 KEY PERFORMANCE INDICATORS</div>',
                unsafe_allow_html=True)

    cards = [
        ("👥", "Total Students",    kpis["total_students"],     "unique students"),
        ("📚", "Total Records",     kpis["total_records"],      "entries in system"),
        ("📖", "Subjects Tracked",  kpis["total_subjects"],     "distinct subjects"),
        ("⭐", "Average Score",     f"{kpis['avg_score']}",     "out of 100"),
        ("📅", "Avg Attendance",    f"{kpis['avg_attendance']}%","present"),
        ("✅", "Pass Rate",         f"{kpis['pass_pct']}%",     f"{kpis['pass_count']} students passed"),
        ("❌", "Fail Count",        kpis["fail_count"],         "score < 40"),
        ("🏆", "Top Score",         kpis["top_score"],          f"Lowest: {kpis['low_score']}"),
    ]

    cols = st.columns(4)
    for i, (icon, label, value, sub) in enumerate(cards):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-sub">{sub}</div>
                <div class="kpi-icon">{icon}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:.6rem'></div>", unsafe_allow_html=True)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
def charts_section(df, kpis):
    df = df.copy()
    df["Grade"] = df["Score"].apply(get_grade)

    st.markdown('<div class="section-header">📈 ANALYTICS & VISUALISATIONS</div>',
                unsafe_allow_html=True)

    # ── Row 1: Histogram | Scatter ──
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = px.histogram(
            df, x="Score", nbins=20, color_discrete_sequence=["#58a6ff"],
            title="📊 Score Distribution",
        )
        fig.update_layout(**PLOTLY_LAYOUT, title_font_size=14)
        fig.update_traces(marker_line_color="#0d1117", marker_line_width=1.2)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig2 = px.scatter(
            df, x="Attendance", y="Score", color="Grade",
            color_discrete_sequence=ACCENT_SEQ,
            hover_data=["Name", "Subject", "Class"],
            title="🔵 Attendance vs Score",
            labels={"Attendance": "Attendance %", "Score": "Score"},
        )
        fig2.update_traces(marker=dict(size=8, opacity=.8))
        fig2.update_layout(**PLOTLY_LAYOUT, title_font_size=14)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 2: Class Bar | Gender Pie ──
    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        class_df = df.groupby("Class")["Score"].mean().reset_index()
        class_df.columns = ["Class", "Avg Score"]
        fig3 = px.bar(
            class_df, x="Class", y="Avg Score",
            color="Class", color_discrete_sequence=ACCENT_SEQ,
            title="🏫 Class-wise Average Score", text_auto=".1f",
        )
        fig3.update_traces(textposition="outside", marker_line_width=0)
        fig3.update_layout(**PLOTLY_LAYOUT, title_font_size=14)
        fig3.update_layout(showlegend=False)

        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        gender_df = df.groupby("Gender")["Score"].mean().reset_index()
        fig4 = px.pie(
            gender_df, values="Score", names="Gender",
            color_discrete_sequence=["#58a6ff", "#f78166"],
            title="🚻 Gender-wise Avg Score", hole=.45,
        )
        fig4.update_layout(**PLOTLY_LAYOUT, title_font_size=14)
        fig4.update_traces(textfont_size=13, pull=[0.03, 0.03])
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3: Grade Dist | Subject Radar ──
    c5, c6 = st.columns(2)

    with c5:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        grade_order = ["A", "B", "C", "D"]
        grade_counts = df["Grade"].value_counts().reindex(grade_order, fill_value=0).reset_index()
        grade_counts.columns = ["Grade", "Count"]
        colors = {"A": "#3fb950", "B": "#58a6ff", "C": "#ffa657", "D": "#f78166"}
        fig5 = px.bar(
            grade_counts, x="Grade", y="Count",
            color="Grade", color_discrete_map=colors,
            title="🏅 Grade Distribution (A/B/C/D)", text_auto=True,
        )
        fig5.update_traces(textposition="outside", marker_line_width=0)
        fig5.update_layout(**PLOTLY_LAYOUT, title_font_size=14)
        fig5.update_layout(showlegend=False)

        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        subj_df = df.groupby("Subject")["Score"].mean().reset_index().sort_values("Score")
        fig6 = px.bar(
            subj_df, x="Score", y="Subject", orientation="h",
            color="Score", color_continuous_scale=["#f78166", "#ffa657", "#3fb950"],
            title="📚 Subject-wise Average Score", text_auto=".1f",
        )
        fig6.update_traces(textposition="outside")
        fig6.update_layout(**PLOTLY_LAYOUT, title_font_size=14,
                           coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

# ─── DATA TABLE ───────────────────────────────────────────────────────────────
def data_table_section():
    st.markdown('<div class="section-header">🗃️ STUDENT RECORDS — INTERACTIVE TABLE</div>',
                unsafe_allow_html=True)

    df = st.session_state.students.copy()

    if df.empty:
        st.info("📭 No records yet. Add students using the sidebar form.")
        return

    # Search filter
    search_col, filter_col1, filter_col2 = st.columns([3, 1.5, 1.5])
    with search_col:
        search = st.text_input("🔍 Search by name or subject", placeholder="Type to filter…")
    with filter_col1:
        class_filter = st.multiselect("Class", CLASSES, default=CLASSES)
    with filter_col2:
        gender_filter = st.multiselect("Gender", GENDERS, default=GENDERS)

    # Apply filters
    mask = (
        df["Class"].isin(class_filter) &
        df["Gender"].isin(gender_filter)
    )
    if search:
        mask &= (
            df["Name"].str.contains(search, case=False, na=False) |
            df["Subject"].str.contains(search, case=False, na=False)
        )
    filtered = df[mask].copy()

    # Add grade column for display
    filtered["Grade"] = filtered["Score"].apply(get_grade)
    filtered["Pass/Fail"] = filtered["Score"].apply(lambda x: "✅ Pass" if x >= 40 else "❌ Fail")

    st.markdown(f"**{len(filtered)}** records found")

    # Display table (hide ID for cleanliness)
    display_cols = ["Name", "Class", "Gender", "Subject", "Score", "Attendance", "Grade", "Pass/Fail", "Timestamp"]
    st.dataframe(
        filtered[display_cols].sort_values("Score", ascending=False),
        use_container_width=True,
        height=320,
        column_config={
            "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"),
            "Attendance": st.column_config.ProgressColumn("Attendance %", min_value=0, max_value=100, format="%d%%"),
        }
    )

    # ── Per-row delete ──
    st.markdown("**🗑️ Delete a specific record:**")
    if not filtered.empty:
        del_options = {
            f"ID {row['ID']} — {row['Name']} · {row['Subject']} · Score: {row['Score']}": row["ID"]
            for _, row in filtered.iterrows()
        }
        selected_del = st.selectbox("Select record to delete", ["— select —"] + list(del_options.keys()))
        if st.button("Delete Selected Record", type="primary"):
            if selected_del != "— select —":
                delete_student(del_options[selected_del])
                st.success("Record deleted.")
                st.rerun()
            else:
                st.warning("Please select a record first.")

# ─── DASHBOARD MAIN ───────────────────────────────────────────────────────────
def dashboard():
    sidebar_entry()

    # ── Page header ──
    col_h1, col_h2 = st.columns([5, 1])
    with col_h1:
        st.markdown("""
        <h1 style='font-family:Space Mono,monospace; font-size:1.8rem; margin-bottom:.2rem;
            background:linear-gradient(135deg,#58a6ff,#3fb950);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            🎓 Student Performance Dashboard
        </h1>
        <p style='color:#8b949e; font-size:.9rem; margin-top:0;'>
            Real-time academic intelligence · Data-driven insights
        </p>
        """, unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"<div style='text-align:right; color:#8b949e; font-size:.8rem; padding-top:1rem;'>👤 {st.session_state.username}</div>",
                    unsafe_allow_html=True)

    st.divider()

    df = st.session_state.students

    # ── No data guard ──
    if df.empty:
        st.warning("⚠️ No student data yet. Use the **sidebar form** to add records and unlock the full dashboard.")
        st.markdown("""
        <div style='text-align:center; padding:4rem 0; color:#8b949e;'>
            <div style='font-size:4rem;'>📋</div>
            <div style='font-size:1.2rem; margin-top:1rem;'>Start by adding a student record →</div>
        </div>
        """, unsafe_allow_html=True)
        return

    kpis = compute_kpis(df)

    # ── KPI Cards ──
    kpi_cards(kpis)

    # ── Class & Gender avg callout ──
    st.divider()
    ca1, ca2 = st.columns(2)
    with ca1:
        st.markdown("**📊 Class-wise Averages**")
        cols_cls = st.columns(len(kpis["class_avg"]) or 1)
        for i, (cls, avg) in enumerate(kpis["class_avg"].items()):
            with cols_cls[i]:
                st.metric(f"Class {cls}", avg)
    with ca2:
        st.markdown("**⚥ Gender-wise Averages**")
        cols_gen = st.columns(len(kpis["gender_avg"]) or 1)
        for i, (gen, avg) in enumerate(kpis["gender_avg"].items()):
            with cols_gen[i]:
                st.metric(gen, avg)

    # ── Charts ──
    charts_section(df, kpis)

    # ── Data Table ──
    st.divider()
    data_table_section()

    # ── Footer ──
    st.divider()
    st.markdown(
        "<div style='text-align:center; color:#30363d; font-size:.75rem; font-family:Space Mono,monospace;'>"
        "EduMetrics · Built with Streamlit & Plotly · © 2025</div>",
        unsafe_allow_html=True
    )

# ─── ROUTER ───────────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    login_page()
else:
    dashboard()
