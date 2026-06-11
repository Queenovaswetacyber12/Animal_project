
import streamlit as st
import numpy as np
import requests
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

# ==========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Livestock AI Assistant",
    page_icon="🐄",
    layout="wide"
)
st.markdown("""
<style>

/* Sidebar radio text */
div[role="radiogroup"] label {
    font-size: 13px !important;
    line-height: 1.1 !important;
}

/* Sidebar title */
section[data-testid="stSidebar"] h1 {
    font-size: 32px !important;
}

/* Sidebar caption */
section[data-testid="stSidebar"] {
    padding-top: 10px !important;
}

</style>
""", unsafe_allow_html=True)
# =========================================
# COLORFUL MOBILE UI
# ==========================================
st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background: linear-gradient(
        135deg,
        #d4fc79,
        #96e6a1,
        #84fab0
    );
    font-family: 'Segoe UI', sans-serif;
}

/* MAIN CONTAINER */

.block-container {
    background: white;
    width: min(100%, 1180px);
    padding: clamp(14px, 3vw, 24px);
    border-radius: 25px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.12);
    color: #1f2937;
}

/* MAIN TEXT */

.block-container p,
.block-container li,
.block-container div,
.block-container label,
.block-container span {
    color: #1f2937 !important;
}

.block-container .stAlert p,
.block-container .stAlert div,
.block-container .stAlert span {
    color: #14532d !important;
}

/* TITLE */

h1 {
    color: #16a34a !important;
    text-align: center;
    font-size: clamp(28px, 5vw, 42px) !important;
    font-weight: 900 !important;
}

/* HEADINGS */

h2, h3 {
    color: #15803d !important;
    font-weight: 800 !important;
    overflow-wrap: anywhere;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #15803d,
        #22c55e
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* BUTTON */

.stButton button {

    width: min(100%, 220px);
    border: none;
    border-radius: 15px;
    padding: 12px;

    background: linear-gradient(
        90deg,
        #16a34a,
        #22c55e
    );

    color: white;
    font-size: 18px;
    font-weight: bold;
    min-height: 48px;
    white-space: normal;
}

.stButton button,
.stButton button * {
    color: white !important;
}

/* INPUT BOX */

.stNumberInput input,
textarea {

    border-radius: 12px !important;
    border: 2px solid #22c55e !important;
    padding: 10px !important;
    font-size: 17px !important;
    background: #ffffff !important;
    color: #111827 !important;
}

textarea::placeholder,
input::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}

/* SELECT BOX */

div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 2px solid #22c55e !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #111827 !important;
}

div[role="listbox"],
div[role="option"] {
    background: #ffffff !important;
    color: #111827 !important;
}

div[role="option"]:hover {
    background: #dcfce7 !important;
}

/* CHAT */

div[data-testid="stChatInput"] {
    width: min(100%, 1100px) !important;
    margin: 0 auto !important;
    padding: 10px !important;
}

