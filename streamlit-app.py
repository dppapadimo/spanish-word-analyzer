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
# Analysis
# -----------------------------
if st.button("Analizar") and word:
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
    st.markdown(f"### {item['text']}")
    st.write(f"- Lemma (ρίζα): {item['lemma']}")
    st.write(f"- Part of Speech: {item['pos']}")
    st.write(f"- Tag: {item['tag']}")
    st.write(f"- Morphology: {item['morph']}")
    st.write("---")
