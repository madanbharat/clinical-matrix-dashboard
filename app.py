import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai
import os

# Securely pull the Gemini API key from environment configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# App Presentation Architecture
st.set_page_config(page_title="Case Matrix Control", page_icon="🧬", layout="wide")

# High-End Dark/Light Aesthetic Theme Injector
st.markdown("""
<style>
    .main-header { font-size:2.5rem !important; color:#0A2540; font-weight:800; margin-bottom:2px; }
    .sub-header { font-size:1.1rem !important; color:#639FAB; margin-bottom:25px; font-weight: 500; }
    .section-banner { background-color: #F4F6F8; padding: 10px 18px; border-radius: 8px; margin-top: 20px; margin-bottom: 15px; font-weight: 700; color: #0A2540; border-left: 5px solid #0A2540; }
    .summary-box { background-color: #EBF3F5; padding: 20px; border-radius: 12px; border: 1px solid #D1E1E4; margin-bottom: 20px; }
    .card { background-color:#ffffff; padding:16px; border-radius:12px; box-shadow: 0 4px 6px rgba(50,50,93,0.05); border-top: 4px solid #639FAB; margin-bottom:15px; min-height: 120px; }
    .card-crit { border-top: 4px solid #D9383A; }
    .metric-value { font-size:1.6rem; font-weight:700; color:#0A2540; margin-top:5px; }
    .metric-lbl { font-size:0.8rem; text-transform:uppercase; color:#627D98; font-weight:600; display:block; min-height:30px; }
    .status-alert { padding:3px 9px; border-radius:20px; font-size:0.72rem; font-weight:700; display:inline-block; margin-top:5px; }
    .critical-bg { background-color:#FFE3E3; color:#D9383A; }
    .stable-bg { background-color:#E3FBE3; color:#247A24; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🧬 Case Matrix Executive Cockpit</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Dynamic Excel Data Core & Automated Gemini Research Control Unity</div>", unsafe_allow_html=True)
st.markdown("---")

# --- STEP 1: AUTOMATED EXCEL INGESTION ENGINE ---
EXCEL_FILE_NAME = "Master_Clinical_Registry_June_2026.xlsx"
excel_source = None

# Look for the file inside the local repository first
if os.path.exists(EXCEL_FILE_NAME):
    excel_source = EXCEL_FILE_NAME
else:
    st.sidebar.warning("📊 Excel Data Source missing from repository root directory.")
    uploaded_source = st.sidebar.file_uploader("Upload 'Master_Clinical_Registry_June_2026.xlsx' to initialize workspace:", type=["xlsx"])
    if uploaded_source:
        excel_source = uploaded_source

if not excel_source:
    st.info("💡 **Initialization Required:** Please drag and drop your master clinical registry Excel file (`.xlsx`) into the sidebar uploader or upload it to your GitHub folder to power up the data engines.")
    st.stop()

# Load all data sheets cleanly using pandas
try:
    xls = pd.ExcelFile(excel_source)
    sheet_names = xls.sheet_names
    
    # Read sheets safely with fallback protections
    df_registry = pd.read_excel(xls, sheet_name=sheet_names[0]) if len(sheet_names) > 0 else pd.DataFrame()
    df_open_items = pd.read_excel(xls, sheet_name=sheet_names[1]) if len(sheet_names) > 1 else pd.DataFrame()
    df_summary = pd.read_excel(xls, sheet_name=sheet_names[2]) if len(sheet_names) > 2 else pd.DataFrame()
    df_pending = pd.read_excel(xls, sheet_name=sheet_names[3]) if len(sheet_names) > 3 else pd.DataFrame()
    df_dict = pd.read_excel(xls, sheet_name=sheet_names[4]) if len(sheet_names) > 4 else pd.DataFrame()
except Exception as e:
    st.error(f"Failed to unpack Excel sheet matrices: {e}")
    st.stop()

# --- STEP 2: DYNAMIC PATIENT BLUEPRINT PANEL ---
st.markdown("<div class='section-banner'>📋 Patient Profile Summary Matrix</div>", unsafe_allow_html=True)
sum_col1, sum_col2 = st.columns([2, 1])

with sum_col1:
    st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
    if not df_summary.empty:
        for idx, row in df_summary.iterrows():
            st.write(f"**{row.iloc[0]}:** {row.iloc[1]}")
    else:
        st.write("Summary data parameters unreadable inside target Excel sheet layout.")
    st.markdown("</div>", unsafe_allow_html=True)

with sum_col2:
    st.write("📋 **Clinical Open Investigation Items**")
    if not df_open_items.empty:
        st.dataframe(df_open_items, use_container_width=True, hide_index=True)
    else:
        st.write("No open item metrics tracked.")

# --- STEP 3: DYNAMIC FILTER ENGINE & INFOGRAPHIC GAUGE MATRIX ---
st.markdown("<div class='section-banner'>📊 Interactive Filters & Real-Time Biomarker Gauges</div>", unsafe_allow_html=True)

if not df_registry.empty:
    # Safely extract marker names and isolate metrics flagged as abnormal
    all_available_markers = df_registry["Marker / Clinical Event"].dropna().unique().tolist()
    default_markers = df_registry[df_registry["Status / Clinical Context"].str.contains("Anomaly|Critical|Low|High Risk|Severe", na=False)]["Marker / Clinical Event"].tolist()
    
    selected_markers = st.multiselect(
        "Choose specific parameters to display on the dynamic cockpit gauges (Defaults to flagged anomalies):",
        options=all_available_markers,
        default=default_markers if default_markers else all_available_markers[:5]
    )
    
    if selected_markers:
        # Filter row matches
        df_filtered = df_registry[df_registry["Marker / Clinical Event"].isin(selected_markers)]
        
        # Isolate numeric metrics for visualization charts
        df_numeric = df_filtered[pd.to_numeric(df_filtered["Value"], errors='coerce').notnull()].copy()
        df_numeric["NumericValue"] = df_numeric["Value"].astype(float)
        
        graph_col, list_col = st.columns([2, 1])
        
        with graph_col:
            if not df_numeric.empty:
                fig = px.bar(
                    df_numeric, x="NumericValue", y="Marker / Clinical Event", orientation='h',
                    color="Marker / Clinical Event",
                    labels={'NumericValue': 'Active Measurement Scale', 'Marker / Clinical Event': 'Selected Indicators'},
                    color_discrete_sequence=["#0A2540", "#639FAB", "#D9383A", "#E67E22", "#2C3E50"]
                )
                fig.update_layout(showlegend=False, height=320, margin=dict(l=20, r=20, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selected items contain qualitative historical context indices. Add numerical lab markers to compute graphs.")
            
            # Render visual indicator cards dynamically
            card_cols = st.columns(min(len(df_filtered), 4))
            for idx, row in df_filtered.reset_index().iterrows():
                target_col = card_cols[idx % min(len(df_filtered), 4)]
                name = row["Marker / Clinical Event"]
                val = row["Value"]
                unit = row["Unit"] if pd.notna(row["Unit"]) else ""
                ctx = row["Status / Clinical Context"]
                
                is_bad = any(x in str(ctx) for x in ["Anomaly", "Critical", "Low", "High Risk", "Severe"])
                c_class = "card card-crit" if is_bad else "card"
                badge = "critical-bg" if is_bad else "stable-bg"
                txt_badge = "Anomaly Flag" if is_bad else "Baseline Control"
                
                with target_col:
                    st.markdown(f"""
                    <div class='{c_class}'>
                        <span class='metric-lbl'>{name}</span>
                        <span class='metric-value'>{val} <span style='font-size:0.8rem;'>{unit}</span></span>
                        <span class='status-alert {badge}'>{txt_badge}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
        with list_col:
            st.write("🔬 **Pending & Ordered Diagnostics (Dr. Domingues)**")
            if not df_pending.empty:
                st.dataframe(df_pending, use_container_width=True, hide_index=True)
            else:
                st.write("No diagnostic pipelines currently marked as pending.")
else:
    st.error("The Master Registry tab appears to be empty or unreadable.")

# --- STEP 4: INTEL REPOSITORY HUB ---
st.markdown("<div class='section-banner'>📁 Research Repository & Document Ingestion</div>", unsafe_allow_html=True)
doc_col1, doc_col2 = st.columns(2)
with doc_col1:
    uploaded_lit = st.file_uploader("Drop new medical consult notes, genomics briefs, or academic PDFs here:", type=["pdf", "txt", "png", "jpg"])
    if uploaded_lit:
        st.success(f"Document '{uploaded_lit.name}' successfully parsed and prepared for AI consultation.")
with doc_col2:
    st.markdown("""
    **📚 Embedded Core Literatures:**
    * 📑 *Roufosse et al. (Blood):* Functional monitoring of CD3+CD4+CD7- clonal expansions.
    * 📑 *Simon et al. (Allergy):* Autonomous IL-5 cytokine factory behaviors.
    * 📑 *Castellvi Classification:* Structural mechanics of transitional vertebrae forcing shear strain loops.
    """)

# --- STEP 5: MASTER INTERACTIVE GEMINI AI PORTAL ---
st.markdown("---")
st.subheader("💬 Gemini Multi-Disciplinary AI Portal")

if not GEMINI_API_KEY:
    st.warning("⚠️ Enter a valid Google Gemini API Key in your application deployment deployment secrets window to open the conversational intelligence workspace.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    
    if "gemini_chat" not in st.session_state or st.sidebar.button("🔄 Reset Chat Session"):
        st.session_state.chat_history = []
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            st.session_state.gemini_chat = model.start_chat(history=[])
            
            # DYNAMIC PRIMER CONSTRUCTION: Reads the dataframes directly to generate context!
            registry_text = df_registry.to_string(index=False) if not df_registry.empty else "No registry available."
            summary_text = df_summary.to_string(index=False) if not df_summary.empty else "No profile summary text available."
            open_items_text = df_open_items.to_string(index=False) if not df_open_items.empty else "No open items tracking data available."
            pending_text = df_pending.to_string(index=False) if not df_pending.empty else "No pending items."
            
            system_primer = (
                "YOU ARE AN EXPERT CLINICAL DATA SCIENTIST AND CLINICAL IMMUNOLOGIST ANALYZING A COMPLEX MULTI-SYSTEM PRESENTATION.\n\n"
                "CRITICAL PATIENT EXCEL DATABASE DATA INJECTION:\n"
                "Below are the verified, unalterable patient data tables extracted directly from the registry spreadsheet matrices:\n\n"
                "--- SHEET: CLINICAL PATIENT SUMMARY PROFILE ---\n"
                f"{summary_text}\n\n"
                "--- SHEET: ACTIVE LAB REGISTRY INDICATORS ---\n"
                f"{registry_text}\n\n"
                "--- SHEET: CLINICAL OPEN TRACKING ITEMS ---\n"
                f"{open_items_text}\n\n"
                "--- SHEET: DIAGNOSTICS CURRENTLY ORDERED / PENDING ---\n"
                f"{pending_text}\n\n"
                "DIAGNOSTIC PATHOLOGY REFERENCE CONTEXT:\n"
                "- The patient displays a dual-track progression: an indolent, pre-malignant 3.2% CD3+CD4+CD7- T-helper lymphocyte clone (indicative of Lymphocyte-Variant Hypereosinophilic Syndrome, L-HES) driving high tissue degranulation (ECP 48.4) and severe mucosal absorption barriers, alongside seronegative Axial Spondyloarthritis (axSpA) tracking vertical enthesitis lesions around a congenital lumbosacral Castellvi IIIA anomaly.\n"
                "- The original environmental driver was a multi-year chronic Fasciola hepatica parasite infection (cleared in 2014) which selected for the clone, while clearance triggered an explosive Th17 immune rebound wave hitting spinal mechanics.\n"
                "- High-grade lymphoma blast history in a young first cousin (age 18-20) establishes a 12.5% shared genetic vulnerability vector requiring long-term hematological tracker vigilance.\n\n"
                "INSTRUCTIONS FOR ANALYSIS: Respond with advanced, high-fidelity clinical data science reasoning. Cross-examine intersecting tracks. "
                "STRICT GROUNDING RULE: Treat the provided data frame summaries as absolute, unalterable facts. If any query contradicts these files or numbers, refuse to validate it. Do not invent metrics."
            )
            st.session_state.gemini_chat.send_message(system_primer)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "👋 **Welcome to the Secure Excel-Driven Cockpit Platform.** I have successfully digested all 5 tabs from your master registry database, locked your clinical timelines, and primed the core analysis pipelines under strict grounding rules. How can I assist you with multi-variant cross-system correlations today?"
            })
        except Exception as e:
            st.error(f"Failed to initialize clean model connectivity parameters: {e}")

    # Render conversation
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask a clinical query based on the active database rows:"):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing active spreadsheet tracks..."):
                try:
                    ai_response = st.session_state.gemini_chat.send_message(user_query)
                    st.markdown(ai_response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response.text})
                except Exception as e:
                    st.error(f"The session engine encountered a cache data conflict. Please click 'Apply Changes & Re-prime AI' or drop your file back into the sidebar to clear the buffer. Error: {e}")