div[data-testid="stChatInput"] textarea {
    min-height: 52px !important;
    color: #111827 !important;
    background: #ffffff !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}

div[data-testid="stChatMessage"] {
    overflow-wrap: anywhere;
}

img {
    max-width: 100%;
    height: auto;
}

/* MOBILE */

@media (max-width: 768px) {

    .stApp {
        background: #ffffff;
    }

    .block-container {
        padding: 12px;
        border-radius: 0;
        box-shadow: none;
        min-width: 0;
    }

    h1 {
        font-size: 28px !important;
        line-height: 1.15 !important;
    }

    h2, h3 {
        font-size: 22px !important;
        line-height: 1.2 !important;
    }

    .stButton button {
        width: 100%;
        font-size: 16px;
    }

    div[data-baseweb="select"] > div,
    .stNumberInput input,
    textarea {
        min-height: 48px !important;
        font-size: 16px !important;
    }

    div[data-testid="stChatInput"] {
        padding: 8px !important;
    }

    div[data-testid="stChatMessage"] {
        padding: 8px 0 !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================
# API KEY
# =========================================

API_KEY = os.getenv("API_KEY", "").strip()
# =========================================
# SIDEBAR MENU
# =========================================

st.sidebar.title("🐄 Livestock Menu")

menu = st.sidebar.radio(
"অপশন নির্বাচন করুন | Choose Option",

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
    ]
  )
# =========================================
# HOME PAGE
# =========================================

if menu == "🏠 হোম | Home":

    st.markdown(
        "<h1>🐄 Livestock AI Assistant</h1>",
        unsafe_allow_html=True
    )

    st.title("🐄 Smart Animal Husbandry App")
    

    st.write(
        "Calculate live weight, market price and get veterinary support."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            "https://images.unsplash.com/photo-1500595046743-cd271d694d30",
            caption="🐄 Cow",
            use_container_width=True
        )

    with col2:

        st.image(
            "https://images.unsplash.com/photo-1524024973431-2ad916746881",
            caption="🐐 Goat",
            use_container_width=True
        )

    st.success("✅ Mobile Friendly UI")

    st.success("✅ Goat & Pig Market Price")

    st.success("✅ Veterinary AI Assistant")

#==========================================
# HOW TO MEASURE GIRTH & LENGTH
# =========================================

elif menu == "📐 গার্থ ও লেন্থ মাপার নিয়ম":

    st.header("📐 How To Measure Heart Girth & length")

    st.info("""
    Heart Girth:
Measure the chest circumference just behind the front legs.

Body Length:
Measure from the point of the shoulder to the pin bone (rear end).

Use both measurements in the Live Weight Calculator.
    """)
    
    st.subheader("🐄 Cow Measurement")

    st.image(
    "cow.jfif",
    use_container_width=True
)

    st.subheader("🐐 Goat Measurement")

    st.image(
    "goat.jfif",
    use_container_width=True
)

    st.subheader("🐖 Pig Measurement")

    st.image(
    "pig.jfif",
    use_container_width=True
)
   
    st.subheader("📏 Typical Heart Girth & body length Range")
    
    st.table({
    "Animal": [
        "Goat",
        "Pig",
        "Cow",
        "Buffalo",
        "Horse"
    ],

    "Typical Girth (inch)": [
        "20 - 40",
        "25 - 55",
        "45 - 90",
        "55 - 100",
        "50 - 85"
    ],

    "Typical Length (inch)": [
        "18 - 35",
        "25 - 50",
        "40 - 80",
        "45 - 90",
        "45 - 75"
    ]
    })

    st.success("""
    Example:

    Goat Chest Size = 30 inch

    Body Length = 28 inch

    Enter these values in the Live Weight Calculator.
    """)

    st.warning("""
    ✔️ Measure just behind the front legs

    ✔️ Keep tape snug but not too tight

    ✔️ Measure in inches

    ✔️ Animal should stand normally
    """)



# =========================================
# LIVE WEIGHT CALCULATOR
# =========================================

elif menu == "📏 লাইভ ওয়েট ক্যালকুলেটর | Live Weight Calculator":

    st.header("📏 Animal Live Weight Calculator")

    animal = st.selectbox(

        "Select Animal",

        [
            "Cow",
            "Buffalo",
            "Horse",
            "Goat",
            "Pig"
        ]
    )

    # =====================================
    # ANIMAL IMAGES
    # =====================================

    if animal == "Cow":

        st.image(
            "https://images.unsplash.com/photo-1500595046743-cd271d694d30",
            caption="🐄 Cow",
            use_container_width=True
        )

    elif animal == "Buffalo":

        st.image(
            "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e",
            caption="🐃 Buffalo",
            use_container_width=True
        )

    elif animal == "Horse":

        st.image(
            "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a",
            caption="🐎 Horse",
            use_container_width=True
        )

    elif animal == "Goat":

        st.image(
            "https://images.unsplash.com/photo-1524024973431-2ad916746881",
            caption="🐐 Goat",
            use_container_width=True
        )

    elif animal == "Pig":

        st.image(
            "https://images.unsplash.com/photo-1516467508483-a7212febe31a",
            caption="🐖 Pig",
            use_container_width=True
        )

    # =====================================
    # INPUT
    # =====================================

    girth = st.number_input(
        "Enter Heart Girth / Chest Size (inch)",
        min_value=1.0
    )

    st.caption(
    "📏 Measure chest circumference just behind the front legs."
    )
    length = st.number_input(
        "Enter Body Length (inch)",
        min_value=1.0
    )
     
    # =====================================
    # CALCULATE BUTTON
    # =====================================

    if st.button("Calculate Live Weight"):

        # =====================================
        # GOAT
        # =====================================

        if animal == "Goat":

            # UNIVERSAL GOAT FORMULA

            weight = (
                girth * girth * length
            ) / 630

            # REALISTIC LIVE WEIGHT ADJUSTMENT

            weight = (
                weight * 0.453592 * 2
            )

            # GOAT MARKET RATE

            if weight < 20:

                rate = 450

            elif weight < 40:

                rate = 500

            elif weight < 60:

                rate = 550

            else:

                rate = 600

            market_price = weight * rate

            st.success(
                f"Estimated Live Weight: {weight:.2f} KG"
            )

            st.info(
                f"Market Rate: ₹{rate} per KG"
            )

            st.success(
                f"Estimated Market Price: ₹{market_price:.2f}"
            )

        # =====================================
        # PIG
        # =====================================

        elif animal == "Pig":

            weight = (
                girth * girth * length
            ) / 800

            weight = weight * 0.453592

            if weight < 40:

                rate = 180

            elif weight < 80:

                rate = 220

            else:

                rate = 280

            market_price = weight * rate

            st.success(
                f"Estimated Pig Live Weight: {weight:.2f} KG"
            )

            st.info(
                f"Pig Market Rate: ₹{rate} per KG"
            )

            st.success(
                f"Estimated Pig Market Price: ₹{market_price:.2f}"
            )

        # =====================================
        # OTHER ANIMALS
        # =====================================

        else:

            weight = (
                girth * girth * length
            ) / 660

            weight = weight * 0.453592

            st.success(
                f"Estimated Live Weight: {weight:.2f} KG"
            )

# =========================================
# MARKET PRICE
# =========================================

elif menu == "💰 Market Price Information":

    st.header("💰 Market Price Information")

    st.info("🐐 Goat Price: ₹400 - ₹650 per KG")

    st.info("🐖 Pig Price: ₹180 - ₹280 per KG")

    st.info("🐄 Cow Price depends on local market")

#=========================================
#🐄 স্মার্ট পশুপালন | Smart Animal Husbandry
#========================================

elif menu == "🐄 স্মার্ট পশুপালন | Smart Animal Husbandry":
        st.write ("smart section loaded") 
        st.header("🐄 স্মার্ট পশুপালন | Smart Animal Husbandry")

        st.success("সফল ও লাভজনক পশুপালনের জন্য গুরুত্বপূর্ণ পরামর্শ")

        st.markdown("""
### 🏠 খামার ব্যবস্থাপনা
✅ খামার পরিষ্কার ও শুকনো রাখুন

✅ পর্যাপ্ত আলো-বাতাসের ব্যবস্থা করুন

✅ নিয়মিত জীবাণুনাশক ব্যবহার করুন

### 🌾 খাদ্য ব্যবস্থাপনা
✅ সুষম খাদ্য প্রদান করুন

✅ সবসময় পরিষ্কার পানি সরবরাহ করুন

✅ বয়স ও ওজন অনুযায়ী খাদ্য দিন

### 💉 স্বাস্থ্য পরিচর্যা
✅ নিয়মিত টিকা প্রদান করুন

✅ কৃমিনাশক প্রয়োগ করুন

✅ অসুস্থ পশুকে আলাদা রাখুন

### 🐄 প্রজনন ব্যবস্থাপনা
✅ সঠিক সময়ে প্রজনন করান

✅ গর্ভবতী পশুর বিশেষ যত্ন নিন

### 📈 লাভ বৃদ্ধির উপায়
✅ নিয়মিত ওজন পর্যবেক্ষণ করুন

✅ উন্নত জাত নির্বাচন করুন

✅ রোগ প্রতিরোধে গুরুত্ব দিন
""")

# =========================================
# DISEASE INFO
# =========================================
elif menu == "🩺 রোগ সম্পর্কিত তথ্য | Disease Info":

    st.header("🩺 রোগ সম্পর্কিত তথ্য | Disease Info")

    search_disease = st.text_input(
        "🔍 রোগের নাম লিখুন | Search Disease Information"
    )

    if search_disease:

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
                        {
                            "role": "system",
                            "content": "You are a veterinary disease information assistant. Answer only in Bengali."
                        },
                        {
                            "role": "user",
                            "content": f"""
পশুর রোগ: {search_disease}

বাংলায় নিম্নলিখিত শিরোনামে উত্তর দাও:

1. রোগের পরিচিতি
2. কারণ
3. লক্ষণ
4. রোগ নির্ণয়
5. চিকিৎসা
6. প্রতিরোধ
"""
                        }
                    ]
                },
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            if "choices" in data:

                reply = data["choices"][0]["message"]["content"]

                st.markdown(reply)

            else:

                st.error("No response received from AI model.")

        except Exception as e:

            st.error(f"Error: {e}")

    if search_disease:
        search_disease = search_disease.lower()
    else:
        search_disease = ""

    # FMD
    if search_disease == "" or "fmd" in search_disease:

        st.subheader("🐄 FMD (Foot and Mouth Disease)")

        st.info("""
🔹 রোগের নাম: Foot and Mouth Disease (FMD)

🦠 কারণ:
ভাইরাসজনিত অত্যন্ত সংক্রামক রোগ।

⚠️ লক্ষণ:
* মুখে ঘা
* অতিরিক্ত লালা ঝরা
* জ্বর
* খাওয়া কমে যাওয়া
* খোঁড়া হয়ে হাঁটা

💊 চিকিৎসা:
* পশু চিকিৎসকের পরামর্শ নিন
* জীবাণুনাশক ব্যবহার করুন
* আক্রান্ত পশুকে আলাদা রাখুন

🛡️ প্রতিরোধ:
* নিয়মিত টিকা দিন
* খামার পরিষ্কার রাখুন
* নতুন পশু আনার আগে পর্যবেক্ষণ করুন
""")

    # Black Quarter
    if (
        search_disease == ""
        or "bq" in search_disease
        or "black quarter" in search_disease
    ):

        st.subheader("🐄 Black Quarter (BQ)")

        st.warning("""
🦠 কারণ:
ব্যাকটেরিয়াজনিত মারাত্মক রোগ।

⚠️ লক্ষণ:
* হঠাৎ জ্বর
* পেশী ফুলে যাওয়া
* চলাফেরায় কষ্ট
* খাওয়া বন্ধ

💊 চিকিৎসা:
* দ্রুত ভেটেরিনারি চিকিৎসা
* অ্যান্টিবায়োটিক

🛡️ প্রতিরোধ:
* BQ টিকা প্রদান
* পরিষ্কার পরিবেশ বজায় রাখা
""")
#============================================
#"🔍 লক্ষণ দেখে রোগ শনাক্ত | Symptom Checker",
#=============================================
elif menu == "🔍 লক্ষণ দেখে রোগ শনাক্ত | Symptom Checker":

    st.header("🔍 লক্ষণ দেখে রোগ শনাক্ত | AI Symptom Checker")

    st.info("লক্ষণ লিখুন, AI সম্ভাব্য রোগ সম্পর্কে প্রাথমিক ধারণা দেবে")

    animal = st.selectbox(
        "🐄 পশু নির্বাচন করুন | Select Animal",
        [
            "Cow",
            "Goat",
            "Buffalo",
            "Sheep",
            "Pig",
            "Poultry"
        ]
    )

    symptom_text = st.text_area(
        "📝 লক্ষণ লিখুন",
        height=150,
        placeholder="""
উদাহরণ:

জ্বর আছে
মুখ দিয়ে লালা পড়ছে
খাবার খাচ্ছে না
খুঁড়িয়ে হাঁটছে

অথবা

Fever, salivation, mouth lesion, lameness
"""
    )

    if st.button("🔍 রোগ বিশ্লেষণ করুন"):

        if symptom_text.strip() == "":

            st.warning("অনুগ্রহ করে লক্ষণ লিখুন")

        else:

            with st.spinner("AI বিশ্লেষণ করছে..."):

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
                                {
                                    "role": "system",
                                    "content": """
You are an expert veterinary assistant.

Analyze the symptoms and provide:

১. সম্ভাব্য রোগ
২. রোগ হওয়ার কারণ
৩. কতটা সম্ভাবনা (High/Medium/Low)
৪. প্রাথমিক করণীয়
৫. প্রতিরোধ ব্যবস্থা
৬. কখন পশু চিকিৎসকের সাথে যোগাযোগ করতে হবে

Important:
- Use simple Bengali.
- Farmer friendly language.
- Mention that it is not a final diagnosis.
"""
                                },
                                {
                                    "role": "user",
                                    "content": f"""
Animal: {animal}

Symptoms:
{symptom_text}
"""
                                }
                            ]
                        }
                    )

                    result = response.json()

                    if "choices" in result:

                        answer = result["choices"][0]["message"]["content"]

                        st.success("✅ বিশ্লেষণ সম্পন্ন")

                        st.markdown(answer)

                        st.warning(
                            "⚠️ এটি শুধুমাত্র AI ভিত্তিক প্রাথমিক বিশ্লেষণ। নিশ্চিত রোগ নির্ণয়ের জন্য পশুচিকিৎসকের পরামর্শ নিন।"
                        )

                    else:

                        st.error("AI থেকে উত্তর পাওয়া যায়নি")

                except Exception as e:

                    st.error(f"ত্রুটি: {e}")

