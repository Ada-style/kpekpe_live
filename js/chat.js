/**
 * Kpékpé - Chat Engine & Logic
 */

// --- STATE MANAGEMENT ---
const STATE = {
    screen: 'onboarding', // onboarding, personality_test, chat_intro, chat_loop, results
    user: {
        name: '',
        age: '',
        status: '', // Collégien, Lycéen, etc.
        personality_scores: {
            ANALYTIQUE: 0,
            METHODIQUE: 0,
            CREATIF: 0,
            SOCIAL: 0
        },
        personality_history: [], // For 'Revenir' button
        personality_type: null,
        answers_log: [],
        extracted_tags: [], // Tags from chat for matching
        weak_subjects: [] // Subjects the user is not good at
    },
    test_question_index: 0,
    chat_turn: 0
};

// --- PERSONALITY TEST QUESTIONS (15 Fixed) ---
const TEST_QUESTIONS = [
    {
        q: "Quel domaine t'attire le plus naturellement ?",
        options: [
            { text: "A) Résoudre des équations et analyser des données (Logique)", value: "ANALYTIQUE" },
            { text: "B) Imaginer des histoires ou créer des designs (Créatif)", value: "CREATIF" },
            { text: "C) Écouter les autres et résoudre leurs problèmes (Social)", value: "SOCIAL" },
            { text: "D) Démonter des machines ou coder des outils (Technique)", value: "METHODIQUE" }
        ]
    },
    {
        q: "Dans quel environnement te sentirais-tu le mieux ?",
        options: [
            { text: "A) Un bureau calme avec des dossiers et de la concentration", value: "METHODIQUE" },
            { text: "B) Un atelier, un studio ou sur le terrain au grand air", value: "CREATIF" },
            { text: "C) Partout où il y a du monde pour échanger et collaborer", value: "SOCIAL" },
            { text: "D) Un laboratoire technologique ou un chantier de construction", value: "ANALYTIQUE" }
        ]
    },
    {
        q: "Quel mode d'action préfères-tu ?",
        options: [
            { text: "A) Diriger une équipe et prendre des décisions stratégiques", value: "ANALYTIQUE" },
            { text: "B) Travailler en expert indépendant sur tes propres créations", value: "CREATIF" },
            { text: "C) Apporter ton aide et ton support à une cause collective", value: "SOCIAL" },
            { text: "D) Inventer de nouveaux systèmes ou explorer des technologies", value: "METHODIQUE" }
        ]
    },
    {
        q: "Quelle est ta principale motivation dans un métier ?",
        options: [
            { text: "A) La sécurité, le salaire et une carrière prestigieuse", value: "ANALYTIQUE" },
            { text: "B) La liberté de créer et l'expression de soi", value: "CREATIF" },
            { text: "C) L'impact positif sur la vie des concitoyens togolais", value: "SOCIAL" },
            { text: "D) La maîtrise parfaite d'un savoir-faire ou d'une technologie", value: "METHODIQUE" }
        ]
    },
    {
        q: "Comment aimes-tu apprendre de nouvelles choses ?",
        options: [
            { text: "A) En étudiant la théorie et en lisant des ouvrages sérieux", value: "ANALYTIQUE" },
            { text: "B) En observant des schémas, des vidéos et en étant intuitif", value: "CREATIF" },
            { text: "C) En discutant avec des experts et en faisant des stages", value: "SOCIAL" },
            { text: "D) En manipulant, en faisant des erreurs et en pratiquant", value: "METHODIQUE" }
        ]
    }
];

// --- CHATBOT QUESTIONS (Flow) ---
const CHAT_QUESTIONS = [
    "Dis-moi, quelles sont tes matières préférées à l’école ou celles où tu es le plus à l’aise ?",
    "Et en dehors des cours, qu’est-ce que tu aimes faire qui te fait vibrer ? (Sport, musique, bricolage...)",
    "Si tu pouvais résoudre un problème au Togo ou dans ton entourage, ce serait quoi ?",
    "Pour ton avenir, qu’est-ce qui compte le plus : la passion, un bon salaire, aider les autres, ou la stabilité ?",
    "As-tu des contraintes particulières ? (Budget études, envie de travailler vite, ou prêt pour de longues études ?)"
];

