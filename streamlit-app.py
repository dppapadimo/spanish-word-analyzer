import streamlit as st
import spacy

# Load Spanish model
@st.cache_resource
def load_model():
    return spacy.load("es_core_news_sm")

nlp = load_model()

st.title("Spanish Word Analyzer")

# Input
word = st.text_input("Escribe una palabra en español:")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Analizar") and word:
    doc = nlp(word)

    for token in doc:
        info = {
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "morph": token.morph
        }
        st.session_state.history.append(info)

# Display results
st.subheader("Resultados")

for item in st.session_state.history:
    st.write(f"**{item['text']}**")
    st.write(f"- Lemma (ρίζα): {item['lemma']}")
    st.write(f"- Parte del discurso: {item['pos']}")
    st.write(f"- Tag: {item['tag']}")
    st.write(f"- Morfología: {item['morph']}")
    st.write("---")