# =========================================
# FEEDING TIPS
# =========================================

elif menu == "🥬 খাদ্য পরামর্শ | Feeding Tips":

    st.header("🥬 খাদ্য পরামর্শ | Feeding Tips")

    st.info("🐾 পশু ও পাখির জন্য সঠিক খাদ্য ব্যবস্থাপনা | Proper Feeding Management for Animals & Birds")

    st.markdown("""
### 💧 সাধারণ নির্দেশনা | General Feeding Tips

✅ সবসময় পরিষ্কার ও বিশুদ্ধ পানি সরবরাহ করুন

✅ ছাঁচযুক্ত, পচা বা দুর্গন্ধযুক্ত খাদ্য দেবেন না

✅ খাদ্য ধীরে ধীরে পরিবর্তন করুন

✅ সুষম খাদ্যের সাথে মিনারেল মিক্সচার ও লবণ ব্যবহার করুন

✅ গর্ভবতী ও দুগ্ধদানকারী প্রাণীর জন্য অতিরিক্ত পুষ্টিকর খাদ্য দিন

---

### 🐄 গরু | Cattle

🌿 সবুজ ঘাস: 15-25 কেজি/দিন

🌾 শুকনা খড়: 3-6 কেজি/দিন

🥣 দানাদার খাদ্য: প্রতি 2-3 লিটার দুধের জন্য 1 কেজি

🧂 মিনারেল মিক্সচার: 50-60 গ্রাম/দিন

💧 40-70 লিটার পরিষ্কার পানি

---

### 🐃 মহিষ | Buffalo

🌿 সবুজ ঘাস: 20-30 কেজি/দিন

🌾 শুকনা খড়: 5-8 কেজি/দিন

🥣 সুষম কনসেনট্রেট খাদ্য

🧂 মিনারেল মিক্সচার

💧 60-100 লিটার পানি

---

### 🐐 ছাগল | Goat

🌿 ঘাস, লতা ও গাছের পাতা

🌾 শুকনা খাদ্য

🥣 200-500 গ্রাম কনসেনট্রেট

🧂 মিনারেল মিক্সচার

💧 পর্যাপ্ত পরিষ্কার পানি

---

### 🐑 ভেড়া | Sheep

🌿 চারণভূমির ঘাস

🌾 শুকনা খড়

🥣 প্রয়োজনে কনসেনট্রেট খাদ্য

🧂 মিনারেল ও লবণ

💧 পরিষ্কার পানি

---

### 🐖 শূকর | Pig

🌽 ভুট্টা, গম ও সুষম ফিড

🥣 উচ্চ প্রোটিনযুক্ত খাদ্য

🥬 শাকসবজি ও কৃষি উপজাত

🧂 ভিটামিন ও মিনারেল

💧 সবসময় পরিষ্কার পানি

---

### 🐔 মুরগি | Poultry

🐣 Starter Feed (0-8 সপ্তাহ)

🐥 Grower Feed (8-20 সপ্তাহ)

🐔 Layer Feed (ডিমপাড়া মুরগি)

🌽 ভুট্টা ও সুষম খাদ্য

🧂 ক্যালসিয়াম ও খনিজ

💧 সার্বক্ষণিক পরিষ্কার পানি

---

### 🦆 হাঁস | Duck

🌾 ধান, ভুট্টা ও হাঁসের ফিড

🐌 শামুক ও জলজ খাদ্য

🧂 খনিজ ও ভিটামিন

💧 পর্যাপ্ত পানি

---

### 🐇 খরগোশ | Rabbit

🌿 নরম ঘাস ও সবুজ পাতা

🥕 গাজর, শাকসবজি

🥣 Rabbit Pellet Feed

💧 পরিষ্কার পানি

---

### 🐎 ঘোড়া | Horse

🌿 উন্নত মানের ঘাস

🌾 খড়

🥣 ওটস ও দানাদার খাদ্য

🧂 মিনারেল সাপ্লিমেন্ট

💧 পর্যাপ্ত পানি

---

### ⚠️ সতর্কতা | Important Warnings

❌ পচা বা ফাঙ্গাসযুক্ত খাদ্য দেবেন না

❌ হঠাৎ খাদ্য পরিবর্তন করবেন না

❌ অপরিষ্কার পানি ব্যবহার করবেন না

❌ অতিরিক্ত দানাদার খাদ্য খাওয়াবেন না

✅ সুষম খাদ্য ও পরিষ্কার পানি সুস্থ প্রাণীর মূল চাবিকাঠি
""")
# =========================================
# VACCINATION GUIDE
# =========================================

