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

const API_URL = "https://billowing-hall-4748.nakiaklocko57.workers.dev";

// Lightweight durable queue for Firebase RTDB
async function processQueue() {
    if (!navigator.onLine) return;
    let queue = JSON.parse(localStorage.getItem("firebase_offline_queue") || "[]");
    if (queue.length === 0) return;

    let remaining = [];
    for (const item of queue) {
        try {
            const userRef = window.firebaseRef(window.firebaseDatabase, `users_delta/${item.userId}`);
            await window.firebaseRunTransaction(userRef, (userData) => {
                if (!userData) userData = {};

                // Replay actions
                if (item.action === "quiz") {
                    userData.personal_total_xp = (userData.personal_total_xp || 0) + item.personalXp;
                    if (item.subject === "math") userData.personal_math_xp = (userData.personal_math_xp || 0) + item.personalXp;
                    if (item.subject === "physics") userData.personal_physics_xp = (userData.personal_physics_xp || 0) + item.personalXp;
                    if (!userData.personal_subjects_xp) userData.personal_subjects_xp = {};
                    userData.personal_subjects_xp[item.subject] = (userData.personal_subjects_xp[item.subject] || 0) + item.personalXp;

                    if (item.passed) {
                        userData.last_quiz_date = item.date;
                        userData.last_active_date = item.date;

                        userData.daily_xp = (userData.daily_xp || 0) + item.publicXp;
                        if (item.subject === "math") userData.math_xp = (userData.math_xp || 0) + item.publicXp;
                        if (item.subject === "physics") userData.physics_xp = (userData.physics_xp || 0) + item.publicXp;

                        if (!userData.subjects_xp) userData.subjects_xp = {};
                        userData.subjects_xp[item.subject] = (userData.subjects_xp[item.subject] || 0) + item.publicXp;
                        userData.total_xp = (userData.total_xp || 0) + item.publicXp;
                    }
                    userData.questions_answered = (userData.questions_answered || 0) + item.totalQs;
                    userData.correct_answers = (userData.correct_answers || 0) + item.correct;
                    userData.quizzes_completed = (userData.quizzes_completed || 0) + 1;

                    if (!userData.quiz_history) userData.quiz_history = {};
                    const mappedSubject = item.subject === "mathematics" ? "math" : item.subject;
                    const historyKey = `${mappedSubject}_${item.topic}`;
                    userData.quiz_history[historyKey] = (userData.quiz_history[historyKey] || 0) + 1;

                } else if (item.action === "weekly") {
                    if (!userData.completed_weekly_exams) userData.completed_weekly_exams = {};
                    if (!userData.completed_weekly_exams[item.examKey]) {
                        userData.completed_weekly_exams[item.examKey] = {
                            date: new Date().toISOString(),
                            score: item.score,
                            total: item.totalQs
                        };
                        userData.personal_total_xp = (userData.personal_total_xp || 0) + item.totalXp;
                        if (!userData.personal_subjects_xp) userData.personal_subjects_xp = {};
                        userData.personal_subjects_xp[item.subject] = (userData.personal_subjects_xp[item.subject] || 0) + item.totalXp;

                        userData.total_xp = (userData.total_xp || 0) + item.totalXp;
                        if (!userData.subjects_xp) userData.subjects_xp = {};
                        userData.subjects_xp[item.subject] = (userData.subjects_xp[item.subject] || 0) + item.totalXp;
                    }
                    userData.questions_answered = (userData.questions_answered || 0) + item.totalQs;
                    userData.correct_answers = (userData.correct_answers || 0) + item.score;
                    userData.quizzes_completed = (userData.quizzes_completed || 0) + 1;
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
    if (!item.userId || item.userId === "undefined" || item.userId === "null") {
        console.error("queueFirebaseAction aborted: Invalid userId", item);
        return;
    }
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

window.getCombinedUserData = async function(userId) {
    try {
        const response = await fetch(`${API_URL}/api/user/${userId}`);
        if (!response.ok) return null;
        const kvData = await response.json();

        // Fetch delta from Firebase
        const deltaSnapshot = await window.firebaseGet(window.firebaseRef(window.firebaseDatabase, `users_delta/${userId}`));
        const delta = deltaSnapshot.val();

        if (delta) {
            if (delta.personal_total_xp) kvData.personal_total_xp = (kvData.personal_total_xp || kvData.total_xp || 0) + delta.personal_total_xp;
            if (delta.personal_math_xp) kvData.personal_math_xp = (kvData.personal_math_xp || kvData.math_xp || 0) + delta.personal_math_xp;
            if (delta.personal_physics_xp) kvData.personal_physics_xp = (kvData.personal_physics_xp || kvData.physics_xp || 0) + delta.personal_physics_xp;

            if (delta.personal_subjects_xp) {
                if (!kvData.personal_subjects_xp) kvData.personal_subjects_xp = {};
                for (const subj in delta.personal_subjects_xp) {
                    kvData.personal_subjects_xp[subj] = (kvData.personal_subjects_xp[subj] || 0) + delta.personal_subjects_xp[subj];
                }
            }

            if (delta.total_xp) kvData.total_xp = (kvData.total_xp || 0) + delta.total_xp;
            if (delta.math_xp) kvData.math_xp = (kvData.math_xp || 0) + delta.math_xp;
            if (delta.physics_xp) kvData.physics_xp = (kvData.physics_xp || 0) + delta.physics_xp;
            if (delta.daily_xp) kvData.daily_xp = (kvData.daily_xp || 0) + delta.daily_xp;

            if (delta.subjects_xp) {
                if (!kvData.subjects_xp) kvData.subjects_xp = {};
                for (const subj in delta.subjects_xp) {
                    kvData.subjects_xp[subj] = (kvData.subjects_xp[subj] || 0) + delta.subjects_xp[subj];
                }
            }

            if (delta.dtech_points) kvData.dtech_points = (kvData.dtech_points || 0) + delta.dtech_points;

            if (delta.questions_answered) kvData.questions_answered = (kvData.questions_answered || 0) + delta.questions_answered;
            if (delta.correct_answers) kvData.correct_answers = (kvData.correct_answers || 0) + delta.correct_answers;

            if (kvData.questions_answered > 0) {
                kvData.accuracy_percentage = Math.round((kvData.correct_answers / kvData.questions_answered) * 100);
            }

            if (delta.last_quiz_date) kvData.last_quiz_date = delta.last_quiz_date;
            if (delta.last_active_date) kvData.last_active_date = delta.last_active_date;

            if (delta.completed_weekly_exams) {
                if (!kvData.completed_weekly_exams) kvData.completed_weekly_exams = {};
                for (const examKey in delta.completed_weekly_exams) {
                    kvData.completed_weekly_exams[examKey] = delta.completed_weekly_exams[examKey];
                }
            }
            if (delta.quiz_history) {
                if (!kvData.quiz_history) kvData.quiz_history = {};
                for (const historyKey in delta.quiz_history) {
                    kvData.quiz_history[historyKey] = (kvData.quiz_history[historyKey] || 0) + delta.quiz_history[historyKey];
                }
            }
        }
        return kvData;
    } catch (e) {
        console.error("Error fetching combined data:", e);
        return null;
    }
};

async function checkAndRunMasterSync() {
    if (!navigator.onLine) return;
    try {
        const lockRef = window.firebaseRef(window.firebaseDatabase, `system/sync_lock`);

        const { committed } = await window.firebaseRunTransaction(lockRef, (currentData) => {
            const now = Date.now();
            if (!currentData || (now - currentData.lastSyncTime > 10 * 60 * 1000 && now - currentData.lockTime > 30 * 1000)) {
                return { lockTime: now, lastSyncTime: currentData ? currentData.lastSyncTime : 0 };
            }
            // Abort transaction if it's not time yet or it's locked
            return;
        });

        if (committed) {
            executeMasterSync(lockRef);
        }
    } catch (e) {
        console.error("Master sync check failed", e);
    }
}

async function executeMasterSync(lockRef) {
    try {
        console.log("Master Sync started...");
        const usersRef = window.firebaseRef(window.firebaseDatabase, 'users_delta');
        const snapshot = await window.firebaseGet(usersRef);
        const usersDelta = snapshot.val();

        if (!usersDelta) {
            // Nothing to sync
            await window.firebaseSet(lockRef, { lockTime: 0, lastSyncTime: Date.now() });
            return;
        }

        const response = await fetch(`${API_URL}/api/master-sync`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ users_delta: usersDelta })
        });

        if (response.ok) {
            // Carefully delete synced data using transactions
            for (const userId in usersDelta) {
                const userRef = window.firebaseRef(window.firebaseDatabase, `users_delta/${userId}`);
                const deltaToSubtract = usersDelta[userId];

                await window.firebaseRunTransaction(userRef, (userData) => {
                    if (!userData) return null; // already deleted

                    // Subtract synced delta
                    if (deltaToSubtract.personal_total_xp) userData.personal_total_xp = (userData.personal_total_xp || 0) - deltaToSubtract.personal_total_xp;
                    if (deltaToSubtract.personal_math_xp) userData.personal_math_xp = (userData.personal_math_xp || 0) - deltaToSubtract.personal_math_xp;
                    if (deltaToSubtract.personal_physics_xp) userData.personal_physics_xp = (userData.personal_physics_xp || 0) - deltaToSubtract.personal_physics_xp;

                    if (deltaToSubtract.personal_subjects_xp && userData.personal_subjects_xp) {
                        for (const subj in deltaToSubtract.personal_subjects_xp) {
                            userData.personal_subjects_xp[subj] = (userData.personal_subjects_xp[subj] || 0) - deltaToSubtract.personal_subjects_xp[subj];
                        }
                    }

                    if (deltaToSubtract.total_xp) userData.total_xp = (userData.total_xp || 0) - deltaToSubtract.total_xp;
                    if (deltaToSubtract.math_xp) userData.math_xp = (userData.math_xp || 0) - deltaToSubtract.math_xp;
                    if (deltaToSubtract.physics_xp) userData.physics_xp = (userData.physics_xp || 0) - deltaToSubtract.physics_xp;
                    if (deltaToSubtract.daily_xp) userData.daily_xp = (userData.daily_xp || 0) - deltaToSubtract.daily_xp;

                    if (deltaToSubtract.subjects_xp && userData.subjects_xp) {
                        for (const subj in deltaToSubtract.subjects_xp) {
                            userData.subjects_xp[subj] = (userData.subjects_xp[subj] || 0) - deltaToSubtract.subjects_xp[subj];
                        }
                    }

                    if (deltaToSubtract.dtech_points) userData.dtech_points = (userData.dtech_points || 0) - deltaToSubtract.dtech_points;

                    if (deltaToSubtract.questions_answered) userData.questions_answered = (userData.questions_answered || 0) - deltaToSubtract.questions_answered;
                    if (deltaToSubtract.correct_answers) userData.correct_answers = (userData.correct_answers || 0) - deltaToSubtract.correct_answers;
                    if (deltaToSubtract.quizzes_completed) userData.quizzes_completed = (userData.quizzes_completed || 0) - deltaToSubtract.quizzes_completed;

                    // Remove non-numerical tracking variables that have been synced
                    if (deltaToSubtract.last_quiz_date === userData.last_quiz_date) {
                        delete userData.last_quiz_date;
                    }
                    if (deltaToSubtract.last_active_date === userData.last_active_date) {
                        delete userData.last_active_date;
                    }

                    if (deltaToSubtract.quiz_history && userData.quiz_history) {
                        for (const historyKey in deltaToSubtract.quiz_history) {
                            userData.quiz_history[historyKey] = (userData.quiz_history[historyKey] || 0) - deltaToSubtract.quiz_history[historyKey];
                            if (userData.quiz_history[historyKey] <= 0) delete userData.quiz_history[historyKey];
                        }
                        if (Object.keys(userData.quiz_history).length === 0) delete userData.quiz_history;
                    }

                    if (deltaToSubtract.completed_weekly_exams && userData.completed_weekly_exams) {
                        for (const examKey in deltaToSubtract.completed_weekly_exams) {
                            if (userData.completed_weekly_exams[examKey] && userData.completed_weekly_exams[examKey].date === deltaToSubtract.completed_weekly_exams[examKey].date) {
                                delete userData.completed_weekly_exams[examKey];
                            }
                        }
                        if (Object.keys(userData.completed_weekly_exams).length === 0) delete userData.completed_weekly_exams;
                    }

                    // Clean up keys if they are 0 or empty objects
                    const keys = Object.keys(userData);
                    let allZero = true;
                    for (const k of keys) {
                        if (typeof userData[k] === 'number') {
                            if (userData[k] <= 0) delete userData[k];
                            else allZero = false;
                        } else if (typeof userData[k] === 'object' && Object.keys(userData[k]).length === 0) {
                            delete userData[k];
                        } else {
                            allZero = false;
                        }
                    }
                    return allZero ? null : userData;
                });
            }

            await window.firebaseSet(lockRef, { lockTime: 0, lastSyncTime: Date.now() });
            console.log("Master Sync completed.");
        } else {
            // failed, release lock so someone else can try
            await window.firebaseSet(lockRef, { lockTime: 0, lastSyncTime: 0 });
        }
    } catch (e) {
        console.error("Error during Master Sync", e);
        await window.firebaseSet(lockRef, { lockTime: 0, lastSyncTime: 0 });
    }
}

// Periodically attempt master sync
setInterval(checkAndRunMasterSync, 60000); // Check every minute
