"""
Logique Ikigaï - Calcul des 4 dimensions pour profil utilisateur
"""

def calculer_score_ikigai(responses):
    """
    Calcule les scores pour les 4 dimensions de l'Ikigaï
    
    Les 4 dimensions :
    1. Ce que tu AIMES (Passion)
    2. Ce dans quoi tu es BON (Excellence)
    3. Ce dont le monde a BESOIN (Mission)
    4. Ce pour quoi tu peux être PAYÉ (Vocation)
    
    Retourne un dictionnaire avec les 4 scores (0-100)
    """
    
    # 1. CE QUE TU AIMES (0-100)
    matieres_preferees = responses.get('matieres_preferees', [])
    activites_favorites = responses.get('activites_favorites', [])
    
    score_aimes = 0
    if matieres_preferees:
        score_aimes += 50 * (len(matieres_preferees) / 5)  # Max 5 matières = 50 points
    if activites_favorites:
        score_aimes += 50 * (len(activites_favorites) / 5)  # Max 5 activités = 50 points
    
    score_aimes = min(score_aimes, 100)
    
    # 2. CE DANS QUOI TU ES BON (0-100)
    matieres_fortes = responses.get('matieres_fortes', [])
    talents = responses.get('talents', [])
    
    score_bon = 0
    if matieres_fortes:
        score_bon += 50 * (len(matieres_fortes) / 5)  # Max 5 matières = 50 points
    if talents:
        score_bon += 50 * (len(talents) / 4)  # Max 4 talents = 50 points
    
    score_bon = min(score_bon, 100)
    
    # 3. CE DONT LE MONDE A BESOIN (0-100)
    probleme = responses.get('probleme', '')
    
    # Si un problème est choisi, score de 80 (forte motivation)
    score_besoin = 80 if probleme else 50
    
    # 4. CE POUR QUOI TU PEUX ÊTRE PAYÉ (0-100)
    priorite = responses.get('priorite', '')
    contraintes = responses.get('contraintes', [])
    
    score_paye = 60  # Score de base
    
    # Ajustements selon priorité
    if priorite == 'Salaire élevé':
        score_paye += 20
    elif priorite == 'Stabilité de l\'emploi':
        score_paye += 15
    elif priorite == 'Équilibre salaire-passion':
        score_paye += 10
    
    # Ajustements selon contraintes
    if 'Longues études acceptées' in contraintes:
        score_paye += 10
    if 'Préférence études courtes et pratiques' in contraintes:
        score_paye += 10
    
    score_paye = min(score_paye, 100)
    
    return {
        'aimes': round(score_aimes),
        'bon': round(score_bon),
        'besoin': round(score_besoin),
        'paye': round(score_paye)
    }


def interpreter_ikigai(scores):
    """
    Interprète les scores Ikigaï et génère un message personnalisé
    """
    interpretations = []
    
    if scores['aimes'] >= 70:
        interpretations.append("✨ Tu as des passions claires ! C'est excellent.")
    elif scores['aimes'] < 50:
        interpretations.append("💡 Explore davantage pour découvrir ce qui te passionne vraiment.")
    
    if scores['bon'] >= 70:
        interpretations.append("🌟 Tu as identifié tes forces ! Continue à les développer.")
    elif scores['bon'] < 50:
        interpretations.append("💪 Teste différentes activités pour découvrir tes talents cachés.")
    
    if scores['besoin'] >= 70:
        interpretations.append("🌍 Tu as une belle mission ! C'est une grande force.")
    
    if scores['paye'] >= 70:
        interpretations.append("💼 Tu as une vision réaliste de ton avenir professionnel.")
    elif scores['paye'] < 50:
        interpretations.append("💰 Pense aussi aux aspects pratiques de ton orientation.")
    
    # Message global
    moyenne = (scores['aimes'] + scores['bon'] + scores['besoin'] + scores['paye']) / 4
    
    if moyenne >= 75:
        message_global = "🎉 Ton profil Ikigaï est très équilibré ! Tu es sur la bonne voie."
    elif moyenne >= 60:
        message_global = "👍 Bon profil Ikigaï ! Quelques ajustements et tu seras parfait."
    else:
        message_global = "🔍 Continue d'explorer pour affiner ton orientation."
    
    return {
        'interpretations': interpretations,
        'message_global': message_global,
        'moyenne': round(moyenne)
    }


def get_recommendations_par_dimension(scores):
    """
    Donne des recommandations basées sur les dimensions Ikigaï faibles
    """
    recommendations = []
    
    if scores['aimes'] < 60:
        recommendations.append({
            'dimension': 'Ce que tu AIMES',
            'conseil': 'Teste de nouvelles activités ! Rejoins un club, essaie un nouveau sport ou hobby.'
        })
    
    if scores['bon'] < 60:
        recommendations.append({
            'dimension': 'Ce dans quoi tu es BON',
            'conseil': 'Investis-toi dans tes matières fortes. Demande à un prof de t\'aider à progresser.'
        })
    
    if scores['besoin'] < 60:
        recommendations.append({
            'dimension': 'Ce dont le monde a BESOIN',
            'conseil': 'Observe autour de toi : quels problèmes te touchent ? Quelle cause te parle ?'
        })
    
    if scores['paye'] < 60:
        recommendations.append({
            'dimension': 'Ce pour quoi tu peux être PAYÉ',
            'conseil': 'Renseigne-toi sur les salaires et débouchés réels des métiers qui t\'intéressent.'
        })
    
    return recommendations