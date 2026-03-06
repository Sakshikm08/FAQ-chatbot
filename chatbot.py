import streamlit as st
import requests

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a0a0f 0%, #0f1a2e 50%, #0a0f1a 100%); min-height: 100vh; }
.title { font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 700; background: linear-gradient(135deg, #f8f6ff, #67e8f9, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 4px; }
.badge { text-align: center; color: #38bdf8; font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 8px; }
.subtitle { text-align: center; color: rgba(232,230,240,0.45); font-size: 14px; margin-bottom: 28px; }
.user-msg { background: linear-gradient(135deg, #1e40af, #1d4ed8); border-radius: 18px 18px 4px 18px; padding: 12px 18px; margin: 8px 0; margin-left: 15%; color: #fff; font-size: 14px; line-height: 1.7; }
.bot-msg { background: rgba(255,255,255,0.07); border: 1px solid rgba(56,189,248,0.2); border-radius: 18px 18px 18px 4px; padding: 12px 18px; margin: 8px 0; margin-right: 15%; color: #e8e6f0; font-size: 14px; line-height: 1.7; }
.error-msg { background: rgba(251,113,133,0.1); border: 1px solid rgba(251,113,133,0.25); border-radius: 18px 18px 18px 4px; padding: 12px 18px; margin: 8px 0; margin-right: 15%; color: #fda4af; font-size: 14px; }
.chat-container { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 20px; padding: 20px; min-height: 350px; max-height: 500px; overflow-y: auto; margin-bottom: 16px; }
.stTextInput input { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(56,189,248,0.25) !important; border-radius: 14px !important; color: #e8e6f0 !important; font-size: 14px !important; padding: 12px 16px !important; }
.stButton > button { background: linear-gradient(135deg, #0ea5e9, #38bdf8) !important; color: #0a0a0f !important; border: none !important; border-radius: 14px !important; font-weight: 600 !important; font-size: 14px !important; width: 100% !important; padding: 12px !important; }
.topic-btn { background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.2); border-radius: 20px; padding: 6px 14px; color: #38bdf8; font-size: 12px; display: inline-block; margin: 3px; }
label { color: rgba(232,230,240,0.5) !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="badge">⚡ Powered by Groq AI · Free API · Ultra Fast</div>', unsafe_allow_html=True)
st.markdown('<div class="title">AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask me anything — Science, Math, History, Coding, Health, Law & more</div>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; margin-bottom:20px;'>
  <span class='topic-btn'>🔬 Science</span>
  <span class='topic-btn'>💻 Coding</span>
  <span class='topic-btn'>📚 History</span>
  <span class='topic-btn'>🏥 Health</span>
  <span class='topic-btn'>⚖️ Law</span>
  <span class='topic-btn'>🧮 Math</span>
  <span class='topic-btn'>🌍 Geography</span>
  <span class='topic-btn'>💰 Finance</span>
</div>
""", unsafe_allow_html=True)

API_KEY = "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"
MODEL   = "llama-3.3-70b-versatile"

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "pending" not in st.session_state:
    st.session_state.pending = None

def ask_groq(user_message, history):
    history.append({"role": "user", "content": user_message})
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": MODEL,
            "messages": [{"role": "system", "content": "You are a helpful, friendly, and knowledgeable AI assistant. Answer questions clearly and concisely from any field including science, math, history, coding, health, law, finance, geography, and more."}] + history,
            "max_tokens": 1024,
            "temperature": 0.7
        }
    )
    data = response.json()
    if "choices" in data and data["choices"]:
        reply = data["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": reply})
        return reply, history
    elif "error" in data:
        return f"Error: {data['error']['message']}", history
    return None, history

# Process pending message BEFORE rendering input
if st.session_state.pending:
    user_msg = st.session_state.pending
    st.session_state.pending = None
    st.session_state.messages.append({"role": "user", "text": user_msg})
    with st.spinner("Thinking..."):
        reply, updated_history = ask_groq(user_msg, st.session_state.history)
    if reply:
        st.session_state.history = updated_history
        st.session_state.messages.append({"role": "bot", "text": reply})
    else:
        st.session_state.messages.append({"role": "error", "text": "Something went wrong. Please try again."})

# Chat display
chat_html = '<div class="chat-container">'
if not st.session_state.messages:
    chat_html += '<div class="bot-msg">👋 Hi! I\'m your AI assistant. Ask me <b>anything</b> — science, math, coding, history, health, and more!</div>'
for msg in st.session_state.messages:
    if msg["role"] == "user":
        chat_html += f'<div class="user-msg">🧑 {msg["text"]}</div>'
    elif msg["role"] == "bot":
        text = msg["text"].replace("\n", "<br>")
        chat_html += f'<div class="bot-msg">🤖 {text}</div>'
    elif msg["role"] == "error":
        chat_html += f'<div class="error-msg">⚠️ {msg["text"]}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Input — key changes on each submit to clear the box
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Ask anything",
        placeholder="Type your question and press Enter or click Send…",
        label_visibility="collapsed",
        key=f"chat_input_{st.session_state.input_key}"
    )
with col2:
    send = st.button("Send ➤")

if (send or user_input) and user_input.strip():
    st.session_state.pending = user_input.strip()
    st.session_state.input_key += 1  # clears the input box
    st.rerun()

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.history = []
    st.session_state.pending = None
    st.rerun()