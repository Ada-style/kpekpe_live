# utils/scoring.py
from typing import Dict, List
import re

def nettoyer_texte(texte: str) -> str:
    if not texte:
        return ""
    texte = texte.lower()
    texte = re.sub(r'[^\w\s]', ' ', texte)
    return ' '.join(texte.split())

def calculer_similarite_mots_cles(user_list: List[str], item_list: List[str]) -> int:
    if not user_list or not item_list:
        return 0
    user_set = set(x.lower() for x in user_list)
    item_set = set(x.lower() for x in item_list)
    return len(user_set & item_set)

def calculer_recommandations_texte_libre(responses: Dict, data: Dict, profil: str) -> List[Dict]:
    recommandations = []
    
    # Texte libre concaténé (moins pondéré que les matières)
    texte_libre = ' '.join([
        responses.get('passion_principale', ''),
        responses.get('forces_naturelles', ''),
        responses.get('impact_souhaite', ''),
        responses.get('priorites_personnelles', '')
    ])
    texte_net = nettoyer_texte(texte_libre)
    
    # Listes utilisateur clés
    matieres_fortes = responses.get('matieres_fortes', [])
    matieres_pref = responses.get('matieres_preferees', [])
    talents = responses.get('talents', [])
    activites = responses.get('activites_favorites', [])
    domaine_prioritaire = responses.get('probleme', '')
    priorite = responses.get('priorite', '')
    contraintes = responses.get('contraintes', [])
    
    # Liste complète des matières importantes de l'utilisateur
    matieres_user = matieres_fortes + matieres_pref
    
    for key, item in data.items():
        score = 0
        
        # 1. MATCH MATIERES → poids TRÈS FORT (priorité absolue)
        mat_match = calculer_similarite_mots_cles(matieres_user, item.get('matieres_importantes', []))
        score += mat_match * 25  # ← AUGMENTÉ DE 10 → 25 : les matières comptent énormément
        
        # Bonus si plusieurs matières matchent
        if mat_match >= 2:
            score += 15
        
        # 2. MATCH COMPÉTENCES / TALENTS / ACTIVITÉS
        comp_match = calculer_similarite_mots_cles(talents + activites, item.get('competences', []))
        score += comp_match * 10
        
        # 3. Similarité texte libre (moins important que les matières)
        item_texte = nettoyer_texte(
            item.get('explication', '') + ' ' + ' '.join(item.get('competences', []))
        )
        mots_communs = len(set(texte_net.split()) & set(item_texte.split()))
        score += mots_communs * 4
        
        # 4. Domaine prioritaire → gros bonus
        if domaine_prioritaire and domaine_prioritaire.lower() in item.get('domaine', '').lower():
            score += 35
        
        # 5. Contraintes et priorités
        duree = item.get('duree_etudes', '').lower()
        if "courtes" in ' '.join(contraintes).lower() or "travailler rapidement" in ' '.join(contraintes).lower():
            if any(mot in duree for mot in ["2", "3", "bts", "cap", "bt", "courte"]):
                score += 20
        if "longues études" in ' '.join(contraintes).lower():
            if any(mot in duree for mot in ["5", "6", "7", "8", "10", "longue"]):
                score += 15
        
        if "bon salaire" in priorite.lower():
            salaire = item.get('salaire', '').lower()
            if "élevé" in salaire or "très demandé" in item.get('debouches_togo', ''):
                score += 18
        
        if "impact social" in priorite.lower():
            if "demandé" in item.get('debouches_togo', '').lower() or "très demandé" in item.get('debouches_togo', ''):
                score += 20
        
        # Pénalité si très peu de match matières (évite de proposer médecine si zéro SVT/Math)
        if mat_match == 0 and "Santé" in item.get('domaine', ''):
            score -= 30
        
        score_normalise = max(0, min(score, 100))
        
        recommandations.append({
            'nom': item.get('nom', key),
            'score': score_normalise,
            'explication': item.get('explication', 'Non défini'),
            'competences': item.get('competences', []),
            'debouches': item.get('debouches_concrets', item.get('debouches', []))[:3],
            'duree': item.get('duree_etudes', 'Non défini'),
            'domaine': item.get('domaine', 'Général')
        })
    
    recommandations.sort(key=lambda x: x['score'], reverse=True)
    return recommandations