// --- DOM ELEMENTS ---
const elements = {
    chatBox: document.getElementById('chat-box'),
    inputArea: document.getElementById('input-area'),
    userInput: document.getElementById('user-input'),
    sendBtn: document.getElementById('send-btn'),
    typingIndicator: document.getElementById('typing-indicator')
};

// --- INITIALIZATION ---
function initApp() {
    // Mobile Viewport Fix
    if (window.visualViewport) {
        const updateHeight = () => {
            const vh = window.visualViewport.height;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        };
        window.visualViewport.addEventListener('resize', updateHeight);
        window.visualViewport.addEventListener('scroll', updateHeight);
        updateHeight();
    }

    // Start with Onboarding
    addMessage("bot", "Salut ! Je suis Kpékpé, ton guide personnel. Je suis là pour t'aider à trouver ta voie scolaire et professionnelle au Togo. Pour commencer comment t'appelles-tu ?");
    STATE.screen = 'onboarding_name';
}

// --- CORE UTILS ---
function addMessage(sender, text, quickReplies = null) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender === 'bot' ? 'bot-message' : 'user-message');

    // Avatar for bot
    if (sender === 'bot') {
        const avatar = document.createElement('div');
        avatar.classList.add('message-avatar');
        avatar.innerHTML = '<i class="fa-solid fa-lightbulb"></i>';
        msgDiv.appendChild(avatar);
    }

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.innerHTML = text; // Allow HTML
    msgDiv.appendChild(contentDiv);

    chatBox.appendChild(msgDiv);

    // Handle Quick Replies (Buttons)
    if (quickReplies && sender === 'bot') {
        const qrDiv = document.createElement('div');
        qrDiv.classList.add('quick-replies');
        msgDiv.dataset.hasButtons = "true"; // Mark this message as having active buttons

        quickReplies.forEach(qr => {
            const btn = document.createElement('button');
            btn.classList.add('qr-btn');
            btn.innerText = qr.text;
            btn.onclick = () => {
                // Disable all buttons in this specific message once one is clicked
                qrDiv.querySelectorAll('.qr-btn').forEach(b => {
                    b.disabled = true;
                    b.style.opacity = "0.6";
                    b.style.cursor = "default";
                });
                handleUserResponse(qr.value || qr.text);
            };
            qrDiv.appendChild(btn);
        });
        chatBox.appendChild(qrDiv);
    }

    // Scroll to bottom
    setTimeout(() => {
        chatBox.scrollTo({
            top: chatBox.scrollHeight,
            behavior: 'smooth'
        });
    }, 50);
}

function showTyping() {
    const typing = document.getElementById('typing-indicator');
    typing.style.display = 'flex';
    document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
}

function hideTyping() {
    document.getElementById('typing-indicator').style.display = 'none';
}

async function botReply(text, delay = 1000, quickReplies = null) {
    showTyping();
    // Minimum 800ms to feel natural, otherwise use requested delay
    await new Promise(r => setTimeout(r, Math.max(800, delay)));
    hideTyping();
    addMessage('bot', text, quickReplies);
}

// --- INPUT HANDLING ---
document.getElementById('send-btn').addEventListener('click', () => {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    if (text) {
        handleUserResponse(text);
        input.value = '';
    }
});

document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') document.getElementById('send-btn').click();
});

