import streamlit as st
import csv
import random
import pandas as pd

# =====================================
# CONFIGURATION PAGE
# =====================================

st.set_page_config(
    page_title="Quiz Game",
    page_icon="🎯",
    layout="centered"
)

# =====================================
# CLASSE QUESTION
# =====================================

class Question:

    def __init__(self, texte, choix, reponse, niveau):

        self.texte = texte
        self.choix = choix
        self.reponse = reponse
        self.niveau = niveau

# =====================================
# CHARGER QUESTIONS
# =====================================

def charger_questions(fichier):

    questions = []

    with open(fichier, newline='', encoding='utf-8') as f:

        reader = csv.DictReader(f)

        for row in reader:

            q = Question(

                row["question"],

                [
                    row["choix1"],
                    row["choix2"],
                    row["choix3"],
                    row["choix4"]
                ],

                row["reponse"],
                row["niveau"]

            )

            questions.append(q)

    return questions

# =====================================
# TITRE
# =====================================

st.title(" Quiz Game")

# =====================================
# CHOIX NIVEAU
# =====================================

st.subheader(" Choisir le niveau")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(" Facile"):

        st.session_state.niveau = "facile"

with col2:

    if st.button(" Moyen"):

        st.session_state.niveau = "moyen"

with col3:

    if st.button(" Difficile"):

        st.session_state.niveau = "difficile"

# niveau par défaut

if "niveau" not in st.session_state:

    st.session_state.niveau = "facile"

niveau_choisi = st.session_state.niveau

# =====================================
# INITIALISATION
# =====================================

if "questions" not in st.session_state or st.session_state.get("old_niveau") != niveau_choisi:

    toutes_questions = charger_questions("questions.csv")

    questions_filtrees = [

        q for q in toutes_questions

        if q.niveau == niveau_choisi
    ]

    random.shuffle(questions_filtrees)

    st.session_state.questions = questions_filtrees
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.reponses = []
    st.session_state.old_niveau = niveau_choisi

# =====================================
# QUESTIONS
# =====================================

if st.session_state.index < len(st.session_state.questions):

    q = st.session_state.questions[st.session_state.index]

    # couleur selon niveau

    if niveau_choisi == "facile":

        st.success(f"Question {st.session_state.index + 1}")

    elif niveau_choisi == "moyen":

        st.warning(f"Question {st.session_state.index + 1}")

    else:

        st.error(f"Question {st.session_state.index + 1}")

    # texte question

    st.subheader(q.texte)

    # réponses

    choix = st.radio(

        "Choisissez une réponse :",

        q.choix

    )

    # validation

    if st.button("✅ Valider"):

        bonne = choix == q.reponse

        if bonne:

            st.success("Bonne réponse ✅")

            st.session_state.score += 1

        else:

            st.error("Mauvaise réponse ❌")

        # sauvegarder réponses

        st.session_state.reponses.append({

            "Question": q.texte,
            "Votre réponse": choix,
            "Bonne réponse": q.reponse

        })

        st.session_state.index += 1

        st.rerun()

# =====================================
# RESULTAT FINAL
# =====================================

else:

    st.balloons()

    total = len(st.session_state.questions)

    st.success(
        f" Quiz terminé ! Score : {st.session_state.score} / {total}"
    )

    # message résultat

    if st.session_state.score == total:

        st.success(" Excellent !")

    elif st.session_state.score >= total / 2:

        st.info(" Bien joué !")

    else:

        st.warning(" Essaie encore !")

    # =====================================
    # CORRECTION
    # =====================================

    st.subheader(" Correction")

    for rep in st.session_state.reponses:

        st.write(" Question :", rep["Question"])

        st.write(" Votre réponse :", rep["Votre réponse"])

        st.write("✅$ Bonne réponse :", rep["Bonne réponse"])

        st.write("---------------------------")

    # =====================================
    # EXPORT CSV
    # =====================================

    df = pd.DataFrame(st.session_state.reponses)

    csv_file = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        " Télécharger résultat CSV",

        csv_file,

        "resultat_quiz.csv",

        "text/csv"

    )

    # =====================================
    # REJOUER
    # =====================================

    if st.button(" Rejouer"):

        random.shuffle(st.session_state.questions)

        st.session_state.index = 0

        st.session_state.score = 0

        st.session_state.reponses = []

        st.rerun()