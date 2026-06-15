import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai

# Securely pull the Gemini API key from environment configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# App Presentation Architecture
st.set_page_config(page_title="Case Matrix Engine", page_icon="🧬", layout="wide")

# --- STEP 1: INITIALIZE DREARY ALL AVAILABLE CASE DATA POINTS ---
# Storing the entire lab ecosystem in state memory for live editing
metrics_data = {
    "Vitamin B12 (pg/mL)": {"val": 177.0, "status": "Low / Critical", "type": "Abnormal"},
    "Homocysteine (µmol/L)": {"val": 20.7, "status": "High Risk", "type": "Abnormal"},
    "ECP Level (µg/L)": {"val": 48.4, "status": "Severe Degranulation", "type": "Abnormal"},
    "CD4+CD7- T-Cell %": {"val": 3.2, "status": "Clonal Suspect", "type": "Abnormal"},
    "CD4/CD8 Ratio": {"val": 1.14, "status": "Low / Abnormal", "type": "Abnormal"},
    "Urine Specific Gravity": {"val": 1.003, "status": "Hypotonic Dilute", "type": "Abnormal"},
    "24h Urine Volume (L)": {"val": 4.0, "status": "Polyuria Flux", "type": "Abnormal"},
    "LDL Cholesterol (mg/dL)": {"val": 169.0, "status": "Elevated Atherogenic", "type": "Abnormal"},
    "ESR (mm/h)": {"val": 25.0, "status": "Inflammatory Acceleration", "type": "Abnormal"},
    "CPK Muscle Enzyme (U/L)": {"val": 381.0, "status": "Myofascial Strain", "type": "Abnormal"},
    "CRP (mg/L)": {"val": 2.37, "status": "Normal Range", "type": "Normal"},
    "Total IgE (kUA/L)": {"val": 31.0, "status": "Normal (Non-Allergic)", "type": "Normal"},
    "Tryptase (ng/mL)": {"val": 5.0, "status": "Normal (Non-Mastocytosis)", "type": "Normal"},
    "Leucocytes (WBC Pool G/l)": {"val": 7.16, "status": "Normal Baseline Pool", "type": "Normal"},
    "Absolute Lymphocytes (G/l)": {"val": 1.905, "status": "Normal Homeostasis", "type": "Normal"},
    "Absolute Blood Eosinophils (G/l)": {"val": 0.62, "status": "Borderline Baseline", "type": "Normal"}
}

for key, info in metrics_data.items():
    state_key = key.replace(" ", "_").lower().split("(")[0].strip("_")
    if state_key not in st.session_state:
        st.session_state[state_key] = info["val"]

