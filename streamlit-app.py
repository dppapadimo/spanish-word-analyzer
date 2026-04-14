import streamlit as st
import spacy

# -----------------------------
# Load spaCy model
# -----------------------------
@st.cache_resource
def load_model():
    return spacy.load("es_core_news_sm")

nlp = load_model()

# -----------------------------
# UI
# -----------------------------
st.title("Spanish Word Analyzer 🇪🇸")

word = st.text_input("Escribe una palabra en español:")

# -----------------------------
# Session state
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Buttons
# -----------------------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    analyze = st.button("Analizar")

with col_btn2:
    clear = st.button("Καθαρισμός")

if clear:
    st.session_state.history = []

# -----------------------------
# Analysis
# -----------------------------
if analyze and word:
    doc = nlp(word)

    for token in doc:
        st.session_state.history.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "morph": str(token.morph)
        })

# -----------------------------
# Output
# -----------------------------
st.subheader("Resultados")

for item in st.session_state.history:

    # 🔎 Highlight λέξης
    st.markdown(f"## 🔎 {item['text']}")

    # 🧱 Card UI
    st.markdown(f"""
    <div style="
        background-color:#1e1e1e;
        padding:15px;
        border-radius:10px;
        margin-bottom:10px;
    ">
    """, unsafe_allow_html=True)

    # 📊 Columns
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Lemma (ρίζα):**", item["lemma"])
        st.write("**POS:**", item["pos"])

    with col2:
        st.write("**Tag:**", item["tag"])
        st.write("**Morphology:**", item["morph"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
