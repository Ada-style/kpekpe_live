import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from data.series import SERIES_DATA
from data.Metier import METIERS_DATA
from data.chatbot_responses import CHATBOT_RESPONSES
from data.universites import trouver_ecoles_par_domaine
from data.debouches_secteurs import DEBOUCHES_PAR_SECTEUR
from data.matieres_togo import MATIERES_TOGO
from utils.scoring import calculer_recommandations_texte_libre

# Configuration de la page
st.set_page_config(
    page_title="Kpékpé - Light on your way",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS avec les couleurs du logo (bleu, orange, jaune)
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
.case-box {
    background: linear-gradient(135deg, #004B87 0%, #0066b3 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 75, 135, 0.3);
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
</style>
""", unsafe_allow_html=True)

# États de session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'profil' not in st.session_state:
    st.session_state.profil = None
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

# Page mot de passe
def check_password():
    st.markdown("<div class='main-header'><h1>KPÉKPÉ</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    st.info("Application en phase de test. Entre le code d'accès.")
    password = st.text_input("Code d'accès", type="password")
    if st.button("Accéder à l'application"):
        if password == "kpekpe2025":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Code incorrect.")

# Page accueil - choix du profil
def page_accueil():
    st.markdown("<div class='main-header'><h1>KPÉKPÉ</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    st.markdown("## Bienvenue")
    st.write("Kpékpé t’accompagne dans ta réflexion sur ton orientation scolaire et professionnelle.")
    
    st.subheader("Choisis ton profil")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Je suis en classe de 3ème", use_container_width=True):
            st.session_state.profil = "collegien"
            st.rerun()
    with col2:
        if st.button("Je suis lycéen ou bachelier", use_container_width=True):
            st.session_state.profil = "lyceen"
            st.rerun()

# Page questionnaire avec les 4 cases cliquables
def page_questionnaire():
    st.markdown("<div class='main-header'><h1>Questionnaire d'orientation</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    
    profil_text = "Collégien (3ème)" if st.session_state.profil == "collegien" else "Lycéen/Bachelier"
    st.info(f"Profil sélectionné : {profil_text}")
    st.write("Réponds avec sincérité. Il n’y a pas de mauvaise réponse.")

    # Case 1
    st.markdown("<div class='case-box'>Ce qui te passionne vraiment - Découvre ce qui fait vibrer ton cœur.</div>", unsafe_allow_html=True)
    with st.expander("Ce qui te passionne vraiment", expanded=False):
        st.session_state.responses['passion_principale'] = st.text_area("Décris ce que tu aimes vraiment faire", height=130, key="passion")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.responses['matieres_preferees'] = st.multiselect("Matières qui t’intéressent", MATIERES_TOGO, key="mat_pref")
        with col2:
            st.session_state.responses['activites_favorites'] = st.multiselect("Activités favorites", [
                "Lire et écrire", "Créer et dessiner", "Calculer et analyser", "Parler et convaincre",
                "Construire et réparer", "Aider les autres", "Organiser et gérer", "Utiliser l’ordinateur", "Expérimenter"
            ], key="act_fav")

    # Case 2
    st.markdown("<div class='case-box'>Tes talents naturels - Identifie les forces que tu possèdes déjà.</div>", unsafe_allow_html=True)
    with st.expander("Tes talents naturels", expanded=False):
        st.session_state.responses['forces_naturelles'] = st.text_area("Ce pour quoi tu es naturellement doué", height=130, key="forces")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.responses['matieres_fortes'] = st.multiselect("Matières où tu réussis", MATIERES_TOGO, key="mat_fortes")
        with col2:
            st.session_state.responses['talents'] = st.multiselect("Tes talents", [
                "Logique et raisonnement", "Créativité", "Communication", "Habileté manuelle",
                "Leadership", "Empathie", "Organisation", "Sens technique"
            ], key="talents_list")

    # Case 3
    st.markdown("<div class='case-box'>L’impact que tu veux avoir - Réfléchis au changement que tu souhaites apporter.</div>", unsafe_allow_html=True)
    with st.expander("L’impact que tu veux avoir", expanded=False):
        st.session_state.responses['impact_souhaite'] = st.text_area("Le changement que tu veux créer", height=130, key="impact")
        st.session_state.responses['probleme'] = st.selectbox("Domaine prioritaire", [
            "Santé et bien-être", "Éducation et formation", "Environnement et climat",
            "Technologie et innovation", "Réduction de la pauvreté", "Construction et infrastructure",
            "Commerce et économie", "Justice et droits", "Agriculture et alimentation"
        ], key="domaine")

    # Case 4
    st.markdown("<div class='case-box'>Tes priorités professionnelles - Définit ce qui compte pour ton avenir.</div>", unsafe_allow_html=True)
    with st.expander("Tes priorités professionnelles", expanded=False):
        st.session_state.responses['priorites_personnelles'] = st.text_area("Ce qui compte pour toi", height=100, key="priorites")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.responses['priorite'] = st.selectbox("Priorité principale", [
                "Un bon salaire", "Faire ce qui me passionne", "Équilibre passion/salaire",
                "Avoir un impact social", "Avoir un emploi stable"
            ], key="priorite_select")
        with col2:
            st.session_state.responses['contraintes'] = st.multiselect("Tes contraintes", [
                "Budget limité pour les études", "Besoin de travailler rapidement",
                "Possibilité de faire de longues études", "Préférence pour des études courtes"
            ], key="contraintes_list")

    st.markdown("---")
    if st.button("Voir mes recommandations", use_container_width=True):
        required = ['passion_principale', 'forces_naturelles', 'impact_souhaite']
        if all(st.session_state.responses.get(k) for k in required):
            st.rerun()
        else:
            st.warning("Merci de remplir au moins les trois premières sections.")

# Page résultats
def page_resultats():
    st.markdown("<div class='main-header'><h1>Tes résultats</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    
    responses = st.session_state.responses
    profil = st.session_state.profil
    
    data = SERIES_DATA if profil == "collegien" else METIERS_DATA
    recommandations = calculer_recommandations_texte_libre(responses, data, profil)
    st.session_state.recommendations = recommandations
    
    titre = "Séries recommandées" if profil == "collegien" else "Métiers et filières recommandés"
    st.subheader(titre)
    st.info("Ces recommandations sont des pistes personnalisées pour t’aider à réfléchir.")
    
    for i, rec in enumerate(recommandations[:3], 1):
        st.markdown(f"### {i}. {rec['nom']}")
        st.success(f"Correspondance : {rec['score']}%")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Pourquoi cette recommandation ?**")
            st.write(rec['explication'])
            st.markdown("**Compétences clés**")
            for c in rec['competences'][:3]:
                st.write(f"• {c}")
            
            domaine = rec.get('domaine', '')
            if domaine in DEBOUCHES_PAR_SECTEUR:
                st.markdown("**Débouchés sectoriels au Togo**")
                for d in DEBOUCHES_PAR_SECTEUR[domaine][:4]:
                    st.write(f"• {d}")
        
        with col2:
            st.markdown("**Débouchés concrets**")
            for d in rec['debouches'][:3]:
                st.write(f"• {d}")
            st.markdown("**Durée d’études**")
            st.write(rec['duree'])
            
            if profil == "lyceen":
                st.markdown("**Où étudier au Togo**")
                ecoles = trouver_ecoles_par_domaine(domaine)
                if ecoles:
                    for e in ecoles:
                        st.info(f"**{e['nom']}** ({e['ville']}) — {e['type']} | Coût : {e['cout']}")
                else:
                    st.info("Université de Lomé (UL) — Public | 50 000-100 000 FCFA/an")
    
    st.markdown("---")
    if st.button("Recommencer le questionnaire"):
        st.session_state.responses = {}
        st.session_state.recommendations = []
        st.session_state.profil = None
        st.rerun()
    
    # Chatbot
    st.subheader("Une question ?")
    question = st.selectbox("Questions fréquentes", ["Choisis une question..."] + list(CHATBOT_RESPONSES.keys()), key="chat_question")
    q_perso = st.text_input("Ou pose ta propre question", key="chat_perso")
    if st.button("Envoyer"):
        if q_perso:
            q_lower = q_perso.lower()
            found = False
            for q, r in CHATBOT_RESPONSES.items():
                if any(word in q_lower for word in q.lower().split()[:3]):
                    st.info(r)
                    found = True
                    break
            if not found:
                st.info("Je n’ai pas compris ta question. Essaie une des questions fréquentes.")
        elif question != "Choisis une question...":
            st.info(CHATBOT_RESPONSES[question])

# Main
def main():
    if not st.session_state.authenticated:
        check_password()
    elif st.session_state.profil is None:
        page_accueil()
    elif not st.session_state.recommendations:
        page_questionnaire()
    else:
        page_resultats()

if __name__ == "__main__":
    main()    border-radius: 15px;
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
.case-box {
    background: linear-gradient(135deg, #004B87 0%, #0066b3 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 75, 135, 0.3);
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
</style>
""", unsafe_allow_html=True)
# États
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'profil' not in st.session_state:
    st.session_state.profil = None
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

def check_password():
    st.markdown("<div class='main-header'><h1>KPÉKPÉ</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    st.info("Application en test. Entre le code d'accès.")
    password = st.text_input("Code d'accès", type="password")
    if st.button("Accéder"):
        if password == "kpekpe2025":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Code incorrect.")

def page_accueil():
    st.markdown("<div class='main-header'><h1>KPÉKPÉ</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    st.markdown("## Bienvenue")
    st.write("Kpékpé t’aide à trouver ta voie scolaire et professionnelle.")
    
    st.subheader("Choisis ton profil")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Je suis en classe de 3ème", use_container_width=True):
            st.session_state.profil = "collegien"
            st.rerun()
    with col2:
        if st.button("Je suis lycéen ou bachelier", use_container_width=True):
            st.session_state.profil = "lyceen"
            st.rerun()

def page_questionnaire():
    st.markdown("<div class='main-header'><h1>Questionnaire d'orientation</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    
    profil_text = "Collégien (3ème)" if st.session_state.profil == "collegien" else "Lycéen/Bachelier"
    st.info(f"Profil : {profil_text}")
    st.write("Réponds sincèrement. Il n’y a pas de mauvaise réponse.")

    # Les 4 cases cliquables
    st.markdown("<div class='case-box'>Ce qui te passionne vraiment - Découvre ce qui fait vibrer ton cœur.</div>", unsafe_allow_html=True)
    with st.expander("Ce qui te passionne vraiment", expanded=False):
        st.session_state.responses['passion_principale'] = st.text_area(
            "Décris ce que tu aimes vraiment faire", height=130, key="passion1")
        st.write("Pour t’aider :")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.responses['matieres_preferees'] = st.multiselect("Matières qui t’intéressent", MATIERES_TOGO, key="mat_pref")
        with col2:
            st.session_state.responses['activites_favorites'] = st.multiselect("Activités que tu aimes", [
                "Lire et écrire", "Créer et dessiner", "Calculer et analyser", "Parler et convaincre",
                "Construire et réparer", "Aider les autres", "Organiser et gérer", "Utiliser l’ordinateur", "Expérimenter"
            ], key="act_fav")

    st.markdown("<div class='case-box'>Tes talents naturels - Identifie les forces que tu possèdes déjà.</div>", unsafe_allow_html=True)
    with st.expander("Tes talents naturels", expanded=False):
        st.session_state.responses['forces_naturelles'] = st.text_area(
            "Ce pour quoi tu es naturellement doué", height=130, key="forces1")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.responses['matieres_fortes'] = st.multiselect("Matières où tu réussis", MATIERES_TOGO, key="mat_fortes")
        with col2:
            st.session_state.responses['talents'] = st.multiselect("Tes talents", [
                "Logique", "Créativité", "Communication", "Habileté manuelle", "Leadership", "Empathie", "Organisation", "Sens technique"
            ], key="talents1")

    st.markdown("<div class='case-box'>L’impact que tu veux avoir - Réfléchis au changement que tu souhaites apporter.</div>", unsafe_allow_html=True)
    with st.expander("L’impact que tu veux avoir", expanded=False):
        st.session_state.responses['impact_souhaite'] = st.text_area(
            "Le changement que tu veux créer", height=130, key="impact1")
        st.session_state.responses['probleme'] = st.selectbox("Domaine prioritaire", [
            "Santé et bien-être", "Éducation", "Environnement", "Technologie", "Pauvreté", "Infrastructure", 
            "Économie", "Justice", "Agriculture"
        ], key="domaine1")

    st.markdown("<div class='case-box'>Tes priorités professionnelles - Définit ce qui compte pour ton avenir.</div>", unsafe_allow_html=True)
    with st.expander("Tes priorités professionnelles", expanded=False):
        st.session_state.responses['priorites_personnelles'] = st.text_area(
            "Ce qui est important pour toi", height=100, key="prio1")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.responses['priorite'] = st.selectbox("Priorité principale", [
                "Bon salaire", "Passion", "Équilibre", "Impact social", "Stabilité"
            ], key="prio_select")
        with col2:
            st.session_state.responses['contraintes'] = st.multiselect("Contraintes", [
                "Budget limité", "Travailler rapidement", "Longues études OK", "Études courtes préférées"
            ], key="contraintes1")

    st.markdown("---")
    if st.button("Voir mes recommandations", use_container_width=True):
        required = ['passion_principale', 'forces_naturelles', 'impact_souhaite']
        if all(st.session_state.responses.get(k) for k in required):
            st.rerun()
        else:
            st.warning("Remplis au moins les 3 premières sections.")

def page_resultats():
    st.markdown("<div class='main-header'><h1>Tes résultats</h1><p class='slogan'>Light on your way</p></div>", unsafe_allow_html=True)
    
    responses = st.session_state.responses
    profil = st.session_state.profil
    
    data = SERIES_DATA if profil == "collegien" else METIERS_DATA
    recommandations = calculer_recommandations_texte_libre(responses, data, profil)
    st.session_state.recommendations = recommandations
    
    titre = "Séries recommandées" if profil == "collegien" else "Métiers recommandés"
    st.subheader(titre)
    st.info("Pistes personnalisées pour t’aider à réfléchir.")
    
    for i, rec in enumerate(recommandations[:3], 1):
        with st.container():
            st.markdown(f"### {i}. {rec['nom']}")
            st.success(f"Correspondance : {rec['score']}%")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Pourquoi cette recommandation ?**")
                st.write(rec['explication'])
                st.markdown("**Compétences clés**")
                for c in rec['competences'][:3]:
                    st.write(f"• {c}")
                
                domaine = rec.get('domaine', '')
                if domaine in DEBOUCHES_PAR_SECTEUR:
                    st.markdown("**Débouchés sectoriels au Togo**")
                    for d in DEBOUCHES_PAR_SECTEUR[domaine][:4]:
                        st.write(f"• {d}")
            
            with col2:
                st.markdown("**Débouchés concrets**")
                for d in rec['debouches'][:3]:
                    st.write(f"• {d}")
                st.markdown("**Durée d’études**")
                st.write(rec['duree'])
                
                if profil == "lyceen":
                    st.markdown("**Où étudier au Togo**")
                    ecoles = trouver_ecoles_par_domaine(domaine)
                    if ecoles:
                        for e in ecoles:
                            st.info(f"**{e['nom']}** ({e['ville']}) — {e['type']} | Coût : {e['cout']}")
                    else:
                        st.info("Université de Lomé (UL) — Public | 50 000-100 000 FCFA/an")
    
    st.markdown("---")
    if st.button("Recommencer"):
        st.session_state.responses = {}
        st.session_state.recommendations = []
        st.session_state.profil = None
        st.rerun()
    
    st.subheader("Une question ?")
    question = st.selectbox("Questions fréquentes", [""] + list(CHATBOT_RESPONSES.keys()))
    q_perso = st.text_input("Ou pose ta question")
    if st.button("Envoyer"):
        if q_perso:
            for q, r in CHATBOT_RESPONSES.items():
                if any(word in q_perso.lower() for word in q.lower().split()[:3]):
                    st.info(r)
                    break
            else:
                st.info("Je n’ai pas compris. Choisis une question dans la liste.")
        elif question:
            st.info(CHATBOT_RESPONSES[question])

def main():
    if not st.session_state.authenticated:
        check_password()
    elif st.session_state.profil is None:
        page_accueil()
    elif not st.session_state.recommendations:
        page_questionnaire()
    else:
        page_resultats()

if __name__ == "__main__":
    main()    text-align: center;
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



