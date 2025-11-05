import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64

# --------------------------------
# Page Configuration & Styling
# --------------------------------
st.set_page_config(
    page_title="ToneFlo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="rgba(255,255,255,0.1)"><polygon points="0,0 1000,50 1000,100 0,100"/></svg>');
        background-size: cover;
    }

    .main-header h1 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        position: relative;
    }

    .mode-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .mode-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2.5rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .mode-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .mode-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }

    .mode-card:hover::before {
        transform: scaleX(1);
    }

    .mode-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        padding: 1rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #667eea20, #764ba220);
        backdrop-filter: blur(10px);
    }

    .mode-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        color: #1a202c;
        background: linear-gradient(135deg, #2d3748, #4a5568);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .mode-desc {
        color: #718096;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .stButton button {
        border-radius: 14px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }

    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .result-box {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border-left: 6px solid #667eea;
        margin: 2rem 0;
        position: relative;
    }

    .result-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.03), rgba(118, 75, 162, 0.03));
        pointer-events: none;
    }

    .section-header {
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
    }

    .section-header h2 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .back-button {
        background: linear-gradient(135deg, #f7fafc, #edf2f7) !important;
        color: #4a5568 !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }

    .back-button:hover {
        background: linear-gradient(135deg, #edf2f7, #e2e8f0) !important;
        transform: translateY(-1px) !important;
    }

    .input-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.3);
    }

    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        font-size: 0.95rem;
    }

    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .file-uploader {
        border: 2px dashed #cbd5e0;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        background: rgba(248, 250, 252, 0.5);
    }

    .file-uploader:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }

    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
    }

    .footer {
        text-align: center;
        padding: 3rem 0 1rem;
        color: #718096;
        position: relative;
    }

    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 25%;
        right: 25%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }

    @media (max-width: 768px) {
        .mode-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .main-header {
            padding: 2rem 1rem;
            margin-bottom: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------
# Header Section
# --------------------------------
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 0.5rem;">💬 ToneFlo</h1>
    <p style="font-size: 1.4rem; font-weight: 300; margin-bottom: 1rem; opacity: 0.95">
        Emotional Intelligence for Your Conversations
    </p>
    <p style="font-size: 1.1rem; opacity: 0.9; max-width: 600px; margin: 0 auto; line-height: 1.6;">
        Your AI conversational co-pilot for confident, emotionally intelligent communication
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------
# ToneFlo Modes - Enhanced Card Layout
# --------------------------------
st.markdown("""
<div class="section-header">
    <h2 class="gradient-text" style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
        Choose Your Mode
    </h2>
    <p style="color: #718096; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
        Select how you'd like to enhance your conversation with AI-powered emotional intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# Create columns for the grid
col1, col2, col3, col4 = st.columns(4)

modes = [
    {
        "icon": "🧠",
        "title": "Decode",
        "description": "Analyze emotional tone and conversation patterns with AI-powered insights",
        "key": "decode",
        "color": "#667eea"
    },
    {
        "icon": "💬",
        "title": "Start",
        "description": "Craft perfect conversation openers tailored to any situation",
        "key": "start",
        "color": "#764ba2"
    },
    {
        "icon": "🔄",
        "title": "Sustain",
        "description": "Keep the conversation flowing naturally with engaging follow-ups",
        "key": "sustain",
        "color": "#f093fb"
    },
    {
        "icon": "❤️",
        "title": "Revive",
        "description": "Reignite stalled conversations with thoughtful revival strategies",
        "key": "revive",
        "color": "#f5576c"
    }
]

for i, mode in enumerate(modes):
    with [col1, col2, col3, col4][i]:
        with st.container():
            st.markdown(f"""
            <div class="mode-card">
                <div class="mode-icon">{mode['icon']}</div>
                <div class="mode-title">{mode['title']}</div>
                <div class="mode-desc">{mode['description']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"✨ Select {mode['title']}", key=f"btn_{mode['key']}", use_container_width=True):
                st.session_state["tone_action"] = mode['key']
                st.rerun()

# --------------------------------
# OpenAI Client Setup
# --------------------------------
api_key = st.secrets.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE")
client = OpenAI(api_key=api_key)


# --------------------------------
# Helper Function
# --------------------------------
def generate_ai_response(prompt=None, messages=None, max_tokens=350):
    try:
        if messages is None:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are ToneFlo — an emotionally intelligent AI assistant "
                        "that helps users understand and improve digital communication. "
                        "You respond with empathy, insight, and natural tone awareness."
                    ),
                },
                {"role": "user", "content": [{"type": "text", "text": prompt}]},
            ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.8,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error("😅 ToneFlo couldn't process your request.")
        st.write(e)
        return None


# --------------------------------
# Action Logic with Enhanced UI
# --------------------------------
if "tone_action" in st.session_state:
    action = st.session_state["tone_action"]

    # Enhanced back button
    st.markdown("""
    <div style="margin-bottom: 2rem;">
    </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_left:
        if st.button("← Back to All Modes", use_container_width=True, key="back_btn"):
            del st.session_state["tone_action"]
            st.rerun()

    # --------------------------
    # 1️⃣ Decode
    # --------------------------
    if action == "decode":
        st.markdown("""
        <div class="section-header">
            <h2 class="gradient-text" style="font-size: 2.5rem; font-weight: 700;">🧠 Decode Emotional Tone</h2>
            <p style="color: #718096; font-size: 1.2rem;">
                Upload chat screenshots or paste a conversation to analyze its emotional tone and patterns
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                <div style="text-align: center; margin-bottom: 1rem;">
                    <h4 style="color: #2d3748; margin-bottom: 0.5rem;">📸 Visual Analysis</h4>
                    <p style="color: #718096; font-size: 0.9rem;">Upload chat screenshots for AI analysis</p>
                </div>
                """, unsafe_allow_html=True)
                uploaded_files = st.file_uploader(
                    "Drop chat screenshots here",
                    type=["png", "jpg", "jpeg"],
                    accept_multiple_files=True,
                    help="Upload images of your conversation for emotional tone analysis",
                    label_visibility="collapsed"
                )

            with col2:
                st.markdown("""
                <div style="text-align: center; margin-bottom: 1rem;">
                    <h4 style="color: #2d3748; margin-bottom: 0.5rem;">💭 Text Analysis</h4>
                    <p style="color: #718096; font-size: 0.9rem;">Paste your conversation text directly</p>
                </div>
                """, unsafe_allow_html=True)
                chat_text = st.text_area(
                    "Paste your conversation here",
                    height=200,
                    placeholder="Example conversation:\nYou: Hey, how was your day?\nThem: It was okay, pretty busy with work\nYou: Hope you get some rest soon!\nThem: Thanks, me too. How about you?",
                    help="Enter the conversation you want to analyze for emotional tone",
                    label_visibility="collapsed"
                )
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔍 Analyze Conversation with AI", use_container_width=True, type="primary"):
            with st.spinner("🔮 Analyzing emotional tone and conversation patterns..."):
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are ToneFlo — an expert in emotional intelligence and communication. "
                            "Analyze the tone, rhythm, and emotional alignment of the conversation. "
                            "Focus on authenticity, empathy, and connection — not grammar."
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": chat_text or "Analyze uploaded screenshots."}
                        ],
                    },
                ]

                # Add screenshots if any
                for file in uploaded_files or []:
                    image = Image.open(file)
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    b64_image = base64.b64encode(buf.getvalue()).decode("utf-8")
                    messages[-1]["content"].append(
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}}
                    )

                result = generate_ai_response(messages=messages, max_tokens=600)
                if result:
                    st.markdown("""
                    <div class="result-box">
                        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                            <div style="font-size: 2rem; margin-right: 1rem;">📊</div>
                            <h3 style="color: #2d3748; margin: 0; font-size: 1.5rem;">Analysis Results</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info(result)

    # --------------------------
    # 2️⃣ Start
    # --------------------------
    elif action == "start":
        st.markdown("""
        <div class="section-header">
            <h2 class="gradient-text" style="font-size: 2.5rem; font-weight: 700;">💬 Start a Conversation</h2>
            <p style="color: #718096; font-size: 1.2rem;">
                Craft the perfect opening message for any situation with AI-powered suggestions
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        context = st.text_area(
            "🎯 Describe your situation",
            placeholder="Examples:\n• Reaching out to a new match on a dating app who loves hiking\n• Reconnecting with an old friend from college after 5 years\n• Starting a conversation with a colleague you admire\n• Messaging someone after a networking event where you discussed AI",
            height=150,
            help="Provide context about who you're messaging and the situation"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🚀 Generate Smart Openers", use_container_width=True, type="primary"):
            with st.spinner("✨ Crafting authentic, emotionally intelligent openers..."):
                prompt = (
                    f"Context: {context}\n\n"
                    "Suggest 3 authentic, emotionally intelligent openers. "
                    "They should sound confident yet natural — no forced humor or pickup lines. "
                    "Match the tone to the situation (warm, curious, thoughtful, friendly)."
                )
                result = generate_ai_response(prompt)
                if result:
                    st.markdown("""
                    <div class="result-box">
                        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                            <div style="font-size: 2rem; margin-right: 1rem;">💡</div>
                            <h3 style="color: #2d3748; margin: 0; font-size: 1.5rem;">Suggested Openers</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success(result)

    # --------------------------
    # 3️⃣ Sustain
    # --------------------------
    elif action == "sustain":
        st.markdown("""
        <div class="section-header">
            <h2 class="gradient-text" style="font-size: 2.5rem; font-weight: 700;">🔄 Sustain the Flow</h2>
            <p style="color: #718096; font-size: 1.2rem;">
                Keep the conversation going with natural, engaging follow-ups powered by AI
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        ongoing_chat = st.text_area(
            "💬 Paste your conversation",
            placeholder="Paste the recent conversation...\n\nExample:\nYou: How was your weekend?\nThem: It was good! Went hiking on Saturday with some friends\nYou: That sounds amazing! Which trail did you do?\nThem: We did the Eagle Rock trail - the views were incredible",
            height=200,
            help="Enter the current conversation to get natural follow-up suggestions"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("💬 Generate Engaging Follow-ups", use_container_width=True, type="primary"):
            with st.spinner("🔄 Finding natural, emotionally intelligent ways to continue..."):
                prompt = (
                    f"Chat snippet: {ongoing_chat}\n\n"
                    "Suggest 3–4 natural, emotionally intelligent follow-ups to keep the conversation flowing. "
                    "Keep it warm, curious, and authentic — no robotic phrasing."
                )
                result = generate_ai_response(prompt)
                if result:
                    st.markdown("""
                    <div class="result-box">
                        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                            <div style="font-size: 2rem; margin-right: 1rem;">🎯</div>
                            <h3 style="color: #2d3748; margin: 0; font-size: 1.5rem;">Conversation Continuations</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info(result)

    # --------------------------
    # 4️⃣ Revive
    # --------------------------
    elif action == "revive":
        st.markdown("""
        <div class="section-header">
            <h2 class="gradient-text" style="font-size: 2.5rem; font-weight: 700;">❤️ Revive the Conversation</h2>
            <p style="color: #718096; font-size: 1.2rem;">
                Breathe new life into stalled conversations with thoughtful revival strategies
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        stalled_text = st.text_area(
            "📝 Where did things pause?",
            placeholder="Examples:\n• They stopped responding after you asked about their weekend plans\n• Conversation died after discussing work projects\n• You've been left on read for a few days after sending a message about meeting up\n• Last exchange was about movie recommendations but they didn't respond",
            height=150,
            help="Provide context about where the conversation stalled"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔥 Generate Revival Messages", use_container_width=True, type="primary"):
            with st.spinner("❤️ Crafting thoughtful revival strategies..."):
                prompt = (
                    f"Stalled chat: {stalled_text}\n\n"
                    "Suggest 2–3 emotionally aware ways to revive the conversation. "
                    "Avoid desperation or overthinking — focus on lightness, humor, or authentic curiosity."
                )
                result = generate_ai_response(prompt)
                if result:
                    st.markdown("""
                    <div class="result-box">
                        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                            <div style="font-size: 2rem; margin-right: 1rem;">✨</div>
                            <h3 style="color: #2d3748; margin: 0; font-size: 1.5rem;">Revival Strategies</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success(result)

# --------------------------------
# Footer
# --------------------------------
st.markdown("""
<div class="footer">
    <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #4a5568;">
        💬 ToneFlo — Emotional Intelligence for Conversations
    </p>
    <p style="font-size: 1rem; font-style: italic; color: #718096;">
        Because connection is a rhythm, not a script
    </p>
</div>
""", unsafe_allow_html=True)