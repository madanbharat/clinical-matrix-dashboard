import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai
import os

# Securely pull the Gemini API key from environment configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Initialize the wide-screen application shell
st.set_page_config(page_title="Case Matrix Command Unit", page_icon="🎛️", layout="wide")

# High-Tech Glassmorphism Visual Theme Injector
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    /* Core Layout Foundations */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #030712 !important;
        color: #F3F4F6 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Header & Console Branding elements */
    .cockpit-title { font-size: 2.6rem; font-weight: 800; color: #FFFFFF; letter-spacing: -1px; margin-bottom: 2px; }
    .cockpit-subtitle { font-size: 0.95rem; color: #00F2FE; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; }
    .panel-header { font-size: 1.1rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }
    
    /* Premium Command Deck Cards */
    .command-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.4) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .card-critical { border-left: 4px solid #EF4444 !important; background: linear-gradient(135deg, rgba(44, 16, 24, 0.7) 0%, rgba(15, 23, 42, 0.5) 100%); }
    
    /* Metric Typography */
    .metric-label { font-size: 0.78rem; text-transform: uppercase; color: #9CA3AF; font-weight: 600; letter-spacing: 0.5px; min-height: 38px; display: flex; align-items: center; }
    .metric-val { font-size: 1.9rem; font-weight: 700; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; margin-top: 4px; }
    .metric-unit { font-size: 0.85rem; color: #00F2FE; font-weight: 500; margin-left: 2px; }
    .metric-desc { font-size: 0.75rem; color: #9CA3AF; margin-top: 8px; line-height: 1.4; min-height: 45px; }
    
    /* Status Badges */
    .alert-badge { padding: 4px 10px; border-radius: 6px; font-size: 0.68rem; font-weight: 700; display: inline-block; text-transform: uppercase; margin-top: 10px; letter-spacing: 0.5px; }
    .badge-critical { background-color: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-baseline { background-color: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    
    /* Modern Dashboard Tabs Layout */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #0F172A; padding: 6px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); }
    .stTabs [data-baseweb="tab"] { color: #9CA3AF; font-weight: 600; border-radius: 8px; padding: 10px 24px; border: none !important; }
    .stTabs [aria-selected="true"] { background-color: #00F2FE !important; color: #030712 !important; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# Console Branding Header
st.markdown("<div class='cockpit-title'>🎛️ Case Matrix Command Bridge</div>", unsafe_allow_html=True)
st.markdown("<div class='cockpit-subtitle'>Longitudinal Health Core & High-Fidelity Tactical Interface</div>", unsafe_allow_html=True)

# --- STEP 1: INITIALIZE STABLE EXCEL LOADER CORE ---
EXCEL_FILE = "Master_Clinical_Registry_June_2026.xlsx"

def load_excel_matrices(source):
    try:
        # FIXED: Added engine_kwargs={'data_only': True} to clear formula calculation crashes
        xls = pd.ExcelFile(source, engine_kwargs={'data_only': True})
        sheets = xls.sheet_names
        st.session_state['df_registry'] = pd.read_excel(xls, "Master Registry") if "Master Registry" in sheets else pd.DataFrame()
        st.session_state['df_open'] = pd.read_excel(xls, "Open Items") if "Open Items" in sheets else pd.DataFrame()
        st.session_state['df_summary'] = pd.read_excel(xls, "Summary") if "Summary" in sheets else pd.DataFrame()
        st.session_state['df_pending'] = pd.read_excel(xls, "Pending & Ordered") if "Pending & Ordered" in sheets else pd.DataFrame()
        st.session_state['data_initialized'] = True
    except Exception as e:
        st.error(f"Critical error unpacking spreadsheet tabs: {e}")

if 'data_initialized' not in st.session_state:
    if os.path.exists(EXCEL_FILE):
        load_excel_matrices(EXCEL_FILE)
    else:
        st.markdown("<div class='command-card'>", unsafe_allow_html=True)
        st.markdown("### 📁 Clinical Knowledge Base Initializer")
        st.write("Please upload your spreadsheet database file (`Master_Clinical_Registry_June_2026.xlsx`) to populate the cockpit panels:")
        uploaded_core = st.file_uploader("Upload Master Excel File Root:", type=["xlsx"])
        st.markdown("</div>", unsafe_allow_html=True)
        if uploaded_core:
            load_excel_matrices(uploaded_core)
            st.rerun()
        st.stop()

# Isolate internal data references
df_registry = st.session_state.get('df_registry', pd.DataFrame())
df_open = st.session_state.get('df_open', pd.DataFrame())
df_summary = st.session_state.get('df_summary', pd.DataFrame())
df_pending = st.session_state.get('df_pending', pd.DataFrame())

# --- STEP 2: RENDER SYSTEM NAVIGATION BACKBONE ---
tab_command, tab_analytics, tab_database, tab_intelligence = st.tabs([
    "🛸 Strategic Command Deck",
    "📈 Longitudinal Analytics",
    "📑 Core Data Registries",
    "🧠 Gemini Deep Chat Unit"
])

# ==================== NAVIGATION TAB 1: STRATEGIC COMMAND DECK ====================
with tab_command:
    col_profile, col_alerts = st.columns([2, 1])
    
    with col_profile:
        st.markdown("<div class='panel-header'>📋 Executive Patient Profile Summary</div>", unsafe_allow_html=True)
        st.markdown("<div class='command-card' style='min-height: 250px;'>", unsafe_allow_html=True)
        if not df_summary.empty:
            # Safely read cover rows and display them cleanly
            for idx, row in df_summary.dropna(subset=[df_summary.columns[0], df_summary.columns[1]], how='any').iterrows():
                lbl = str(row.iloc[0]).strip()
                val = str(row.iloc[1]).strip()
                if any(x in lbl.lower() for x in ["rows", "priority", "result", "question", "imaging"]):
                    st.markdown(f"<div style='margin-bottom:8px;'><strong style='color:#00F2FE;'>{lbl}:</strong> <span style='color:#E5E7EB;'>{val}</span></div>", unsafe_allow_html=True)
        else:
            st.info("Profile summary overview empty or format mismatched.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_alerts:
        st.markdown("<div class='panel-header' style='color:#EF4444;'>⚡ Priority Action Gaps</div>", unsafe_allow_html=True)
        st.markdown("<div class='command-card' style='min-height: 250px; overflow-y: auto;'>", unsafe_allow_html=True)
        if not df_open.empty and "Issue" in df_open.columns:
            for _, row in df_open.iterrows():
                st.markdown(f"<div style='padding: 6px 10px; background: rgba(239,68,68,0.08); border-left: 3px solid #EF4444; border-radius:4px; margin-bottom:8px; font-size:0.85rem;'>{row['Issue']}</div>", unsafe_allow_html=True)
        elif not df_open.empty:
            for _, row in df_open.iterrows():
                st.markdown(f"<div style='padding: 6px 10px; background: rgba(239,68,68,0.08); border-left: 3px solid #EF4444; border-radius:4px; margin-bottom:8px; font-size:0.85rem;'>{row.iloc[2]}</div>", unsafe_allow_html=True)
        else:
            st.write("No active priority gaps recorded.")
        st.markdown("</div>", unsafe_allow_html=True)

    # FIXED: Re-mapped directly to matching spreadsheet columns ('Flag / Status' and 'Clinical Context / Interpretation (careful)')
    st.markdown("<div class='panel-header'>🚨 Flagged Anomalies & Laboratory Exceptions</div>", unsafe_allow_html=True)
    if not df_registry.empty and "Flag / Status" in df_registry.columns:
        df_anomalies = df_registry[df_registry["Flag / Status"].str.contains("High|Low|Abnormal|Critical|Severe|Elevated|Missing", na=False, case=False)]
        
        if not df_anomalies.empty:
            anomaly_cols = st.columns(4)
            for idx, (_, row) in enumerate(df_anomalies.reset_index().iterrows()):
                target_col = anomaly_cols[idx % 4]
                unit_label = row['Unit'] if pd.notna(row['Unit']) else ''
                desc_label = row['Clinical Context / Interpretation (careful)'] if pd.notna(row['Clinical Context / Interpretation (careful)']) else ''
                
                with target_col:
                    st.markdown(f"""
                    <div class='command-card card-critical'>
                        <div class='metric-label'>{row['Marker / Clinical Event']}</div>
                        <div class='metric-val'>{row['Value']}<span class='metric-unit'> {unit_label}</span></div>
                        <div class='alert-badge badge-critical'>{row['Flag / Status']}</div>
                        <div class='metric-desc'>{desc_label}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("All lab parameters currently sit within verified standard references.")
    else:
        st.warning("Master Registry spreadsheet columns unreadable or mismatched.")

    # Row 3: Therapeutic Frameworks & Diagnostics
    st.markdown("<div class='panel-header'>💊 Strategies & Screenings</div>", unsafe_allow_html=True)
    col_tx, col_pd = st.columns(2)
    with col_tx:
        st.markdown("<div class='command-card' style='min-height:220px;'>", unsafe_allow_html=True)
        st.write("🏋️‍♂️ **Active Treatment / Exercise Tracking Loops**")
        st.markdown("""
        - **Parenteral Repletion Regimen:** Bypassing underlying eosinophilic gastric mucosal absorption blocks.
        - **Targeted Methylation Acceleration Support:** Lowering high systemic neurotoxic Homocysteine volumes.
        - **Sacroiliac Joint Decompression Stretching:** Daily mobility target sequences structured to unburden the lower *Castellvi IIIA* segment mechanics.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_pd:
        st.markdown("<div class='command-card' style='min-height:220px;'>", unsafe_allow_html=True)
        st.write("🔬 **Pending / Ordered Specialized Screenings (Dr. Domingues)**")
        if not df_pending.empty:
            st.dataframe(df_pending, use_container_width=True, hide_index=True)
        else:
            st.write("No specialized screening items currently pending or processing.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== NAVIGATION TAB 2: LONGITUDINAL ANALYTICS ====================
with tab_analytics:
    st.markdown("### 📈 Cross-Filter Graphical Analytics Engine")
    if not df_registry.empty and "Marker / Clinical Event" in df_registry.columns:
        all_unique_markers = df_registry["Marker / Clinical Event"].dropna().unique().tolist()
        critical_markers = df_registry[df_registry["Flag / Status"].str.contains("High|Low|Abnormal|Critical|Severe|Elevated", na=False, case=False)]["Marker / Clinical Event"].tolist()
        
        filter_choices = st.multiselect(
            "Select parameters to display on the analytics field:",
            options=all_unique_markers, default=critical_markers[:6] if critical_markers else all_unique_markers[:5]
        )
        
        if filter_choices:
            df_slice = df_registry[df_registry["Marker / Clinical Event"].isin(filter_choices)].copy()
            df_slice_numeric = df_slice[pd.to_numeric(df_slice["Value"], errors='coerce').notnull()].copy()
            df_slice_numeric["NumericValue"] = df_slice_numeric["Value"].astype(float)
            
            if not df_slice_numeric.empty:
                fig = px.bar(
                    df_slice_numeric, x="NumericValue", y="Marker / Clinical Event", orientation='h',
                    color="Marker / Clinical Event",
                    color_discrete_sequence=["#00F2FE", "#3B82F6", "#EF4444", "#F59E0B", "#10B981"],
                    template="plotly_dark"
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False, height=360, font=dict(family="Plus Jakarta Sans", color="#F3F4F6")
                )
                fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title_text="Measurement Level Scale")
                fig.update_yaxes(showgrid=False, title_text="")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selected values contain historical qualitative markers. Choose numeric data fields to compute graphs.")
                
            st.dataframe(df_slice, use_container_width=True, hide_index=True)
    else:
        st.write("Ecosystem laboratory columns unavailable.")

# ==================== NAVIGATION TAB 3: CORE DATA REGISTRIES ====================
with tab_database:
    st.markdown("### Live Database Core Editor")
    if not df_registry.empty:
        edited_df = st.data_editor(df_registry, use_container_width=True, num_rows="dynamic", key="editor_widget_stable")
        if st.button("⚡ Save Spreadsheet Updates & Sync Engine"):
            st.session_state['df_registry'] = edited_df
            if "gemini_chat" in st.session_state:
                del st.session_state.gemini_chat
            st.toast("Ecosystem parameters synchronized successfully!", icon="⚡")
            st.rerun()

# ==================== NAVIGATION TAB 4: GEMINI DEEP CHAT UNIT ====================
with tab_intelligence:
    st.markdown("### 🧠 Grounded Conversational Medical Intelligence Workspace")
    if not GEMINI_API_KEY:
        st.warning("⚠️ Enter your Google Gemini API Key in your application deployment deployment secrets to engage chat services.")
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        if "gemini_chat" not in st.session_state:
            st.session_state.chat_history = []
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                st.session_state.gemini_chat = model.start_chat(history=[])
                
                txt_registry = df_registry.to_string(index=False) if not df_registry.empty else ""
                txt_summary = df_summary.to_string(index=False) if not df_summary.empty else ""
                txt_open = df_open.to_string(index=False) if not df_open.empty else ""
                
                system_primer = (
                    "MASTER SYSTEMIC CASE CONTEXT PROTOCOL INJECTION:\n\n"
                    "You are accessing a high-fidelity clinical repository control center. "
                    "Below are the verified metrics parsed directly from the user's active spreadsheet registry:\n\n"
                    f"--- SHEET: PATIENT OVERVIEW PROFILE ---\n{txt_summary}\n\n"
                    f"--- SHEET: ACTIVE LAB METRIC TRACKS ---\n{txt_registry}\n\n"
                    f"--- SHEET: WORKSPACE OPEN TASKS ---\n{txt_open}\n\n"
                    "DIAGNOSTIC PATHOLOGY ROADMAP:\n"
                    "- Patient exhibits a dual-track timeline: an indolent, pre-malignant 3.2% CD3+CD4+CD7- T-helper lymphocyte clone (L-HES signature) causing chronic tissue degranulation (ECP 48.4) and severe mucosal B12 malabsorption, intersecting with a seronegative Axial Spondyloarthritis (axSpA) track manifesting active bone edema and vertical L4 corner enthesitis. Structural lesions locate directly around a congenital lumbosacral Castellvi IIIA transitional fault.\n"
                    "- Onset was anchored via historical chronic Fasciola hepatica parasite stress (cleared in 2014) which selected for the legacy clone, while eradication triggered an explosive Th17 inflammatory rebound line along spinal mechanics.\n"
                    "- An early youth terminal lymphoma blast crisis in a first cousin (age 18-20) confirms a 12.5% shared genetic vulnerability cluster requiring long-term hematological tracking vigilance.\n\n"
                    "STRICT GROUNDING RULE: Treat the provided data frame tables as absolute, unalterable facts. If any query contradicts these files or numbers, refuse to validate it. Do not invent metrics."
                )
                st.session_state.gemini_chat.send_message(system_primer)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "🧬 **Strategic Medical Engine Initialized.** I have successfully digested all active tables from your data core sheets, established cross-system parameters, and locked your clinical timelines under strict grounding constraints. How can I assist your cross-disciplinary analysis loops today?"
                })
            except Exception as e:
                st.error(f"AI interface communication fault: {e}")

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_query := st.chat_input("Query the clinical matrix:"):
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
                        st.error(f"Session buffer conflict. Reset or refresh. Details: {e}")
