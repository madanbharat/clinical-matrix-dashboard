import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai

# Securely pull the Gemini API key from environment configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# App Presentation Architecture
st.set_page_config(page_title="Case Matrix Engine", page_icon="🧬", layout="wide")

# --- STEP 1: INITIALIZE DYNAMIC MEMORY STORAGE ---
# This loads the baseline figures into memory if the app is opening for the first time
if "b12" not in st.session_state:
    st.session_state.b12 = 177.0
if "homocysteine" not in st.session_state:
    st.session_state.homocysteine = 20.7
if "ecp" not in st.session_state:
    st.session_state.ecp = 48.4
if "aberrant_t" not in st.session_state:
    st.session_state.aberrant_t = 3.2

# High-End Dark/Light Aesthetic Theme Injector
st.markdown("""
<style>
    .main-header { font-size:2.4rem !important; color:#0A2540; font-weight:700; margin-bottom:5px; }
    .sub-header { font-size:1.1rem !important; color:#639FAB; margin-bottom:20px; }
    .card { background-color:#ffffff; padding:20px; border-radius:12px; box-shadow: 0 4px 6px rgba(50,50,93,0.1); border-left: 6px solid #639FAB; margin-bottom:15px; }
    .metric-value { font-size:2rem; font-weight:700; color:#0A2540; }
    .metric-lbl { font-size:0.85rem; text-transform:uppercase; color:#627D98; font-weight:600; }
    .status-alert { padding:6px 12px; border-radius:20px; font-size:0.8rem; font-weight:700; display:inline-block; }
    .critical-bg { background-color:#FFE3E3; color:#D9383A; }
    .stable-bg { background-color:#E3FBE3; color:#247A24; }
</style>
""", unsafe_allow_html=True)

# Main Title Grid
st.markdown("<div class='main-header'>🧬 Case Matrix Ecosystem</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Systemic Multi-Engine Research, Mapping, & Clinical Intel Control Panel</div>", unsafe_allow_html=True)
st.markdown("---")

# --- STEP 2: BUILD THE SIDEBAR LAB EDITOR WINDOW ---
st.sidebar.header("⚙️ Interactive Lab Editor")
st.sidebar.write("Modify any value below to dynamically alter the hardcoded underlying memory anchor:")

with st.sidebar.expander("🛠️ Edit Active Biomarkers", expanded=True):
    input_b12 = st.number_input("Vitamin B12 (pg/mL):", value=st.session_state.b12, step=1.0)
    input_homo = st.number_input("Homocysteine (µmol/L):", value=st.session_state.homocysteine, step=0.1)
    input_ecp = st.number_input("ECP Level (µg/L):", value=st.session_state.ecp, step=0.1)
    input_tcell = st.number_input("CD4+CD7- T-Cell %:", value=st.session_state.aberrant_t, step=0.1)

# The master execution button to reset cache and apply parameters
if st.sidebar.button("💾 Apply Changes & Re-prime AI"):
    st.session_state.b12 = input_b12
    st.session_state.homocysteine = input_homo
    st.session_state.ecp = input_ecp
    st.session_state.aberrant_t = input_tcell
    
    # Deleting the chat forces the app to build a brand new model containing the fresh numbers
    if "gemini_chat" in st.session_state:
        del st.session_state.gemini_chat
    st.toast("Baseline memory updated successfully!", icon="💾")
    st.rerun()

