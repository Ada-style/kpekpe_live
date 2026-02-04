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
    
    # Texte libre (poids réduit)
    texte_libre = ' '.join([
        responses.get('passion_principale', ''),
        responses.get('forces_naturelles', ''),
        responses.get('impact_souhaite', ''),
        responses.get('priorites_personnelles', '')
    ])
    texte_net = nettoyer_texte(texte_libre)
    
    matieres_fortes = responses.get('matieres_fortes', [])
    matieres_pref = responses.get('matieres_preferees', [])
    talents = responses.get('talents', [])
    activites = responses.get('activites_favorites', [])
    domaine_prioritaire = responses.get('probleme', '')
    priorite = responses.get('priorite', '')
    contraintes = responses.get('contraintes', [])
    
    matieres_user = matieres_fortes + matieres_pref  # matières les plus importantes
    
    for key, item in data.items():
        score = 0
        
        # 1. MATCH MATIÈRES → poids EXTRÊMEMENT FORT
        mat_match = calculer_similarite_mots_cles(matieres_user, item.get('matieres_importantes', []))
        score += mat_match * 40  # ← très lourd : 1 match = +40, 2 = +80, etc.
        
        # Bonus si 2+ matières matchent
        if mat_match >= 2:
            score += 50
        
        # Pénalité forte si métier exige des matières que tu n'as PAS
        matieres_item = item.get('matieres_importantes', [])
        matieres_manquantes = [m for m in matieres_item if m.lower() not in [x.lower() for x in matieres_user]]
        if len(matieres_manquantes) > 1:
            score -= 60  # -60 si 2+ matières clés manquent
        elif len(matieres_manquantes) == 1:
            score -= 30  # -30 si 1 matière clé manque
        
        # 2. MATCH COMPÉTENCES / TALENTS
        comp_match = calculer_similarite_mots_cles(talents + activites, item.get('competences', []))
        score += comp_match * 12
        
        # 3. Similarité texte libre (poids réduit)
        item_texte = nettoyer_texte(
            item.get('explication', '') + ' ' + ' '.join(item.get('competences', []))
        )
        mots_communs = len(set(texte_net.split()) & set(item_texte.split()))
        score += mots_communs * 5
        
        # 4. Domaine prioritaire → gros bonus
        if domaine_prioritaire and domaine_prioritaire.lower() in item.get('domaine', '').lower():
            score += 40
        
        # 5. Contraintes et priorités (bonus ciblé)
        duree = item.get('duree_etudes', '').lower()
        if "courtes" in ' '.join(contraintes).lower() or "travailler rapidement" in ' '.join(contraintes).lower():
            if any(mot in duree for mot in ["2", "3", "bts", "cap", "bt", "courte"]):
                score += 25
        if "longues études" in ' '.join(contraintes).lower():
            if any(mot in duree for mot in ["5", "6", "7", "8", "10", "longue"]):
                score += 20
        
        if "bon salaire" in priorite.lower():
            salaire = item.get('salaire', '').lower()
            if "élevé" in salaire or "très demandé" in item.get('debouches_togo', ''):
                score += 25
        
        if "impact social" in priorite.lower():
            if "demandé" in item.get('debouches_togo', '').lower() or "très demandé" in item.get('debouches_togo', ''):
                score += 25
        
        # Pénalité supplémentaire pour métiers très éloignés des matières fortes
        if mat_match == 0 and score < 50:
            score = 0  # on élimine les métiers sans aucun match matière
        
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
