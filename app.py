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

# High-Tech Micro-Cockpit Visual Theme Injector
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    /* Core Layout Foundations */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #040814 !important;
        color: #F3F4F6 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Header Console elements */
    .cockpit-title { font-size: 2.3rem; font-weight: 800; color: #FFFFFF; letter-spacing: -1px; margin-bottom: 2px; }
    .cockpit-subtitle { font-size: 0.85rem; color: #00F2FE; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 25px; }
    .panel-header { font-size: 1rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase; letter-spacing: 1px; margin-top: 15px; margin-bottom: 15px; }
    
    /* Compact Instruments Matrix Cards */
    .command-card {
        background: linear-gradient(135deg, rgba(11, 20, 50, 0.7) 0%, rgba(18, 32, 77, 0.4) 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 12px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
    }
    .card-crit { border-top: 3px solid #FF3366 !important; background: linear-gradient(135deg, rgba(40, 12, 24, 0.7) 0%, rgba(11, 20, 50, 0.4) 100%); }
    .card-normal { border-top: 3px solid #00F2FE !important; }
    
    /* Condensed Typography Layout */
    .metric-label { font-size: 0.72rem; text-transform: uppercase; color: #9CA3AF; font-weight: 600; letter-spacing: 0.3px; line-height: 1.3; margin-bottom: 4px; }
    .metric-val { font-size: 1.55rem; font-weight: 700; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }
    .metric-unit { font-size: 0.75rem; color: #00F2FE; font-weight: 500; margin-left: 1px; }
    .metric-desc { font-size: 0.72rem; color: #9CA3AF; margin-top: 6px; padding-top: 6px; border-top: 1px solid rgba(255,255,255,0.05); line-height: 1.35; }
    
    /* Status Badges */
    .alert-badge { padding: 2px 8px; border-radius: 4px; font-size: 0.62rem; font-weight: 700; display: inline-block; margin-top: 6px; text-transform: uppercase; }
    .badge-critical { background-color: rgba(255, 51, 102, 0.12); color: #FF4D7D; border: 1px solid rgba(255, 51, 102, 0.25); }
    .badge-baseline { background-color: rgba(0, 242, 254, 0.1); color: #00F2FE; border: 1px solid rgba(0, 242, 254, 0.2); }
    
    /* Tabs Overhaul */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; background-color: #0B1432; padding: 4px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: #9CA3AF; font-weight: 600; border-radius: 6px; padding: 8px 18px; font-size: 0.85rem; }
    .stTabs [aria-selected="true"] { background-color: #00F2FE !important; color: #040814 !important; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# Console Branding Header
st.markdown("<div class='cockpit-title'>🎛️ Case Matrix Command Bridge</div>", unsafe_allow_html=True)
st.markdown("<div class='cockpit-subtitle'>Longitudinal Health Core & High-Fidelity Tactical Interface</div>", unsafe_allow_html=True)

# --- STEP 1: INITIALIZE STABLE EXCEL DATA INFLOW ---
EXCEL_FILE = "Master_Clinical_Registry_June_2026.xlsx"

def load_excel_matrices(source):
    try:
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

df_registry = st.session_state.get('df_registry', pd.DataFrame())
df_open = st.session_state.get('df_open', pd.DataFrame())
df_summary = st.session_state.get('df_summary', pd.DataFrame())
df_pending = st.session_state.get('df_pending', pd.DataFrame())

# --- STEP 2: RENDER BACKBONE COCKPIT NAVIGATION ---
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
        st.markdown("<div class='command-card' style='min-height: 210px;'>", unsafe_allow_html=True)
        if not df_summary.empty:
            for idx, row in df_summary.dropna(subset=[df_summary.columns[0], df_summary.columns[1]], how='any').iterrows():
                lbl = str(row.iloc[0]).strip()
                val = str(row.iloc[1]).strip()
                if any(x in lbl.lower() for x in ["rows", "priority", "result", "question", "imaging"]):
                    st.markdown(f"<div style='margin-bottom:6px; font-size:0.85rem;'><strong style='color:#00F2FE;'>{lbl}:</strong> <span style='color:#E5E7EB;'>{val}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_alerts:
        st.markdown("<div class='panel-header' style='color:#FF3366;'>⚡ Priority Action Gaps</div>", unsafe_allow_html=True)
        st.markdown("<div class='command-card' style='min-height: 210px; overflow-y: auto;'>", unsafe_allow_html=True)
        if not df_open.empty:
            col_target_issue = 'Issue' if 'Issue' in df_open.columns else df_open.columns[2]
            for _, row in df_open.iterrows():
                st.markdown(f"<div style='padding: 4px 8px; background: rgba(255,51,102,0.06); border-left: 3px solid #FF3366; border-radius:4px; margin-bottom:6px; font-size:0.8rem; color:#F3F4F6;'>{row[col_target_issue]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # RE-DESIGNED INSTRUMENT COMPACT GRID SYSTEM
    st.markdown("<div class='panel-header'>🚨 System Instrument Panel & Metric Gauges</div>", unsafe_allow_html=True)
    if not df_registry.empty and "Flag / Status" in df_registry.columns:
        
        # FIXED: Created columns OUTSIDE the loop to permanently eliminate empty rectangular gaps
        anomaly_cols = st.columns(4)
        
        for idx, (_, row) in enumerate(df_registry.dropna(subset=['Value']).reset_index().iterrows()):
            target_col = anomaly_cols[idx % 4]
            
            ctx_flag = str(row['Flag / Status']).strip()
            is_bad = any(x in ctx_flag.lower() for x in ["high", "low", "abnormal", "critical", "severe", "elevated", "missing", "anomaly"])
            
            card_style = "card-crit" if is_bad else "card-normal"
            badge_style = "badge-critical" if is_bad else "badge-baseline"
            
            unit = row['Unit'] if pd.notna(row['Unit']) else ''
            desc = str(row['Clinical Context / Interpretation (careful)']).strip() if pd.notna(row['Clinical Context / Interpretation (careful)']) else ''
            
            with target_col:
                st.markdown(f"""
                <div class='command-card {card_style}'>
                    <div class='metric-label'>{row['Marker / Clinical Event']}</div>
                    <div class='metric-val'>{row['Value']}<span class='metric-unit'> {unit}</span></div>
                    <div class='alert-badge {badge_style}'>{ctx_flag}</div>
                """, unsafe_allow_html=True)
                
                # FIXED: Description field renders conditionally to remove empty whitespace
                if desc and desc.lower() != 'nan' and desc != '':
                    st.markdown(f"<div class='metric-desc'>{desc}</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

    # Row 3: Therapeutic Frameworks & Diagnostics
    st.markdown("<div class='panel-header'>💊 Strategies & Screenings</div>", unsafe_allow_html=True)
    col_tx, col_pd = st.columns(2)
    with col_tx:
        st.markdown("<div class='command-card' style='min-height:180px;'>", unsafe_allow_html=True)
        st.write("🏋️‍♂️ **Active Treatment / Exercise Tracking Loops**")
        st.markdown("<div style='font-size:0.85rem; line-height:1.4;'>• <strong>Parenteral Repletion Regimen:</strong> Bypassing eosinophilic mucosal blocks.<br>• <strong>Methylation Support:</strong> Lowering high systemic neurotoxic Homocysteine volumes.<br>• <strong>Sacroiliac Joint Decompression:</strong> Targeted routines to unburden Castellvi IIIA segment mechanics.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_pd:
        st.markdown("<div class='command-card' style='min-height:180px;'>", unsafe_allow_html=True)
        st.write("🔬 **Pending / Ordered Specialized Screenings (Dr. Domingues)**")
        if not df_pending.empty:
            st.dataframe(df_pending, use_container_width=True, hide_index=True)
        else:
            st.write("No diagnostic tracking metrics currently pending.")
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
                    showlegend=False, height=340, font=dict(family="Plus Jakarta Sans", color="#F3F4F6")
                )
                st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_slice, use_container_width=True, hide_index=True)

# ==================== NAVIGATION TAB 3: CORE DATA REGISTRIES ====================
with tab_database:
    st.markdown("### Live Database Core Editor")
    if not df_registry.empty:
        edited_df = st.data_editor(df_registry, use_container_width=True, num_rows="dynamic", key="editor_widget_final_v2")
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
        st.warning("⚠️ Enter your Google Gemini API Key in your deployment secrets to engage chat services.")
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