elif menu == "💉 টিকা নির্দেশিকা | Vaccination Guide":

    st.header("💉 টিকা নির্দেশিকা | Vaccination Guide")

    animal = st.selectbox(
        "🐾 প্রাণী নির্বাচন করুন | Select Animal",
        [
            "🐄 Cow",
            "🐐 Goat",
            "🐑 Sheep",
            "🐖 Pig"
        ]
    )

    if animal == "🐄 Cow":

        st.subheader("🐄 Cow Vaccination Schedule")

        st.table({
            "Disease": [
                "FMD (Foot & Mouth Disease)",
                "HS (Haemorrhagic Septicaemia)",
                "BQ (Black Quarter)",
                "Brucellosis",
                "Theileriosis (Risk Area)"
            ],
            "Vaccination Time": [
                "Every 6 months",
                "Once yearly (Before Monsoon)",
                "Once yearly",
                "Female calf at 4-8 months",
                "As advised by veterinarian"
            ]
        })

        st.success("✅ Calves should receive colostrum within 2 hours of birth.")
        st.success("✅ Deworm before vaccination whenever possible.")
        st.success("✅ Vaccinate only healthy animals.")
        st.info("💡 Maintain vaccine cold chain (2-8°C).")

    elif animal == "🐐 Goat":

        st.subheader("🐐 Goat Vaccination Schedule")

        st.table({
            "Disease": [
                "PPR",
                "Goat Pox",
                "Enterotoxaemia",
                "FMD",
                "HS"
            ],
            "Vaccination Time": [
                "Once yearly",
                "Once yearly",
                "Once yearly",
                "Every 6 months",
                "Once yearly"
            ]
        })

        st.success("✅ Vaccinate kids after recommended age.")
        st.success("✅ Keep newly vaccinated animals stress-free.")
        st.success("✅ Deworm regularly.")
        st.info("💡 Provide clean drinking water after vaccination.")

    elif animal == "🐑 Sheep":

        st.subheader("🐑 Sheep Vaccination Schedule")

        st.table({
            "Disease": [
                "PPR",
                "Sheep Pox",
                "Enterotoxaemia",
                "FMD",
                "HS"
            ],
            "Vaccination Time": [
                "Once yearly",
                "Once yearly",
                "Once yearly",
                "Every 6 months",
                "Once yearly"
            ]
        })

        st.success("✅ Vaccinate before disease season.")
        st.success("✅ Avoid overcrowding after vaccination.")
        st.success("✅ Maintain proper nutrition.")
        st.info("💡 Record all vaccination dates.")

    elif animal == "🐖 Pig":

        st.subheader("🐖 Pig Vaccination Schedule")

        st.table({
            "Disease": [
                "Classical Swine Fever",
                "Swine Erysipelas",
                "FMD",
                "Parvovirus (Breeding Animals)",
                "Leptospirosis (Risk Area)"
            ],
            "Vaccination Time": [
                "Once yearly",
                "Once yearly",
                "Every 6 months",
                "As advised by veterinarian",
                "As advised by veterinarian"
            ]
        })

        st.success("✅ Vaccinate piglets at appropriate age.")
        st.success("✅ Keep pens clean and dry.")
        st.success("✅ Isolate sick animals immediately.")
        st.info("💡 Follow veterinarian's vaccination protocol.")

    st.markdown("---")

    st.subheader("📌 General Vaccination Tips")

    st.success("✅ Store vaccines at 2-8°C.")
    st.success("✅ Use sterile needles and syringes.")
    st.success("✅ Vaccinate only healthy animals.")
    st.success("✅ Keep vaccination records.")
    st.success("✅ Consult a veterinarian for local vaccination schedules.")

    st.warning(
        "⚠️ Vaccination schedules may vary depending on disease prevalence, region, and government guidelines."
    )
