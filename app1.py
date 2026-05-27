
import streamlit as st
import numpy as np
import requests
import json
import os

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Livestock AI Assistant",
    page_icon="🐄",
    layout="wide"
)

# =========================================
# COLORFUL MOBILE UI
# =========================================

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
    padding: 20px;
    border-radius: 25px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.12);
}

/* TITLE */

h1 {
    color: #16a34a !important;
    text-align: center;
    font-size: 42px !important;
    font-weight: 900 !important;
}

/* HEADINGS */

h2, h3 {
    color: #15803d !important;
    font-weight: 800 !important;
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

    width: 100%;
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
}

/* INPUT BOX */

.stNumberInput input,
textarea {

    border-radius: 12px !important;
    border: 2px solid #22c55e !important;
    padding: 10px !important;
    font-size: 17px !important;
}

/* MOBILE */

@media (max-width: 768px) {

    h1 {
        font-size: 30px !important;
    }

    .block-container {
        padding: 14px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================
# API KEY
# =========================================

API_KEY = os.getenv("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")
# =========================================
# SIDEBAR MENU
# =========================================

st.sidebar.title("🐄 Livestock Menu")

menu = st.sidebar.radio(

    "Choose Option",

    [
        "🏠 Home",
        "📏 Live Weight Calculator",
        "💰 Market Price",
        "🩺 Disease Info",
        "🥬 Feeding Tips",
        "💉 Vaccination Guide",
        "🤖 AI Veterinary Assistant",
        "ℹ️ About App"
    ]
)

# =========================================
# HOME PAGE
# =========================================

if menu == "🏠 Home":

    st.markdown(
        "<h1>🐄 Livestock AI Assistant</h1>",
        unsafe_allow_html=True
    )

    st.subheader(
        "Smart Veterinary & Market Price System"
    )

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

# =========================================
# LIVE WEIGHT CALCULATOR
# =========================================

elif menu == "📏 Live Weight Calculator":

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
            width=320
        )

    elif animal == "Buffalo":

        st.image(
            "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e",
            caption="🐃 Buffalo",
            width=320
        )

    elif animal == "Horse":

        st.image(
            "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a",
            caption="🐎 Horse",
            width=320
        )

    elif animal == "Goat":

        st.image(
            "https://images.unsplash.com/photo-1524024973431-2ad916746881",
            caption="🐐 Goat",
            width=320
        )

    elif animal == "Pig":

        st.image(
            "https://images.unsplash.com/photo-1516467508483-a7212febe31a",
            caption="🐖 Pig",
            width=320
        )

    # =====================================
    # INPUT
    # =====================================

    girth = st.number_input(
        "Enter Heart Girth / Chest Size (inch)",
        min_value=1.0
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

                rate = 400

            elif weight < 40:

                rate = 450

            elif weight < 60:

                rate = 500

            else:

                rate = 650

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

elif menu == "💰 Market Price":

    st.header("💰 Market Price Information")

    st.info("🐐 Goat Price: ₹400 - ₹650 per KG")

    st.info("🐖 Pig Price: ₹180 - ₹280 per KG")

    st.info("🐄 Cow Price depends on local market")

# =========================================
# DISEASE INFO
# =========================================

elif menu == "🩺 Disease Info":

    st.header("🩺 Common Animal Diseases")

    st.warning("🐐 Goat: PPR, Fever, Diarrhea")

    st.warning("🐄 Cow: FMD, Mastitis")

    st.warning("🐖 Pig: Swine Fever")

# =========================================
# FEEDING TIPS
# =========================================

elif menu == "🥬 Feeding Tips":

    st.header("🥬 Feeding Tips")

    st.success("Provide clean water daily")

    st.success("Use green grass & dry feed")

    st.success("Use mineral mixture")

# =========================================
# VACCINATION GUIDE
# =========================================

elif menu == "💉 Vaccination Guide":

    st.header("💉 Vaccination Guide")

    st.info("🐐 Goat PPR Vaccine: Every year")

    st.info("🐄 Cow FMD Vaccine: Every 6 months")

    st.info("🐖 Pig Swine Fever Vaccine")

# =========================================
# AI VETERINARY ASSISTANT
# =========================================

elif menu == "🤖 AI Veterinary Assistant":

    st.header("🤖 AI Veterinary Assistant")

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

    user_problem = st.text_area(
        "Describe Animal Problem"
    )

    if st.button("Get AI Analysis"):

        if user_problem.strip() == "":

            st.warning(
                "Please describe the problem."
            )

        else:

            try:

                prompt = f"""
                You are an expert veterinary assistant.

                Animal:
                {animal}

                Problem:
                {user_problem}

                Give:
                1. Possible disease
                2. Feeding advice
                3. Treatment tips
                4. Emergency warning
                """

                response = requests.post(

                    url="https://openrouter.ai/api/v1/chat/completions",

                    headers={

                        "Authorization": f"Bearer {API_KEY}",

                        "Content-Type": "application/json",
                    },

                    data=json.dumps({

                        "model":
                        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",

                        "messages": [

                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    }),
                )

                response_data = response.json()

                if "error" in response_data:

                    st.error(
                        f"API Error: {response_data['error']}"
                    )

                else:

                    reply = response_data[
                        "choices"
                    ][0]["message"]["content"]

                    st.success("AI Veterinary Report")

                    st.write(reply)

            except Exception as e:

                st.error(f"Error: {e}")

# =========================================
# ABOUT APP
# =========================================

elif menu == "ℹ️ About App":

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