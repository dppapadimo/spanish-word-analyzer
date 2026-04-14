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
# POS mapping (Spanish)
# -----------------------------
POS_MAP_ES = {
    "VERB": "verbo",
    "NOUN": "sustantivo",
    "ADJ": "adjetivo",
    "ADV": "adverbio",
    "PRON": "pronombre",
    "DET": "determinante",
    "ADP": "preposición",
    "AUX": "verbo auxiliar",
    "PROPN": "nombre propio",
    "CCONJ": "conjunción",
    "SCONJ": "conjunción subordinante",
    "NUM": "número",
    "INTJ": "interjección"
}

# -----------------------------
# Morphology mapping (Spanish)
# -----------------------------
TENSE_MAP = {
    "Pres": "presente",
    "Past": "pretérito",
    "Imp": "imperfecto",
    "Fut": "futuro"
}

PERSON_MAP = {
    "1": "yo",
    "2": "tú",
    "3": "él/ella"
}

NUMBER_MAP = {
    "Sing": "singular",
    "Plur": "plural"
}

# -----------------------------
# Extract verb info
# -----------------------------
def analyze_verb(token):
    morph = token.morph

    tense = morph.get("Tense")
    person = morph.get("Person")
    number = morph.get("Number")

    result = {}

    if tense:
        result["Tiempo"] = TENSE_MAP.get(tense[0], tense[0])

    if person:
        result["Persona"] = PERSON_MAP.get(person[0], person[0])

    if number:
        result["Número"] = NUMBER_MAP.get(number[0], number[0])

    return result

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
    clear = st.button("Limpiar")

if clear:
    st.session_state.history = []

# -----------------------------
# Analysis
# -----------------------------
if analyze and word:
    doc = nlp(word)

    for token in doc:
        verb_info = analyze_verb(token) if token.pos_ in ["VERB", "AUX"] else {}

        st.session_state.history.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "morph": str(token.morph),
            "verb_info": verb_info
        })

# -----------------------------
# Output
# -----------------------------
st.subheader("Resultados")

for item in st.session_state.history:

    # 🔎 Highlight
    st.markdown(f"## 🔎 {item['text']}")

    # 🧱 Card
    st.markdown("""
    <div style="
        background-color:#1e1e1e;
        padding:15px;
        border-radius:10px;
        margin-bottom:10px;
    ">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Lema:**", item["lemma"])
        st.write("**Parte del discurso:**", POS_MAP_ES.get(item["pos"], item["pos"]))

    with col2:
        st.write("**Etiqueta:**", item["tag"])
        st.write("**Morfología:**", item["morph"])

    # 🔥 Verb extra analysis
    if item["verb_info"]:
        st.write("### 🔥 Análisis del verbo")
        for k, v in item["verb_info"].items():
            st.write(f"- {k}: {v}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
