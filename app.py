import streamlit as st
import pickle
import base64

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="SpamShield AI",
    page_icon="🛡️",
    layout="centered"
)

# -----------------------------
# Background Image
# -----------------------------
def set_bg():
    st.markdown(
        """
        <style>

        /* Main animated background */
        .stApp {
            background: linear-gradient(-45deg,#021B3A,#043C7A,#0A2A5A,#021433);
            background-size: 400% 400%;
            animation: gradientBG 12s ease infinite;
        }

        /* Background animation */
        @keyframes gradientBG {
            0% {background-position:0% 50%}
            50% {background-position:100% 50%}
            100% {background-position:0% 50%}
        }

        /* White border frame around page */
        .block-container {
            border: 2px solid white;
            border-radius: 15px;
            padding: 40px;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(8px);
        }

        /* Main content box */
        .main-box{
            background: rgba(0,0,0,0.65);
            padding:40px;
            border-radius:15px;
            border:1px solid white;
        }

        /* Title styling */
        .title{
            text-align:center;
            color:#00e5ff;
            font-size:40px;
            font-weight:bold;
            text-shadow:0px 0px 12px #00e5ff;
        }

        /* Subtitle */
        .subtitle{
            text-align:center;
            color:white;
            margin-bottom:20px;
        }

        /* Footer */
        .footer{
            text-align:center;
            color:#cfd8ff;
            margin-top:30px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# -----------------------------
# Load ML Model
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# -----------------------------
# Login Session
# -----------------------------
if "login" not in st.session_state:
    st.session_state.login = False


# -----------------------------
# LOGIN PAGE
# -----------------------------
if not st.session_state.login:

    st.markdown('<div class="title">🛡️ SpamShield AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Cyber Security Spam Detection System</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="main-box">', unsafe_allow_html=True)

        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):

            if username == "admin" and password == "1234":
                st.session_state.login = True
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# MAIN APP
# -----------------------------
else:

    st.markdown('<div class="title">📩 AI Spam Message Detector</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Detect malicious or spam messages using Machine Learning</div>', unsafe_allow_html=True)

    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    message = st.text_area(
        "Enter Message",
        placeholder="Example: Congratulations! You won a free iPhone..."
    )

    if st.button("Analyze Message 🔍"):

        if message.strip() == "":
            st.warning("Please enter a message")

        else:

            vector = vectorizer.transform([message])

            prediction = model.predict(vector)[0]
            probability = model.predict_proba(vector)

            if prediction == 1:

                spam_prob = probability[0][1] * 100

                st.error("⚠️ Spam Message Detected")

                st.progress(int(spam_prob))

                st.markdown(
                    f"""
                    ### 🚨 Spam Probability
                    **{spam_prob:.2f}%**
                    """
                )

            else:

                not_spam_prob = probability[0][0] * 100

                st.success("✅ Message is Safe")

                st.progress(int(not_spam_prob))

                st.markdown(
                    f"""
                    ### 🔒 Safe Message Probability
                    **{not_spam_prob:.2f}%**
                    """
                )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

    st.markdown(
        """
        <div class="footer">
        🛡️ SpamShield AI • Machine Learning Cyber Security System
        </div>
        """,
        unsafe_allow_html=True
    )
