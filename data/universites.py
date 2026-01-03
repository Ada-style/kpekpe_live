"""
Universités et écoles au Togo (2025-2026)
97 établissements reconnus : 4 publics, 93 privés
"""

UNIVERSITES_PUBLIQUES = [
    {
        "nom": "Université de Lomé (UL)",
        "type": "Public",
        "ville": "Lomé",
        "filieres": [
            "Sciences et technologies",
            "Sciences agronomiques",
            "Droit",
            "Économie",
            "Médecine",
            "Lettres",
            "Ingénierie (génie civil, électrique, mécanique, logiciel)",
            "Environnement"
        ],
        "cout": "Abordable (50 000-100 000 FCFA/an)",
        "niveaux": ["Licence", "Master", "Doctorat"],
        "description": "Principale université publique du Togo, offrant une large gamme de formations à coût abordable avec subventions d'État."
    },
    {
        "nom": "Université de Kara",
        "type": "Public",
        "ville": "Kara",
        "filieres": [
            "Sciences",
            "Ingénierie",
            "Agronomie",
            "Santé",
            "Lettres",
            "Économie"
        ],
        "cout": "Abordable (50 000-100 000 FCFA/an)",
        "niveaux": ["Licence", "Master", "Doctorat"],
        "description": "Université publique dans le nord du Togo, accessible et offrant des formations diversifiées."
    },
    {
        "nom": "École Normale Supérieure d'Atakpamé",
        "type": "Public",
        "ville": "Atakpamé",
        "filieres": [
            "Formation des enseignants",
            "Pédagogie"
        ],
        "cout": "Abordable (50 000-100 000 FCFA/an)",
        "niveaux": ["Licence", "Master"],
        "description": "École spécialisée dans la formation des professeurs pour l'enseignement secondaire."
    },
    {
        "nom": "Centre International de Recherche et d'Étude de Langues",
        "type": "Public",
        "ville": "Lomé (Village du Bénin)",
        "filieres": [
            "Langues",
            "Recherche linguistique"
        ],
        "cout": "Abordable",
        "niveaux": ["Licence", "Master"],
        "description": "Centre spécialisé dans l'étude et la recherche linguistique."
    }
]

UNIVERSITES_PRIVEES_PRINCIPALES = [
    {
        "nom": "Université Catholique de l'Afrique de l'Ouest (UCAO-UUT)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Théologie",
            "Sciences sociales",
            "Gestion",
            "Droit"
        ],
        "cout": "Cher (environ 1 000 000 FCFA/an)",
        "niveaux": ["Licence", "Master"],
        "description": "Université catholique réputée offrant des formations de qualité dans un cadre religieux."
    },
    {
        "nom": "École Supérieure d'Audit et de Management (ESAM)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Audit",
            "Management",
            "Finance",
            "Comptabilité"
        ],
        "cout": "Cher (500 000-1 500 000 FCFA/an)",
        "niveaux": ["BTS", "Licence", "Master"],
        "description": "École privée de référence en audit, gestion et finance au Togo."
    },
    {
        "nom": "Institut Supérieur de Management Adonaï (ISM-Adonaï)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Management",
            "Commerce",
            "Informatique"
        ],
        "cout": "Cher (500 000-1 500 000 FCFA/an)",
        "niveaux": ["BTS", "Licence", "Master"],
        "description": "Institut privé proposant des formations en gestion, commerce et informatique."
    },
    {
        "nom": "Centre de Formation Bancaire du Togo (CFBT)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Banque",
            "Finance"
        ],
        "cout": "Cher",
        "niveaux": ["BTS", "Licence"],
        "description": "Centre spécialisé dans la formation bancaire et financière."
    },
    {
        "nom": "Centre de Perfectionnement aux Techniques Économiques et Commerciales (CPTEC)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Économie",
            "Commerce",
            "Gestion"
        ],
        "cout": "Cher",
        "niveaux": ["Licence", "Master"],
        "description": "Centre de formation en économie, commerce et gestion."
    },
    {
        "nom": "École de Finance (Ex AIA)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Finance",
            "Comptabilité"
        ],
        "cout": "Cher",
        "niveaux": ["BTS", "Licence"],
        "description": "École spécialisée en finance et comptabilité."
    },
    {
        "nom": "École des Cadres",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Management",
            "Administration"
        ],
        "cout": "Cher",
        "niveaux": ["Licence"],
        "description": "Formation des cadres en management et administration."
    },
    {
        "nom": "École des Hautes Études de Sciences et Technologies (HEST)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Sciences",
            "Technologies"
        ],
        "cout": "Cher",
        "niveaux": ["Licence", "Master"],
        "description": "École privée en sciences et technologies."
    },
    {
        "nom": "École Maritime du Togo (EMARITO)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Maritime",
            "Navigation"
        ],
        "cout": "Cher",
        "niveaux": ["BTS", "Licence"],
        "description": "École spécialisée dans les métiers maritimes et la navigation."
    },
    {
        "nom": "École Supérieure des Affaires (ESA)",
        "type": "Privé",
        "ville": "Lomé (Agoè et Super Taco)",
        "filieres": [
            "Affaires",
            "Management",
            "35 filières BTS (gestion, finance, etc.)"
        ],
        "cout": "Cher (500 000-1 500 000 FCFA/an)",
        "niveaux": ["BTS", "Licence", "Master"],
        "description": "Grande école privée offrant 35 filières différentes en gestion et affaires."
    },
    {
        "nom": "École Supérieure des Études Cinématographiques (ESEC)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Cinéma",
            "Audiovisuel"
        ],
        "cout": "Cher",
        "niveaux": ["BTS", "Licence"],
        "description": "École spécialisée en cinéma et production audiovisuelle."
    },
    {
        "nom": "École Supérieure des Ponts",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Ingénierie civile",
            "Génie civil"
        ],
        "cout": "Cher",
        "niveaux": ["Licence", "Master"],
        "description": "École d'ingénierie civile et construction."
    },
    {
        "nom": "Institut Africain d'Informatique (IAI)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Informatique",
            "Réseaux",
            "Systèmes"
        ],
        "cout": "Cher",
        "niveaux": ["Licence", "Master"],
        "description": "Institut de référence en informatique et réseaux au Togo."
    },
    {
        "nom": "American Institute of Africa (AIA)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Divers (enseignement anglophone)"
        ],
        "cout": "Cher",
        "niveaux": ["Licence"],
        "description": "Institut anglophone offrant diverses formations."
    },
    {
        "nom": "École Supérieure de Formation Professionnelle (FIMAC)",
        "type": "Privé",
        "ville": "Lomé",
        "filieres": [
            "Leadership",
            "Entrepreneuriat",
            "Management"
        ],
        "cout": "Cher",
        "niveaux": ["BTS", "Licence", "Master"],
        "description": "École axée sur l'entrepreneuriat et le leadership."
    }
]

