import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# =========================
# Load Environment
# =========================
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# Konfigurasi Halaman
# =========================
st.set_page_config(
    page_title="Naruto Chatbot",
    page_icon="🍥",
    layout="centered"
)

# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("🍥 Naruto AI")

    st.write(
        "Ngobrol dengan Naruto Uzumaki "
        "yang siap menyemangatimu!"
    )

    mood = st.selectbox(
        "Pilih Mood Naruto",
        [
            "Semangat",
            "Bijak",
            "Lucu"
        ]
    )

    st.divider()

    if st.button("🗑️ Hapus Riwayat"):
        st.session_state.messages = []
        st.rerun()

# =========================
# Judul
# =========================
st.title("🍜 Naruto Chatbot")

st.caption(
    "Teman curhat virtual ala Naruto Uzumaki"
)

# =========================
# Tampilkan Riwayat Chat
# =========================
for message in st.session_state.messages:

    avatar = "🙂"

    if message["role"] == "assistant":
        avatar = "🍥"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.write(message["content"])

# =========================
# Input User
# =========================
user_input = st.chat_input(
    "Tulis pesanmu..."
)

if user_input:

    # Simpan pesan user
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Tampilkan pesan user
    with st.chat_message(
        "user",
        avatar="🙂"
    ):
        st.write(user_input)

    # =========================
    # Membuat History Chat
    # =========================
    history = ""

    for msg in st.session_state.messages:
        history += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    # =========================
    # Prompt Naruto
    # =========================
    prompt = f"""
Kamu adalah Naruto Uzumaki.

Karakter Naruto:
- Ramah
- Optimis
- Suka memberi semangat
- Peduli pada teman
- Sesekali mengatakan "Dattebayo!"
- Selalu menjawab dalam Bahasa Indonesia

Mood Naruto saat ini:
{mood}

Jika mood:
- Semangat → penuh energi dan motivasi
- Bijak → lebih tenang dan reflektif
- Lucu → suka bercanda ringan

Riwayat Percakapan:
{history}

Tugas:
Jawab pesan terakhir user sebagai Naruto.
"""

    # =========================
    # Request ke Gemini
    # =========================
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    bot_reply = response.text

    # Simpan jawaban AI
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

    # Tampilkan jawaban AI
    with st.chat_message(
        "assistant",
        avatar="🍥"
    ):
        st.write(bot_reply)