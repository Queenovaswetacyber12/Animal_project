import streamlit as st
import numpy as np
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load Environment Variables safely
load_dotenv(Path(__file__).with_name(".env"))

# ==========================================
# PAGE INITIALIZATION & PRO THEME SETUP
# =========================================

st.set_page_config(
    page_title="Livestock AI Assistant",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Mobile-First Custom CSS Injection 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;900&display=swap');
    
    /* Global Base UI Engine Resets */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* Main Content Container Optimization */
    .block-container {
        background: #ffffff;
        max-width: 1160px !important;
        padding: 2rem 2.5rem !important;
        margin-top: 1rem;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02);
    }
    
    /* Premium Sidebar UI Layout Configuration */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #064e3b 0%, #0f766e 100%) !important;
        box-shadow: 4px 0 25px rgba(0, 0, 0, 0.12);
    }
    
    /* Modern Navigation Button Styling Override */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px 0;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.04) !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin: 0 !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Clear native radio elements to create UI list item appearance */
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"]::before {
        content: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label [width] {
        display: none !important;
    }
    
    /* Active / Selected Tab State Indicator */
    [data-testid="stSidebar"] div[role="radiogroup"] [data-checked="true"] {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
        transform: scale(1.02);
    }
    
    /* Item Hover States */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.12) !important;
    }
    
    /* Navigation Text Settings */
    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: #ffffff !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        letter-spacing: 0.3px;
    }

    /* Enterprise Breadcrumb CSS Component Blueprint */
    .pro-breadcrumb {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #f1f5f9;
        padding: 10px 18px;
        border-radius: 10px;
        margin-bottom: 2rem;
        font-size: 14px;
        font-weight: 500;
        color: #64748b;
    }
    .pro-breadcrumb a {
        color: #10b981;
        text-decoration: none;
    }
    .pro-breadcrumb span.separator {
        color: #cbd5e1;
    }
    .pro-breadcrumb span.current {
        color: #334155;
        font-weight: 600;
    }
    
    /* Interactive Card Interface Wrapper */
    .pro-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 5px solid #10b981;
        margin-bottom: 1.25rem;
    }
    
    /* Buttons Custom Layout UI */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.15) !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.25) !important;
    }

    /* Input Field Theme Adjustments */
    div[data-baseweb="select"], .stNumberInput input, textarea {
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1a202c !important;
    }

    /* Adaptive Mobile Optimization Views */
    @media (max-width: 768px) {
        .block-container {
            margin-top: 0 !important;
            padding: 1rem !important;
            border-radius: 0 !important;
            box-shadow: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Secure Extraction of API Credentials
API_KEY = os.getenv("API_KEY", "").strip()

# =========================================
# APPLICATION NAVIGATION (SIDEBAR)
# =========================================

with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white; font-weight:700; margin-top:15px; margin-bottom: 25px;'>🐄 Livestock Pro</h2>", unsafe_allow_html=True)
    
    # Clean, English-Only Selection Node Array to avoid UI overlap issues
    menu = st.radio(
        "Navigation Menu",
        [
            "Home Dashboard",
            "Measurement Guide",
            "Live Weight Calculator",
            "Smart Husbandry Strategy",
            "Disease Information Database",
            "Symptom Checker Engine",
            "Nutritional Feeding Manuals",
            "Vaccination Matrix Protocol",
            "AI Veterinary Assistant Chat",
            "Application Infrastructure Info"
        ],
        label_visibility="collapsed"
    )

# =========================================
# HELPER METHOD: BREADCRUMB RENDERING ENGINE
# =========================================

def render_breadcrumb(current_node_title):
    st.markdown(f"""
    <div class="pro-breadcrumb">
        <a href="#">Livestock App Workspace</a>
        <span class="separator">/</span>
        <span class="current">{current_node_title}</span>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# MODULE 1: INTERACTIVE HOME DASHBOARD
# =========================================

if menu == "Home Dashboard":
    render_breadcrumb("Home Dashboard")
    st.markdown("<h1 style='color: #0f172a; font-weight:800; margin-top: -10px;'>Livestock AI Assistant Workspace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Calculate live weight matrices, monitor baseline structural parameters, and evaluate clinical symptoms through open reasoning networks.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1500595046743-cd271d694d30", caption="Dairy Livestock Management Node", use_container_width=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1524024973431-2ad916746881", caption="Caprine Livestock Management Node", use_container_width=True)

    st.markdown("<br>### System Architecture Matrix Tools", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**📱 Production Ready Build**\n\nResponsive layout adjustments for APK compilation wrappers and mobile viewports.")
    with c2:
        st.success("**⚖️ Dynamic Regression Formula**\n\nLive arithmetic calculators processing physical sizing data points instantly.")
    with c3:
        st.warning("**🤖 Reasoning AI Layer**\n\nCloud pipeline models interpreting symptomatic descriptions.")

# =========================================
# MODULE 2: MEASUREMENT PROTOCOLS
# =========================================

elif menu == "Measurement Guide":
    render_breadcrumb("Measurement Protocols")
    st.title("📐 Structural Measurement Configurations")
    
    st.markdown("""
    <div class='pro-card'>
        <h4>📌 Measurement Methodology Reference Guide</h4>
        <p><b>Heart Girth:</b> Measure the global circumference around the chest casing immediately behind the front forelegs.</p>
        <p><b>Body Length:</b> Measure the linear spacing stretching directly from the tip of the shoulder to the rear pin bone structure.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📏 Standard Structural Matrix Ranges")
    st.table({
        "Animal Archetype": ["Goat / Sheep", "Swine / Pig", "Cattle / Cow", "Dairy Buffalo", "Equine / Horse"],
        "Optimal Girth Range (Inches)": ["20 - 40", "25 - 55", "45 - 90", "55 - 100", "50 - 85"],
        "Optimal Length Range (Inches)": ["18 - 35", "25 - 50", "40 - 80", "45 - 90", "45 - 75"]
    })

# =========================================
# MODULE 3: WEIGHT CONVERSION ALGORITHMS
# =========================================

elif menu == "Live Weight Calculator":
    render_breadcrumb("Live Weight Calculator")
    st.title("📏 Automated Biomass Computational Engine")
    
    animal = st.selectbox("Select Target Animal Archetype", ["Cow", "Buffalo", "Horse", "Goat", "Pig"])
    
    col1, col2 = st.columns(2)
    with col1:
        girth = st.number_input("Input Heart Girth Metric (Inches)", min_value=1.0, value=30.0, step=0.5)
    with col2:
        length = st.number_input("Input Body Length Metric (Inches)", min_value=1.0, value=28.0, step=0.5)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Execute Computational Analysis"):
        if animal == "Goat":
            base_lbs = (girth * girth * length) / 630
            weight_kg = base_lbs * 0.453592 * 2  
            rate = 450 if weight_kg < 20 else (500 if weight_kg < 40 else (550 if weight_kg < 60 else 600))
        elif animal == "Pig":
            base_lbs = (girth * girth * length) / 800
            weight_kg = base_lbs * 0.453592
            rate = 180 if weight_kg < 40 else (220 if weight_kg < 80 else 280)
        else:
            base_lbs = (girth * girth * length) / 660
            weight_kg = base_lbs * 0.453592
            rate = 0 
            
        st.markdown("### 📊 Computation Calculations Results")
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("Calculated Mass Value (KG)", f"{weight_kg:.2f} KG")
        
        if rate > 0:
            metric_col2.metric("Projected Financial Valuation", f"₹{(weight_kg * rate):,.2f}")
            st.info(f"Target calculation mapped using local dynamic base rate of ₹{rate}/KG.")
        else:
            st.warning("Valuation complete. Market parameters for this asset category require localized manual updates.")

# =========================================
# MODULE 4: HUSBANDRY STRATEGY (BENGALI CORE WORKLIST)
# =========================================

elif menu == "Smart Husbandry Strategy":
    render_breadcrumb("Smart Husbandry Strategy")
    st.title("🐄 স্মার্ট পশুপালন | Optimization Parameters")
    
    st.markdown("""
    <div class='pro-card'>
        <h3>🏠 ১. খামার পরিকাঠামো ও পরিচ্ছন্নতা</h3>
        <p>বায়ু চলাচল ব্যবস্থার আধুনিকায়ন নিশ্চিত করুন। জীবাণুনাশক প্রয়োগ চক্র নিয়মিত বজায় রাখুন।</p>
    </div>
    <div class='pro-card'>
        <h3>🌾 ২. বৈজ্ঞানিক খাদ্য পুষ্টি উপাদান</h3>
        <p>সবুজ ঘাস এবং দানাদার সুষম মিশ্রণ দিন। প্রতিটি পশুর শরীরের ওজনের সমতুল্য পরিচ্ছন্ন পানীয় জল সরবরাহ নিশ্চিত করুন।</p>
    </div>
    <div class='pro-card'>
        <h3>🩺 ৩. বায়ো-সিকিউরিটি প্রোটোকল</h3>
        <p>পরজীবী দমন প্রোটোকল মেনে চলুন। সংক্রমণ পরিলক্ষিত হলে দ্রুত কোয়ারেন্টাইন ব্যবস্থা গ্রহণ করুন।</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# MODULE 5: INFERENCE ENGINE - DISEASE KNOWLEDGE
# =========================================

elif menu == "Disease Information Database":
    render_breadcrumb("Disease Database Lookup")
    st.title("🩺 Clinical Pathology Information Repository")
    
    search_disease = st.text_input("🔍 Search Nomenclature Input Vector (e.g., FMD, BQ, Anthrax)")
    
    if search_disease:
        with st.spinner("Querying Remote Medical Datastores..."):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                        "messages": [
                            {"role": "system", "content": "You are a professional veterinary scientist expert system. Always answer in clear, elite standard Indian Bengali language using appropriate medical terminology."},
                            {"role": "user", "content": f"রোগের বিবরণ দাও: {search_disease}. শিরোনাম: ১. রোগের পরিচিতি ২. প্রধান কারণ ৩. দৃশ্যমান লক্ষণ ৪. প্রাথমিক চিকিৎসা ও প্রতিরোধ"}
                        ]
                    },
                    timeout=30
                )
                data = response.json()
                if "choices" in data:
                    st.markdown(f"<div class='pro-card'>{data['choices'][0]['message']['content']}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Inference Connection Timeout Error: {e}")

# =========================================
# MODULE 6: CLOUD AI DIAGNOSTICS DETECTOR
# =========================================

elif menu == "Symptom Checker Engine":
    render_breadcrumb("Symptom Analysis Matrix")
    st.title("🔍 Automated AI Diagnostics Inference Engine")
    
    selected_animal = st.selectbox("Select Target Patient Family Profile", ["Cow", "Goat", "Buffalo", "Sheep", "Pig"])
    symptoms = st.text_area("Detailed Diagnostic Symptom Inputs", placeholder="Enter observations: high temperature, foot lesions, salivation changes...")
    
    if st.button("Initialize Clinical Analysis Sequence"):
        if not symptoms.strip():
            st.warning("Input processing failed. Symptom log strings cannot be empty.")
        else:
            with st.spinner("Processing Symptom Feature Arrays..."):
                try:
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                            "messages": [
                                {"role": "system", "content": "You are a top-tier veterinary AI assistant. Use easy farmer-friendly Indian Bengali language. Do not use the word 'পানি', use 'জল' or 'পানীয় জল'."},
                                {"role": "user", "content": f"Animal Type: {selected_animal}. Symptoms: {symptoms}."}
                            ]
                        }
                    )
                    res_data = response.json()
                    if "choices" in res_data:
                        st.write(res_data['choices'][0]['message']['content'])
                        st.markdown("---")
                        st.warning("⚠️ **Notice Requirement:** This automated classification is an initial baseline suggestion only. Consult field professionals prior to therapeutic drug deployment.")
                except Exception as e:
                    st.error(f"Transmission Path Failure: {e}")

# =========================================
# MODULE 7: ANIMAL CALORIC / FEEDING MANUALS
# =========================================

elif menu == "Nutritional Feeding Manuals":
    render_breadcrumb("Nutritional Schedules")
    st.title("🥬 Caloric Calculation & Feeding Requirements")
    
    tab1, tab2, tab3 = st.tabs(["🐄 Cattle Profiles", "🐐 Caprine / Small Ruminants", "🐔 Avian / Poultry Systems"])
    
    with tab1:
        st.markdown("""
        ### Core Daily Rations Configuration
        * **Green Biomass Grass Range:** 15 - 25 KG adjusted against global body mass index.
        * **Dry Cellulose Fodder / Hay:** 3 - 6 KG.
        * **Balanced Dry Concentrates:** Add 1 KG for every 3 Liters of volumetric milk yield output.
        * **Trace Mineral Elements:** 50 - 60 Grams continuously.
        """)
    with tab2:
        st.markdown("""
        ### Caprine Diet Structures
        * **Principal Intake Vectors:** Tree foliage varieties, shrubbery browses, tender green ground flora.
        * **Concentrate Additives:** 200 - 500 Grams daily for gestational or conditioning support cycles.
        * **Hydration Elements:** Continuous provision of clean, non-contaminated drinking water.
        """)
    with tab3:
        st.markdown("""
        ### Structured Poultry Feeding Protocols
        * **Starter Feed Rations:** Target developmental phase spanning Weeks 0 - 8.
        * **Grower Feed Rations:** Target maintenance phase spanning Weeks 8 - 20.
        * **Layer Feed Rations:** Optimal calcium enrichment structures engineered for production phases.
        """)

# =========================================
# MODULE 8: VACCINE PROPHYLAXIS SCHEDULER
# =========================================

elif menu == "Vaccination Matrix Protocol":
    render_breadcrumb("Vaccination Schedules")
    st.title("💉 Immunization Timelines & Prophylaxis Registers")
    
    v_animal = st.selectbox("Select Animal For Schedule View", ["Cow", "Goat", "Pig"])
    
    if v_animal == "Cow":
        st.table({
            "Target Pathogen Target": ["FMD (Foot and Mouth Disease)", "HS (Haemorrhagic Septicaemia)", "BQ (Black Quarter)", "Brucellosis Profile"],
            "Recommended Execution Cadence": ["Every 6 months recurrent cycle", "Once per annum (Pre-monsoon phases)", "Once per annum cycle", "Female heifers within 4-8 month age windows"]
        })
    elif v_animal == "Goat":
        st.table({
            "Target Pathogen Target": ["PPR Disease Control", "Goat Pox Virus", "FMD Prophylaxis"],
            "Recommended Execution Cadence": ["Once per annum interval", "Once per annum interval", "Every 6 months recurrent cycle"]
        })
    else:
        st.table({
            "Target Pathogen Target": ["Classical Swine Fever Variant", "Swine Erysipelas Organisms", "FMD Prophylaxis"],
            "Recommended Execution Cadence": ["Once per annum baseline interval", "Once per annum baseline interval", "Every 6 months recurrent cycle"]
        })

# =========================================
# MODULE 9: CONTEXT-AWARE AI CHAT BOT
# =========================================

elif menu == "AI Veterinary Assistant Chat":
    render_breadcrumb("AI Assistant Space")
    st.title("🤖 Chat Workspace: Conversational Logic Engine")
    
    if "vet_chat_messages" not in st.session_state:
        st.session_state.vet_chat_messages = []
        
    chat_animal = st.selectbox("Context Isolation Target Profile", ["Cow", "Goat", "Pig", "Buffalo", "Horse"])
    
    if st.button("Reset Dynamic Context Frame"):
        st.session_state.vet_chat_messages = []
        st.rerun()
        
    for msg in st.session_state.vet_chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    user_query = st.chat_input("Input problem scenario descriptions here...")
    
    if user_query:
        st.session_state.vet_chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        with st.chat_message("assistant"):
            if not API_KEY:
                st.error("Infrastructure Error: Remote token key undefined.")
                st.stop()
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                        "messages": [
                            {"role": "system", "content": f"You are a helpful livestock assistant. If answering in Bengali, use formal Indian Bengali terms. Avoid using 'পানি', use 'জল'. Target Profile: {chat_animal}."},
                            *st.session_state.vet_chat_messages[-5:]
                        ],
                        "temperature": 0.3
                    }
                )
                res_json = response.json()
                reply_txt = res_json["choices"][0]["message"]["content"]
                st.markdown(reply_txt)
                st.session_state.vet_chat_messages.append({"role": "assistant", "content": reply_txt})
            except Exception as e:
                st.error(f"Inference Pipeline Error: {e}")

# =========================================
# MODULE 10: METADATA & VERSION CONTROL
# =========================================

elif menu == "Application Infrastructure Info":
    render_breadcrumb("Application Specifications")
    st.title("ℹ️ Application Environment Parameters")
    st.markdown("""
    <div class='pro-card'>
        <h3>Livestock App Workspace Engine — v2.5.0 (Enterprise Architecture)</h3>
        <p><b>Visual Interface Layout:</b> Optimized Responsive Custom List Wrapper Injection System avoiding overlapping node parameters.</p>
        <p><b>Target Form Factor Architecture:</b> Engineered to process across standardized browser matrix profiles and native Cordova/Capacitor runtime wrapper contexts.</p>
    </div>
    """, unsafe_allow_html=True)