// --- MAIN CONTROLLER ---
function handleUserResponse(text) {
    if (!text) return;

    // Detect if text is a URL or a local page (for quick replies)
    if (text.startsWith('http') || text.endsWith('.html')) {
        // Use assign for same-window navigation for local files
        window.location.assign(text);
        return;
    }

    addMessage('user', text);

    // 1. ONBOARDING
    if (STATE.screen === 'onboarding_name') {
        // Smart name extraction: ignore common phrases and take last capital word if it's a phrase
        let name = text.replace(/^(je m'appelle|je suis|mon nom est|je me nomme|m'appelle|salut|bonjour)\s+/i, '').trim();

        // If it's still a sentence (more than 2 words), try to pick the most likely name
        const words = name.split(/\s+/);
        if (words.length > 2) {
            // Take the last word as the name if it's capitalized, or just the last word
            name = words[words.length - 1];
        } else if (words.length === 2) {
            // Likely "First Last", keep it
        }

        // Capitalize first letter
        name = name.charAt(0).toUpperCase() + name.slice(1);

        STATE.user.name = name;
        STATE.screen = 'onboarding_status';
        botReply(`Enchanté ${STATE.user.name} ! 😊<br>Quelle est ta situation actuelle ?`, 1000, [
            { text: "Collégien (3ème)", value: "Collégien" },
            { text: "Lycéen", value: "Lycéen" },
            { text: "Bachelier", value: "Bachelier" },
            { text: "Étudiant", value: "Étudiant" }
        ]);
        return;
    }

    if (STATE.screen === 'onboarding_status') {
        STATE.user.status = text;
        STATE.screen = 'personality_intro';
        botReply(`Ça marche. Avant de discuter de tes rêves, faisons un petit test rapide pour cerner ta personnalité (5 questions).<br>C'est parti ? 🚀`, 1200, [
            { text: "C'est parti !", value: "GO" }
        ]);
        return;
    }

    // 2. PERSONALITY TEST
    if (STATE.screen === 'personality_intro' || STATE.screen === 'personality_test') {
        if (text !== "GO" && STATE.screen === 'personality_intro') return;

        if (STATE.screen === 'personality_test') {
            if (text === "BACK") {
                const lastProfile = STATE.user.personality_history.pop();
                if (lastProfile) STATE.user.personality_scores[lastProfile]--;
                STATE.test_question_index--;
            } else {
                // Find which profile matches the text
                const currentQuestion = TEST_QUESTIONS[STATE.test_question_index];
                const matchedOption = currentQuestion.options.find(opt => opt.text === text);
                const profile = matchedOption ? matchedOption.value : null;

                if (profile) {
                    STATE.user.personality_scores[profile]++;
                    STATE.user.personality_history.push(profile);
                }
                STATE.test_question_index++;
            }
        }

        STATE.screen = 'personality_test';

        if (STATE.test_question_index >= TEST_QUESTIONS.length) {
            calculateProfile();
            return;
        }

        const q = TEST_QUESTIONS[STATE.test_question_index];
        const options = q.options.map(opt => ({ text: opt.text, value: opt.text }));

        // Add "Back" button if not the first question
        if (STATE.test_question_index > 0) {
            options.push({ text: "⬅️ Revenir", value: "BACK" });
        }

        botReply(q.q, 600, options);
        return;
    }

    // 3. CHAT LOOP
    if (STATE.screen === 'chat_intro' || STATE.screen === 'chat_loop') {
        STATE.screen = 'chat_loop';
        STATE.user.answers_log.push(text);
        const newTags = extractKeywords(text);
        STATE.user.extracted_tags = [...STATE.user.extracted_tags, ...newTags];
        STATE.chat_turn++;

        if (STATE.chat_turn >= CHAT_QUESTIONS.length) {
            finishChat();
        } else {
            const encouragements = ["Super !", "Intéressant.", "Je vois.", "C'est noté !", "Top !"];
            const randEnc = encouragements[Math.floor(Math.random() * encouragements.length)];
            botReply(`${randEnc} ${CHAT_QUESTIONS[STATE.chat_turn]}`, 1000);
        }
        return;
    }

    // 4. RESULTS ACTIONS
    if (STATE.screen === 'results') {
        if (text === 'RESTART') {
            restartApp();
        } else if (text === 'PDF') {
            triggerPDFMessage();
        } else if (text === 'MORE') {
            triggerSurvey();
        }
        return;
    }
}