# Écoles professionnelles et centres de formation
ECOLES_PROFESSIONNELLES = [
    {
        "nom": "CIFOP",
        "type": "Professionnel",
        "ville": "Lomé",
        "specialites": ["Formations pratiques diverses", "Stages en entreprise"],
        "description": "Centre de formation professionnelle avec focus pratique."
    },
    {
        "nom": "FORMATEC",
        "type": "Professionnel",
        "ville": "Lomé",
        "specialites": ["Techniques", "Stages"],
        "description": "Formation technique et professionnelle."
    },
    {
        "nom": "Shekina",
        "type": "Professionnel",
        "ville": "Lomé",
        "specialites": ["Formations pratiques", "Stages"],
        "description": "Centre de formation professionnelle."
    },
    {
        "nom": "CERFER",
        "type": "Professionnel",
        "ville": "Lomé",
        "specialites": ["Entretien routier", "Travaux publics"],
        "description": "Centre spécialisé en entretien routier."
    },
    {
        "nom": "CRETFP (Centres régionaux)",
        "type": "Professionnel",
        "ville": "Diverses régions",
        "specialites": ["Formations techniques régionales"],
        "description": "Centres régionaux de formation technique et professionnelle."
    },
    {
        "nom": "CET/LETP",
        "type": "Professionnel",
        "ville": "Diverses villes",
        "specialites": ["Techniques diverses"],
        "description": "Collèges d'enseignement technique et lycées techniques."
    }
]

# École régionale (non togolaise mais fréquentée par des Togolais)
ECOLES_REGIONALES = [
    {
        "nom": "2IE - Institut International d'Ingénierie de l'Eau et de l'Environnement",
        "type": "Privé régional",
        "ville": "Ouagadougou, Burkina Faso",
        "filieres": [
            "Ingénierie de l'eau",
            "Ingénierie de l'environnement"
        ],
        "cout": "Cher",
        "niveaux": ["Licence", "Master", "Doctorat"],
        "description": "École d'ingénierie prestigieuse en Afrique de l'Ouest, accessible via partenariats régionaux. Des Togolais y étudient."
    }
]

# Fonction utilitaire pour rechercher des écoles par domaine
def trouver_ecoles_par_domaine(domaine):
    """
    Retourne les écoles correspondant à un domaine d'études
    """
    domaine_lower = domaine.lower()
    resultats = []
    
    # Rechercher dans les universités publiques
    for univ in UNIVERSITES_PUBLIQUES:
        for filiere in univ['filieres']:
            if domaine_lower in filiere.lower():
                resultats.append(univ)
                break
    
    # Rechercher dans les universités privées
    for univ in UNIVERSITES_PRIVEES_PRINCIPALES:
        for filiere in univ['filieres']:
            if domaine_lower in filiere.lower():
                resultats.append(univ)
                break
    
    return resultats


def trouver_ecoles_par_budget(budget_max):
    """
    Retourne les écoles accessibles selon le budget (en FCFA/an)
    """
    resultats = []
    
    # Toujours inclure les universités publiques (abordables)
    resultats.extend(UNIVERSITES_PUBLIQUES)
    
    # Ajouter les privées si budget suffisant
    if budget_max >= 500000:
        resultats.extend(UNIVERSITES_PRIVEES_PRINCIPALES)
    
    return resultats
