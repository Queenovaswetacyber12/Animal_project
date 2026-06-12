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

# Professional Mobile-First App Injection Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;900&display=swap');
    
    /* Global Base Engine Resets */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* Web App / APK Viewport Optimization Wrapper */
    .block-container {
        background: #ffffff;
        max-width: 1160px !important;
        padding: 2rem 2.5rem !important;
        margin-top: 1.5rem;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
    }
    
    /* Premium Sidebar UI Overhaul (Fixes Screenshot (23).jpg UI) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #064e3b 0%, #0f766e 100%) !important;
        box-shadow: 4px 0 25px rgba(0, 0, 0, 0.15);
    }
    
    /* HIDE NATIVE STREAMLIT RADIO BUTTON CIRCLES AND FIX ALIGNMENT */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 12px 16px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin: 0 !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.25s ease-in-out !important;
        display: block !important;
    }
    
    /* Hide the radio circles globally inside the sidebar */
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"]::before {
        content: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label [width] {
        display: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] [data-checked="true"] {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
        transform: translateX(4px);
    }
    
    /* Hover adjustments for the navigation tabs */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        transform: translateX(2px);
    }
    
    /* Fix typography within hidden radio elements */
    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: #ffffff !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        line-height: 1.4 !important;
        word-wrap: break-word !important;
        white-space: normal !important;
    }

    /* Form & Input Fields - Premium Rounded Styling */
    div[data-baseweb="select"], .stNumberInput input, textarea {
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1a202c !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="select"]:focus-within, .stNumberInput input:focus, textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15) !important;
    }
    
    /* Interactive Component Styling */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.2) !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Clean Cards for App Features */
    .pro-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 5px solid #10b981;
        margin-bottom: 1rem;
    }
    
    /* APK / Mobile Viewport Responsive Overrides */
    @media (max-width: 768px) {
        body {
            background-color: #ffffff;
        }
        .block-container {
            margin-top: 0 !important;
            padding: 1.25rem !important;
            border-radius: 0 !important;
            box-shadow: none !important;
        }
        h1 { font-size: 1.75rem !important; }
        h2 { font-size: 1.35rem !important; }
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
    
    menu = st.radio(
        "Navigation Menu",
        [
            "🏠 হোম | Home",
            "📐 গার্থ ও লেন্থ মাপার নিয়ম",
            "📏 লাইভ ওয়েট ক্যালকুলেটর | Live Weight Calculator",
            "🐄 স্মার্ট পশুপালন | Smart Animal Husbandry",
            "🩺 রোগ সম্পর্কিত তথ্য | Disease Info",
            "🔍 লক্ষণ দেখে রোগ শনাক্ত | Symptom Checker",
            "🥬 খাদ্য পরামর্শ | Feeding Tips",
            "💉 টিকা নির্দেশিকা | Vaccination Guide",
            "🤖 AI পশু চিকিৎসা সহায়ক",
            "ℹ️ অ্যাপ সম্পর্কে | About App"
        ],
        label_visibility="collapsed"
    )

# =========================================
# MODULE 1: INTERACTIVE HOME DASHBOARD
# =========================================

if menu == "🏠 হোম | Home":
    st.markdown("<h1 style='color: #0f172a; font-weight:800;'>Livestock AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Calculate live weight, estimate valuations, and check health diagnostics via AI pipelines.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1500595046743-cd271d694d30", caption="Dairy Livestock Management", use_container_width=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1524024973431-2ad916746881", caption="Caprine Livestock Management", use_container_width=True)

    st.markdown("<br>### System Diagnostics Capabilities", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**📱 Target Ready Architecture**\n\nOptimized WebView scaling engine for fast mobile application wrappers.")
    with c2:
        st.success("**⚖️ Precision Calculation Engine**\n\nAutomated math conversion tables matching field metrics.")
    with c3:
        st.warning("**🤖 Core Diagnostic Engine**\n\nDirect low-latency inference pathways linking OpenRouter AI layers.")

# =========================================
# MODULE 2: GRAPHICAL MEASUREMENT SCHEMES
# =========================================

elif menu == "📐 গার্থ ও লেন্থ মাপার নিয়ম":
    st.title("📐 Heart Girth & Length Measurement Protocols")
    
    st.markdown("""
    <div class='pro-card'>
        <h4>📌 Standard Measurement Protocol Instruction</h4>
        <p><b>Heart Girth:</b> Measure the chest circumference just behind the front forelegs.</p>
        <p><b>Body Length:</b> Measure in a straight linear projection from the point of the shoulder down to the pin bone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📏 Reference Metric Range Matrices")
    st.table({
        "Animal Archetype": ["Goat / Sheep", "Swine / Pig", "Cattle / Cow", "Dairy Buffalo", "Equine / Horse"],
        "Optimal Girth Range (Inches)": ["20 - 40", "25 - 55", "45 - 90", "55 - 100", "50 - 85"],
        "Optimal Length Range (Inches)": ["18 - 35", "25 - 50", "40 - 80", "45 - 90", "45 - 75"]
    })

    st.success("💡 **Practical Metric Test Case**: Caprine Animal with 30\" Girth and 28\" Length parameters.")

# =========================================
# MODULE 3: WEIGHT CONVERSION ALGORITHMS
# =========================================

elif menu == "📏 লাইভ ওয়েট ক্যালকুলেটর | Live Weight Calculator":
    st.title("📏 Live Weight & Valuation Matrix")
    
    animal = st.selectbox("Select Target Animal Archetype", ["Cow", "Buffalo", "Horse", "Goat", "Pig"])
    
    col1, col2 = st.columns([1, 1])
    with col1:
        girth = st.number_input("Enter Heart Girth Size (Inches)", min_value=1.0, value=30.0, step=0.5)
    with col2:
        length = st.number_input("Enter Body Length Profile (Inches)", min_value=1.0, value=28.0, step=0.5)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Run Analytical Computation"):
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
        metric_col1.metric("Calculated Mass (KG)", f"{weight_kg:.2f} KG")
        
        if rate > 0:
            metric_col2.metric("Projected Market Valuation", f"₹{(weight_kg * rate):,.2f}")
            st.info(f"Target calculation mapped using local dynamic base rate of ₹{rate}/KG.")
        else:
            st.warning("Valuation computation completed. Pricing data requires manual localized checks.")

# =========================================
# MODULE 4: STRATEGIC MANAGEMENT
# =========================================

elif menu == "🐄 স্মার্ট পশুপালন | Smart Animal Husbandry":
    st.title("🐄 স্মার্ট পশুপালন | Smart Husbandry Strategy")
    
    st.markdown("""
    <div class='pro-card'>
        <h3>🏠 ১. আধুনিক খামার পরিকাঠামো</h3>
        <p>বায়ু চলাচল ব্যবস্থার আধুনিকায়ন নিশ্চিত করুন। জীবাণুনাশক প্রয়োগ চক্র নিয়মিত বজায় রাখুন।</p>
    </div>
    <div class='pro-card'>
        <h3>🌾 ২. বৈজ্ঞানিক খাদ্য পুষ্টি উপাদান</h3>
        <p>সবুজ ঘাস এবং দানাদার সুষম মিশ্রণ দিন। প্রতিটি পশুর শরীরের ওজনের সমতুল্য পরিচ্ছন্ন পানীয় জল সরবরাহ নিশ্চিত করুন।</p>
    </div>
    <div class='pro-card'>
        <h3>🩺 ৩. নিয়মিত বায়ো-সিকিউরিটি</h3>
        <p>পরজীবী দমন প্রোটোকল মেনে চলুন। যেকোনো সংক্রমণের ক্ষেত্রে কোয়ারেন্টাইন ব্যবস্থা গ্রহণ করুন।</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# MODULE 5: INFERENCE ENGINE - DISEASE KNOWLEDGE
# =========================================

elif menu == "🩺 রোগ সম্পর্কিত তথ্য | Disease Info":
    st.title("🩺 পশুর রোগ ব্যাধি সম্পর্কিত তথ্য ভাণ্ডার")
    
    search_disease = st.text_input("🔍 রোগের বৈজ্ঞানিক বা সাধারণ নাম লিখুন (যেমন: FMD, BQ)")
    
    if search_disease:
        with st.spinner("মেডিকেল নলেজ ডাটাবেস অনুসন্ধান করা হচ্ছে..."):
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
                            {"role": "system", "content": "You are a professional veterinary scientist expert system. Always answer in clear, elite standard Indian Bengali language."},
                            {"role": "user", "content": f"রোগের বিবরণ দাও: {search_disease}. ১. রোগের পরিচিতি ২. প্রধান কারণ ৩. দৃশ্যমান লক্ষণ ৪. প্রাথমিক চিকিৎসা ও প্রতিরোধ"}
                        ]
                    },
                    timeout=30
                )
                data = response.json()
                if "choices" in data:
                    st.markdown(f"<div class='pro-card'>{data['choices'][0]['message']['content']}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"রিমোট সার্ভার সংযোগ বিচ্ছিন্ন বা ত্রুটি ঘটেছে: {e}")

# =========================================
# MODULE 6: CLOUD AI DIAGNOSTICS DETECTOR
# =========================================

elif menu == "🔍 লক্ষণ দেখে রোগ শনাক্ত | Symptom Checker":
    st.title("🔍 লক্ষণ ভিত্তিক স্বয়ংক্রিয় এআই রোগ বিশ্লেষণ")
    
    selected_animal = st.selectbox("প্রাণীর প্রজাতি নির্বাচন করুন", ["Cow", "Goat", "Buffalo", "Sheep", "Pig"])
    symptoms = st.text_area("লক্ষণ বা অস্বাভাবিক আচরণ বিস্তারিত লিখুন", placeholder="উদা: মুখ দিয়ে লালা ঝড়ছে, তাপমাত্রা বেশি, খুঁড়িয়ে হাঁটছে...")
    
    if st.button("এআই ডায়াগনস্টিকস রান করুন"):
        if not symptoms.strip():
            st.warning("অনুগ্রহ করে লক্ষণ সমূহের বিবরণ দিন।")
        else:
            with st.spinner("লক্ষণ প্যাটার্ন প্রসেস করা হচ্ছে..."):
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
                        st.warning("⚠️ এটি শুধুমাত্র এআই ভিত্তিক প্রাথমিক ধারণা। চূড়ান্ত চিকিৎসার পূর্বে অবশ্যই রেজিস্টার্ড চিকিৎসকের পরামর্শ নিন।")
                except Exception as e:
                    st.error(f"সংযোগ ত্রুটি: {e}")

# =========================================
# MODULE 7: ANIMAL CALORIC / FEEDING MANUALS
# =========================================

elif menu == "🥬 খাদ্য পরামর্শ | Feeding Tips":
    st.title("🥬 বৈজ্ঞানিক পুষ্টি ও খাদ্য তালিকা ব্যবস্থাপনা")
    
    tab1, tab2, tab3 = st.tabs(["🐄 গবাদি পশু (Cattle)", "🐐 ছাগল ও ভেড়া", "🐔 পোল্ট্রি ও অন্যান্য"])
    
    with tab1:
        st.markdown("""
        ### গরুর দৈনিক পুষ্টির অনুপাত
        * **সবুজ কাঁচা ঘাস:** ১৫ - ২৫ কেজি (ওজন ভিত্তিক)
        * **শুকনো খড়:** ৩ - ৬ কেজি
        * **দানাদার সুষম খাদ্য মিশ্রণ:** প্রতি ৩ লিটার দুধ উৎপাদনের জন্য ১ কেজি অতিরিক্ত
        * **খনিজ লবণ মিশ্রণ:** ৫০ - ৬০ গ্রাম প্রতিদিন
        """)
    with tab2:
        st.markdown("""
        ### ছাগলের পুষ্টির নিয়মাবলী
        * **প্রধান খাদ্য:** গাছের পাতা, লতাগুল্ম এবং কাঁচা নরম ঘাস।
        * **দানাদার খাদ্য:** দৈনিক ২০০ থেকে ৫০০ গ্রাম পর্যাপ্ত পুষ্টির জন্য।
        * **বিশুদ্ধ জল:** সার্বক্ষণিক সহজলভ্য রাখতে হবে।
        """)
    with tab3:
        st.markdown("""
        ### পোল্ট্রি ফিড চার্ট
        * **স্টার্টার ফিড:** ০ - ৮ সপ্তাহ বয়সের বাচ্চার জন্য।
        * **গ্রোয়ার ফিড:** ৮ - ২০ সপ্তাহ বয়সের জন্য।
        * **লেয়ার ফিড:** ডিম উৎপাদনকারী মুরগির জন্য বিশেষ ক্যালসিয়াম সমৃদ্ধ খাদ্য।
        """)

# =========================================
# MODULE 8: VACCINE PROPHYLAXIS SCHEDULER
# =========================================

elif menu == "💉 টিকা নির্দেশিকা | Vaccination Guide":
    st.title("💉 প্রো-অ্যাক্টিভ ইমিউনাইজেশন ও ভ্যাকসিন নির্দেশিকা")
    
    v_animal = st.selectbox("ভ্যাকসিন শিডিউল দেখার জন্য প্রাণী বেছে নিন", ["Cow", "Goat", "Pig"])
    
    if v_animal == "Cow":
        st.table({
            "Target Pathogen / Disease": ["FMD (খুরারোগ)", "HS (গলাফুলা)", "BQ (বাদলা রোগ)", "Brucellosis"],
            "Vaccination Interval Period": ["প্রতি ৬ মাস অন্তর", "বছরে ১ বার (বর্ষার পূর্বে)", "বছরে ১ বার", "৪-৮ মাস বয়সের বকনা বাছুরকে"]
        })
    elif v_animal == "Goat":
        st.table({
            "Target Pathogen / Disease": ["PPR", "Goat Pox", "FMD"],
            "Vaccination Interval Period": ["বছরে ১ বার", "বছরে ১ বার", "প্রতি ৬ মাস অন্তর"]
        })
    else:
        st.table({
            "Target Pathogen / Disease": ["Classical Swine Fever", "Swine Erysipelas", "FMD"],
            "Vaccination Interval Period": ["বছরে ১ বার", "বছরে ১ বার", "প্রতি ৬ মাস অন্তর"]
        })

# =========================================
# MODULE 9: CONTEXT-AWARE AI CHAT BOT
# =========================================

elif menu == "🤖 AI পশু চিকিৎসা সহায়ক":
    st.title("🤖 রিয়েল-টাইম এআই ভেটেরিনারি চ্যাট অ্যাসিস্ট্যান্ট")
    
    if "vet_chat_messages" not in st.session_state:
        st.session_state.vet_chat_messages = []
        
    chat_animal = st.selectbox("কথোপকথনের জন্য প্রাণী সিলেক্ট করুন", ["Cow", "Goat", "Pig", "Buffalo", "Horse"])
    
    if st.button("ক্লিয়ার চ্যাট হিস্ট্রি (Reset)"):
        st.session_state.vet_chat_messages = []
        st.rerun()
        
    for msg in st.session_state.vet_chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    user_query = st.chat_input("আপনার পশুর যেকোনো সমস্যা বা প্রশ্ন এখানে লিখুন...")
    
    if user_query:
        st.session_state.vet_chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        with st.chat_message("assistant"):
            if not API_KEY:
                st.error("API Key missing.")
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
                            {"role": "system", "content": f"You are a helpful livestock assistant. If answering in Bengali, use formal Indian Bengali terms. Avoid using 'পানি', use 'জল'. Target Animal: {chat_animal}."},
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
                st.error(f"ব্যর্থতা ঘটেছে: {e}")

# =========================================
# MODULE 10: METADATA & VERSION CONTROL
# =========================================

elif menu == "ℹ️ অ্যাপ সম্পর্কে | About App":
    st.title("ℹ️ Enterprise Core Metadata Architecture")
    st.markdown("""
    <div class='pro-card'>
        <h3>Livestock AI Assistant - v2.2.0 (Premium UI Update)</h3>
        <p>This deployment introduces an modernized custom navigation engine optimized for both mobile web view wrappers and multi-device platforms.</p>
    </div>
    """, unsafe_allow_html=True)
