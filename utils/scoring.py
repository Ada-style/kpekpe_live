# utils/scoring.py
import re
from typing import List, Dict

def nettoyer_texte(texte: str) -> str:
    """Nettoie et normalise le texte pour comparaison."""
    if not texte:
        return ""
    texte = texte.lower()
    texte = re.sub(r'[^\w\s]', ' ', texte)
    return ' '.join(texte.split())

def calculer_similarite_mots_cles(user_list: List[str], item_list: List[str]) -> int:
    """Compte le nombre de correspondances entre deux listes."""
    if not user_list or not item_list:
        return 0
    user_set = set(x.lower() for x in user_list)
    item_set = set(x.lower() for x in item_list)
    return len(user_set & item_set)

def calculer_recommandations_texte_libre(responses: Dict, data: Dict, profil: str) -> List[Dict]:
    """
    Calcule les recommandations pour séries (collegien) ou métiers (lyceen)
    """
    recommandations = []
    
    # Texte libre concaténé
    texte_libre = ' '.join([
        responses.get('passion_principale', ''),
        responses.get('forces_naturelles', ''),
        responses.get('impact_souhaite', ''),
        responses.get('priorites_personnelles', '')
    ])
    texte_net = nettoyer_texte(texte_libre)
    
    # Listes utilisateur
    matieres_fortes = responses.get('matieres_fortes', [])
    matieres_pref = responses.get('matieres_preferees', [])
    talents = responses.get('talents', [])
    activites = responses.get('activites_favorites', [])
    domaine_prioritaire = responses.get('probleme', '')
    priorite = responses.get('priorite', '')
    contraintes = responses.get('contraintes', [])
    
    for key, item in data.items():
        score = 0
        
        # 1. Matching matières importantes
        mat_match = calculer_similarite_mots_cles(
            matieres_fortes + matieres_pref,
            item.get('matieres_importantes', [])
        )
        score += mat_match * 10  # Poids fort
        
        # 2. Matching compétences / talents
        comp_match = calculer_similarite_mots_cles(
            talents + activites,
            item.get('competences', [])
        )
        score += comp_match * 8
        
        # 3. Similarité textuelle simple
        item_texte = nettoyer_texte(
            item.get('explication', '') + ' ' + ' '.join(item.get('competences', []))
        )
        mots_communs = len(set(texte_net.split()) & set(item_texte.split()))
        score += mots_communs * 3
        
        # 4. Domaine prioritaire
        if domaine_prioritaire:
            domaine_item = item.get('domaine', '')
            if domaine_prioritaire.lower() in domaine_item.lower():
                score += 20
        
        # 5. Priorités et contraintes
        duree = item.get('duree_etudes', '')
        if "courtes" in ' '.join(contraintes).lower() or "travailler rapidement" in ' '.join(contraintes).lower():
            if any(mot in duree.lower() for mot in ["2", "3", "bts", "cap", "bt"]):
                score += 15
        
        if "longues études" in ' '.join(contraintes).lower():
            if any(mot in duree.lower() for mot in ["5", "6", "7", "8", "10"]):
                score += 10
        
        if "bon salaire" in priorite.lower():
            salaire = item.get('salaire', '')
            if "élevé" in salaire.lower():
                score += 12
        
        if "impact social" in priorite.lower():
            if "demandé" in item.get('debouches_togo', '').lower():
                score += 15
        
        # Normalisation score (cap à 100 pour affichage)
        score_normalise = min(score, 100)
        
        recommandations.append({
            'nom': item['nom'],
            'score': score_normalise,
            'explication': item['explication'],
            'competences': item['competences'],
            'debouches': item['debouches_concrets'],
            'duree': item['duree_etudes'],
            'domaine': item.get('domaine', 'Général')
        })
    
    # Tri et retour top résultats
    recommandations.sort(key=lambda x: x['score'], reverse=True)
    return recommandations
