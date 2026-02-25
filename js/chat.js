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
        extracted_tags: [], // Keep for backward compatibility or simple tags
        weighted_tags: [], // New: [{tag: "code", weight: 3, type: "passion"}]
        weak_subjects: [] // Subjects the user is not good at
    },
    test_question_index: 0,
    chat_turn: 0
};

// --- PERSONALITY TEST QUESTIONS (15 Fixed) ---
const TEST_QUESTIONS = [
    {
        q: "Face à une nouvelle tâche compliquée, comment réagis-tu ?",
        options: [
            { text: "A) Je l'analyse en détail avant de commencer", value: "ANALYTIQUE" },
            { text: "B) Je prépare un plan d'action ordonné", value: "METHODIQUE" },
            { text: "C) Je cherche une façon originale de la faire", value: "CREATIF" },
            { text: "D) Je demande à quelqu'un de me montrer", value: "SOCIAL" }
        ]
    },
    {
        q: "Qu’est-ce qui te motive le plus dans un projet ?",
        options: [
            { text: "A) Résoudre un problème logique", value: "ANALYTIQUE" },
            { text: "B) Voir le projet fini et bien rangé", value: "METHODIQUE" },
            { text: "C) Créer quelque chose de nouveau", value: "CREATIF" },
            { text: "D) Aider les autres et collaborer", value: "SOCIAL" }
        ]
    },
    {
        q: "Ton environnement de travail idéal est :",
        options: [
            { text: "A) Calme et propice à la réflexion", value: "ANALYTIQUE" },
            { text: "B) Structuré avec des règles claires", value: "METHODIQUE" },
            { text: "C) Libre et sans trop de contraintes", value: "CREATIF" },
            { text: "D) Animé avec beaucoup d'échanges", value: "SOCIAL" }
        ]
    },
    {
        q: "Quand tu dois prendre une décision, tu te fies à :",
        options: [
            { text: "A) La logique et les faits froids", value: "ANALYTIQUE" },
            { text: "B) Tes expériences passées et l'ordre", value: "METHODIQUE" },
            { text: "C) Ton instinct et ton imagination", value: "CREATIF" },
            { text: "D) L'impact que ça aura sur les gens", value: "SOCIAL" }
        ]
    },
    {
        q: "Tes amis disent souvent de toi que tu es :",
        options: [
            { text: "A) Le cerveau de l'équipe", value: "ANALYTIQUE" },
            { text: "B) La personne sur qui on peut compter", value: "METHODIQUE" },
            { text: "C) L'artiste du groupe", value: "CREATIF" },
            { text: "D) L'ami(e) toujours à l'écoute", value: "SOCIAL" }
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

        // AMÉLIORATION 1 — Pondération par question
        const questionWeights = [2, 3, 2, 1.5, 1]; // x2, x3, x2, x1.5, x1
        const questionTypes = ["competence", "passion", "utilite", "valeurs", "filtre"];

        const currentWeight = questionWeights[STATE.chat_turn];
        const currentType = questionTypes[STATE.chat_turn];

        const newTags = extractKeywords(text);

        newTags.forEach(tag => {
            STATE.user.weighted_tags.push({
                tag: tag,
                weight: currentWeight,
                type: currentType
            });
        });

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
    const weightedTags = STATE.user.weighted_tags;
    const weakSubjects = STATE.user.weak_subjects;
    const userProfile = STATE.user.personality_type;

    // AMÉLIORATION 3 — Score Ikigaï croisé
    const scoredJobs = JOBS_DATA.map(job => {
        let passionScore = 0;
        let competenceScore = 0;
        let utiliteScore = 0;
        let salaireScore = 0;
        let weakPenalty = 0;
        let personalityBoost = 0;

        // Calculate scores based on weighted tags
        weightedTags.forEach(wt => {
            const hasTag = job.tags.some(t => t.toLowerCase() === wt.tag.toLowerCase());
            if (hasTag) {
                if (wt.type === "passion") passionScore += wt.weight * 40;
                if (wt.type === "competence") competenceScore += wt.weight * 35;
                if (wt.type === "utilite") utiliteScore += wt.weight * 30;
                // Add weighting for other types if needed, or default logic
            }
        });

        // Salaire score
        if (job.salary_indice === "Élevé") salaireScore = 20;
        else if (job.salary_indice === "Moyen") salaireScore = 10;
        else if (job.salary_indice === "Variable") salaireScore = 5;

        // AMÉLIORATION 2 — Pénalité matières faibles
        // Check if job series overlap with weak subjects
        let weakMatchCount = 0;
        job.series.forEach(sKey => {
            const sData = SERIES_DATA[sKey];
            if (sData) {
                const isWeak = weakSubjects.some(ws =>
                    sData.keywords.some(k => k.toLowerCase() === ws.toLowerCase()) ||
                    sData.name.toLowerCase().includes(ws.toLowerCase())
                );
                if (isWeak) weakMatchCount++;
            }
        });
        weakPenalty = -60 * weakMatchCount;

        // Personality boost
        personalityBoost = job.profiles.includes(userProfile) ? 30 : -10;

        const totalScore = passionScore + competenceScore + utiliteScore + salaireScore + weakPenalty + personalityBoost;

        return {
            job,
            score: totalScore,
            details: { passionScore, competenceScore, utiliteScore, salaireScore, weakPenalty, personalityBoost }
        };
    });

    // AMÉLIORATION 4 — Diversité forcée du top 3
    scoredJobs.sort((a, b) => b.score - a.score);

    const top3 = [];
    const usedCategories = new Set();

    for (const item of scoredJobs) {
        if (top3.length >= 3) break;
        if (!usedCategories.has(item.job.category)) {
            top3.push(item);
            usedCategories.add(item.job.category);
        }
    }

    // Fallback if we don't have enough categories
    if (top3.length < 3) {
        for (const item of scoredJobs) {
            if (top3.length >= 3) break;
            if (!top3.includes(item)) top3.push(item);
        }
    }

    // Generate HTML for recommendations
    let html = `Voici 3 pistes qui te correspondent à merveille, ${STATE.user.name} :<br><br>`;

    top3.forEach((item, idx) => {
        const job = item.job;
        const isStudent = (STATE.user.status === "Collégien" || STATE.user.status === "Lycéen");

        let pathInfo = "";
        if (isStudent) {
            const recommendedSeries = job.series.slice(0, 3).map(sKey => {
                const sData = SERIES_DATA[sKey];
                return sData ? `<li><strong>${sData.name}</strong></li>` : `<li>${sKey}</li>`;
            }).join("");
            pathInfo = `<p><strong>Séries conseillées :</strong></p><ul class="series-list">${recommendedSeries}</ul>`;
        } else {
            const recommendedSchools = getSchoolsForJob(job.tags);
            const schoolText = recommendedSchools.length > 0 ? recommendedSchools.join(", ") : "Universités publiques ou privées du Togo";
            pathInfo = `<p><strong>Écoles :</strong> ${schoolText}</p>`;
        }

        html += `
        <div class="job-card animated-item">
            <div class="job-rank">#${idx + 1}</div>
            <h4>${job.title}</h4>
            <div class="job-category-badge">${job.category}</div>
            <div class="job-details">
                <p><em>${job.desc}</em></p>
                ${pathInfo}
                <div class="job-meta">
                    <span><i class="fa-solid fa-money-bill-wave"></i> ${job.salary_indice}</span>
                    <span><i class="fa-solid fa-graduation-cap"></i> ${job.studies}</span>
                </div>
            </div>
        </div>`;
    });

    botReply(html, 500);

    // AMÉLIORATION 5 — Pont vers Learnia & Feedback
    setTimeout(() => {
        showFeedbackSection(top3);
    }, 2000);
}

// --- AMÉLIORATION 5 : FEEDBACK & LEARNIA ---

function showFeedbackSection(top3) {
    const feedbackHtml = `
        <div class="feedback-block animated-item">
            <p>Ta recommandation t'a plu ? Aide-nous à améliorer Kpékpé ! ⭐</p>
            <div class="star-rating">
                <span class="star" onclick="submitRating(1)">★</span>
                <span class="star" onclick="submitRating(2)">★</span>
                <span class="star" onclick="submitRating(3)">★</span>
                <span class="star" onclick="submitRating(4)">★</span>
                <span class="star" onclick="submitRating(5)">★</span>
            </div>
            <div id="comment-area" style="display:none; margin-top: 10px;">
                <textarea id="feedback-comment" placeholder="Un commentaire ? (optionnel)" class="chat-textarea"></textarea>
                <button onclick="submitFeedback()" class="qr-btn" style="margin-top:5px">Envoyer mon avis</button>
            </div>
        </div>
    `;

    // Store data for local storage
    STATE.current_recommendation = top3.map(t => t.job.title);

    botReply(feedbackHtml, 1000);

    setTimeout(() => {
        showLearniaSection(top3);
    }, 2000);
}

window.submitRating = function (rating) {
    STATE.user_rating = rating;
    const stars = document.querySelectorAll('.star');
    stars.forEach((s, idx) => {
        s.style.color = idx < rating ? "#fce100" : "#ccc";
    });
    document.getElementById('comment-area').style.display = 'block';
};

window.submitFeedback = function () {
    const comment = document.getElementById('feedback-comment').value;
    const feedback = {
        name: STATE.user.name,
        rating: STATE.user_rating,
        comment: comment,
        personality: STATE.user.personality_type,
        top3_jobs: STATE.current_recommendation,
        timestamp: Date.now()
    };
    localStorage.setItem('kpekpe_feedback', JSON.stringify(feedback));

    const commentArea = document.getElementById('comment-area');
    commentArea.innerHTML = "<p>Merci pour ton retour ! 🙏</p>";
};

function showLearniaSection(top3) {
    let learniaHtml = `🎓 Basé sur ton profil, voici ce que Kpékpé Learnia te propose :<br><br>`;

    top3.forEach(item => {
        const job = item.job;
        const formationData = LEARNIA_FORMATIONS[job.category] || LEARNIA_FORMATIONS["Numérique"];
        const schools = getSchoolsForJob(job.tags);
        const schoolName = schools.length > 0 ? schools[0] : "Centre partenaire Kpékpé";

        learniaHtml += `
            <div class="learnia-mini-card animated-item">
                <div class="lmc-title">${formationData.formation}</div>
                <div class="lmc-sub">${job.title}</div>
                <div class="lmc-info">
                    <span><i class="fa-solid fa-clock"></i> ${formationData.duree}</span>
                    <span><i class="fa-solid fa-tag"></i> ${formationData.prix}</span>
                </div>
                <div class="lmc-school">${schoolName}</div>
                <div class="lmc-badge">✅ Centre vérifié</div>
            </div>
        `;
    });

    botReply(learniaHtml, 1500);

    setTimeout(() => {
        showLearniaFilter();
    }, 2500);
}

function showLearniaFilter() {
    const categories = [...new Set(JOBS_DATA.map(j => j.category))];
    const catOptions = categories.map(c => `<option value="${c}">${c}</option>`).join("");

    const filterHtml = `
        <div class="learnia-filter-block animated-item">
            <p>Tu veux explorer d'autres domaines ? Utilise ce filtre 👇</p>
            <div class="filter-group">
                <label>Domaine</label>
                <select id="filter-domain">${catOptions}</select>
            </div>
            <div class="filter-group">
                <label>Budget</label>
                <select id="filter-budget">
                    <option value="any">Tous les budgets</option>
                    <option value="0">Gratuit</option>
                    <option value="20000">Moins de 20 000 FCFA</option>
                    <option value="50000">20 000 à 50 000 FCFA</option>
                    <option value="above">Plus de 50 000 FCFA</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Durée</label>
                <select id="filter-duration">
                    <option value="any">Toutes les durées</option>
                    <option value="3">Moins de 3 mois</option>
                    <option value="6">3-6 mois</option>
                    <option value="more">Plus de 6 mois</option>
                </select>
            </div>
            <button onclick="applyLearniaFilter()" class="qr-btn" style="width:100%; margin-top:10px; background:var(--color-primary); color:white;">Voir les formations →</button>
        </div>
    `;

    botReply(filterHtml, 1000);

    setTimeout(() => {
        botReply("Et voilà ! Qu'est-ce qu'on fait maintenant ?", 1000, [
            { text: "🎓 Découvrir Learnia", value: "learnia.html" },
            { text: "⭐ Donner mon avis", value: "contact.html" },
            { text: "🔄 Recommencer", value: "RESTART" }
        ]);
    }, 2000);
}

window.applyLearniaFilter = function () {
    const domain = document.getElementById('filter-domain').value;
    const formation = LEARNIA_FORMATIONS[domain] || { formation: "Formation non disponible", duree: "-", prix: "-", niveau: "-" };

    const resultHtml = `
        <div class="learnia-mini-card">
            <div class="lmc-title">${formation.formation}</div>
            <div class="lmc-info">
                <span><i class="fa-solid fa-clock"></i> ${formation.duree}</span>
                <span><i class="fa-solid fa-tag"></i> ${formation.prix}</span>
            </div>
            <div class="lmc-school">Centre partenaire Kpékpé</div>
            <div class="lmc-badge">✅ Centre vérifié</div>
        </div>
        <p style="font-size:0.8em; margin-top:10px;"><em>Retrouve toutes les formations sur la page Learnia.</em></p>
    `;
    addMessage('bot', resultHtml);
};



// Start
window.onload = initApp;
