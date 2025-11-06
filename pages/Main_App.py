import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
import re

# --------------------------------
# AUTHENTICATION CHECK
# --------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please log in first to access ToneFlo.")
    st.switch_page("Home.py")

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(page_title="ToneFlo", layout="wide", initial_sidebar_state="expanded")

# --------------------------------
# Sidebar with Logout
# --------------------------------
with st.sidebar:


    # Show logged-in user
    st.markdown(
        f"<p style='font-size:1rem; text-align:center; color:#a3bffa;'>🤗 Welcome <b>{st.session_state.current_user}</b></p>",
        unsafe_allow_html=True
    )

    # Logout button with custom style
    st.markdown(
        """
        <style>
        .logout-btn button {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            width: 100%;
            border: none;
            transition: 0.3s ease;
        }
        .logout-btn button:hover {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
            transform: scale(1.03);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        if st.button("👋 Bounce Out", key="logout_sidebar", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.success("✅ Logged out successfully.")
            st.switch_page("Home.py")

# --------------------------------
# Main Page Aesthetic CSS
# --------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: radial-gradient(circle at 20% 20%, #f9faff, #eef2ff);
}

/* --- MAIN HEADER --- */
.main-header {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    border-radius: 28px;
    padding: 3.5rem 2rem;
    color: #fff;
    text-align: center;
    position: relative;
    box-shadow: 0 10px 50px rgba(102, 126, 234, 0.3);
    margin-bottom: 4rem;
    overflow: hidden;
}

.main-header::after {
    content: '';
    position: absolute;
    top: -20%;
    left: -20%;
    width: 140%;
    height: 140%;
    background: radial-gradient(circle at 60% 60%, rgba(255,255,255,0.15), transparent 70%);
    animation: glow 8s ease-in-out infinite alternate;
}

@keyframes glow {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.main-header h1 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 3.8rem;
    letter-spacing: -1px;
    margin-bottom: 0.5rem;
}

.main-header p {
    opacity: 0.95;
    font-size: 1.2rem;
}

/* --- BUTTONS --- */
.stButton button {
    border-radius: 16px;
    padding: 1.2rem 2rem;
    font-weight: 600;
    font-size: 1.05rem;
    border: none;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(118, 75, 162, 0.25);
}

.stButton button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #764ba2, #667eea);
    box-shadow: 0 8px 28px rgba(118, 75, 162, 0.35);
}

/* --- RESULT BOX --- */
.result-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-left: 6px solid rgba(255,255,255,0.6);
    border-radius: 22px;
    padding: 2.5rem;
    box-shadow: 0 10px 40px rgba(118, 75, 162, 0.3);
    margin: 2.5rem 0;
}

/* --- CHAT BUBBLES --- */
.chat-box {
    background: rgba(255,255,255,0.9);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 2rem;
    box-shadow: 0 6px 25px rgba(0,0,0,0.08);
}

.user-msg {
    background: #667eea;
    color: white;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    max-width: 80%;
    margin-left: auto;
}

.ai-msg {
    background: #f1f3ff;
    color: #1a202c;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    max-width: 80%;
}

/* --- MARQUEE --- */
.scrolling-text-container {
    width: 100%;
    overflow: hidden;
    background: #0f1117;
    padding: 1.8rem 0;
    margin: 4rem auto 2rem;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    display: flex;
    justify-content: center;
    align-items: center;
}

.scrolling-text-wrapper {
    display: flex;
    align-items: center;
    white-space: nowrap;
    animation: scroll 25s linear infinite;
}

.scrolling-text-wrapper span {
    font-size: 2rem;
    font-weight: 700;
    color: #cbd5e0;
    margin: 0 2.5rem;
    letter-spacing: 0.5px;
}

.scrolling-text-wrapper span::after {
    content: " • ";
    color: #ff4d4d;
    margin-left: 1.5rem;
}

@keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# Header
# --------------------------------
st.markdown("""
<div class="main-header">
    <h1>💬 ToneFlo</h1>
    <p style="font-weight:500;">Emotional Intelligence for Your Conversations</p>
    <p style="opacity:0.85;">Your AI conversational co-pilot — confident, emotionally aware & charming.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------
# Mode Selection
# --------------------------------
st.markdown("<h2 style='text-align:center;'>✨ Choose Your Mode</h2>", unsafe_allow_html=True)
modes = {"upload": "Upload Chat Screenshots", "overview": "Overview of the Person", "check_compatibility": "Check Compatibility"}
col1, col2, col3 = st.columns(3)
for i, (key, label) in enumerate(modes.items()):
    with [col1, col2, col3][i]:
        if st.button(label, key=f"btn_{key}", use_container_width=True):
            st.session_state["wing_action"] = key
            st.rerun()

# --------------------------------
# OpenAI Client
# --------------------------------
api_key = st.secrets.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE")
client = OpenAI(api_key=api_key)

def generate_ai_response(prompt=None, max_tokens=300, messages=None):
    try:
        if messages is None:
            messages = [
                {"role": "system", "content": "You are Wingman AI — brutally honest, confident, emotionally intelligent, and funny like Barney Stinson or Joey Tribbiani."},
                {"role": "user", "content": [{"type": "text", "text": prompt}]},
            ]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.9,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error("😅 Wingman AI couldn’t process your request.")
        st.write(e)
        return None

# --------------------------------
# Wingman Logic
# --------------------------------
if "wing_action" in st.session_state:
    action = st.session_state["wing_action"]

    # --- UPLOAD CHAT SCREENSHOTS ---
    if action == "upload":
        st.markdown("### 📸 Upload Chat Screenshots")
        uploaded_files = st.file_uploader(
            "Drop your chat screenshots here 👇", type=["png", "jpg", "jpeg"], accept_multiple_files=True
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} screenshot(s) uploaded successfully!")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Wingman AI — a mix of Barney Stinson and Joey Tribbiani. "
                        "You're the ultimate bro who reads chats like a romance detective, "
                        "calling out the hidden signals, teasing where needed, and hyping your friend up when they score. "
                        "You're funny, confident, flirty, and emotionally sharp — always helping your bro understand whether the other person is actually into them or just being polite. "
                        "Use humor, charisma, and brutal honesty — but always keep it fun and supportive, like a best friend giving real talk."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Bro, analyze these chat screenshots like a true wingman — "
                                "spot the interest level, emotional chemistry, and hidden subtext. "
                                "Tell me if she’s flirting, friend-zoning, or just vibing. "
                                "Give me your honest, funny take like Barney or Joey would."
                            )
                        }
                    ],
                },
            ]

            for file in uploaded_files:
                image = Image.open(file)
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                b64_image = base64.b64encode(buf.getvalue()).decode("utf-8")
                messages[-1]["content"].append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}})

            with st.spinner("🕵️‍♂️ Wingman is analyzing your chat…"):
                result = generate_ai_response(messages=messages, max_tokens=450)
                if result:
                    st.session_state["wingman_chat_analysis"] = result
                    st.markdown(f'<div class="result-box"><h3>🧩 Wingman POV</h3><p>{result}</p></div>', unsafe_allow_html=True)
                    st.success("✅ Analysis complete — now chat with your Wingman below!")

        # --- Wingman Chat (after analysis) ---
        if "wingman_chat_analysis" in st.session_state:
            st.markdown("### 💬 Chat with Wingman AI")
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    {"role": "system", "content": "You are Wingman AI — give real-time flirty, funny, emotionally intelligent advice."},
                    {"role": "assistant", "content": st.session_state["wingman_chat_analysis"]},
                ]

            for msg in st.session_state.chat_history[1:]:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
                elif msg["role"] == "assistant":
                    st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)

            user_input = st.text_input("Type your message to Wingman:", key="wingman_input")
            if st.button("Engage Wingman", use_container_width=True):
                if user_input.strip():
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    messages = st.session_state.chat_history.copy()
                    response = generate_ai_response(messages=messages, max_tokens=250)
                    if response:
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        st.rerun()

    # --- Overview and Compatibility remain unchanged ---
    elif action == "overview":
        st.markdown("### Describe Your Crush")
        crush_description = st.text_area("Tell your Wingman what they're like — their vibe, energy, personality:", height=150)
        if st.button("💡 Analyze Their Vibe", use_container_width=True):
            if crush_description.strip():
                prompt = f"Describe the vibe, energy, and personality of this person: '{crush_description}'. Then, give flirty, fun insights as if Barney Stinson or Joey were analyzing it."
                result = generate_ai_response(prompt, max_tokens=400)
                if result:
                    st.session_state["crush_overview"] = crush_description
                    st.markdown(f'<div class="result-box"><h3>🧠 Wingman’s Take</h3><p>{result}</p></div>', unsafe_allow_html=True)
                    st.success("📝 Got it, bro! Crush overview saved.")
            else:
                st.warning("Bro, give me something to work with — describe your crush first 😅")

    elif action == "check_compatibility":
        if "crush_overview" not in st.session_state:
            st.warning("⚠️ Bro, first tell me about your crush in 'Overview of the Person' 😉")
        else:
            st.markdown("### Check Compatibility with Your Crush")
            self_description = st.text_area("Now describe yourself, bro — your vibe, personality, and energy:", height=150)
            if st.button("💫 Check Compatibility", use_container_width=True):
                if not self_description.strip():
                    st.warning("Come on bro, tell me about yourself 😅")
                else:
                    crush = st.session_state["crush_overview"]
                    prompt = f"Compare compatibility between:\n\nCrush: {crush}\n\nSelf: {self_description}\n\nGive a brutally honest, funny, and realistic verdict like Barney or Joey."
                    result = generate_ai_response(prompt, max_tokens=500)
                    if result:
                        st.markdown(f'<div class="result-box"><h3> Compatibility Verdict</h3><p>{result}</p></div>', unsafe_allow_html=True)
                        verdict_lower = result.lower()
                        if any(word in verdict_lower for word in ["compatible", "perfect match", "good match", "great chemistry"]):
                            st.success("🔥 Go get her, bro!")
                        elif any(word in verdict_lower for word in ["not compatible", "no chemistry", "bad match"]):
                            st.error("💔 She's out of your league, Baburao!")
                        else:
                            st.info("🤔 Mixed signals, bro. Proceed with caution!")

