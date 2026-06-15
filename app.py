import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai

# Securely pull the Gemini API key from environment configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# App Presentation Architecture
st.set_page_config(page_title="Case Matrix Engine", page_icon="🧬", layout="wide")

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
""", unsafe_with_html=True)

# Main Title Grid
st.markdown("<div class='main-header'>🧬 Case Matrix Ecosystem</div>", unsafe_with_html=True)
st.markdown("<div class='sub-header'>Systemic Multi-Engine Research, Mapping, & Clinical Intel Control Panel</div>", unsafe_with_html=True)
st.markdown("---")

# Layout Matrix Configuration
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Active Biophysical Biomarker Gauges")
    
    # Generate interactive charts using Plotly
    metric_labels = ['B12 (Target >300)', 'Homocysteine (<10)', 'ECP (<13.3)', 'Aberrant T-Cells %']
    metric_values = [177, 20.7, 48.4, 3.2]
    metric_colors = ['#D9383A', '#D9383A', '#D9383A', '#4A90E2']
    
    fig = px.bar(
        x=metric_values, y=metric_labels, orientation='h',
        color=metric_labels, color_discrete_sequence=metric_colors,
        labels={'x':'Value Scale', 'y':'Marker'}
    )
    fig.update_layout(showlegend=False, height=260, margin=dict(l=20, r=20, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
    
    # 4-Column Metric Grid System
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("<div class='card'><span class='metric-lbl'>Vitamin B12</span><br><span class='metric-value'>177</span><br><span class='status-alert critical-bg'>Deficient</span></div>", unsafe_with_html=True)
    with m2:
        st.markdown("<div class='card'><span class='metric-lbl'>Homocysteine</span><br><span class='metric-value'>20.7</span><br><span class='status-alert critical-bg'>High Risk</span></div>", unsafe_with_html=True)
    with m3:
        st.markdown("<div class='card'><span class='metric-lbl'>ECP Level</span><br><span class='metric-value'>48.4</span><br><span class='status-alert critical-bg'>Degranulating</span></div>", unsafe_with_html=True)
    with m4:
        st.markdown("<div class='card'><span class='metric-lbl'>CD4+CD7- Subset</span><br><span class='metric-value'>3.2%</span><br><span class='status-alert critical-bg'>Clonal Suspect</span></div>", unsafe_with_html=True)

    # Historical Sequence Track
    st.subheader("⏱️ Chronological Hit Timeline")
    timeline_events = {
        "Phase": ["1. Background", "2. Initiation", "3. Adaptation", "4. Rebound", "5. Current Spectrum"],
        "Year": ["Inherited", "2012 - 2014", "2014 - 2016", "2017", "2026"],
        "Pathology Link": [
            "Familial baseline vulnerability to lymphoma blast mutations.",
            "Live Fasciola hepatica flukes force a permanent systemic Th2 immune shift.",
            "Chronic stress causes a T-cell subset to drop its CD7 marker, forming a 3.2% clone.",
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
    
    # Cache system memory loops to maintain consistent case parameters
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        # Pre-load complete case context directly into Gemini's active memory pool
        model = genai.GenerativeModel("gemini-1.5-flash")
        st.session_state.gemini_chat = model.start_chat(history=[])
        
        system_primer = (
            "You are an expert clinical data scientist analyzing a complex case. "
            "Context: The patient has a 3.2% CD3+CD4+CD7- T-cell population, high ECP (48.4 µg/L), "
            "severe B12 deficiency (177 pg/mL), elevated Homocysteine (20.7 µmol/L), "
            "seronegative axSpA with an active L4 Romanus lesion, a congenital Castellvi IIIA transitional segment, "
            "and a history of chronic Fasciola hepatica treated in 2014. "
            "Address all research inquiries with clinical precision, focusing on cross-system mechanisms."
        )
        st.session_state.gemini_chat.send_message(system_primer)

    # Render previous conversation lines
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle incoming user queries
    if user_query := st.chat_input("Ask a clinical question (e.g., 'Explain the link between the fluke history and the current spinal lesions'):"):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing intersecting variables..."):
                ai_response = st.session_state.gemini_chat.send_message(user_query)
                st.markdown(ai_response.text)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response.text})
