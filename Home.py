import streamlit as st
from supabase import create_client, Client

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="ToneFlo | Login & Register", layout="centered", initial_sidebar_state="collapsed")

# -------------------------------
# Supabase Connection
# -------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Session State Setup
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# -------------------------------
# Redirect if Already Logged In
# -------------------------------
if st.session_state.logged_in:
    st.switch_page("pages/Main_App.py")

# -------------------------------
# Modern Aesthetic CSS (with Gradient Tabs & Buttons)
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(115deg, #0f0c29 0%, #302b63 45%, #24243e 100%);
    background-attachment: fixed;
    color: #e2e8f0;
    min-height: 100vh;
    overflow-x: hidden;
}

body::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(from 90deg, rgba(106,17,203,0.25), rgba(37,117,252,0.25), rgba(106,17,203,0.25));
    filter: blur(120px);
    animation: rotate 30s linear infinite;
    z-index: -2;
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* -------------------------------
   Header Section
------------------------------- */
.topbar {
    text-align: center;
    margin-top: -2rem;
    margin-bottom: 1.5rem;
}

.topbar h1 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 3.3rem;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #a855f7, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}

.topbar p {
    font-weight: 400;
    font-size: 1.05rem;
    color: #c7d2fe;
    opacity: 0.9;
}

/* -------------------------------
   Tabs Styling
------------------------------- */
.stTabs [data-baseweb="tab-list"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 2rem !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0 auto 2.5rem !important;
}

/* Remove red underline or focus ring */
.stTabs [data-baseweb="tab"]:focus {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
}

.stTabs [data-baseweb="tab"] {
    flex: none !important;
    white-space: nowrap !important;
    font-weight: 600;
    font-size: 1.15rem;
    color: #e2e8f0 !important;
    border: none !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 14px;
    padding: 0.75rem 1.6rem;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
    box-shadow: none !important;
}

/* Hover styles */
.stTabs [data-baseweb="tab"]:hover {
    color: white !important;
    background: linear-gradient(135deg, rgba(106,17,203,0.3), rgba(37,117,252,0.3)) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(106,17,203,0.25);
}

/* Active tab (Login / Register) */
.stTabs [aria-selected="true"]:nth-child(1) {
    background: linear-gradient(135deg, #7e22ce, #5b21b6) !important; /* Purple tone for Login */
    color: white !important;
    box-shadow: 0 6px 25px rgba(126,34,206,0.5);
    border: none !important;
    outline: none !important;
}

.stTabs [aria-selected="true"]:nth-child(2) {
    background: linear-gradient(135deg, #2563eb, #1e3a8a) !important; /* Blue tone for Register */
    color: white !important;
    box-shadow: 0 6px 25px rgba(37,99,235,0.5);
    border: none !important;
    outline: none !important;
}

/* -------------------------------
   Input Box Styling
------------------------------- */
.stTextInput > div > div {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.1);
    transition: all 0.3s ease;
}

.stTextInput > div > div:hover {
    border-color: rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.08);
}

.stTextInput > div > div > input {
    background: transparent !important;
    color: #e2e8f0 !important;
    border: none !important;
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
}

/* -------------------------------
   Gradient Buttons
------------------------------- */
.stButton button {
    border-radius: 14px;
    padding: 0.9rem 2rem;
    font-weight: 600;
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    color: white;
    border: none;
    transition: all 0.35s ease;
    width: 100%;
    font-size: 1rem;
    letter-spacing: 0.3px;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(106,17,203,0.4);
}

/* -------------------------------
   Footer
------------------------------- */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.95rem;
    margin-top: 4rem;
    padding: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown("""
<div class="topbar">
    <h1>ToneFlo</h1>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Tabs: Login / Register
# -------------------------------
tab1, tab2 = st.tabs(["Login", "Register"])

# ---------- LOGIN ----------
with tab1:
    st.markdown("<h4 style='text-align:center;'>Welcome</h4>", unsafe_allow_html=True)
    login_email = st.text_input("📧 Email", key="login_email", placeholder="Enter your email")
    login_pass = st.text_input("🔒 Password", type="password", key="login_pass", placeholder="Enter your password")

    if st.button("🚀 Login to ToneFlo"):
        if not login_email or not login_pass:
            st.warning("⚠️ Please enter both email and password.")
        else:
            try:
                user = supabase.auth.sign_in_with_password({
                    "email": login_email,
                    "password": login_pass
                })
                st.session_state.logged_in = True
                st.session_state.current_user = user.user.email
                st.success(f"🎉 Welcome, {user.user.email}!")
                st.switch_page("pages/Main_App.py")
            except Exception as e:
                st.error(f"❌ Login failed: {e}")

# ---------- REGISTER ----------
with tab2:
    st.markdown("<h4 style='text-align:center;'>Join ToneFlo</h4>", unsafe_allow_html=True)
    name = st.text_input("👤 Full Name", key="reg_name", placeholder="Your full name")
    reg_email = st.text_input("📧 Email", key="reg_email", placeholder="Your email")
    reg_pass = st.text_input("🔒 Password", type="password", key="reg_pass", placeholder="Create a password")

    if st.button("🌟 Create Account"):
        if not name or not reg_email or not reg_pass:
            st.warning("⚠️ Please fill in all fields.")
        else:
            try:
                res = supabase.auth.sign_up({
                    "email": reg_email,
                    "password": reg_pass
                })
                st.success("🎉 Account created! Please verify your email before logging in.")
            except Exception as e:
                st.error(f"❌ Registration failed: {e}")

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<div class="footer">
    <p style="font-size:1.1rem; font-weight:600; color:#cbd5e1; margin-bottom:0.3rem;">
       <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; color: transparent;">
        ToneFlo</span> — Emotional Intelligence for Conversations
    </p>
    <p style="font-style: italic; color: #a0aec0; margin-top:0.2rem;">
        Because connection is a rhythm, not a script.
    </p>
</div>
""", unsafe_allow_html=True)
