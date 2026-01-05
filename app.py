import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from data.series import SERIES_DATA
from data.Metier import METIERS_DATA
from data.chatbot_responses import CHATBOT_RESPONSES
from data.universites import UNIVERSITES_PUBLIQUES, UNIVERSITES_PRIVEES_PRINCIPALES, trouver_ecoles_par_domaine
from data.debouches_secteurs import DEBOUCHES_PAR_SECTEUR
from data.matieres_togo import MATIERES_TOGO
from utils.scoring import calculer_recommandations_texte_libre

st.set_page_config(
    page_title="Kpékpé - Light on your way",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS avec les couleurs du logo (bleu #004B87, orange #FF6B35, jaune #FDB913)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}
.main {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}
.main-header {
    background: linear-gradient(135deg, #004B87 0%, #0066b3 100%);
    padding: 3rem 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(0, 75, 135, 0.2);
    border: 4px solid #FF6B35;
}
.main-header h1 {
    color: white;
    font-weight: 700;
    margin: 0;
    font-size: 3.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.main-header .slogan {
    color: #FDB913;
    font-weight: 500;
    font-size: 1.6rem;
    font-style: italic;
    margin-top: 0.5rem;
}
.stButton>button {
    background: linear-gradient(135deg, #FF6B35 0%, #ff8c5a 100%);
    color: white;
    border-radius: 12px;
    padding: 0.9rem 2.5rem;
    font-weight: 600;
    border: none;
    font-size: 1.1rem;
    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}
.stButton>button:hover {
    background: linear-gradient(135deg, #e55a2b 0%, #ff6b35 100%);
    box-shadow: 0 6px 20px rgba(255, 107, 53, 0.5);
    transform: translateY(-2px);
}
.section-header {
    color: #004B87;
    font-weight: 700;
    font-size: 1.8rem;
    margin-top: 2rem;
    margin-bottom: 1.5rem;
    padding-bottom: 0.8rem;
    border-bottom: 3px solid #FF6B35;
}
.result-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    border-left: 6px solid #004B87;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(0, 75, 135, 0.15);
}
.result-score {
    background: linear-gradient(135deg, #FF6B35 0%, #FDB913 100%);
    color: white;
    font-weight: 700;
    font-size: 1.3rem;
    padding: 0.5rem 1.5rem;
    border-radius: 25px;
    display: inline-block;
    margin-bottom: 1rem;
}
.chatbot-container {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-top: 3rem;
    border: 2px solid #004B87;
}
</style>
""", unsafe_allow_html=True)

# États de session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

def check_password():
    st.markdown("<div class='main-header'><h1>KPÉKPÉ</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    
    st.info("Cette application est en phase de test. Merci d'entrer le code d'accès.")
    
    password = st.text_input("Code d'accès", type="password")
    
    if st.button("Accéder à l'application"):
        if password == "kpekpe2025":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Code incorrect. Contacte l'équipe Kpékpé.")

def page_accueil():
    st.markdown("<div class='main-header'><h1>KPÉKPÉ</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    
    st.markdown("## Bienvenue sur Kpékpé")
    st.write("Nous t'accompagnons dans ta réflexion sur ton orientation scolaire et professionnelle.")
    
    st.info("Ce qui te passionne vraiment - Découvre ce qui fait vibrer ton cœur.")
    st.info("Tes talents naturels - Identifie les forces que tu possèdes déjà.")
    st.info("L'impact que tu veux avoir - Réfléchis au changement que tu souhaites apporter.")
    st.info("Tes priorités professionnelles - Définit ce qui compte pour ton avenir.")
    
    st.markdown("---")
    st.subheader("Commençons par te connaître")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Je suis en classe de 3ème", use_container_width=True):
            st.session_state.profil = "collegien"
            st.session_state.quiz_started = True
            st.rerun()
    
    with col2:
        if st.button("Je suis lycéen ou bachelier", use_container_width=True):
            st.session_state.profil = "lyceen"
            st.session_state.quiz_started = True
            st.rerun()

# Le reste du code (page_quiz, page_resultats, afficher_chatbot, main) reste exactement le même que dans la version précédente

# ... (colle ici le reste du code que je t'ai donné précédemment : page_quiz, page_resultats, afficher_chatbot, main)

def main():
    if not st.session_state.authenticated:
        check_password()
    else:
        if not st.session_state.quiz_started:
            page_accueil()
        elif not st.session_state.quiz_completed:
            page_quiz()
        else:
            page_resultats()

if __name__ == "__main__":
    main()
