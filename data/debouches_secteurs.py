"""
Débouchés réels par secteur au Togo
47 métiers prometteurs identifiés par l'ANPE
Secteurs prioritaires : Agriculture, Logistique, Énergie, Santé, IT, Tourisme
"""

DEBOUCHES_PAR_SECTEUR = {
    "Logistique": {
        "description": "Secteur en croissance avec le développement du port autonome de Lomé",
        "metiers": [
            {
                "nom": "Technicien d'emballage",
                "formation_requise": "BTS Logistique",
                "demande": "Forte",
                "salaire_debut": "80 000-120 000 FCFA"
            },
            {
                "nom": "Conducteur d'engins lourds",
                "formation_requise": "CAP/Formation professionnelle",
                "demande": "Très forte",
                "salaire_debut": "100 000-150 000 FCFA"
            },
            {
                "nom": "Mécanicien poids lourds",
                "formation_requise": "CAP/BEP Mécanique",
                "demande": "Forte",
                "salaire_debut": "80 000-130 000 FCFA"
            },
            {
                "nom": "Mécanicien véhicules légers",
                "formation_requise": "CAP/BEP Mécanique",
                "demande": "Moyenne",
                "salaire_debut": "70 000-110 000 FCFA"
            }
        ]
    },
    
    "Transport maritime": {
        "description": "Port autonome de Lomé = hub régional majeur",
        "metiers": [
            {
                "nom": "Amarreur",
                "formation_requise": "Formation maritime courte",
                "demande": "Forte",
                "salaire_debut": "80 000-120 000 FCFA"
            },
            {
                "nom": "Agent de manutention portuaire",
                "formation_requise": "Formation courte",
                "demande": "Très forte",
                "salaire_debut": "70 000-110 000 FCFA"
            },
            {
                "nom": "Conducteur de chaloupe",
                "formation_requise": "BTS Maritime",
                "demande": "Moyenne",
                "salaire_debut": "100 000-150 000 FCFA"
            },
            {
                "nom": "Capitaine de navire",
                "formation_requise": "Licence Maritime (EMARITO)",
                "demande": "Moyenne",
                "salaire_debut": "200 000-350 000 FCFA"
            },
            {
                "nom": "Mécanicien graisseur maritime",
                "formation_requise": "BTS Mécanique maritime",
                "demande": "Forte",
                "salaire_debut": "90 000-140 000 FCFA"
            }
        ]
    },
    
    "Transport aérien": {
        "description": "Aéroport international de Lomé-Tokoin en expansion",
        "metiers": [
            {
                "nom": "Pilote de ligne",
                "formation_requise": "Formation aéronautique spécialisée",
                "demande": "Moyenne",
                "salaire_debut": "500 000-1 000 000 FCFA+"
            },
            {
                "nom": "Ingénieur mainteneur d'avion",
                "formation_requise": "BAC+5 Aéronautique",
                "demande": "Forte",
                "salaire_debut": "250 000-400 000 FCFA"
            },
            {
                "nom": "Dispatcher aérien",
                "formation_requise": "BTS/Licence Aéronautique",
                "demande": "Moyenne",
                "salaire_debut": "120 000-180 000 FCFA"
            },
            {
                "nom": "Technicien avion",
                "formation_requise": "BTS Aéronautique",
                "demande": "Forte",
                "salaire_debut": "100 000-160 000 FCFA"
            },
            {
                "nom": "Agent de scheduling",
                "formation_requise": "BTS/Licence",
                "demande": "Moyenne",
                "salaire_debut": "90 000-130 000 FCFA"
            }
        ]
    },
    
    "Énergie renouvelable": {
        "description": "Secteur prioritaire du Plan National de Développement (PND)",
        "metiers": [
            {
                "nom": "Technicien solaire",
                "formation_requise": "BTS Électrotechnique/Formation spécialisée",
                "demande": "Très forte",
                "salaire_debut": "90 000-150 000 FCFA"
            },
            {
                "nom": "Technicien biogaz",
                "formation_requise": "BTS/Formation spécialisée",
                "demande": "Forte",
                "salaire_debut": "80 000-130 000 FCFA"
            },
            {
                "nom": "Ingénieur énergies renouvelables",
                "formation_requise": "BAC+5 Énergie",
                "demande": "Forte",
                "salaire_debut": "200 000-350 000 FCFA"
            }
        ]
    },
    
    "Santé": {
        "description": "Besoins criants en personnel médical qualifié",
        "metiers": [
            {
                "nom": "Infirmier de bloc opératoire",
                "formation_requise": "BAC+3 Soins infirmiers",
                "demande": "Très forte",
                "salaire_debut": "90 000-130 000 FCFA"
            },
            {
                "nom": "Infirmier du travail",
                "formation_requise": "BAC+3 Soins infirmiers",
                "demande": "Forte",
                "salaire_debut": "100 000-140 000 FCFA"
            },
            {
                "nom": "Médecin spécialiste",
                "formation_requise": "BAC+10+ Médecine",
                "demande": "Très forte",
                "salaire_debut": "400 000-700 000 FCFA+"
            },
            {
                "nom": "Sage-femme",
                "formation_requise": "BAC+3/4",
                "demande": "Très forte",
                "salaire_debut": "80 000-120 000 FCFA"
            }
        ]
    },
    
    "Informatique et Télécoms": {
        "description": "Digitalisation de l'économie togolaise en cours",
        "metiers": [
            {
                "nom": "Ingénieur télécommunications",
                "formation_requise": "BAC+5 Télécoms",
                "demande": "Forte",
                "salaire_debut": "200 000-350 000 FCFA"
            },
            {
                "nom": "Ingénieur réseaux",
                "formation_requise": "BAC+5 Informatique/Réseaux",
                "demande": "Très forte",
                "salaire_debut": "180 000-320 000 FCFA"
            },
            {
                "nom": "Ingénieur IP",
                "formation_requise": "BAC+5 Réseaux",
                "demande": "Forte",
                "salaire_debut": "200 000-350 000 FCFA"
            },
            {
                "nom": "Ingénieur mobile",
                "formation_requise": "BAC+5 Télécoms",
                "demande": "Forte",
                "salaire_debut": "180 000-300 000 FCFA"
            },
            {
                "nom": "Développeur web/mobile",
                "formation_requise": "BAC+2/3 Informatique",
                "demande": "Très forte",
                "salaire_debut": "120 000-200 000 FCFA"
            },
            {
                "nom": "Ingénieur géomatique",
                "formation_requise": "BAC+5 Géomatique",
                "demande": "Moyenne",
                "salaire_debut": "150 000-250 000 FCFA"
            },
            {
                "nom": "Actuaire",
                "formation_requise": "BAC+5 Actuariat",
                "demande": "Moyenne",
                "salaire_debut": "200 000-350 000 FCFA"
            }
        ]
    },
    
    "Agriculture": {
        "description": "Secteur clé (40% du PIB) en modernisation",
        "metiers": [
            {
                "nom": "Ingénieur agronome",
                "formation_requise": "BAC+5 Agronomie",
                "demande": "Très forte",
                "salaire_debut": "180 000-300 000 FCFA"
            },
            {
                "nom": "Technicien de forage",
                "formation_requise": "BTS Hydraulique",
                "demande": "Forte",
                "salaire_debut": "90 000-140 000 FCFA"
            },
            {
                "nom": "Technicien d'irrigation",
                "formation_requise": "BTS Agronomie",
                "demande": "Forte",
                "salaire_debut": "80 000-130 000 FCFA"
            },
            {
                "nom": "Meunier",
                "formation_requise": "Formation professionnelle",
                "demande": "Moyenne",
                "salaire_debut": "70 000-100 000 FCFA"
            },
            {
                "nom": "Mécanicien d'engins agricoles",
                "formation_requise": "CAP/BEP Mécanique",
                "demande": "Forte",
                "salaire_debut": "80 000-120 000 FCFA"
            },
            {
                "nom": "Agent de qualité agricole",
                "formation_requise": "BTS Agronomie",
                "demande": "Moyenne",
                "salaire_debut": "70 000-110 000 FCFA"
            },
            {
                "nom": "Conseiller agricole",
                "formation_requise": "Licence Agronomie",
                "demande": "Forte",
                "salaire_debut": "100 000-150 000 FCFA"
            },
            {
                "nom": "Aménagiste rural",
                "formation_requise": "BAC+3/5 Agronomie",
                "demande": "Moyenne",
                "salaire_debut": "120 000-180 000 FCFA"
            },
            {
                "nom": "Inspecteur semencier",
                "formation_requise": "Licence Agronomie",
                "demande": "Moyenne",
                "salaire_debut": "90 000-130 000 FCFA"
            },
            {
                "nom": "Transformateur agroalimentaire",
                "formation_requise": "BTS/Formation professionnelle",
                "demande": "Forte",
                "salaire_debut": "80 000-130 000 FCFA"
            }
        ]
    },
    
    "Eau et Assainissement": {
        "description": "Infrastructures en développement, besoins importants",
        "metiers": [
            {
                "nom": "Technicien eau et assainissement",
                "formation_requise": "BTS Hydraulique",
                "demande": "Très forte",
                "salaire_debut": "90 000-140 000 FCFA"
            },
            {
                "nom": "Ingénieur eau et assainissement",
                "formation_requise": "BAC+5 Hydraulique/Environnement",
                "demande": "Forte",
                "salaire_debut": "200 000-350 000 FCFA"
            },
            {
                "nom": "Agent de qualité de l'eau",
                "formation_requise": "BTS Chimie/Environnement",
                "demande": "Moyenne",
                "salaire_debut": "70 000-110 000 FCFA"
            },
            {
                "nom": "Responsable station d'épuration",
                "formation_requise": "Licence/Master Environnement",
                "demande": "Moyenne",
                "salaire_debut": "120 000-180 000 FCFA"
            },
            {
                "nom": "Agent d'entretien réseau eau",
                "formation_requise": "Formation professionnelle",
                "demande": "Forte",
                "salaire_debut": "70 000-100 000 FCFA"
            }
        ]
    },
    
    "Cadastre": {
        "description": "Modernisation du système foncier en cours",
        "metiers": [
            {
                "nom": "Ingénieur cadastre",
                "formation_requise": "BAC+5 Topographie/Géomatique",
                "demande": "Moyenne",
                "salaire_debut": "180 000-300 000 FCFA"
            },
            {
                "nom": "Technicien cadastre",
                "formation_requise": "BTS Topographie",
                "demande": "Moyenne",
                "salaire_debut": "90 000-140 000 FCFA"
            }
        ]
    },
    
    "Tourisme et Hôtellerie": {
        "description": "Secteur en développement avec potentiel touristique du Togo",
        "metiers": [
            {
                "nom": "Cuisinier professionnel",
                "formation_requise": "CAP/BTS Hôtellerie",
                "demande": "Forte",
                "salaire_debut": "70 000-120 000 FCFA"
            },
            {
                "nom": "Conseiller en voyage",
                "formation_requise": "BTS Tourisme",
                "demande": "Moyenne",
                "salaire_debut": "80 000-130 000 FCFA"
            },
            {
                "nom": "Agent d'accueil hôtelier",
                "formation_requise": "BTS Hôtellerie",
                "demande": "Moyenne",
                "salaire_debut": "70 000-110 000 FCFA"
            },
            {
                "nom": "Animateur touristique",
                "formation_requise": "BTS Tourisme/Animation",
                "demande": "Moyenne",
                "salaire_debut": "60 000-100 000 FCFA"
            },
            {
                "nom": "Agent d'hébergement",
                "formation_requise": "BTS Hôtellerie",
                "demande": "Moyenne",
                "salaire_debut": "70 000-110 000 FCFA"
            }
        ]
    }
}

# Statistiques du marché de l'emploi
STATS_EMPLOI = {
    "taux_chomage_urbain": "6,2%",
    "taux_sous_emploi": "25%",
    "secteur_dominant": "Agriculture (40% du PIB)",
    "taux_insertion_cible": ">80% d'ici 2025",
    "informalite": "25%+ des diplômés",
    "secteurs_prioritaires_pnd": [
        "Agriculture",
        "Énergie renouvelable",
        "Numérique",
        "Tourisme",
        "Logistique portuaire"
    ]
}

# Fonction utilitaire
def obtenir_metiers_par_secteur(secteur):
    """Retourne les métiers d'un secteur donné"""
    return DEBOUCHES_PAR_SECTEUR.get(secteur, {}).get('metiers', [])


def obtenir_metiers_forte_demande():
    """Retourne tous les métiers avec demande forte ou très forte"""
    metiers_forte_demande = []
    for secteur, data in DEBOUCHES_PAR_SECTEUR.items():
        for metier in data['metiers']:
            if metier['demande'] in ['Forte', 'Très forte']:
                metiers_forte_demande.append({
                    'secteur': secteur,
                    **metier
                })
    return metiers_forte_demande