function restartApp() {
    // Reset State
    STATE.screen = 'onboarding_name';
    STATE.user = {
        name: '',
        age: '',
        status: '',
        personality_scores: {
            ANALYTIQUE: 0,
            METHODIQUE: 0,
            CREATIF: 0,
            SOCIAL: 0
        },
        personality_history: [],
        personality_type: null,
        answers_log: [],
        extracted_tags: [],
        weak_subjects: []
    };
    STATE.test_question_index = 0;
    STATE.chat_turn = 0;

    // Clear UI
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';

    // Add typing indicator back (it was cleared)
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.classList.add('message', 'bot-message');
    typingDiv.style.display = 'none';
    typingDiv.innerHTML = `
        <div class="message-avatar"><i class="fa-solid fa-lightbulb"></i></div>
        <div class="typing-buble">
            <span></span><span></span><span></span>
        </div>
    `;
    chatBox.appendChild(typingDiv);

    // Re-init
    initApp();
}

function triggerSurvey() {
    botReply("Kpékpé sera bientôt disponible sur mobile grâce à ton avis. Peux-tu nous donner ton retour pour nous aider à nous améliorer ? 💡", 800, [
        { text: "📝 Remplir le formulaire", value: "contact.html" },
        { text: "🏠 Retour au début", value: "RESTART" }
    ]);
}

function triggerPDFMessage() {
    botReply("📄 <strong>Téléchargement PDF :</strong><br><br>Kpékpé est actuellement en phase de développement. Cette fonctionnalité sera disponible très bientôt ! 🚀<br><br>En attendant, tu peux nous aider à l'améliorer en donnant tes retours sur ce formulaire :", 800, [
        { text: "📋 Donner mon avis", value: "contact.html" },
        { text: "🔙 Revenir", value: "RESTART" }
    ]);
}

// --- LOGIC FUNCTIONS ---
function calculateProfile() {
    const scores = STATE.user.personality_scores;

    // Find profile with max score
    let mainProfile = "ANALYTIQUE"; // Default
    let maxScore = -1;

    for (const [profile, score] of Object.entries(scores)) {
        if (score > maxScore) {
            maxScore = score;
            mainProfile = profile;
        }
    }

    STATE.user.personality_type = mainProfile;
    const profileData = PERSONALITY_PROFILES[mainProfile];

    STATE.screen = 'chat_intro';
    botReply(`Ton profil est : <strong>${profileData.label}</strong> 🎯<br>${profileData.desc}<br>Génial ! On va utiliser ça pour te guider.`, 1500);
    setTimeout(() => {
        botReply(`Maintenant, passons aux choses sérieuses. ${CHAT_QUESTIONS[0]}`, 2000);
    }, 2000);
}

function askChatQuestion() {
    // Current question is handled in loop logic
}

