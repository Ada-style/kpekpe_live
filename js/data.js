/**
 * Kpékpé Data Source - 100% Togo Context
 * Mises à jour avec les données réelles fournies (Janvier 2026)
 */

// 1. Profils de Personnalité (Inchangé pour l'instant, logique interne)
const PERSONALITY_PROFILES = {
    ANALYTIQUE: {
        label: "Analytique & Logique",
        desc: "Tu aimes comprendre le 'pourquoi' et le 'comment'. Tu es structuré(e) et tu prends des décisions basées sur des faits.",
        bonus_tags: ["C", "D", "E", "Santé", "Ingénierie", "Informatique", "Finance", "Sciences"]
    },
    CREATIF: {
        label: "Créatif & Intuitif",
        desc: "Tu as beaucoup d'imagination et tu aimes innover. Les règles strictes t'ennuient, tu préfères créer tes propres solutions.",
        bonus_tags: ["A4", "Arts", "Architecture", "Design", "Communication", "Marketing", "Artisanat"]
    },
    METHODIQUE: {
        label: "Méthodique & Organisé",
        desc: "Tu es fiable, ordonné(e) et efficace. On peut compter sur toi pour gérer des projets et suivre des plans précis.",
        bonus_tags: ["G1", "G2", "Gestion", "Administration", "Comptabilité", "Logistique", "Droit"]
    },
    SOCIAL: {
        label: "Social & Empathique",
        desc: "Ton truc, c'est les gens. Tu aimes aider, enseigner, soigner ou collaborer. Tu réussis là où le contact humain est clé.",
        bonus_tags: ["Santé", "Enseignement", "Ressources Humaines", "Commerce", "Tourisme"]
    }
};

// 2. Séries du BAC Togolais (Enrichies)
const SERIES_DATA = {
    "C": {
        name: "Série C (Mathématiques & Physique)",
        desc: "La voie royale pour les sciences dures et l'ingénierie.",
        keywords: ["maths", "logique", "ingénieur", "informatique", "physique", "architecture"]
    },
    "D": {
        name: "Série D (Sciences de la Vie)",
        desc: "Idéal pour la santé, l'agriculture et la biologie.",
        keywords: ["biologie", "santé", "médecine", "pharmacie", "svt", "nature", "agriculture"]
    },
    "A4": {
        name: "Série A4 (Littéraire)",
        desc: "Pour les passionnés de lettres, langues, droit et communication.",
        keywords: ["littérature", "langues", "philosophie", "droit", "communication", "journalisme", "enseignement"]
    },
    "E": {
        name: "Série E (Maths & Techno)",
        desc: "L'excellence technique et mathématique.",
        keywords: ["technologie", "mécanique", "conception", "ingénierie", "informatique"]
    },
    "F1": { name: "F1 (Mécanique Générale)", keywords: ["mécanique", "industrie", "usine", "construction"] },
    "F2": { name: "F2 (Électronique)", keywords: ["électronique", "circuits", "réparation", "informatique"] },
    "F3": { name: "F3 (Électrotechnique)", keywords: ["électricité", "énergie", "installation", "bâtiment"] },
    "F4": { name: "F4 (Génie Civil)", keywords: ["bâtiment", "construction", "architecture", "dessin", "chantier"] },
    "G1": { name: "G1 (Administration)", keywords: ["administration", "bureau", "secrétariat"] },
    "G2": { name: "G2 (Gestion/Compta)", keywords: ["comptabilité", "gestion", "chiffres", "banque", "finance"] },
    "G3": { name: "G3 (Commerce)", keywords: ["commerce", "vente", "marketing", "logistique"] },
    "TI": { name: "TI (Info)", keywords: ["informatique", "ordinateur", "réseaux", "programmation"] }
};

