/**
 * Kpékpé Learnia - Demo Experience Logic (100% Client-Side)
 * Permet de simuler le Dashboard et le Course Player pour les présentations.
 */

const DEMO_STATE = {
    view: 'landing', // landing, dashboard, player
    user: {
        name: 'Utilisateur Démo',
        enrolledCourses: [
            { id: 'google-pro', title: 'Google Workspace Pro', progress: 65, category: 'Informatique', image: 'fa-brands fa-google' },
            { id: 'ia-gen', title: 'IA Générative pour Étudiants', progress: 30, category: 'IA', image: 'fa-solid fa-wand-magic-sparkles' },
            { id: 'soft-skills', title: 'Réussir son Entretien au Togo', progress: 0, category: 'Emploi', image: 'fa-solid fa-briefcase' }
        ]
    },
    currentCourse: null,
    currentLessonIndex: 0
};

const COURSE_CONTENT = {
    'google-pro': {
        title: 'Google Workspace Pro',
        lessons: [
            { title: "Introduction à la collaboration Cloud", duration: "10:00", type: "video" },
            { title: "Maîtriser Google Sheets (Formules Togo)", duration: "15:30", type: "video" },
            { title: "Slides : Présenter son projet comme un Pro", duration: "12:00", type: "quiz" }
        ]
    },
    'ia-gen': {
        title: 'IA Générative pour Étudiants',
        lessons: [
            { title: "C'est quoi un Prompt ?", duration: "08:00", type: "video" },
            { title: "Utiliser ChatGPT pour résumer ses cours", duration: "14:20", type: "video" },
            { title: "Générer des images avec Midjourney", duration: "11:00", type: "video" }
        ]
    }
};

// --- NAVIGATION ---
function switchView(viewName) {
    DEMO_STATE.view = viewName;

    // Hide all sections
    document.querySelectorAll('.demo-section').forEach(s => s.style.display = 'none');
    document.querySelector('.landing-section').style.display = (viewName === 'landing') ? 'block' : 'none';

    // Show target section
    const target = document.getElementById(`demo-${viewName}`);
    if (target) {
        target.style.display = 'block';
        window.scrollTo(0, 0);
    }

    if (viewName === 'dashboard') renderDashboard();
}

function openCourse(courseId) {
    DEMO_STATE.currentCourse = COURSE_CONTENT[courseId] || COURSE_CONTENT['google-pro'];
    DEMO_STATE.currentLessonIndex = 0;
    switchView('player');
    renderPlayer();
}

// --- RENDERING ---
function renderDashboard() {
    const container = document.getElementById('enrolled-courses-grid');
    if (!container) return;

    container.innerHTML = DEMO_STATE.user.enrolledCourses.map(course => `
        <div class="course-card-demo" onclick="openCourse('${course.id}')">
            <div class="course-card-icon"><i class="${course.image}"></i></div>
            <div class="course-card-body">
                <span class="badge-cat">${course.category}</span>
                <h4>${course.title}</h4>
                <div class="progress-container">
                    <div class="progress-bar" style="width: ${course.progress}%"></div>
                </div>
                <div class="course-meta">
                    <span>${course.progress}% complété</span>
                    <button class="btn-continue">Continuer <i class="fa-solid fa-play"></i></button>
                </div>
            </div>
        </div>
    `).join('');
}

function renderPlayer() {
    const course = DEMO_STATE.currentCourse;
    const lesson = course.lessons[DEMO_STATE.currentLessonIndex];

    document.getElementById('player-course-title').innerText = course.title;
    document.getElementById('player-lesson-title').innerText = lesson.title;

    // Playlist
    const playlist = document.getElementById('player-playlist');
    playlist.innerHTML = course.lessons.map((l, i) => `
        <div class="playlist-item ${i === DEMO_STATE.currentLessonIndex ? 'active' : ''}" onclick="playLesson(${i})">
            <div class="play-icon"><i class="fa-solid ${i < DEMO_STATE.currentLessonIndex ? 'fa-circle-check' : 'fa-play'}"></i></div>
            <div class="play-text">
                <p>${l.title}</p>
                <span>${l.duration}</span>
            </div>
        </div>
    `).join('');
}

function playLesson(index) {
    DEMO_STATE.currentLessonIndex = index;
    renderPlayer();
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    // Inject Demo Sections if they don't exist (or we could just have them in HTML)
    // We will assume they are in HTML for better control.

    // Handle "Accéder à la démo" buttons
    const demoBtns = document.querySelectorAll('.btn-demo-trigger');
    demoBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            switchView('dashboard');
        });
    });
});
