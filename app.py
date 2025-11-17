# ---------------------------------------------------------
#  Genesis MedAI - Polished Streamlit UI
# ---------------------------------------------------------

import os, json, time
from datetime import datetime
import streamlit as st

from src.utils.image_utils import read_prescription
from src.utils.audio_utils import transcribe_audio, generate_notes
from src.utils.video_utils import analyze_video_posture
from src.utils.chat_utils import chat_assistant

# ---------------------------------------------------------
# Basic Setup
# ---------------------------------------------------------
ASSET_TEMP = "assets/temp"
HISTORY_PATH = os.path.join(ASSET_TEMP, "history.json")
LOGO_PATH = "assets/logo.png"

st.set_page_config(
    page_title="Genesis MedAI",
    page_icon=LOGO_PATH,
    layout="wide",
)

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def ensure_dirs():
    os.makedirs(ASSET_TEMP, exist_ok=True)

ensure_dirs()


def save_uploaded_file(uploaded_file, folder=ASSET_TEMP):
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path


def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH, "r") as f:
        return json.load(f)


def save_history(entry):
    history = load_history()
    history.insert(0, entry)
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.image(LOGO_PATH, use_container_width = True)
    st.markdown("### **Genesis MedAI**")
    st.markdown("Your multimodal healthcare assistant.")

    if st.button("🗑 Clear History"):
        if os.path.exists(HISTORY_PATH):
            os.remove(HISTORY_PATH)
        st.success("History cleared!")


# Title + Description
st.markdown(
    """
    <div style='padding: 10px 0 10px 0;'>
        <h1 style='color:#20B2AA;'>Genesis MedAI</h1>
        <p style='font-size:18px; color:gray;'>
            A multimodal AI assistant that reads prescriptions, analyzes posture, transcribes audio, 
            and answers general health questions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
tabs = st.tabs(
    [
        "🧾 Prescription Reader",
        "🎥 Posture Analysis",
        "💬 Chat Assistant",
        "🎤 Audio Notes",
        "🗂 History",
    ]
)

# ---------------------------------------------------------
# Progress Wrapper
# ---------------------------------------------------------
def run_with_progress(func, *args):
    progress = st.progress(0)

    def update_progress(frac):
        progress.progress(int(frac * 100))

    return func(*args, progress_callback=update_progress)


# ---------------------------------------------------------
# TAB 1 — Prescription Reader
# ---------------------------------------------------------
with tabs[0]:
    st.subheader("📌 Upload a Prescription Image")
    st.markdown("AI will extract text and structure it clearly.")

    file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    if file and st.button("📖 Read Prescription"):
        path = save_uploaded_file(file)

        with st.spinner("Reading prescription..."):
            result = read_prescription(path)

        st.success("Done!")
        st.text_area("Extracted Text:", result, height=180)

        save_history({
            "type": "prescription",
            "input": path,
            "result": result,
            "timestamp": str(datetime.now())
        })


# ---------------------------------------------------------
# TAB 2 — Posture Analysis
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("🎥 Upload Exercise / Physiotherapy Video")
    st.markdown("AI will detect posture issues and give general guidance.")

    video = st.file_uploader("Upload video", type=["mp4", "mov", "avi"])

    if video and st.button("🧠 Analyze Posture"):
        path = save_uploaded_file(video)

        result = run_with_progress(analyze_video_posture, path)

        st.text_area("Posture Report:", result, height=220)

        save_history({
            "type": "video",
            "input": path,
            "result": result,
            "timestamp": str(datetime.now())
        })


# ---------------------------------------------------------
# TAB 3 — Chat Assistant
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("💬 Ask a general health question")
    st.markdown("AI gives safe, non-medical guidance only.")

    question = st.text_input("Your question:")

    if st.button("Ask AI"):
        if question.strip():
            answer = run_with_progress(chat_assistant, question)
            st.text_area("AI Answer:", answer, height=200)

            save_history({
                "type": "chat",
                "input": question,
                "result": answer,
                "timestamp": str(datetime.now())
            })


# ---------------------------------------------------------
# TAB 4 — Audio Transcription + Notes
# ---------------------------------------------------------
with tabs[3]:
    st.subheader("🎤 Upload Doctor–Patient Conversation")
    st.markdown("AI transcribes and converts speech into structured notes.")

    audio = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a"])

    if audio and st.button("🎧 Generate Notes"):
        path = save_uploaded_file(audio)

        with st.spinner("Transcribing..."):
            raw = transcribe_audio(path)

        with st.spinner("Summarizing notes..."):
            notes = generate_notes(raw)

        st.text_area("Structured Notes:", notes, height=220)

        save_history({
            "type": "audio",
            "input": path,
            "result": notes,
            "timestamp": str(datetime.now())
        })


# ---------------------------------------------------------
# TAB 5 — History
# ---------------------------------------------------------
with tabs[4]:
    st.subheader("🗂 Past Results")
    history = load_history()

    if not history:
        st.info("No history yet.")
    else:
        for i, item in enumerate(history):
            st.markdown(f"### 📝 {item['type'].capitalize()} — {item['timestamp']}")
            st.text_area("", item["result"], key=f"hist_{i}", height=150)
            st.markdown("---")