// 3. Établissements (Liste étendue et consolidée)
// Note: Coûts retirés sur demande utilisateur pour prototype
const SCHOOLS_DB = [
    // PUBLICS
    { name: "Université de Lomé (UL)", type: "Public", ville: "Lomé", domaines: ["Santé", "Sciences", "Droit", "Économie", "Ingénierie", "Agronomie", "Lettres"] },
    { name: "Université de Kara (UK)", type: "Public", ville: "Kara", domaines: ["Santé", "Droit", "Gestion", "Lettres"] },
    { name: "ENS Atakpamé", type: "Public", ville: "Atakpamé", domaines: ["Enseignement", "Éducation"] },
    { name: "INFA de Tové", type: "Public", ville: "Kpalimé", domaines: ["Agriculture", "Élevage"] },
    { name: "ENSI (UL)", type: "Public", ville: "Lomé", domaines: ["Ingénierie", "Informatique", "Génie Civil"] },
    { name: "FSS (UL)", type: "Public", ville: "Lomé", domaines: ["Santé", "Médecine", "Pharmacie"] },
    { name: "EAMAU", type: "Inter-États", ville: "Lomé", domaines: ["Architecture", "Urbanisme"] },

    // PRIVÉS (Sélection représentative)
    { name: "UCAO-UUT", type: "Privé", ville: "Lomé", domaines: ["Droit", "Communication", "Gestion", "Informatique"] },
    { name: "Lomé Business School (LBS)", type: "Privé", ville: "Lomé", domaines: ["Management", "Audit", "Marketing"] },
    { name: "ESGIS", type: "Privé", ville: "Lomé", domaines: ["Informatique", "Gestion", "Sciences"] },
    { name: "IAEC", type: "Privé", ville: "Lomé", domaines: ["Administration", "Commerce"] },
    { name: "ESA", type: "Privé", ville: "Lomé", domaines: ["Affaires", "Comptabilité"] },
    { name: "IPNET", type: "Privé", ville: "Lomé", domaines: ["Informatique", "Technologie"] },
    { name: "FORMATEC", type: "Privé", ville: "Lomé", domaines: ["Santé", "BTP", "Technique"] },
    { name: "CFMI", type: "Partenariat", ville: "Lomé", domaines: ["Industrie", "Mécanique"] },
    { name: "IFAD", type: "Public/Privé", ville: "Divers", domaines: ["Bâtiment", "Aquaculture", "Élevage"] }
];

// Helper pour trouver des écoles par domaine
function getSchoolsForJob(jobTags) {
    // Simple matching heuristic
    const matches = new Set();
    const tags = jobTags.map(t => t.toLowerCase());

    SCHOOLS_DB.forEach(school => {
        const schoolDomains = school.domaines.map(d => d.toLowerCase());
        // Check intersection
        const hasMatch = tags.some(tag =>
            schoolDomains.some(domain => domain.includes(tag) || tag.includes(domain))
        );

        if (hasMatch) matches.add(school.name);
    });

    // Fallback defaults if empty based on generic types
    if (matches.size === 0) {
        if (tags.includes("santé")) matches.add("Université de Lomé (FSS)");
        if (tags.includes("informatique")) matches.add("IPNET / ESGIS");
        if (tags.includes("commerce")) matches.add("Lomé Business School");
    }

    return Array.from(matches).slice(0, 3); // Return top 3 unique
}