# High-End Dark/Light Aesthetic Theme Injector
st.markdown("""
<style>
    .main-header { font-size:2.4rem !important; color:#0A2540; font-weight:700; margin-bottom:5px; }
    .sub-header { font-size:1.1rem !important; color:#639FAB; margin-bottom:20px; }
    .card { background-color:#ffffff; padding:18px; border-radius:12px; box-shadow: 0 4px 6px rgba(50,50,93,0.1); border-left: 6px solid #639FAB; margin-bottom:15px; min-height: 140px; }
    .metric-value { font-size:1.8rem; font-weight:700; color:#0A2540; margin-top:5px; margin-bottom:2px; }
    .metric-lbl { font-size:0.8rem; text-transform:uppercase; color:#627D98; font-weight:600; display:block; min-height:35px; }
    .status-alert { padding:4px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; display:inline-block; }
    .critical-bg { background-color:#FFE3E3; color:#D9383A; }
    .stable-bg { background-color:#E3FBE3; color:#247A24; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🧬 Case Matrix Ecosystem</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Systemic Multi-Engine Research, Mapping, & Clinical Intel Control Panel</div>", unsafe_allow_html=True)
st.markdown("---")

# --- STEP 2: SIDEBAR LAB REGISTRY EDITOR ---
st.sidebar.header("⚙️ Comprehensive Lab Registry")
st.sidebar.write("Update hardcoded parameters inside the baseline system:")

with st.sidebar.expander("🛠️ Edit Data Repository Fields", expanded=False):
    edit_b12 = st.number_input("Vitamin B12:", value=st.session_state.vitamin_b12, step=1.0)
    edit_homo = st.number_input("Homocysteine:", value=st.session_state.homocysteine, step=0.1)
    edit_ecp = st.number_input("ECP Level:", value=st.session_state.ecp_level, step=0.1)
    edit_tcell = st.number_input("CD4+CD7- T-Cell %:", value=st.session_state.cd4+cd7-_t-cell, step=0.1)
    edit_ratio = st.number_input("CD4/CD8 Ratio:", value=st.session_state.cd4/cd8_ratio, step=0.01)
    edit_sg = st.number_input("Urine Specific Gravity:", value=st.session_state.urine_specific_gravity, format="%.3f", step=0.001)
    edit_uvol = st.number_input("24h Urine Volume:", value=st.session_state.24h_urine_volume, step=0.1)
    edit_ldl = st.number_input("LDL Cholesterol:", value=st.session_state.ldl_cholesterol, step=1.0)
    edit_esr = st.number_input("ESR Rate:", value=st.session_state.esr, step=1.0)
    edit_cpk = st.number_input("CPK Muscle Enzyme:", value=st.session_state.cpk_muscle_enzyme, step=1.0)
    edit_crp = st.number_input("CRP Rate:", value=st.session_state.crp, step=0.1)
    edit_ige = st.number_input("Total IgE:", value=st.session_state.total_ige, step=1.0)
    edit_tryp = st.number_input("Tryptase:", value=st.session_state.tryptase, step=0.1)

if st.sidebar.button("💾 Apply Changes & Re-prime AI"):
    st.session_state.vitamin_b12 = edit_b12
    st.session_state.homocysteine = edit_homo
    st.session_state.ecp_level = edit_ecp
    st.session_state.cd4+cd7-_t-cell = edit_tcell
    st.session_state.cd4/cd8_ratio = edit_ratio
    st.session_state.urine_specific_gravity = edit_sg
    st.session_state.24h_urine_volume = edit_uvol
    st.session_state.ldl_cholesterol = edit_ldl
    st.session_state.esr = edit_esr
    st.session_state.cpk_muscle_enzyme = edit_cpk
    st.session_state.crp = edit_crp
    st.session_state.total_ige = edit_ige
    st.session_state.tryptase = edit_tryp
    if "gemini_chat" in st.session_state:
        del st.session_state.gemini_chat
    st.toast("System master memory updated!", icon="💾")
    st.rerun()

# --- STEP 3: MASTER FILTER MANAGEMENT WORKSPACE ---
st.subheader("🔍 Filter & Select Target Matrix Indicators")
all_available_labels = list(metrics_data.keys())
default_abnormal_labels = [k for k, v in metrics_data.items() if v["type"] == "Abnormal"]

selected_display_metrics = st.multiselect(
    "Choose specific indicators to analyze on the charts (Defaults to flagged abnormal markers):",
    options=all_available_labels,
    default=default_abnormal_labels
)

# Render Graphics and Metric Cards dynamically based on user filters
if not selected_display_metrics:
    st.info("💡 Select at least one marker from the menu above to compute visual data streams.")
else:
    # Build Map
    chart_mapping = {
        "Vitamin B12 (pg/mL)": st.session_state.vitamin_b12,
        "Homocysteine (µmol/L)": st.session_state.homocysteine,
        "ECP Level (µg/L)": st.session_state.ecp_level,
        "CD4+CD7- T-Cell %": st.session_state.cd4+cd7-_t-cell,
        "CD4/CD8 Ratio": st.session_state.cd4/cd8_ratio,
        "Urine Specific Gravity": st.session_state.urine_specific_gravity,
        "24h Urine Volume (L)": st.session_state.24h_urine_volume,
        "LDL Cholesterol (mg/dL)": st.session_state.ldl_cholesterol,
        "ESR (mm/h)": st.session_state.esr,
        "CPK Muscle Enzyme (U/L)": st.session_state.cpk_muscle_enzyme,
        "CRP (mg/L)": st.session_state.crp,
        "Total IgE (kUA/L)": st.session_state.total_ige,
        "Tryptase (ng/mL)": st.session_state.tryptase,
        "Leucocytes (WBC Pool G/l)": st.session_state.leucocytes,
        "Absolute Lymphocytes (G/l)": st.session_state.absolute_lymphocytes,
        "Absolute Blood Eosinophils (G/l)": st.session_state.absolute_blood_eosinophils
    }
    
    filtered_values = [chart_mapping[m] for m in selected_display_metrics]
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        fig = px.bar(
            x=filtered_values, y=selected_display_metrics, orientation='h',
            labels={'x': 'Value Index', 'y': 'Selected Indicators'},
            color=selected_display_metrics, color_discrete_sequence=px.colors.qualitative.Slate
        )
        fig.update_layout(showlegend=False, height=300, margin=dict(l=20, r=20, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        
        # Render clean grid cards dynamically for selected items
        card_columns = st.columns(min(len(selected_display_metrics), 4))
        for idx, name in enumerate(selected_display_metrics):
            col_target = card_columns[idx % 4]
            val_current = chart_mapping[name]
            is_abnormal = metrics_data[name]["type"] == "Abnormal"
            bg_style = "critical-bg" if is_abnormal else "stable-bg"
            lbl_style = "Flagged Anomaly" if is_abnormal else "Normal/Baseline"
            
            with col_target:
                st.markdown(f"""
                <div class='card'>
                    <span class='metric-lbl'>{name}</span>
                    <span class='metric-value'>{val_current}</span>
                    <span class='status-alert {bg_style}'>{lbl_style}</span>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        st.subheader("⏱️ Chronological Hit Timeline")
        timeline_events = {
            "Phase": ["1. Background", "2. Initiation", "3. Adaptation", "4. Rebound", "5. Current Status"],
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

st.markdown("---")
st.markdown("<div id='chat-section'></div>", unsafe_allow_html=True)
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
            
            # THE COMPLETE CLINICAL KNOWLEDGE ENGINE INJECTION BLOCK
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
                "3. CELLULAR DISCOVERY & METRICS (CURRENT ADJUSTED SYSTEM STATE):\n"
                f"- Vitamin B12: {st.session_state.vitamin_b12} pg/mL\n"
                f"- Homocysteine: {st.session_state.homocysteine} µmol/L\n"
                f"- Eosinophil Cationic Protein (ECP): {st.session_state.ecp_level} µg/L\n"
                f"- Aberrant T-Helper Cell Clone (CD3+CD4+CD7-): {st.session_state.cd4+cd7-_t-cell}%\n"
                f"- CD4/CD8 Ratio: {st.session_state.cd4/cd8_ratio}\n"
                f"- Urine Specific Gravity: {st.session_state.urine_specific_gravity}\n"
                f"- 24h Urine Volume: {st.session_state.24h_urine_volume} L\n"
                f"- LDL Cholesterol: {st.session_state.ldl_cholesterol} mg/dL\n"
                f"- ESR Rate: {st.session_state.esr} mm/h\n"
                f"- CPK Muscle Enzyme: {st.session_state.cpk_muscle_enzyme} U/L\n"
                f"- CRP Level: {st.session_state.crp} mg/L\n"
                f"- Total IgE: {st.session_state.total_ige} kUA/L\n"
                f"- Tryptase: {st.session_state.tryptase} ng/mL\n"
                f"- Leucocytes (WBC): {st.session_state.leucocytes} G/l\n"
                f"- Absolute Lymphocytes: {st.session_state.absolute_lymphocytes} G/l\n"
                f"- Absolute Blood Eosinophils: {st.session_state.absolute_blood_eosinophils} G/l\n\n"
                "4. SAFETY EXCLUSIONS:\n"
                "- Total IgE and Tryptase remain perfectly normal. Rules out standard allergies and mastocytosis.\n\n"
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
            
            # FIX FOR EYE-LINE CONFUSION: Automatically populate an initial response greeting
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": "👋 **Welcome to the Secure Case Matrix Engine.** I have fully aligned all available clinical data points, genetic histories, parasitic context records, and custom lab filters. The workspace is active and primed under strict grounding constraints. How can I assist you with cross-system data correlation or risk assessment analysis today?"
            })
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
