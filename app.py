import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai
import os

# Securely pull the Gemini API key from environment configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Configure master layout for wide-screen display
st.set_page_config(page_title="Case Matrix Control Center", page_icon="🎛️", layout="wide")

# Premium High-Tech Dark Medical Cockpit UI Style Injector
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; background-color: #060B26; color: #F4F6FA; }
    .main-header { font-size:2.5rem !important; color:#FFFFFF; font-weight:800; letter-spacing: -0.5px; margin-bottom:2px; }
    .sub-header { font-size:1.05rem !important; color:#00E5FF; margin-bottom:25px; font-weight: 400; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Cockpit Glassmorphism Widgets */
    .cockpit-card { background: linear-gradient(135deg, rgba(10,22,59,0.7) 0%, rgba(16,36,96,0.5) 100%); border: 1px solid rgba(0,229,255,0.15); border-radius: 16px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); }
    .cockpit-card-crit { border-left: 5px solid #FF3366; background: linear-gradient(135deg, rgba(44,14,32,0.8) 0%, rgba(16,20,54,0.6) 100%); }
    
    .metric-title { font-size: 0.78rem; text-transform: uppercase; color: #8A99AD; font-weight: 600; letter-spacing: 0.5px; }
    .metric-display { font-size: 2rem; font-weight: 700; color: #FFFFFF; margin-top: 5px; margin-bottom: 5px; }
    .metric-unit { font-size: 0.9rem; color: #00E5FF; font-weight: 400; }
    
    .status-badge { padding: 4px 12px; border-radius: 30px; font-size: 0.72rem; font-weight: 700; display: inline-block; text-transform: uppercase; }
    .badge-crit { background-color: rgba(255,51,102,0.15); color: #FF3366; border: 1px solid rgba(255,51,102,0.3); }
    .badge-stable { background-color: rgba(0,230,118,0.15); color: #00E676; border: 1px solid rgba(0,230,118,0.3); }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: rgba(10,22,59,0.5); padding: 8px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
    .stTabs [data-baseweb="tab"] { color: #8A99AD; font-weight: 600; border-radius: 8px; padding: 10px 20px; transition: all 0.3s; }
    .stTabs [data-baseweb="tab"]:hover { color: #00E5FF; background-color: rgba(0,229,255,0.05); }
    .stTabs [aria-selected="true"] { color: #FFFFFF !important; background-color: #00E5FF !important; color: #060B26 !important; }
</style>
""", unsafe_allow_html=True)

# App Control Title Block
st.markdown("<div class='main-header'>🧬 Case Matrix Control Engine</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Systemic Immune Integration Core & Multidisciplinary Operational Unit</div>", unsafe_allow_html=True)

# --- STEP 1: EXCEL RECOVERY & CONVERSATIONAL CACHE MANAGEMENT ---
EXCEL_FILE = "Master_Clinical_Registry_June_2026.xlsx"
df_registry, df_open, df_summary, df_pending, df_dict = [pd.DataFrame()] * 5

# Locate spreadsheet within repository or query via file uploader
if os.path.exists(EXCEL_FILE):
    excel_target = EXCEL_FILE
else:
    st.sidebar.markdown("### 📁 Clinical Data Core Input")
    uploaded_xlsx = st.sidebar.file_uploader("Upload 'Master_Clinical_Registry_June_2026.xlsx' to activate console metrics:", type=["xlsx"])
    excel_target = uploaded_xlsx if uploaded_xlsx else None

if not excel_target:
    st.info("💡 **Initialization Portal Open:** Please upload your master data registry file (`Master_Clinical_Registry_June_2026.xlsx`) in the sidebar field to launch the strategic graphic modules.")
    st.stop()

# Initialize dataframes securely
try:
    xls = pd.ExcelFile(excel_target)
    sheets = xls.sheet_names
    if "Master Registry" in sheets: df_registry = pd.read_excel(xls, "Master Registry")
    if "Open Items" in sheets: df_open = pd.read_excel(xls, "Open Items")
    if "Summary" in sheets: df_summary = pd.read_excel(xls, "Summary")
    if "Pending & Ordered" in sheets: df_pending = pd.read_excel(xls, "Pending & Ordered")
    if "Data Dictionary" in sheets: df_dict = pd.read_excel(xls, "Data Dictionary")
except Exception as e:
    st.error(f"Ecosystem configuration read failure: {e}")
    st.stop()

# --- STEP 2: BUILD THE FUNCTIONAL COCKPIT TABS ---
tab_dashboard, tab_analytics, tab_registers, tab_ai = st.tabs([
    "🎛️ Strategic Command Deck", 
    "📊 Longitudinal Analytics", 
    "📋 Master Data Registers", 
    "💬 Gemini Clinical AI"
])

# ==================== TAB 1: STRATEGIC COMMAND DECK ====================
with tab_dashboard:
    col_profile, col_open_items = st.columns([2, 1])
    
    with col_profile:
        st.markdown("<div style='color:#00E5FF; font-weight:700; margin-bottom:10px;'>📋 PATIENT PROFILE BRIEF</div>", unsafe_allow_html=True)
        st.markdown("<div class='cockpit-card'>", unsafe_allow_html=True)
        if not df_summary.empty:
            for _, row in df_summary.iterrows():
                st.markdown(f"<div style='margin-bottom:8px;'><strong style='color:#00E5FF;'>{row.iloc[0]}:</strong> <span style='color:#EDF2F7;'>{row.iloc[1]}</span></div>", unsafe_allow_html=True)
        else:
            st.write("Summary data layout empty or parsing format mismatched.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_open_items:
        st.markdown("<div style='color:#FF3366; font-weight:700; margin-bottom:10px;'>⚠️ HIGH-PRIORITY OPEN ACTIONS</div>", unsafe_allow_html=True)
        st.markdown("<div class='cockpit-card' style='min-height:215px;'>", unsafe_allow_html=True)
        if not df_open.empty:
            for _, row in df_open.iterrows():
                st.markdown(f"• <span style='color:#F4F6FA; font-size:0.9rem;'>{row.iloc[0]}</span><br><small style='color:#8A99AD;'>Target Coordinate Tracking Group</small><br><div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
        else:
            st.write("No open clinical items listed.")
        st.markdown("</div>", unsafe_allow_html=True)

    # DYNAMIC METRIC CALLOUT ROW (AUTOMATICALLY LOADS KEY ABNORMAL LABS)
    st.markdown("<div style='color:#00E5FF; font-weight:700; margin-top:10px; margin-bottom:10px;'>🚨 FLAGGED BIOMARKER ANOMALIES</div>", unsafe_allow_html=True)
    if not df_registry.empty:
        df_anomalies = df_registry[df_registry["Status / Clinical Context"].str.contains("Anomaly|Critical|Low|High Risk|Severe", na=False)]
        
        if not df_anomalies.empty:
            metric_cols = st.columns(min(len(df_anomalies), 4))
            for idx, (_, row) in enumerate(df_anomalies.reset_index().iterrows()):
                target_col = metric_cols[idx % 4]
                with target_col:
                    st.markdown(f"""
                    <div class='cockpit-card cockpit-card-crit'>
                        <div class='metric-title'>{row['Marker / Clinical Event']}</div>
                        <div class='metric-display'>{row['Value']} <span class='metric-unit'>{row['Unit'] if pd.notna(row['Unit']) else ''}</span></div>
                        <div class='status-badge badge-crit'>{row['Status / Clinical Context']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("No anomalies flagged. All indicators sitting inside normal parameters.")

    # THERAPEUTICS & LOGISTICS OVERVIEW
    st.markdown("<div style='color:#00E5FF; font-weight:700; margin-top:15px; margin-bottom:10px;'>💊 ACTIVE THERAPEUTIC REGIMENS & ORDERED TESTS</div>", unsafe_allow_html=True)
    tx_col1, tx_col2 = st.columns(2)
    with tx_col1:
        st.markdown("<div class='cockpit-card' style='min-height:200px;'>", unsafe_allow_html=True)
        st.write("🏋️‍♂️ **Active Treatment / Exercise Tracking Loops**")
        st.markdown("""
        - **Parenteral Hydroxocobalamin Cycles:** Bypassing gastrointestinal mucosal block vectors.
        - **Targeted Methylation Acceleration:** Driving conversion paths to collapse high Homocysteine.
        - **Sacroiliac Decompression Stretch Protocols:** Targeted daily physical routines designed to structurally offload the *Castellvi IIIA* segment.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    with tx_col2:
        st.markdown("<div class='cockpit-card' style='min-height:200px;'>", unsafe_allow_html=True)
        st.write("🔬 **Pending Diagnostic Workups (Dr. Domingues / CHL)**")
        if not df_pending.empty:
            st.dataframe(df_pending.style.set_properties(**{'background-color': '#0A163B', 'color': '#FFFFFF'}), use_container_width=True, hide_index=True)
        else:
            st.write("No diagnostic pipelines currently flagged as pending.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 2: LONGITUDINAL ANALYTICS ====================
with tab_analytics:
    st.markdown("### 📊 Cross-Filter Metric Matrix Workspace")
    if not df_registry.empty:
        all_markers = df_registry["Marker / Clinical Event"].dropna().unique().tolist()
        anomaly_markers = df_registry[df_registry["Status / Clinical Context"].str.contains("Anomaly|Critical|Low|High Risk|Severe", na=False)]["Marker / Clinical Event"].tolist()
        
        chosen_markers = st.multiselect(
            "Configure active filters to isolatively chart biomarkers against standard references:",
            options=all_markers, default=anomaly_markers
        )
        
        if chosen_markers:
            df_plot = df_registry[df_registry["Marker / Clinical Event"].isin(chosen_markers)].copy()
            df_plot_numeric = df_plot[pd.to_numeric(df_plot["Value"], errors='coerce').notnull()].copy()
            df_plot_numeric["NumericValue"] = df_plot_numeric["Value"].astype(float)
            
            if not df_plot_numeric.empty:
                fig = px.bar(
                    df_plot_numeric, x="NumericValue", y="Marker / Clinical Event", orientation='h',
                    color="Marker / Clinical Event",
                    color_discrete_sequence=["#00E5FF", "#3366FF", "#FF3366", "#FF9F43", "#10AC84"],
                    template="plotly_dark"
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False, height=350, font=dict(family="Inter", color="#F4F6FA")
                )
                fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selected values contain historical qualitative context items. Add numeric lab entries to render lines.")
                
            # Full structured metric readout table
            st.dataframe(df_plot, use_container_width=True, hide_index=True)
    else:
        st.write("No laboratory data available to graph.")

# ==================== TAB 3: MASTER DATA REGISTERS ====================
with tab_registers:
    st.markdown("### 📋 Live Data Core Editor")
    st.write("Modify spreadsheet parameters inside the dynamic console below. The charts and the Gemini AI engine will read your modifications in real-time.")
    
    # Render interactive, beautifully unstyled spreadsheets as an elite data editor widget
    if not df_registry.empty:
        edited_registry = st.data_editor(
            df_registry, use_container_width=True, num_rows="dynamic",
            key="registry_editor_widget"
        )
        if st.button("⚡ Save Spreadsheet Updates & Sync Engine"):
            df_registry = edited_registry
            if "gemini_chat" in st.session_state:
                del st.session_state.gemini_chat
            st.toast("Ecosystem data matrices successfully updated!", icon="⚡")
            st.rerun()
    else:
        st.write("Master repository sheet disconnected.")

# ==================== TAB 4: GEMINI CLINICAL AI ====================
with tab_ai:
    st.markdown("### 💬 Advanced Multidisciplinary AI Workspace")
    st.write("This workspace operates under strict clinical grounding guardrails. It references the real-time values in your Excel sheet to prevent memory drift.")

    if not GEMINI_API_KEY:
        st.warning("⚠️ Enter your Google Gemini API Key in the application deployment secrets file to engage the live network chat streams.")
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        
        if "gemini_chat" not in st.session_state:
            st.session_state.chat_history = []
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                st.session_state.gemini_chat = model.start_chat(history=[])
                
                # Dynamic conversion of dataframes directly into structured text blocks for Gemini
                reg_str = df_registry.to_string(index=False) if not df_registry.empty else ""
                sum_str = df_summary.to_string(index=False) if not df_summary.empty else ""
                open_str = df_open.to_string(index=False) if not df_open.empty else ""
                
                system_primer = (
                    "MASTER SYSTEMIC CASE CONTEXT INJECTION:\n\n"
                    "You are accessing a high-fidelity clinical repository control center. "
                    "Below are the verified metrics parsed directly from the active spreadsheet registry:\n\n"
                    f"--- PATIENT ACCOUNT RECAP PROFILE ---\n{sum_str}\n\n"
                    f"--- ACTIVE LAB METRIC TRACKS ---\n{reg_str}\n\n"
                    f"--- WORKSPACE OPEN TASKS ---\n{open_str}\n\n"
                    "DIAGNOSTIC PATHOLOGY ROADMAP:\n"
                    "- Patient exhibits a dual-track timeline: an indolent, pre-malignant 3.2% CD3+CD4+CD7- T-helper lymphocyte clone (L-HES signature) causing chronic tissue degranulation (ECP 48.4) and severe mucosal B12 malabsorption, intersecting with a seronegative Axial Spondyloarthritis (axSpA) track manifesting active bone edema and vertical L4 corner enthesitis. Structural lesions locate directly around a congenital lumbosacral Castellvi IIIA transitional fault.\n"
                    "- Onset was anchored via historical chronic Fasciola hepatica parasite stress (cleared in 2014) which selected for the legacy clone, while eradication triggered an explosive Th17 inflammatory rebound line along spinal mechanics.\n"
                    "- An early youth terminal lymphoma blast crisis in a first cousin (age 18-20) confirms a 12.5% shared genetic vulnerability cluster requiring long-term hematological tracking vigilance.\n\n"
                    "STRICT GROUNDING RULE: Treat the provided data frame tables as absolute, unalterable facts. If any query contradicts these files or numbers, refuse to validate it. Do not invent metrics."
                )
                st.session_state.gemini_chat.send_message(system_primer)
                
                # Pre-populate the dark screen space with a welcoming clinical greeting
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "🧬 **Strategic Medical Engine Initialized.** I have successfully digested all active tables from your data core sheets, established cross-system parameters, and locked your clinical timelines under strict grounding constraints. How can I assist your cross-disciplinary analysis loops today?"
                })
            except Exception as e:
                st.error(f"AI interface communication fault: {e}")

        # Render conversation logs smoothly
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Capture text query inputs
        if user_query := st.chat_input("Query the clinical matrix (e.g., 'Map out the connection between my ECP level and my high homocysteine'):"):
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            with st.chat_message("assistant"):
                with st.spinner("Anatomizing data files..."):
                    try:
                        ai_response = st.session_state.gemini_chat.send_message(user_query)
                        st.markdown(ai_response.text)
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_response.text})
                    except Exception as e:
                        st.error(f"The session engine encountered an isolated memory block conflict. Please toggle an input or click 'Reset Chat Session' to flush the buffer. Error details: {e}")