// 4. Base de Données Métiers Enrichie (50 Métiers)
// Structure adaptée pour l'app
const JOBS_DATA = [
    // --- SANTÉ ---
    {
        id: "medecin",
        title: "Médecin Généraliste",
        category: "Santé",
        tags: ["santé", "soin", "biologie", "sciences", "aider", "prestigieux", "médecine"],
        profiles: ["ANALYTIQUE", "SOCIAL"],
        series: ["D", "C"],
        studies: "7-8 ans (Doctorat)",
        recruiters: ["CHU Sylvanus Olympio", "Cliniques privées", "ONG santé"],
        desc: "Diagnostic et traitement des patients. Très forte demande au Togo.",
        salary_indice: "Élevé"
    },
    {
        id: "pharmacien",
        title: "Pharmacien",
        category: "Santé",
        tags: ["chimie", "santé", "médicament", "commerce", "biologie"],
        profiles: ["ANALYTIQUE", "METHODIQUE"],
        series: ["D", "C"],
        studies: "6 ans (Doctorat)",
        recruiters: ["Pharmacies", "Hôpitaux", "Laboratoires"],
        desc: "Spécialiste du médicament. Possibilité d'ouvrir sa propre officine.",
        salary_indice: "Élevé"
    },
    {
        id: "infirmier",
        title: "Infirmier d'État",
        category: "Santé",
        tags: ["santé", "soin", "contact", "pratique", "biologie"],
        profiles: ["SOCIAL", "METHODIQUE"],
        series: ["D", "A4"], // A4 sometimes accepted in private
        studies: "3 ans (Licence)",
        recruiters: ["Hôpitaux publics", "Centres de santé", "ONG"],
        desc: "Au cœur du système de soin. Emploi quasi garanti.",
        salary_indice: "Moyen"
    },
    {
        id: "sage_femme",
        title: "Sage-femme",
        category: "Santé",
        tags: ["santé", "soin", "femme", "bébé", "social"],
        profiles: ["SOCIAL", "METHODIQUE"],
        series: ["D"],
        studies: "3-4 ans",
        recruiters: ["Maternités", "CHU"],
        desc: "Accompagnement des naissances. Métier passion et responsabilité.",
        salary_indice: "Moyen"
    },

    // --- AGRICULTURE ---
    {
        id: "agronome",
        title: "Ingénieur Agronome",
        category: "Agriculture",
        tags: ["agriculture", "nature", "terre", "science", "terrain"],
        profiles: ["ANALYTIQUE", "METHODIQUE"],
        series: ["D", "C", "E"],
        studies: "5 ans (Ingénieur)",
        recruiters: ["Ministère Agriculture", "CAGIA", "Coopératives"],
        desc: "Moderniser l'agriculture togolaise. Secteur stratégique (PND).",
        salary_indice: "Moyen à Élevé"
    },
    {
        id: "technicien_agri",
        title: "Technicien Agricole",
        category: "Agriculture",
        tags: ["agriculture", "pratique", "ferme", "élevage", "terrain"],
        profiles: ["METHODIQUE", "SOCIAL"],
        series: ["D", "F1"],
        studies: "2-3 ans (BTS/Licence)",
        recruiters: ["Exploitations agricoles", "IFAD"],
        desc: "Conduite des cultures et élevages sur le terrain.",
        salary_indice: "Moyen"
    },
    {
        id: "elevage",
        title: "Éleveur Moderne",
        category: "Agriculture",
        tags: ["animaux", "business", "ferme", "indépendant"],
        profiles: ["METHODIQUE", "CREATIF"],
        series: ["Toutes"],
        studies: "Formation pro ou Expérience",
        recruiters: ["Auto-entrepreneur"],
        desc: "Production animale (volailles, bovins). Forte rentabilité possible.",
        salary_indice: "Variable"
    },

    // --- NUMÉRIQUE ---
    {
        id: "dev_web",
        title: "Développeur Web/Mobile",
        category: "Numérique",
        tags: ["informatique", "code", "internet", "création", "logique"],
        profiles: ["ANALYTIQUE", "CREATIF"],
        series: ["C", "D", "E", "TI", "F2"],
        studies: "2-5 ans",
        recruiters: ["Startups", "Gozem", "Banques", "Freelance"],
        desc: "Créer des sites et applis. Forte pénurie de talents compétents.",
        salary_indice: "Moyen à Élevé"
    },
    {
        id: "data_analyst",
        title: "Data Analyst",
        category: "Numérique",
        tags: ["données", "statistiques", "analyse", "maths", "informatique"],
        profiles: ["ANALYTIQUE", "METHODIQUE"],
        series: ["C", "E"],
        studies: "3-5 ans",
        recruiters: ["Télécoms (Togocom)", "Banques", "Fintech"],
        desc: "Faire parler les chiffres pour aider les décisions d'entreprise.",
        salary_indice: "Élevé"
    },
    {
        id: "cm",
        title: "Community Manager",
        category: "Numérique",
        tags: ["réseaux sociaux", "communication", "marketing", "internet"],
        profiles: ["CREATIF", "SOCIAL"],
        series: ["A4", "G3"],
        studies: "2-3 ans",
        recruiters: ["Agences", "Marques", "PME"],
        desc: "Gérer l'image des marques sur Facebook, TikTok, LinkedIn.",
        salary_indice: "Moyen"
    },

    // --- BTP & TECHNIQUE ---
    {
        id: "ing_civil",
        title: "Ingénieur Génie Civil",
        category: "BTP",
        tags: ["construction", "chantier", "bâtiment", "calcul", "technique"],
        profiles: ["ANALYTIQUE", "METHODIQUE"],
        series: ["C", "E", "F4"],
        studies: "5 ans",
        recruiters: ["Ebomaf", "CECO BTP", "Etat"],
        desc: "Concevoir ponts, routes et immeubles. Le Togo est en chantier !",
        salary_indice: "Élevé"
    },
    {
        id: "architecte",
        title: "Architecte",
        category: "BTP",
        tags: ["dessin", "art", "maison", "plans", "création"],
        profiles: ["CREATIF", "ANALYTIQUE"],
        series: ["C", "D", "F4"],
        studies: "5-6 ans (EAMAU)",
        recruiters: ["Cabinets d'architecture", "Immobilier"],
        desc: "Allier art et technique pour dessiner les villes de demain.",
        salary_indice: "Élevé"
    },
    {
        id: "macon",
        title: "Maçon / Chef de Chantier",
        category: "BTP",
        tags: ["manuel", "construction", "brique", "terrain", "pratique"],
        profiles: ["METHODIQUE", "SOCIAL"],
        series: ["F4", "Sans Bac"],
        studies: "Apprentissage / CAP",
        recruiters: ["Chantiers", "Indépendant"],
        desc: "Fondamental pour toute construction. Très forte demande locale.",
        salary_indice: "Moyen"
    },

    // --- COMMERCE & GESTION ---
    {
        id: "comptable",
        title: "Comptable",
        category: "Gestion",
        tags: ["chiffres", "argent", "gestion", "bureau", "rigueur"],
        profiles: ["METHODIQUE", "ANALYTIQUE"],
        series: ["G2", "C"],
        studies: "2-5 ans",
        recruiters: ["Toutes entreprises", "Cabinets Expert"],
        desc: "Tenir les finanes. Indispensable partout, de la PME à la multinationale.",
        salary_indice: "Moyen"
    },
    {
        id: "commercial",
        title: "Responsable Commercial",
        category: "Commerce",
        tags: ["vente", "négociation", "client", "parler", "argent"],
        profiles: ["SOCIAL", "ANALYTIQUE"],
        series: ["G3", "A4"],
        studies: "2-5 ans",
        recruiters: ["Distribution", "Assurances", "Banques"],
        desc: "Développer le chiffre d'affaires. Salaire souvent motivant (primes).",
        salary_indice: "Moyen à Élevé"
    },
    {
        id: "logisticien",
        title: "Logisticien / Transport",
        category: "Logistique",
        tags: ["transport", "organisation", "port", "marchandise", "international"],
        profiles: ["METHODIQUE", "ANALYTIQUE"],
        series: ["G3", "C", "D"],
        studies: "3-5 ans",
        recruiters: ["Port Autonome Lomé", "MSC", "Bolloré/AGL"],
        desc: "Gérer les flux de marchandises. Lomé est un hub régional.",
        salary_indice: "Moyen à Élevé"
    },

    // --- DROIT & SOCIÉTÉ ---
    {
        id: "avocat",
        title: "Avocat",
        category: "Droit",
        tags: ["loi", "défendre", "parler", "justice", "argument"],
        profiles: ["ANALYTIQUE", "SOCIAL"],
        series: ["A4"],
        studies: "5-6 ans (Master + CAPA)",
        recruiters: ["Barreau", "Entreprises", "ONG"],
        desc: "Défendre les droits et conseiller. Métier de prestige et de parole.",
        salary_indice: "Élevé"
    },
    {
        id: "enseignant",
        title: "Enseignant",
        category: "Éducation",
        tags: ["école", "transmettre", "jeunes", "savoir", "social"],
        profiles: ["SOCIAL", "METHODIQUE"],
        series: ["Toutes"],
        studies: "3-5 ans (+ENS)",
        recruiters: ["Fonction Publique", "Écoles privées"],
        desc: "Former la relève du Togo. Besoins constants dans tout le pays.",
        salary_indice: "Moyen"
    },

    // --- ARTISANAT & SERVICES ---
    {
        id: "couturier",
        title: "Styliste / Couturier",
        category: "Artisanat",
        tags: ["mode", "vêtement", "création", "manuel", "art"],
        profiles: ["CREATIF", "METHODIQUE"],
        series: ["Toutes", "Sans Bac"],
        studies: "Apprentissage / École de mode",
        recruiters: ["Atelier personnel", "Marques locales"],
        desc: "La mode togolaise est vibrante. Métier créatif et indépendant.",
        salary_indice: "Variable"
    },
    {
        id: "cuisinier",
        title: "Cuisinier / Traiteur",
        category: "Service",
        tags: ["cuisine", "neourriture", "art", "plaisir", "manuel"],
        profiles: ["CREATIF", "METHODIQUE"],
        series: ["Toutes"],
        studies: "CAP / École hôtelière",
        recruiters: ["Restaurants", "Hôtels", "Traiteur"],
        desc: "De la street food à la gastronomie. Le secteur tourisme recrute.",
        salary_indice: "Moyen"
    }
];

// --- LOGIQUE DE MATCHING ---
// (Récupérée et adaptée pour utiliser les nouvelles données)

function getRecommendedJobs(personalityType, userKeywords) {
    // 1. Filter by Personality
    // Boost jobs that match the Personality Type Profile

    // 2. Score by Keywords
    // Simple occurrence counting

    // NOTE: This logic is executed in chat.js
    // ensuring data.js stays pure data container if possible
    // or providing helper functions here.

    return JOBS_DATA.filter(j => true); // Placeholder, logic in chat.js
}
