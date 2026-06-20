import streamlit as st
import pandas as pd
import datetime
import os

# App Core Configuration
st.set_page_config(page_title="Task Master - Rohit Control", layout="wide")

# Premium Dynamic CSS Theme (Safe & Fluid Animation)
st.markdown("""
<style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #060913, #0f172a, #0c1020, #020408) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 12s ease infinite !important;
        color: #e2e8f0;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    .title-box {
        text-align: center;
        color: #00f2fe;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 4px;
        font-size: 36px !important;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
        margin-bottom: 5px;
        margin-top: 10px;
    }
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 35px;
    }
    .card {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(0, 242, 254, 0.35) !important;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #05060c !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3) !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.8) !important;
        transform: translateY(-2px);
        color: #ffffff !important;
    }
    .stTextInput>div>div>input {
        background-color: #070a14 !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #05070f !important;
        border-right: 1px solid rgba(0, 242, 254, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Database Setup -----------------
TASK_FILE = "shared_tasks.csv"
PROGRESS_FILE = "priyanshi_progress.csv"

if not os.path.exists(TASK_FILE):
    pd.DataFrame(columns=["TaskID", "Date", "TaskName", "AssignedBy"]).to_csv(TASK_FILE, index=False)
if not os.path.exists(PROGRESS_FILE):
    pd.DataFrame(columns=["Date", "TaskID", "TaskName", "Status", "TimeCompleted"]).to_csv(PROGRESS_FILE, index=False)

# ----------------- Navigation Panel -----------------
st.sidebar.markdown("<h2 style='color:#00f2fe; text-align:center;'>🎛️ CONTROL UNIT</h2>", unsafe_allow_html=True)
user_role = st.sidebar.radio("CHOOSE ACCESS PORTAL:", ["👤 PRIYANSHI PANEL", "👑 MENTOR ROHIT PANEL"])

st.markdown("<h1 class='title-box'>🎯 DIRECTIVE TASK TRACKER</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>ACCOUNTABILITY & PERFORMANCE MANAGEMENT SYSTEM</p>", unsafe_allow_html=True)
st.write("---")

today_str = str(datetime.date.today())

# ==================== 1. MENTOR ROHIT PANEL ====================
if user_role == "👑 MENTOR ROHIT PANEL":
    st.subheader("🛠️ COMMAND CENTER - ACCESS RESTRICTED")
    mentor_pass = st.text_input("ENTER COMMANDER ACCESS CODE:", type="password", placeholder="Enter Password")
    
    if mentor_pass == "ROHIT99":
        st.success("ACCESS GRANTED. WELCOME BACK, COMMANDER ROHIT.")
        col1, col2 = st.columns([1, 1.3])
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#00f2fe; margin-top:0;'>➕ DEPLOY NEW DIRECTIVE</h4>", unsafe_allow_html=True)
            new_task = st.text_input("ENTER TASK FOR PRIYANSHI:", placeholder="e.g., Complete assignment")
            
            if st.button("DEPLOY TASK"):
                if new_task.strip() != "":
                    df_tasks = pd.read_csv(TASK_FILE)
                    task_id = len(df_tasks) + 1
                    new_row = {"TaskID": task_id, "Date": today_str, "TaskName": new_task, "AssignedBy": "Rohit"}
                    df_tasks = pd.concat([df_tasks, pd.DataFrame([new_row])], ignore_index=False)
                    df_tasks.to_csv(TASK_FILE, index=False)
                    st.success("DIRECTIVE BROADCASTED TO PRIYANSHI'S BOARD!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#00f2fe; margin-top:0;'>📊 PRIYANSHI RECON REPORT</h4>", unsafe_allow_html=True)
            df_prog = pd.read_csv(PROGRESS_FILE)
            if df_prog.empty:
                st.info("NO ACTIVE OBJECTIVES SECURED BY PRIYANSHI YET.")
            else:
                st.dataframe(df_prog.sort_values(by="Date", ascending=False), use_container_width=True)
                st.markdown("<h5 style='color:#e2e8f0; margin-top:15px;'>PRIYANSHI'S OVERALL PERFORMANCE GRAPH:</h5>", unsafe_allow_html=True)
                chart_data = df_prog.groupby("Date").size().reset_index(name="Tasks Completed")
                st.bar_chart(chart_data.set_index("Date"))
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; padding: 15px; border-radius: 8px; color: #f87171; font-weight: bold; text-align: center;'>⚠️ RESTRICTED AREA: UNAUTHORIZED ACCESS ATTEMPTS WILL BE LOGGED</div>", unsafe_allow_html=True)

# ==================== 2. PRIYANSHI PANEL ====================
elif user_role == "👤 PRIYANSHI PANEL":
    st.subheader("📋 PRIYANSHI'S DIRECTIVES BOARD")
    st.write(f"Directives for Today: **{datetime.date.today().strftime('%d %B %Y')}**")
    
    df_tasks = pd.read_csv(TASK_FILE)
    df_prog = pd.read_csv(PROGRESS_FILE)
    
    today_tasks = df_tasks[df_tasks["Date"] == today_str]
    today_progress = df_prog[df_prog["Date"] == today_str]
    
    if today_tasks.empty:
        st.info("🟢 STATUS CLEAR: No active directives assigned by Rohit for today yet.")
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for index, row in today_tasks.iterrows():
            t_id = row["TaskID"]
            t_name = row["TaskName"]
            
            is_completed = not today_progress[(today_progress["TaskID"] == t_id) & (today_progress["Status"] == "Completed")].empty
            
            if is_completed:
                st.checkbox(f"✅ {t_name} (OBJECTIVE SECURED)", value=True, disabled=True, key=f"done_{t_id}")
            else:
                check_btn = st.checkbox(f"⬜ {t_name}", key=f"active_{t_id}")
                if check_btn:
                    now_time = datetime.datetime.now().strftime("%I:%M %p")
                    new_prog = {"Date": today_str, "TaskID": t_id, "TaskName": t_name, "Status": "Completed", "TimeCompleted": now_time}
                    df_prog = pd.concat([df_prog, pd.DataFrame([new_prog])], ignore_index=False)
                    df_prog.to_csv(PROGRESS_FILE, index=False)
                    st.success(f"Objective Secured: '{t_name}' completed.")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        total = len(today_tasks)
        done = len(today_progress)
        efficiency = int(done / total * 100) if total > 0 else 0
        st.write(f"**PRIYANSHI'S MISSION EFFICIENCY FOR TODAY:** {done}/{total} Objectives Secured ({efficiency}%)")
        st.progress(done / total if total > 0 else 0)