function extractKeywords(text) {
    const lower = text.toLowerCase();
    const tags = [];

    // Subjects & Science
    if (lower.includes("math")) tags.push("maths", "chiffres");
    if (lower.includes("physique") || lower.includes("chimie")) tags.push("physique", "chimie");
    if (lower.includes("bio") || lower.includes("svt") || lower.includes("nature")) tags.push("biologie", "nature", "svt");
    if (lower.includes("géo")) tags.push("géographie");
    if (lower.includes("hist")) tags.push("histoire");
    if (lower.includes("langue") || lower.includes("anglais") || lower.includes("fran") || lower.includes("littéra")) tags.push("langues", "parler", "écriture", "littérature");
    if (lower.includes("éco") || lower.includes("argent")) tags.push("économie", "argent", "business");
    if (lower.includes("justice") || lower.includes("loi")) tags.push("loi", "justice");

    // Arts & Media
    if (lower.includes("dessin") || lower.includes("art")) tags.push("art", "dessin", "création");
    if (lower.includes("ciné") || lower.includes("film") || lower.includes("réalisa")) tags.push("cinéma", "vidéo", "image", "réalisateur");
    if (lower.includes("théâtre") || lower.includes("acteur") || lower.includes("comédien")) tags.push("théâtre", "spectacle", "expression", "acteur");
    if (lower.includes("musique") || lower.includes("chanter") || lower.includes("son")) tags.push("musique", "spectacle");
    if (lower.includes("photo")) tags.push("photo", "image");

    // Crafts & Manual
    if (lower.includes("cuisine") || lower.includes("manger") || lower.includes("plat")) tags.push("cuisine", "nourriture");
    if (lower.includes("bois") || lower.includes("menuis")) tags.push("bois", "menuiserie", "manuel");
    if (lower.includes("vêtement") || lower.includes("mode") || lower.includes("couture") || lower.includes("stylis") || lower.includes("dessin")) tags.push("mode", "vêtement", "couture", "art", "stylisme");
    if (lower.includes("répa") || lower.includes("manuel") || lower.includes("main")) tags.push("manuel", "technique", "réparation");

    // Interests & Speed
    if (lower.includes("aide") || lower.includes("social")) tags.push("aider", "social");
    if (lower.includes("voyage") || lower.includes("découv")) tags.push("voyage");
    if (lower.includes("ordi") || lower.includes("code") || lower.includes("info") || lower.includes("programma") || lower.includes("dévelop") || lower.includes("logiciel") || lower.includes("appli") || lower.includes("web") || lower.includes("numérique") || lower.includes("ia") || lower.includes("intelligence") || lower.includes("réseau") || lower.includes("cloud")) tags.push("informatique", "code", "internet", "programmation", "développement");
    if (lower.includes("climat") || lower.includes("météo")) tags.push("climat", "météo", "environnement");
    if (lower.includes("reportage") || lower.includes("info")) tags.push("reportage", "communication");

    // Quick entry to workforce
    if (lower.includes("vite") || lower.includes("rapide") || lower.includes("court") || lower.includes("immédiat")) tags.push("court");

    // Negative Detection (Weaknesses)
    const words = lower.split(/\s+/);
    const negativeKeywords = ["pas", "déteste", "nul", "mauvais", "difficile", "horreur", "aime pas"];

    const isNegative = negativeKeywords.some(nk => lower.includes(nk));

    if (isNegative) {
        if (lower.includes("math")) STATE.user.weak_subjects.push("maths");
        if (lower.includes("physique") || lower.includes("chimie") || lower.includes("science") || lower.includes("scientifique")) STATE.user.weak_subjects.push("sciences");
        if (lower.includes("bio") || lower.includes("svt")) STATE.user.weak_subjects.push("biologie");
        if (lower.includes("langue") || lower.includes("anglais") || lower.includes("fran") || lower.includes("lettre") || lower.includes("littéra")) STATE.user.weak_subjects.push("littérature");
    }

    return [...new Set(tags)]; // Unique tags
}

function finishChat() {
    STATE.screen = 'results';
    botReply("Merci pour tes réponses ! Laisse-moi analyser tout ça avec mes données sur le Togo... 🇹🇬", 1000);

    setTimeout(() => {
        showRecommendations();
    }, 2500);
}