# =========================================
# AI VETERINARY ASSISTANT
# =========================================

elif menu == "🤖 AI পশু চিকিৎসা সহায়ক":

    st.header("🤖 AI Veterinary Assistant")

    if "vet_chat_messages" not in st.session_state:

        st.session_state.vet_chat_messages = []

    if "vet_chat_animal" not in st.session_state:

        st.session_state.vet_chat_animal = None

    animal = st.selectbox(

        "Select Animal",

        [
            "Cow",
            "Goat",
            "Pig",
            "Buffalo",
            "Horse"
        ]
    )

    if st.session_state.vet_chat_animal != animal:

        st.session_state.vet_chat_messages = []
        st.session_state.vet_chat_animal = animal

    if st.button("Clear Chat"):

        st.session_state.vet_chat_messages = []
        st.rerun()

    for message in st.session_state.vet_chat_messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    user_problem = st.chat_input("Describe your problem")

    if user_problem:

        st.session_state.vet_chat_messages.append(
            {
                "role": "user",
                "content": user_problem,
            }
        )

        with st.chat_message("user"):

            st.markdown(user_problem)

        with st.chat_message("assistant"):

            try:
                if not API_KEY:

                    st.error(
                        "OpenRouter API key not found. Add API_KEY to Animal_project/.env and restart Streamlit."
                    )

                    st.stop()

                system_prompt = f"""
                If the user asks in Bengali, always reply in standard Indian Bengali.
                Never use the word "পানি"; use "জল" or "পানীয় জল" instead.
               
                Use Indian Bengali medical terms and natural vocabulary.
                You are a careful veterinary triage assistant for livestock farmers.
                The selected animal is: {animal}.

                Use the recent chat history to answer follow-up questions in context.

                Important rules:
                - Do not claim a confirmed diagnosis.
                - Do not answer with only questions, "None", or a refusal.
                - Always give the best practical provisional guidance from the available details.
                - If details are limited, clearly say "Based on the limited information" and continue with likely causes and safe care steps.
                - Prioritize emergency warning signs and when to call a veterinarian.
                - Keep medicine advice general; do not give exact drug dosages unless a veterinarian has prescribed them.
                - Use clear farmer-friendly language.
                - If the farmer asks a follow-up, answer it directly using the previous context.
                - Ask follow-up questions only after giving useful guidance.
                - Ask at most 1 focused follow-up question, and skip it if the next step is already clear.
            

                For a new health problem, use this structure:
                1. Quick Triage
                2. Possible Diseases / Causes
                3. What To Do Now
                4. Feeding And Water
                5. What Not To Do
                6. When To Call A Veterinarian

                For a follow-up question, do not restart the whole interview. Use the chat context and give direct next steps.
                """

                previous_messages = st.session_state.vet_chat_messages[:-1][-3:]
                current_message = st.session_state.vet_chat_messages[-1:]

                response = requests.post(

                    url="https://openrouter.ai/api/v1/chat/completions",

                    headers={

                        "Authorization": f"Bearer {API_KEY}",

                        "Content-Type": "application/json",
                    },

                    json={

                        "model":
                        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",

                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt,
                            },
                            *previous_messages,
                            *current_message,
                        ],
                        "temperature": 0.2,
                    },
                )

                response_data = response.json()

                if "error" in response_data:

                    api_error = response_data["error"]
                    api_message = (
                        api_error.get("message", api_error)
                        if isinstance(api_error, dict)
                        else api_error
                    )

                    st.error(
                        f"API Error: {api_message}"
                    )

                else:

                    reply = response_data[
                        "choices"
                    ][0]["message"]["content"]

                    st.markdown(reply)

                    st.session_state.vet_chat_messages.append(
                        {
                            "role": "assistant",
                            "content": reply,
                        }
                    )

            except Exception as e:

                st.error(f"Error: {e}")

# =========================================
# ABOUT APP
# =========================================

elif menu == "ℹ️ অ্যাপ সম্পর্কে | About App":

    st.header("ℹ️ About App")

    st.write("""

    🐄 Livestock AI Assistant helps farmers:

    ✅ Calculate Live Weight

    ✅ Estimate Market Price

    ✅ Learn Disease Information

    ✅ Get Feeding Tips

    ✅ AI Veterinary Support

    ✅ Mobile Friendly Veterinary App

    """)
