def calculer_recommandations_texte_libre(responses: Dict, data: Dict, profil: str) -> List[Dict]:
    recommandations = []
    
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
    
    for key, item in data.items():
        score = 0
        
        # Matching matières
        mat_match = calculer_similarite_mots_cles(
            matieres_fortes + matieres_pref,
            item.get('matieres_importantes', [])
        )
        score += mat_match * 10
        
        # Matching compétences
        comp_match = calculer_similarite_mots_cles(
            talents + activites,
            item.get('competences', [])
        )
        score += comp_match * 8
        
        # Similarité texte
        item_texte = nettoyer_texte(
            item.get('explication', '') + ' ' + ' '.join(item.get('competences', []))
        )
        mots_communs = len(set(texte_net.split()) & set(item_texte.split()))
        score += mots_communs * 3
        
        # Domaine prioritaire
        if domaine_prioritaire and domaine_prioritaire.lower() in item.get('domaine', '').lower():
            score += 20
        
        # Contraintes et priorités
        duree = item.get('duree_etudes', '')
        if "courtes" in ' '.join(contraintes).lower() or "travailler rapidement" in ' '.join(contraintes).lower():
            if any(mot in duree.lower() for mot in ["2", "3", "bts", "cap", "bt"]):
                score += 15
        if "longues études" in ' '.join(contraintes).lower():
            if any(mot in duree.lower() for mot in ["5", "6", "7", "8", "10"]):
                score += 10
        if "bon salaire" in priorite.lower():
            if "élevé" in item.get('salaire', '').lower():
                score += 12
        if "impact social" in priorite.lower():
            if "demandé" in item.get('debouches_togo', '').lower():
                score += 15
        
        score_normalise = min(score, 100)
        
        recommandations.append({
            'nom': item['nom'],
            'score': score_normalise,
            'explication': item.get('explication', 'Non défini'),
            'competences': item.get('competences', []),
            'debouches': item.get('debouches_concrets', item.get('debouches', []))[:3],
            'duree': item.get('duree_etudes', 'Non défini'),
            'domaine': item.get('domaine', 'Général')
        })
    
    recommandations.sort(key=lambda x: x['score'], reverse=True)
    return recommandations