function showRecommendations() {
    const userTags = STATE.user.extracted_tags;

    // Score each job
    const scores = JOBS_DATA.map(job => {
        let interestScore = 0;
        let personalityScore = 0;
        let seriesBoost = 0;

        // 1. Interest Score (Keywords) - Primary Driver
        const matches = userTags.filter(tag =>
            job.tags.some(t => t.toLowerCase() === tag.toLowerCase())
        );
        interestScore = matches.length * 40; // 40 points per match

        // 2. Series Boost (Togolese Academic Correlation)
        // If the user mentioned a subject that is key to this job's series
        job.series.forEach(sKey => {
            const seriesInfo = SERIES_DATA[sKey];
            if (seriesInfo) {
                const subjectMatch = userTags.some(tag =>
                    seriesInfo.keywords.some(k => k.toLowerCase() === tag.toLowerCase())
                );
                if (subjectMatch) seriesBoost += 100; // Big boost for academic alignment
            }
        });

        // 3. Personality Score (Secondary Driver - 20%)
        if (job.profiles.includes(STATE.user.personality_type)) {
            personalityScore = 30;
        } else {
            personalityScore = -10;
        }

        // 4. Category Bonus
        if (userTags.some(tag => job.category.toLowerCase().includes(tag.toLowerCase()))) {
            interestScore += 20;
        }

        const totalScore = interestScore + seriesBoost + personalityScore;
        return { job, score: totalScore };
    });

    // Filter to ensure we ONLY recommend jobs with a positive total score if possible
    let topJobs = scores.filter(s => s.score > 0);

    // Fallback if filtering is too strict
    if (topJobs.length < 3) topJobs = scores;

    // Sort and take Top 3
    topJobs.sort((a, b) => b.score - a.score);
    const top3 = topJobs.slice(0, 3);

    // Generate HTML
    let html = `Voici 3 pistes qui te correspondent à merveille, ${STATE.user.name} :<br><br>`;

    top3.forEach((item, idx) => {
        const job = item.job;

        // Logic for Students vs Others
        const isStudent = (STATE.user.status === "Collégien" || STATE.user.status === "Lycéen");

        // Filtering Incompatible Series (Academic Orientation Logic)
        let filteredSeries = job.series;
        if (isStudent && STATE.user.weak_subjects.includes("maths")) {
            // If weak in math, remove Series C, E, G2 if possible
            filteredSeries = job.series.filter(s => !["C", "E", "G2"].includes(s));
            // Ensure we still have something to recommend
            if (filteredSeries.length === 0) filteredSeries = ["A4", "D", "G3", "G1"];
        }

        let pathInfo = "";
        if (isStudent) {
            const seriesDetails = filteredSeries.slice(0, 3).map(sKey => {
                const sData = SERIES_DATA[sKey];
                return sData ? `<li><strong>${sData.name}</strong> : ${sData.domain}</li>` : `<li>${sKey}</li>`;
            }).join("");
            pathInfo = `<p><strong>Formations conseillées au Lycée :</strong></p><ul style="margin: 5px 0 10px 15px; font-size: 0.9em;">${seriesDetails}</ul>`;
        } else {
            const recommendedSchools = getSchoolsForJob(job.tags);
            const schoolText = recommendedSchools.length > 0 ? recommendedSchools.join(", ") : "Universités publiques ou privées du Togo";
            pathInfo = `<p><strong>Écoles recommandées :</strong> ${schoolText}</p>`;
        }

        html += `
        <div class="job-card">
            <h4>${idx + 1}. ${job.title} (${job.category})</h4>
            <div class="job-details">
                <p><strong>Pourquoi toi ?</strong> ${job.desc}</p>
                ${pathInfo}
                <p><strong>Débouchés :</strong> ${job.recruiters.join(", ")}</p>
                <div class="job-meta">
                    <span class="badge">Salaire: ${job.salary_indice}</span>
                    <span class="badge">Études: ${job.studies}</span>
                </div>
            </div>
        </div>`;
    });

    html += `<br>Qu'en penses-tu ? Ça te parle ?`;

    botReply(html, 500, [
        { text: "En savoir plus", value: "MORE" },
        { text: "Recommencer", value: "RESTART" },
        { text: "Télécharger PDF", value: "PDF" }
    ]);
}



// Start
window.onload = initApp;