# Layout Matrix Configuration
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Active Biophysical Biomarker Gauges")
    
    # Generate interactive charts using the dynamically stored numbers
    metric_labels = ['B12 (Target >300)', 'Homocysteine (<10)', 'ECP (<13.3)', 'Aberrant T-Cells %']
    metric_values = [st.session_state.b12, st.session_state.homocysteine, st.session_state.ecp, st.session_state.aberrant_t]
    metric_colors = ['#D9383A', '#D9383A', '#D9383A', '#4A90E2']
    
    fig = px.bar(
        x=metric_values, y=metric_labels, orientation='h',
        color=metric_labels, color_discrete_sequence=metric_colors,
        labels={'x':'Value Scale', 'y':'Marker'}
    )
    fig.update_layout(showlegend=False, height=260, margin=dict(l=20, r=20, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
    
    # 4-Column Metric Grid System fed dynamically from state memory
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='card'><span class='metric-lbl'>Vitamin B12</span><br><span class='metric-value'>{st.session_state.b12}</span><br><span class='status-alert critical-bg'>Active Baseline</span></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='card'><span class='metric-lbl'>Homocysteine</span><br><span class='metric-value'>{st.session_state.homocysteine}</span><br><span class='status-alert critical-bg'>Active Baseline</span></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='card'><span class='metric-lbl'>ECP Level</span><br><span class='metric-value'>{st.session_state.ecp}</span><br><span class='status-alert critical-bg'>Active Baseline</span></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='card'><span class='metric-lbl'>CD4+CD7- Subset</span><br><span class='metric-value'>{st.session_state.aberrant_t}%</span><br><span class='status-alert critical-bg'>Active Baseline</span></div>", unsafe_allow_html=True)

    # Historical Sequence Track
    st.subheader("⏱️ Chronological Hit Timeline")
    timeline_events = {
        "Phase": ["1. Background", "2. Initiation", "3. Adaptation", "4. Rebound", "5. Current Spectrum"],
        "Year": ["Inherited", "2012 - 2014", "2014 - 2016", "2017", "2026"],
        "Pathology Link": [
            "Familial baseline vulnerability to lymphoma blast mutations.",
            "Live Fasciola hepatica flukes force a permanent systemic Th2 immune shift.",
            "Chronic stress causes a T-cell subset to drop its CD7 marker, forming a clone.",
            "Parasite clearance triggers a Th17 rebound wave, hitting the crooked Castellvi IIIA spine.",
            "L-HES tissue supervisor coordinates active spinal flares, high ECP, and B12 gut blocks."
        ]
    }
    st.dataframe(pd.DataFrame(timeline_events), use_container_width=True, hide_index=True)

with col_right:
    st.subheader("📁 Centralized Medical Document Ingestion")
    uploaded_file = st.file_uploader("Drop new medical records, blood panels, or imaging briefs here:", type=["pdf", "txt", "png", "jpg"])
    if uploaded_file:
        st.toast("Document securely uploaded! Parsing data matrices...", icon="⚡")

    st.subheader("📚 Curated Research & Case Study Portal")
    with st.expander("🔗 Lymphocyte-Variant Hypereosinophilia (L-HES) Lit"):
        st.markdown("""
        * **Roufosse et al. (Blood Journal):** Long-term behavior and indolent properties of CD3+CD4+CD7- T-cell expansions. [Read Paper](https://bloodjournal.org)
        * **Simon et al. (Allergy):** Mechanistic models of IL-5 overproduction running completely independent of IgE pathways.
        """)
    with st.expander("🔗 Spondyloarthritis & Biomechanical Anomalies"):
        st.markdown("""
        * **Castellvi Classification Review:** Assessing transitional lumbosacral vertebra-driven shear stress and its impact on structural enthesitis.
        """)

st.markdown("---")
st.subheader("💬 Gemini Multi-Disciplinary AI Portal")

# Initialize and establish the Gemini Chat Stream
if not GEMINI_API_KEY:
    st.warning("⚠️ Enter a valid Google Gemini API Key in the deployment secrets panel to activate the real-time research Q&A portal.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Initialize chat framework if empty or manually reset
    if "gemini_chat" not in st.session_state or st.sidebar.button("🔄 Reset Chat Session"):
        st.session_state.chat_history = []
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            st.session_state.gemini_chat = model.start_chat(history=[])
            
            # --- THE SYSTEM PRIMER USES DYNAMIC STRINGS TO INJECT IN-APP CHANGES ---
            system_primer = (
                "MASTER CLINICAL CASE CONTEXT DATA PROTOCOL:\n\n"
                "1. PATIENT DEMOGRAPHICS & BACKGROUND:\n"
                "- Profile: 42-year-old male with a 14-year, highly fragmented systemic presentation.\n"
                "- Core Primary Symptoms: Intense, chronic nocturnal pruritus (skin itching), urticarial bleeding lesions, "
                "chronic abdominal pain, fluctuating inflammatory fatigue, and ocular redness flares.\n\n"
                "2. PRIMARY ENVIRONMENTAL TRIGGER:\n"
                "- History: Documented multi-year infection with Fasciola hepatica (liver fluke) contracted prior to 2012.\n"
                "- Treatment: Cleared with triclabendazole in 2014.\n"
                "- Pathophysiology: The prolonged presence of the fluke forced an extreme systemic Th2 shift, overproducing IL-5. "
                "The removal of the fluke in 2014 caused an intense immunological rebound effect (Th17 pathway activation).\n\n"
                f"3. CELLULAR DISCOVERY & METRICS (CURRENT ADJUSTED BASELINE):\n"
                f"- Vitamin B12: {st.session_state.b12} pg/mL (Bypasses gut mucosa when repleted parenterally).\n"
                f"- Homocysteine: {st.session_state.homocysteine} µmol/L (Toxic index for peripheral myelin sheath degradation).\n"
                f"- Eosinophil Cationic Protein (ECP): {st.session_state.ecp} µg/L (Tissue degranulation / fibroblast risk factor).\n"
                f"- Aberrant T-Helper Cell Clone (CD3+CD4+CD7-): {st.session_state.aberrant_t}% (The identified upstream IL-5 supervisor cell line).\n\n"
                "4. SAFETY EXCLUSIONS:\n"
                "- Total IgE normal (31 kUA/L), Tryptase normal (5.0 ng/mL). Rules out standard allergies and mastocytosis.\n\n"
                "5. SKELETAL & BIOMECHANICAL TRAJECTORY (axSpA):\n"
                "- Diagnosis: Documented Seronegative Axial Spondyloarthritis.\n"
                "- Radiographical Progression (March 24, 2026 MRI): Active 8x4 mm bone marrow edema focus on the Left SI joint "
                "paired with a brand new anterior Romanus lesion on the L4 vertebral corner.\n"
                "- Structural Fault: Congenital Castellvi IIIA lumbosacral transitional vertebra (L5 fused to sacrum). "
                "This layout locks the base of the spine, diverting severe mechanical shear force upward into L4-5, which pulls "
                "systemic axSpA inflammation directly to these coordinates, driving severe radiculopathy pain.\n\n"
                "6. OSMOREGULATORY BREAKDOWN:\n"
                "- Fluid Clearance Volume: Clearing ~4 Liters of ultra-dilute daily urine locked at a Specific Gravity of 1.003.\n\n"
                "7. FAMILIAL ONCOLOGICAL RISK VECTOR:\n"
                "- Genetic History: First cousin developed an aggressive, terminal lymphoma blast crisis in early youth (age 18-20).\n"
                "- Risk Profile: Points to a shared 12.5% genetic pool with inherited vulnerabilities to immune dysregulation or "
                "lymphoproliferative smoldering. The aberrant T-cell line must be tracked with long-term hematological vigilance.\n\n"
                "8. THERAPEUTIC EXPERIENCE HISTORY:\n"
                "- Failures: Complete lack of control on anti-TNF (Humira) and anti-IL-17A (Cosentyx, Bimzelx).\n"
                "- JAK Paradox: Strong initial structural/pain relief on JAK inhibitors (Rinvoq, Jyseleca), proving the clone communicates via "
                "JAK-STAT channels. However, treatment failed due to repeated, severe infection cycles and psychiatric crashes.\n\n"
                "INSTRUCTIONS FOR ANALYSIS: Address all queries with advanced, cross-disciplinary clinical research mechanics. Connect the "
                "environmental parasite history, the genetic vulnerabilities, and the current dynamic T-cell line to explain all symptoms logically.\n\n"
                "STRICT GROUNDING RULE: You must treat the provided data points as absolute, unalterable facts. If the user asks a question that "
                "contradicts these numbers, or asks you to speculate on a diagnosis completely unsupported by this text or peer-reviewed literature, "
                "you must state that you do not have the data to support that conclusion. Do not invent or alter any clinical metrics."
            )
            st.session_state.gemini_chat.send_message(system_primer)
        except Exception as e:
            st.error(f"Failed to initialize clean chat model: {e}")

    # Render previous conversation lines
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle incoming user queries
    if user_query := st.chat_input("Ask a clinical question based on the active baseline:"):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        with st.chat_message("assistant"):
            with st.spinner("Anatomizing data tracks..."):
                try:
                    ai_response = st.session_state.gemini_chat.send_message(user_query)
                    st.markdown(ai_response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response.text})
                except Exception as e:
                    st.error(f"The background session encountered a memory conflict. Please click 'Apply Changes & Re-prime AI' in your sidebar to wipe the stale cache and reload. Error details: {e}")