# --------------------------------
# Marquee Animation
# --------------------------------
st.markdown("""
<div class="scrolling-text-container">
  <div class="scrolling-text-wrapper">
    <span>Wingman Advice</span>
    <span>Pickup Lines</span>
    <span>Compatibility Match</span>
    <span>Emotional Insights</span>
    <span>Flirty Openers</span>
    <span>Chat Tone Analysis</span>
    <span>Confidence Boosters</span>
    <span>Crush Decode</span>
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------
# Pickup Line Generator
# --------------------------------
st.markdown("### 💬 Need a Pickup Line?")
style = st.selectbox("Choose your style:", ["Cheesy 😍", "Smooth Operator 😎", "Sigma 💪"], index=1)

if st.button("✨ Generate Pickup Line", use_container_width=True):
    if "Cheesy" in style:
        prompt = (
            "You are Joey Tribbiani, Barney Stinson, and Michael Scott combined — a lovable, overconfident, and funny flirt. "
            "Generate one short, dramatic, and adorably cheesy pickup line that would make someone laugh and blush. "
            "Keep it playful and a little over-the-top."
        )
    elif "Smooth" in style:
        prompt = (
            "You are a blend of Barney Stinson, Sam Malone, and Jeff Winger — effortlessly charming, confident, and witty. "
            "Generate one short, suave pickup line that sounds natural, classy, and smooth without trying too hard."
        )
    elif "Sigma" in style:
        prompt = (
            "You are Harvey Specter, Dr. Gregory House, Raymond Holt, and James Bond rolled into one — calm, bold, and mysterious. "
            "Generate one short, powerful pickup line that feels self-assured and high-value. "
            "It should sound more like a statement of intent than a plea for attention."
        )
    else:
        prompt = "Generate one short, confident, funny pickup line."

    line = generate_ai_response(prompt, max_tokens=60)
    if line:
        st.markdown(
            f'<div class="result-box"><h3>💬 {style} Line</h3><p>{line}</p></div>',
            unsafe_allow_html=True,
        )

# --------------------------------
# Footer
# --------------------------------
st.markdown("""
<div class="footer" style="text-align:center; margin-top:3rem;">
    <p style="font-size:1.1rem; font-weight:600; color:#4a5568;">
        💬 <span style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; color: transparent;">
        ToneFlo</span> — Emotional Intelligence for Conversations
    </p>
    <p style="font-style: italic; color: #718096;">Because connection is a rhythm, not a script.</p>
</div>
""", unsafe_allow_html=True)
