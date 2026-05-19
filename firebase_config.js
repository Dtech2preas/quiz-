import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getDatabase, ref, get, set, update, onValue, runTransaction } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-database.js";

const firebaseConfig = {
  apiKey: "AIzaSyBQ4-OjJxoO7x5Gm5OV-yZarDp93W19UwQ",
  authDomain: "quiz-b03ce.firebaseapp.com",
  projectId: "quiz-b03ce",
  storageBucket: "quiz-b03ce.firebasestorage.app",
  messagingSenderId: "722098500595",
  appId: "1:722098500595:web:0e8e84293b0e62d1d1d886",
  measurementId: "G-CC8J1DLDQC",
  databaseURL: "https://quiz-b03ce-default-rtdb.firebaseio.com"
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

window.firebaseDatabase = database;
window.firebaseRef = ref;
window.firebaseGet = get;
window.firebaseSet = set;
window.firebaseUpdate = update;
window.firebaseOnValue = onValue;
window.firebaseRunTransaction = runTransaction;

// Lightweight durable queue for Firebase RTDB
async function processQueue() {
    if (!navigator.onLine) return;
    let queue = JSON.parse(localStorage.getItem("firebase_offline_queue") || "[]");
    if (queue.length === 0) return;

    let remaining = [];
    for (const item of queue) {
        try {
            const userRef = window.firebaseRef(window.firebaseDatabase, `users/${item.userId}`);
            await window.firebaseRunTransaction(userRef, (userData) => {
                if (!userData) userData = {};

                // Replay actions
                if (item.action === "quiz") {
                    userData.personal_total_xp = (userData.personal_total_xp || userData.total_xp || 0) + item.personalXp;
                    if (item.subject === "math") userData.personal_math_xp = (userData.personal_math_xp || userData.math_xp || 0) + item.personalXp;
                    if (item.subject === "physics") userData.personal_physics_xp = (userData.personal_physics_xp || userData.physics_xp || 0) + item.personalXp;
                    if (!userData.personal_subjects_xp) userData.personal_subjects_xp = {};
                    userData.personal_subjects_xp[item.subject] = (userData.personal_subjects_xp[item.subject] || 0) + item.personalXp;

                    if (item.passed) {
                        if (userData.last_quiz_date !== item.date) {
                            userData.daily_xp = 0;
                            userData.last_quiz_date = item.date;
                        }
                        userData.last_active_date = item.date;

                        let publicXp = item.publicXp;
                        if ((userData.daily_xp || 0) + publicXp > 350) {
                            publicXp = Math.max(0, 350 - (userData.daily_xp || 0));
                        }

                        userData.daily_xp = (userData.daily_xp || 0) + publicXp;
                        if (item.subject === "math") userData.math_xp = (userData.math_xp || 0) + publicXp;
                        if (item.subject === "physics") userData.physics_xp = (userData.physics_xp || 0) + publicXp;

                        if (!userData.subjects_xp) userData.subjects_xp = {};
                        userData.subjects_xp[item.subject] = (userData.subjects_xp[item.subject] || 0) + publicXp;
                        userData.total_xp = (userData.total_xp || 0) + publicXp;
                    }
                    userData.questions_answered = (userData.questions_answered || 0) + item.totalQs;
                    userData.correct_answers = (userData.correct_answers || 0) + item.correct;
                    userData.accuracy_percentage = userData.questions_answered > 0 ? Math.round((userData.correct_answers / userData.questions_answered) * 100) : 0;
                } else if (item.action === "weekly") {
                    if (!userData.completed_weekly_exams) userData.completed_weekly_exams = {};
                    if (!userData.completed_weekly_exams[item.examKey]) {
                        userData.completed_weekly_exams[item.examKey] = {
                            date: new Date().toISOString(),
                            score: item.score,
                            total: item.totalQs
                        };
                        userData.personal_total_xp = (userData.personal_total_xp || userData.total_xp || 0) + item.totalXp;
                        if (!userData.personal_subjects_xp) userData.personal_subjects_xp = {};
                        userData.personal_subjects_xp[item.subject] = (userData.personal_subjects_xp[item.subject] || 0) + item.totalXp;

                        userData.total_xp = (userData.total_xp || 0) + item.totalXp;
                        if (!userData.subjects_xp) userData.subjects_xp = {};
                        userData.subjects_xp[item.subject] = (userData.subjects_xp[item.subject] || 0) + item.totalXp;
                    }
                } else if (item.action === "points") {
                    userData.dtech_points = (userData.dtech_points || 0) + item.points;
                }

                return userData;
            });
        } catch (e) {
            console.error("Queue process error", e);
            remaining.push(item);
        }
    }
    localStorage.setItem("firebase_offline_queue", JSON.stringify(remaining));
}

window.queueFirebaseAction = function(item) {
    let queue = JSON.parse(localStorage.getItem("firebase_offline_queue") || "[]");
    queue.push(item);
    localStorage.setItem("firebase_offline_queue", JSON.stringify(queue));
    processQueue();
};

window.addEventListener('online', processQueue);
document.addEventListener('DOMContentLoaded', processQueue);

window.triggerFinalSync = async function(closeApp = true, isExplicitExit = false) {
    await processQueue();
    if (closeApp && window.AndroidExit) {
        window.AndroidExit.closeApp();
    }
};
