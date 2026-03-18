"""
InsightPulse AI - Shared UI Utilities v5.0
=====================================================================
CSS injection, API call wrappers, and shared constants.
All backend calls route through this layer for consistency.
"""
import streamlit as st
import requests
import pandas as pd
import os
from pathlib import Path

# Backend URL - configurable via environment
BACKEND = os.environ.get("BACKEND_URL", "http://localhost:8000")

TIMEOUT_GENERATE = 90   # NL -> SQL -> Charts can take up to 90s on large datasets
TIMEOUT_UPLOAD   = 60
TIMEOUT_QUICK    = 5


def is_dark() -> bool:
    return st.session_state.get("theme", "dark") == "dark"


def inject_css():
    st.markdown("""
<style>
/* ═══════════════════════════════════════════════════
   InsightPulse AI - Global Design System v5.0
   Dark-first, sci-fi neon, enterprise quality
═══════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
  --bg:       #080818;
  --surface:  #0F0F2A;
  --card:     #13132E;
  --border:   rgba(99,102,241,0.15);
  --txt:      #E2E8F0;
  --txt-mute: #64748B;
  --purple:   #6366F1;
  --violet:   #8B5CF6;
  --pink:     #EC4899;
  --teal:     #14B8A6;
  --grad:     linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
  --glow:     0 0 20px rgba(99,102,241,0.25);
}

/* Base */
.stApp, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  font-family: 'Inter', 'Outfit', sans-serif !important;
}
* { font-family: 'Inter', 'Outfit', sans-serif !important; }
h1, h2, h3, h4 { color: var(--txt) !important; font-weight: 800 !important; }

/* Sidebar */
[data-testid="stSidebar"] {
  background: rgba(13,13,40,0.95) !important;
  border-right: 1px solid var(--border) !important;
  backdrop-filter: blur(20px) !important;
}
[data-testid="stSidebar"] * { color: var(--txt) !important; }

/* Cards */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.3), var(--glow);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.card:hover {
  border-color: rgba(99,102,241,0.35);
  box-shadow: 0 8px 40px rgba(0,0,0,0.4), 0 0 30px rgba(99,102,241,0.2);
}

/* Gradient text */
.gradient-text {
  background: var(--grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent !important;
}

/* Metric pills */
.metric-pill {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  background: rgba(99,102,241,0.12);
  border: 1px solid rgba(99,102,241,0.25);
  color: #A5B4FC !important;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.3px;
}

/* Badge variants */
.badge-ok  { background: rgba(16,185,129,0.15); color: #34D399 !important;
             padding: 3px 10px; border-radius: 6px; font-weight: 700; font-size: 0.8rem; }
.badge-err { background: rgba(239,68,68,0.15);  color: #F87171 !important;
             padding: 3px 10px; border-radius: 6px; font-weight: 700; font-size: 0.8rem; }
.badge-warn{ background: rgba(245,158,11,0.15); color: #FCD34D !important;
             padding: 3px 10px; border-radius: 6px; font-weight: 700; font-size: 0.8rem; }

/* Insight rows */
.insight-row {
  background: rgba(99,102,241,0.06);
  border-left: 3px solid var(--purple);
  padding: 8px 14px;
  border-radius: 0 8px 8px 0;
  margin: 6px 0;
  font-size: 0.88rem;
  color: var(--txt);
  line-height: 1.5;
}

/* SQL box */
.sql-box {
  background: rgba(10,10,30,0.8);
  border: 1px solid rgba(99,102,241,0.2);
  border-radius: 10px;
  padding: 12px 16px;
  font-family: 'Courier New', monospace !important;
  font-size: 0.82rem;
  color: #A5B4FC;
  overflow-x: auto;
  white-space: pre-wrap;
}

/* Streamlit metric cards */
div[data-testid="stMetric"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: 14px 18px !important;
  box-shadow: var(--glow) !important;
}
div[data-testid="stMetricValue"] { color: #A5B4FC !important; font-weight: 800 !important; }
div[data-testid="stMetricLabel"] { color: var(--txt-mute) !important; font-size: 0.82rem !important; }

/* Buttons */
.stButton > button {
  border-radius: 10px !important;
  font-weight: 600 !important;
  transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
  border: none !important;
  box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  margin: 6px 0 !important;
}

/* Progress bar */
.stProgress > div > div {
  background: var(--grad) !important;
}

/* Expander */
.streamlit-expanderHeader {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
  background: rgba(99,102,241,0.04) !important;
  border: 2px dashed rgba(99,102,241,0.25) !important;
  border-radius: 14px !important;
}

/* Tabs */
[data-testid="stTabs"] button {
  font-weight: 600 !important;
  color: var(--txt-mute) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--purple) !important;
  border-bottom: 2px solid var(--purple) !important;
}

/* EMERGENCY visibility guardrails */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"] {
  visibility: visible !important;
  opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)


FLOATING_CHATBOT_HTML = """
<div id="ip-fab" onclick="toggleChat()"
  style="position:fixed;bottom:28px;right:28px;width:58px;height:58px;border-radius:50%;
         background:linear-gradient(135deg,#6366F1,#8B5CF6);display:flex;align-items:center;
         justify-content:center;cursor:pointer;z-index:9999;font-size:1.6rem;
         box-shadow:0 8px 32px rgba(99,102,241,0.5);transition:transform 0.2s;"
  onmouseenter="this.style.transform='scale(1.12)'"
  onmouseleave="this.style.transform='scale(1)'">[ENGINE]</div>

<div id="ip-chat"
  style="display:none;position:fixed;bottom:100px;right:28px;width:360px;height:480px;
         background:rgba(8,8,24,0.97);border:1px solid rgba(99,102,241,0.3);border-radius:20px;
         z-index:9998;flex-direction:column;overflow:hidden;
         box-shadow:0 16px 64px rgba(0,0,0,0.6),0 0 30px rgba(99,102,241,0.15);
         backdrop-filter:blur(20px);">
  <div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);padding:14px 18px;
              display:flex;justify-content:space-between;align-items:center;">
    <span style="color:#fff;font-weight:700;font-size:0.95rem;">[ENGINE] InsightPulse Assistant</span>
    <span onclick="toggleChat()" style="color:rgba(255,255,255,0.7);cursor:pointer;font-size:1.2rem;">✕</span>
  </div>
  <div id="ip-msgs"
    style="flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:8px;"></div>
  <div style="padding:10px;background:rgba(15,15,40,0.8);border-top:1px solid rgba(99,102,241,0.15);
              display:flex;gap:6px;">
    <input id="ip-input" placeholder="Ask anything about your data..."
      style="flex:1;background:rgba(15,15,35,0.8);border:1px solid rgba(99,102,241,0.25);
             color:#E2E8F0;padding:9px 12px;border-radius:10px;outline:none;font-size:0.85rem;"
      onkeypress="if(event.key==='Enter')sendMsg()"/>
    <button onclick="sendMsg()"
      style="background:linear-gradient(135deg,#6366F1,#8B5CF6);border:none;color:#fff;
             border-radius:10px;padding:0 14px;cursor:pointer;font-weight:600;">Go</button>
  </div>
</div>

<script src="https://js.puter.com/v2/"></script>
<script>
let chatVisible = false;
function toggleChat() {
  chatVisible = !chatVisible;
  const c = document.getElementById('ip-chat');
  c.style.display = chatVisible ? 'flex' : 'none';
  if (chatVisible && document.getElementById('ip-msgs').children.length === 0) {
    addMsg('AI', '👋 Hi! I\'m your InsightPulse AI assistant. Ask me anything about your data!');
  }
}
function addMsg(role, txt) {
  const d = document.getElementById('ip-msgs');
  const m = document.createElement('div');
  const isAI = role === 'AI';
  m.style.cssText = `max-width:85%;padding:9px 12px;border-radius:${isAI?'4px 12px 12px':'12px 4px 12px'} 12px;
    background:${isAI?'rgba(99,102,241,0.12)':'rgba(139,92,246,0.12)'};
    color:#E2E8F0;font-size:0.84rem;line-height:1.5;align-self:${isAI?'flex-start':'flex-end'};
    border:1px solid rgba(99,102,241,0.15);`;
  m.innerHTML = `<span style="font-size:0.7rem;color:#64748B;display:block;margin-bottom:3px;">${role}</span>${txt}`;
  d.appendChild(m);
  d.scrollTop = d.scrollHeight;
}
async function sendMsg() {
  const i = document.getElementById('ip-input');
  const m = i.value.trim();
  if (!m) return;
  addMsg('You', m);
  i.value = '';
  try {
    const r = await puter.ai.chat(m);
    const txt = typeof r === 'string' ? r : (r?.message?.content || 'How can I help with your data?');
    addMsg('AI', txt);
  } catch(e) {
    addMsg('AI', '💡 Use the main chat panel for full AI-powered data analysis!');
  }
}
</script>
"""


# ── API Call wrappers

def api_health():
    try:
        r = requests.get(f"{BACKEND}/health", timeout=TIMEOUT_QUICK)
        return r.ok, (r.json() if r.ok else {})
    except Exception:
        return False, {}


def api_upload(file):
    try:
        r = requests.post(
            f"{BACKEND}/upload",
            files={"file": (file.name, file.getvalue(), "application/octet-stream")},
            timeout=TIMEOUT_UPLOAD
        )
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def api_generate(query: str, session_id: str, history: list):
    """Call /generate and return the full response dict."""
    try:
        r = requests.post(
            f"{BACKEND}/generate",
            json={"query": query, "session_id": session_id,
                  "chat_history": history[-6:]},   # last 3 exchanges
            timeout=TIMEOUT_GENERATE
        )
        return r.json()
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}


def api_analyze(payload: dict):
    try:
        r = requests.post(f"{BACKEND}/analyze", json=payload, timeout=90)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def api_profile():
    try:
        r = requests.get(f"{BACKEND}/profile", timeout=15)
        return r.json() if r.ok else {}
    except Exception:
        return {}


def api_distributions():
    try:
        r = requests.get(f"{BACKEND}/distributions", timeout=15)
        return r.json() if r.ok else {}
    except Exception:
        return {}


def api_sample_queries():
    try:
        r = requests.get(f"{BACKEND}/sample-queries", timeout=TIMEOUT_QUICK)
        return r.json() if r.ok else []
    except Exception:
        return []


def api_schema():
    try:
        r = requests.get(f"{BACKEND}/schema", timeout=TIMEOUT_QUICK)
        return r.json() if r.ok else {}
    except Exception:
        return {}
