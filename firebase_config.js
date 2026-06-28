import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getDatabase, ref, get, set, update, onValue, runTransaction } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-database.js";
import { getAuth, signInAnonymously } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";

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
const auth = getAuth(app);

signInAnonymously(auth).catch((error) => {
    console.error("Firebase Anonymous Auth Error:", error.code, error.message);
});

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
            const userRef = window.firebaseRef(window.firebaseDatabase, `user_commands/${item.userId}/${item.unique_id}`);
            await window.firebaseSet(userRef, item);
        } catch (e) {
            console.error("Queue process error", e);
            remaining.push(item);
        }
    }
    localStorage.setItem("firebase_offline_queue", JSON.stringify(remaining));
}

function generateUniqueId() {
    return 'cmd_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 9);
}

window.queueFirebaseAction = function(item) {
    if (!item.userId || item.userId === "undefined" || item.userId === "null") {
        console.error("queueFirebaseAction aborted: Invalid userId", item);
        return;
    }

    // Attach unique ID and timestamp to every command if missing
    if (!item.unique_id) {
        item.unique_id = generateUniqueId();
    }
    if (!item.timestamp) {
        item.timestamp = Date.now();
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

window.getCombinedUserData = async function(userId, queryParams = "", isPublic = false) {
    try {
        const endpoint = isPublic ? `/api/public-user/${userId}` : `/api/user/${userId}`;
        const response = await fetch(`${API_URL}${endpoint}${queryParams}`);
        if (!response.ok) return null;
        return await response.json();
    } catch (e) {
        console.error("Error fetching user data:", e);
        return null;
    }
};
