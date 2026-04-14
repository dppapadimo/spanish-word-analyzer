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
    "AUX": "verbo auxiliar",
    "NOUN": "sustantivo",
    "ADJ": "adjetivo",
    "ADV": "adverbio",
    "PRON": "pronombre",
    "DET": "determinante",
    "ADP": "preposición",
    "PROPN": "nombre propio",
}

# -----------------------------
# SMART VERB ENGINE v1
# -----------------------------
def smart_verb_engine(token):
    text = token.text.lower()
    morph = token.morph

    tense = morph.get("Tense")
    person = morph.get("Person")
    number = morph.get("Number")

    result = {
        "lemma": token.lemma_,
        "tense": None,
        "person": None,
        "number": None
    }

    # -------------------------
    # 1. FIX LEMMA (imperfecto)
    # -------------------------
    if text.endswith("ábamos") or text.endswith("íamos"):
        # remove conjugation → infinitive guess
        if "ar" in token.lemma_ or text.endswith("ábamos"):
            result["lemma"] = text[:-6] + "ar"
        else:
            result["lemma"] = text[:-5] + "er"

    # -------------------------
    # 2. TENSE DETECTION
    # -------------------------
    if tense:
        t = tense[0]
        if t == "Imp":
            result["tense"] = "imperfecto"
        elif t == "Past":
            result["tense"] = "pretérito"
        elif t == "Pres":
            result["tense"] = "presente"
        elif t == "Fut":
            result["tense"] = "futuro"

    # -------------------------
    # 3. PERSON + NUMBER FIX
    # -------------------------
    if person and number:
        p = person[0]
        n = number[0]

        if p == "1" and n == "Sing":
            result["person"] = "yo"
        elif p == "2" and n == "Sing":
            result["person"] = "tú"
        elif p == "3" and n == "Sing":
            result["person"] = "él/ella"
        elif p == "1" and n == "Plur":
            result["person"] = "nosotros"
        elif p == "2" and n == "Plur":
            result["person"] = "vosotros"
        elif p == "3" and n == "Plur":
            result["person"] = "ellos"

        if n == "Sing":
            result["number"] = "singular"
        elif n == "Plur":
            result["number"] = "plural"

    return result

# -----------------------------
# UI
# -----------------------------
st.title("Spanish Word Analyzer 🇪🇸 + Smart Verb Engine v1")

word = st.text_input("Escribe una palabra en español:")

if "history" not in st.session_state:
    st.session_state.history = []

# Buttons
col1, col2 = st.columns(2)

with col1:
    analyze = st.button("Analizar")

with col2:
    clear = st.button("Limpiar")

if clear:
    st.session_state.history = []

# -----------------------------
# Analysis
# -----------------------------
if analyze and word:
    doc = nlp(word)

    for token in doc:

        verb_data = smart_verb_engine(token) if token.pos_ in ["VERB", "AUX"] else None

        st.session_state.history.append({
            "text": token.text,
            "lemma": verb_data["lemma"] if verb_data else token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "morph": str(token.morph),
            "verb": verb_data
        })

# -----------------------------
# Output
# -----------------------------
st.subheader("Resultados")

for item in st.session_state.history:

    st.markdown(f"## 🔎 {item['text']}")

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

    # -------------------------
    # SMART VERB OUTPUT
    # -------------------------
    if item["verb"]:
        st.markdown("### 🔥 Smart Verb Analysis")

        if item["verb"]["tense"]:
            st.write("Tiempo:", item["verb"]["tense"])

        if item["verb"]["person"]:
            st.write("Persona:", item["verb"]["person"])

        if item["verb"]["number"]:
            st.write("Número:", item["verb"]["number"])

    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")
