const ALLOWED_ORIGIN = "https://quiz.dtech-services.co.za";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

const FIREBASE_DB_URL = "https://quiz-b03ce-default-rtdb.firebaseio.com";
const FIREBASE_API_KEY = "AIzaSyBQ4-OjJxoO7x5Gm5OV-yZarDp93W19UwQ";

async function getFirebaseAuthToken(env) {
    if (!env.FIREBASE_WORKER_EMAIL || !env.FIREBASE_WORKER_PASSWORD) return null;
    try {
        const response = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=${FIREBASE_API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: env.FIREBASE_WORKER_EMAIL,
                password: env.FIREBASE_WORKER_PASSWORD,
                returnSecureToken: true
            })
        });
        if (response.ok) {
            const data = await response.json();
            return data.idToken;
        }
    } catch (e) {
        console.error("Auth Error:", e);
    }
    return null;
}

async function handleGenerateToken(request, env) {
  const body = await request.json();
  const { user_id } = body;
  if (!user_id) {
    return jsonResponse({ error: "User ID is required" }, 400);
  }

  // Verify user exists
  const userStr = await env.RANK_KV.get(`user:${user_id}`);
  if (!userStr) {
    return jsonResponse({ error: "User not found" }, 404);
  }

  // Generate a random token
  const token = crypto.randomUUID();

  // Save to KV with expiration of 5 minutes (300 seconds)
  await env.RANK_KV.put(`login_token:${token}`, user_id, { expirationTtl: 300 });

  return jsonResponse({ token: token }, 200);
}

async function handleConsumeToken(request, env) {
  const body = await request.json();
  const { token } = body;
  if (!token) {
    return jsonResponse({ error: "Token is required" }, 400);
  }

  const userId = await env.RANK_KV.get(`login_token:${token}`);
  if (!userId) {
    return jsonResponse({ error: "Invalid or expired token" }, 401);
  }

  // Token is single use, so delete it immediately
  await env.RANK_KV.delete(`login_token:${token}`);

  return jsonResponse({ user_id: userId }, 200);
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(handleScheduledSync(env));
  },

  async fetch(request, env, ctx) {
    const origin = request.headers.get("Origin");

    // Block if Origin is present and doesn't match ALLOWED_ORIGIN
    if (origin && origin !== ALLOWED_ORIGIN) {
      return new Response("Forbidden", { status: 403 });
    }

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
      if (request.method === "POST" && path === "/api/generate-token") {
        return await handleGenerateToken(request, env);
      }
      if (request.method === "POST" && path === "/api/consume-token") {
        return await handleConsumeToken(request, env);
      }
      if (request.method === "POST" && path === "/api/signup") {
        return await handleSignup(request, env);
      }
      if (request.method === "POST" && path === "/api/login") {
        return await handleLogin(request, env);
      }
      if (request.method === "GET" && path.startsWith("/api/user/")) {
        return await handleGetUser(request, env, path);
      }
      if (request.method === "PUT" && path.match(/^\/api\/user\/([^/]+)\/avatar$/)) {
        return await handleUpdateAvatar(request, env, path);
      }
      if (request.method === "PUT" && path.match(/^\/api\/user\/([^/]+)\/profile$/)) {
        return await handleUpdateProfile(request, env, path);
      }
      if (request.method === "GET" && path.startsWith("/api/public-user/")) {
        return await handleGetPublicUser(request, env, path);
      }
      if (request.method === "POST" && path === "/api/submit-quiz") {
        return await handleSubmitQuiz(request, env, ctx);
      }
      if (request.method === "POST" && path === "/api/submit-weekly-exam") {
        return await handleSubmitWeeklyExam(request, env, ctx);
      }
      if (request.method === "GET" && path === "/api/schools") {
        return await handleGetSchools(request, env);
      }
      if (request.method === "POST" && path === "/api/store/click-ad") {
        return await handleAdClick(request, env);
      }
      if (request.method === "POST" && path === "/api/store/sync-points") {
        return await handleSyncPoints(request, env);
      }
      if (request.method === "POST" && path === "/api/store/purchase") {
        return await handleStorePurchase(request, env);
      }
      if (request.method === "POST" && path === "/api/store/equip") {
        return await handleStoreEquip(request, env);
      }
      if (request.method === "POST" && path === "/api/batch-sync") {
        return await handleBatchSync(request, env, ctx);
      }
      if (request.method === "GET" && path === "/api/leaderboard") {
        return await handleGetLeaderboards(request, env);
      }
      if (request.method === "GET" && path === "/api/admin/data") {
        return await handleAdminData(request, env);
      }
      if (request.method === "DELETE" && path.startsWith("/api/admin/user/")) {
        return await handleAdminDeleteUser(request, env, path);
      }

      return jsonResponse({ error: "Not Found" }, 404);
    } catch (err) {
      return jsonResponse({ error: "Internal Server Error", message: err.message }, 500);
    }
  },
};

function jsonResponse(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...CORS_HEADERS,
      ...extraHeaders,
    },
  });
}

async function hashPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hash = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hash));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

function generateUserId() {
  return crypto.randomUUID();
}

function getCurrentWeek() {
  const date = new Date();
  const day = (date.getDay() + 6) % 7; // Monday = 0
  date.setDate(date.getDate() - day + 3); // Nearest Thursday
  const firstThursday = new Date(date.getFullYear(), 0, 4);
  const week = Math.round(((date.getTime() - firstThursday.getTime()) / 86400000 - 3 + (firstThursday.getDay() + 6) % 7) / 7) + 1;
  return `${date.getFullYear()}-W${week.toString().padStart(2, '0')}`;
}

async function handleSignup(request, env) {
  const body = await request.json();
  const { password, name, surname, grade, school } = body;
  const username = body.username ? body.username.trim() : "";

  if (!username || !password) {
    return jsonResponse({ error: "Username and password are required" }, 400);
  }

  // Basic password rules: min 8 chars, 1 capital, 1 number
  if (password.length < 8 || !/[A-Z]/.test(password) || !/[0-9]/.test(password)) {
    return jsonResponse({ error: "Password must be at least 8 characters long, contain at least one capital letter and one number" }, 400);
  }

  // Check if username already exists
  const existingUser = await env.RANK_KV.get(`user_by_name:${username}`);
  if (existingUser) {
    return jsonResponse({ error: "Username already taken" }, 400);
  }

  const userId = generateUserId();
  const passwordHash = await hashPassword(password);

  const newUser = {
    user_id: userId,
    username,
    password_hash: passwordHash,
    name: name || "",
    surname: surname || "",
    grade: grade || "grade12",
    school: school || "",
    avatar_url: "",
    math_xp: 0,
    physics_xp: 0,
    subjects_xp: {}, // new dynamic tracking
    total_xp: 0,
    personal_math_xp: 0,
    personal_physics_xp: 0,
    personal_subjects_xp: {},
    personal_total_xp: 0,
    weekly_xp: 0,
    questions_answered: 0,
    correct_answers: 0,
    accuracy_percentage: 0,
    study_streak_days: 0,
    quizzes_completed: 0,
    last_quiz_date: null,
    topic_accuracy: {},
    completed_weekly_exams: {}
  };

  await env.RANK_KV.put(`user:${userId}`, JSON.stringify(newUser));
  await env.RANK_KV.put(`user_by_name:${username}`, userId); // Map username to user_id

  // Instantly place user on the leaderboards with 0 XP
  // Note: For handleSignup, we don't need ctx.waitUntil since this block is awaited or we can just await updateLeaderboards
  const currentWeek = getCurrentWeek();
  await updateLeaderboards(env, newUser, currentWeek, 0, "batch");
  await updateLeaderboardUser(env, userId, newUser);

  return jsonResponse({ message: "Signup successful", user_id: userId });
}

async function handleLogin(request, env) {
  const body = await request.json();
  const { password } = body;
  const username = body.username ? body.username.trim() : "";

  if (!username || !password) {
    return jsonResponse({ error: "Username and password are required" }, 400);
  }

  const userId = await env.RANK_KV.get(`user_by_name:${username}`);
  if (!userId) {
    return jsonResponse({ error: "Invalid username or password" }, 401);
  }

  const userDataString = await env.RANK_KV.get(`user:${userId}`);
  if (!userDataString) {
    return jsonResponse({ error: "User data not found" }, 500);
  }

  const userData = JSON.parse(userDataString);
  const passwordHash = await hashPassword(password);

  if (userData.password_hash !== passwordHash) {
    return jsonResponse({ error: "Invalid username or password" }, 401);
  }

  const today = new Date().toISOString().split('T')[0];
  if (userData.last_active_date !== today) {
    userData.last_active_date = today;
    await env.RANK_KV.put(`user:${userId}`, JSON.stringify(userData));
  }

  return jsonResponse({ message: "Login successful", user_id: userId });
}

async function handleGetUser(request, env, path) {
  const url = new URL(request.url);
  const userId = path.split("/").pop();
  if (!userId) return jsonResponse({ error: "User ID required" }, 400);

  const requestedSubjectsStr = url.searchParams.get("subjects");
  const requestedSubjects = requestedSubjectsStr ? requestedSubjectsStr.split(",") : ["math", "physics"];

  const userDataString = await env.RANK_KV.get(`user:${userId}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);

  // Exclude password hash from response
  delete userData.password_hash;

  if (!userData.grade) userData.grade = "grade12";
  const grade = userData.grade;
  if (!userData.school) userData.school = "";

  // Initialize new cosmetic fields if missing
  if (userData.dtech_points === undefined) userData.dtech_points = 0;

  // Calculate True Available Balance without mutating userData
  let pending_points = 0;
  try {
    let authQuery = "";
    if (env.FIREBASE_WORKER_EMAIL && env.FIREBASE_WORKER_PASSWORD) {
        const token = await getFirebaseAuthToken(env);
        if (token) authQuery = `?auth=${token}`;
    } else if (env.FIREBASE_SECRET) {
        authQuery = `?auth=${env.FIREBASE_SECRET}`;
    }
    const fbResponse = await fetch(`${FIREBASE_DB_URL}/user_commands/${userId}.json${authQuery}`);
    if (fbResponse.ok) {
      const commands = await fbResponse.json();
      if (commands) {
        for (const key in commands) {
          const cmd = commands[key];
          if (cmd && cmd.action === "points" && typeof cmd.points === "number") {
            pending_points += cmd.points;
          }
        }
      }
    }
  } catch (err) {
    console.error("Error fetching pending commands:", err);
  }
  userData.available_balance = userData.dtech_points + pending_points;

  if (userData.ad_clicks_today === undefined) userData.ad_clicks_today = 0;
  if (!userData.last_ad_click_date) userData.last_ad_click_date = "";
  if (!userData.last_push_claim_date) userData.last_push_claim_date = "";
  if (!userData.unlocked_cosmetics) userData.unlocked_cosmetics = [];
  if (!userData.equipped_cosmetics) userData.equipped_cosmetics = {};

  // Calculate ranks
  const overallLeaderboardStr = await env.RANK_KV.get(`leaderboard:${grade}:overall`) || await env.RANK_KV.get("leaderboard:overall") || "[]";
  const allGradesOverallStr = await env.RANK_KV.get("leaderboard:allgrades:overall") || "[]";
  const overallLeaderboard = JSON.parse(overallLeaderboardStr);
  const allGradesOverall = JSON.parse(allGradesOverallStr);

  const findRank = (board) => {
    const index = board.findIndex(u => u.user_id === userId);
    return index !== -1 ? index + 1 : "-";
  };

  userData.ranks = {
    overall: findRank(overallLeaderboard),
    all_grades_overall: findRank(allGradesOverall)
  };

  for (const sub of requestedSubjects) {
    const boardStr = await env.RANK_KV.get(`leaderboard:${grade}:${sub}`) || (grade === "grade12" ? await env.RANK_KV.get(`leaderboard:${sub}`) : null) || "[]";
    userData.ranks[sub] = findRank(JSON.parse(boardStr));
  }

  // Ensure backwards compatibility by maintaining math and physics ranks if they weren't requested specifically
  if (!requestedSubjects.includes("math")) {
      const mathStr = await env.RANK_KV.get(`leaderboard:${grade}:math`) || await env.RANK_KV.get("leaderboard:math") || "[]";
      userData.ranks.math = findRank(JSON.parse(mathStr));
  }
  if (!requestedSubjects.includes("physics")) {
      const physStr = await env.RANK_KV.get(`leaderboard:${grade}:physics`) || await env.RANK_KV.get("leaderboard:physics") || "[]";
      userData.ranks.physics = findRank(JSON.parse(physStr));
  }

  return jsonResponse(userData);
}

async function handleUpdateAvatar(request, env, path) {
  const match = path.match(/^\/api\/user\/([^/]+)\/avatar$/);
  if (!match) return jsonResponse({ error: "Invalid path" }, 400);
  const userId = match[1];

  const body = await request.json();
  const { avatar_url } = body;

  if (!avatar_url) {
    return jsonResponse({ error: "Avatar URL is required" }, 400);
  }

  const userDataString = await env.RANK_KV.get(`user:${userId}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);
  userData.avatar_url = avatar_url;

  await env.RANK_KV.put(`user:${userId}`, JSON.stringify(userData));

  // Update avatar in leaderboards
  await updateLeaderboardUser(env, userId, userData);

  return jsonResponse({ message: "Avatar updated successfully", avatar_url });
}

async function handleUpdateProfile(request, env, path) {
  const match = path.match(/^\/api\/user\/([^/]+)\/profile$/);
  if (!match) return jsonResponse({ error: "Invalid path" }, 400);
  const userId = match[1];

  const body = await request.json();
  const { name, surname, password, grade, school } = body;
  const username = body.username ? body.username.trim() : undefined;

  const userDataString = await env.RANK_KV.get(`user:${userId}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);
  const oldGrade = userData.grade || "grade12";


  // If username changes, check availability and update mapping
  if (username && username !== userData.username) {
    const existingUser = await env.RANK_KV.get(`user_by_name:${username}`);
    if (existingUser) {
      return jsonResponse({ error: "Username already taken" }, 400);
    }
    await env.RANK_KV.delete(`user_by_name:${userData.username}`);
    await env.RANK_KV.put(`user_by_name:${username}`, userId);
    userData.username = username;
  }

  if (name !== undefined) userData.name = name;
  if (surname !== undefined) userData.surname = surname;
  if (grade !== undefined) userData.grade = grade;
  if (!userData.grade) userData.grade = "grade12";
  if (school !== undefined) userData.school = school;

  if (password) {
    if (password.length < 8 || !/[A-Z]/.test(password) || !/[0-9]/.test(password)) {
      return jsonResponse({ error: "Password must be at least 8 characters long, contain at least one capital letter and one number" }, 400);
    }
    userData.password_hash = await hashPassword(password);
  }

  await env.RANK_KV.put(`user:${userId}`, JSON.stringify(userData));

  // Update profile details in leaderboards
  await updateLeaderboardUser(env, userId, userData);

  return jsonResponse({ message: "Profile updated successfully" });
}

async function updateLeaderboardUser(env, userId, userData) {
  const currentWeek = getCurrentWeek();
  const grade = userData.grade || "grade12";

  // Update overall and weekly dynamically, plus any subject leaderboards the user might be in.
  // Instead of hardcoding keys, we scan standard keys + subject keys found in userData.subjects_xp
  const baseKeys = [
    `leaderboard:${grade}:overall`, `leaderboard:${grade}:weekly:${currentWeek}`,
    "leaderboard:allgrades:overall", `leaderboard:allgrades:weekly:${currentWeek}`,
    "leaderboard:overall", `leaderboard:weekly:${currentWeek}`
  ];

  const subjects = Object.keys(userData.subjects_xp || {});
  // Legacy subjects
  if (!subjects.includes("math")) subjects.push("math");
  if (!subjects.includes("physics")) subjects.push("physics");

  for (const sub of subjects) {
    baseKeys.push(`leaderboard:${grade}:${sub}`);
    baseKeys.push(`leaderboard:allgrades:${sub}`);
    baseKeys.push(`leaderboard:${sub}`);
  }

  for (const key of baseKeys) {
    let boardStr = await env.RANK_KV.get(key);
    if (!boardStr) continue;

    let board = JSON.parse(boardStr);

    let updated = false;
    for (let i = 0; i < board.length; i++) {
      if (board[i].user_id === userId) {
        // Only update if there's an actual change in the profile fields
        if (
          board[i].username !== userData.username ||
          board[i].name !== userData.name ||
          board[i].surname !== userData.surname ||
          board[i].avatar_url !== userData.avatar_url ||
          JSON.stringify(board[i].equipped_cosmetics || {}) !== JSON.stringify(userData.equipped_cosmetics || {})
        ) {
          board[i].username = userData.username;
          board[i].name = userData.name;
          board[i].surname = userData.surname;
          board[i].avatar_url = userData.avatar_url;
          board[i].equipped_cosmetics = userData.equipped_cosmetics || {};
          updated = true;
        }
        break;
      }
    }

    if (updated) {
      await env.RANK_KV.put(key, JSON.stringify(board));
    }
  }
}

async function handleGetPublicUser(request, env, path) {
  const url = new URL(request.url);
  const username = decodeURIComponent(path.split("/").pop()).trim();
  if (!username) return jsonResponse({ error: "Username required" }, 400);

  const requestedSubjectsStr = url.searchParams.get("subjects");
  const requestedSubjects = requestedSubjectsStr ? requestedSubjectsStr.split(",") : ["math", "physics"];

  const userId = await env.RANK_KV.get(`user_by_name:${username}`);
  if (!userId) return jsonResponse({ error: "User not found" }, 404);

  const userDataString = await env.RANK_KV.get(`user:${userId}`);
  if (!userDataString) return jsonResponse({ error: "User data not found" }, 500);

  const userData = JSON.parse(userDataString);

  // Exclude sensitive info
  const publicData = {
    user_id: userId,
    username: userData.username,
    name: userData.name,
    surname: userData.surname,
    grade: userData.grade || "grade12",
    school: userData.school || "",
    avatar_url: userData.avatar_url || "",
    total_xp: userData.total_xp || 0,
    personal_total_xp: userData.personal_total_xp || 0,
    questions_answered: userData.questions_answered || 0,
    correct_answers: userData.correct_answers || 0,
    accuracy_percentage: userData.accuracy_percentage || 0,
    study_streak_days: userData.study_streak_days || 0,
    topic_accuracy: userData.topic_accuracy || {},
    completed_weekly_exams: userData.completed_weekly_exams || {},
    equipped_cosmetics: userData.equipped_cosmetics || {}
  };

  if (!userData.grade) userData.grade = "grade12";
  const grade = userData.grade;

  // Calculate ranks
  const overallLeaderboardStr = await env.RANK_KV.get(`leaderboard:${grade}:overall`) || await env.RANK_KV.get("leaderboard:overall") || "[]";
  const allGradesOverallStr = await env.RANK_KV.get("leaderboard:allgrades:overall") || "[]";

  const overallLeaderboard = JSON.parse(overallLeaderboardStr);
  const allGradesOverall = JSON.parse(allGradesOverallStr);

  const findRank = (board) => {
    const index = board.findIndex(u => u.user_id === userId);
    return index !== -1 ? index + 1 : "-";
  };

  publicData.ranks = {
    overall: findRank(overallLeaderboard),
    all_grades_overall: findRank(allGradesOverall)
  };

  for (const sub of requestedSubjects) {
    const boardStr = await env.RANK_KV.get(`leaderboard:${grade}:${sub}`) || (grade === "grade12" ? await env.RANK_KV.get(`leaderboard:${sub}`) : null) || "[]";
    publicData.ranks[sub] = findRank(JSON.parse(boardStr));
  }

  // Ensure backwards compatibility
  if (!requestedSubjects.includes("math")) {
      const mathStr = await env.RANK_KV.get(`leaderboard:${grade}:math`) || await env.RANK_KV.get("leaderboard:math") || "[]";
      publicData.ranks.math = findRank(JSON.parse(mathStr));
  }
  if (!requestedSubjects.includes("physics")) {
      const physStr = await env.RANK_KV.get(`leaderboard:${grade}:physics`) || await env.RANK_KV.get("leaderboard:physics") || "[]";
      publicData.ranks.physics = findRank(JSON.parse(physStr));
  }

  return jsonResponse(publicData, 200, {
    "Cache-Control": "public, max-age=60"
  });
}

async function handleSubmitQuiz(request, env, ctx) {
  const body = await request.json();
  const { user_id, subject, topic, total_questions, correct_answers } = body;

  if (!user_id || !subject || !topic || total_questions === undefined || correct_answers === undefined) {
    return jsonResponse({ error: "Missing required fields" }, 400);
  }

  const userDataString = await env.RANK_KV.get(`user:${user_id}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  let userData = JSON.parse(userDataString);

  // Initialize new personal XP fields if they don't exist
  if (userData.personal_total_xp === undefined) userData.personal_total_xp = userData.total_xp || 0;
  if (userData.personal_math_xp === undefined) userData.personal_math_xp = userData.math_xp || 0;
  if (userData.personal_physics_xp === undefined) userData.personal_physics_xp = userData.physics_xp || 0;
  if (userData.subjects_xp === undefined) userData.subjects_xp = {};
  if (userData.personal_subjects_xp === undefined) userData.personal_subjects_xp = {};

  // Map legacy mathematics to math
  const normalizedSubject = subject === "mathematics" ? "math" : subject;

  // Personal XP: +5 per correct answer (always added)
  const personalXpEarned = body.personalXp !== undefined ? body.personalXp : correct_answers * 5;
  userData.personal_total_xp += personalXpEarned;
  if (normalizedSubject === "math") {
    userData.personal_math_xp += personalXpEarned;
  } else if (normalizedSubject === "physics") {
    userData.personal_physics_xp += personalXpEarned;
  }

  if (!userData.personal_subjects_xp[normalizedSubject]) userData.personal_subjects_xp[normalizedSubject] = 0;
  userData.personal_subjects_xp[normalizedSubject] += personalXpEarned;

  // Public/Ranked XP and Streak Logic
  const scorePercentage = total_questions > 0 ? (correct_answers / total_questions) * 100 : 0;
  const passedThreshold = scorePercentage >= 50; // New minimum threshold requirement

  let publicXpEarned = 0;
  const currentWeek = getCurrentWeek();
  const today = new Date().toISOString().split('T')[0];

  if (passedThreshold) {
    const rawPublicXpEarned = body.publicXp !== undefined ? body.publicXp : correct_answers * 5;

    // Daily cap logic is now handled strictly by the frontend before sending payload,
    // but we still update the streak and last_active_date here.
    if (userData.last_quiz_date !== today) {
      userData.daily_xp = 0;
      userData.last_quiz_date = today;

      // Manage streak only if they pass
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = yesterday.toISOString().split('T')[0];
      if (userData.last_active_date === yesterdayStr) {
        userData.study_streak_days += 1;
      } else if (userData.last_active_date !== today) {
        userData.study_streak_days = 1;
      }
    }

    userData.last_active_date = today;

    // We trust the frontend's calculation for publicXpEarned (with a hard sanity cap just in case)
    publicXpEarned = Math.min(rawPublicXpEarned, correct_answers * 5); // Sanity max per quiz to prevent injection, but allows full legit XP

    userData.daily_xp = (userData.daily_xp || 0) + publicXpEarned;

    if (normalizedSubject === "math") {
      userData.math_xp += publicXpEarned;
    } else if (normalizedSubject === "physics") {
      userData.physics_xp += publicXpEarned;
    }

    if (!userData.subjects_xp[normalizedSubject]) userData.subjects_xp[normalizedSubject] = 0;
    userData.subjects_xp[normalizedSubject] += publicXpEarned;

    userData.total_xp += publicXpEarned;

    // Update weekly XP (reset if new week)
    if (userData.last_week !== currentWeek) {
      userData.weekly_xp = 0;
      userData.last_week = currentWeek;
    }
    userData.weekly_xp += publicXpEarned;
  } else {
    // Did not pass the threshold. Still reset weekly xp logic if it's a new week so old data isn't kept.
    if (userData.last_week !== currentWeek) {
      userData.weekly_xp = 0;
      userData.last_week = currentWeek;
    }
  }

  // Always update global stats regardless of score
  userData.questions_answered += total_questions;
  userData.correct_answers += correct_answers;
  if (body.rewarded_completions !== undefined) {
      userData.rewarded_completions = { ...(userData.rewarded_completions || {}), ...body.rewarded_completions };
  } else if (publicXpEarned > 0) {
      if (!userData.rewarded_completions) userData.rewarded_completions = {};
      const historyKey = `${normalizedSubject}_${topic}`;
      userData.rewarded_completions[historyKey] = (userData.rewarded_completions[historyKey] || 0) + 1;
  }
  userData.accuracy_percentage = userData.questions_answered > 0 ? Math.round((userData.correct_answers / userData.questions_answered) * 100) : 0;
  userData.quizzes_completed += 1;

  // Topic accuracy
  if (!userData.topic_accuracy[topic]) {
    userData.topic_accuracy[topic] = { correct: 0, total: 0 };
  }
  userData.topic_accuracy[topic].correct += correct_answers;
  userData.topic_accuracy[topic].total += total_questions;

  await env.RANK_KV.put(`user:${user_id}`, JSON.stringify(userData));

  // Update leaderboards sequentially to prevent race conditions during high load
  if (publicXpEarned > 0) {
    await updateLeaderboards(env, userData, currentWeek, publicXpEarned, normalizedSubject);
  }

  return jsonResponse({
    message: "Quiz submitted successfully",
    xp_earned: publicXpEarned,
    personal_xp_earned: personalXpEarned,
    passed_threshold: passedThreshold,
    score_percentage: scorePercentage
  });
}

async function handleSubmitWeeklyExam(request, env, ctx) {
  const body = await request.json();
  const { user_id, subject, exam_week, total_questions, correct_answers } = body;

  if (!user_id || !subject || !exam_week || total_questions === undefined || correct_answers === undefined) {
    return jsonResponse({ error: "Missing required fields" }, 400);
  }

  const userDataString = await env.RANK_KV.get(`user:${user_id}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  let userData = JSON.parse(userDataString);

  if (userData.completed_weekly_exams === undefined) userData.completed_weekly_exams = {};

  const examKey = `${exam_week}_${subject}`;
  if (userData.completed_weekly_exams[examKey]) {
    return jsonResponse({ error: "Weekly exam already completed for this subject" }, 403);
  }

  // Mark as completed
  userData.completed_weekly_exams[examKey] = {
    date: new Date().toISOString(),
    score: correct_answers,
    total: total_questions
  };

  if (userData.personal_total_xp === undefined) userData.personal_total_xp = userData.total_xp || 0;
  if (userData.subjects_xp === undefined) userData.subjects_xp = {};
  if (userData.personal_subjects_xp === undefined) userData.personal_subjects_xp = {};

  const normalizedSubject = subject === "mathematics" ? "math" : subject;

  const scorePercentage = total_questions > 0 ? (correct_answers / total_questions) * 100 : 0;

  let bonusXp = 0;
  let examXpEarned = body.totalXp !== undefined ? body.totalXp : 0;
  let pointsEarned = body.points !== undefined ? body.points : 0;

  if (body.totalXp === undefined && scorePercentage >= 40) {
    let base_xp = correct_answers * 8;

    if (scorePercentage > 80) {
        if (scorePercentage >= 95) bonusXp = 150;
        else if (scorePercentage >= 90) bonusXp = 100;
        else bonusXp = 50;
    }
    examXpEarned = base_xp + bonusXp;
    pointsEarned = examXpEarned * 2;
  }

  const currentWeek = getCurrentWeek();

  // Note: Weekly exam points bypass the daily cap!

  if (examXpEarned > 0) {
      // Update Personal XP
      userData.personal_total_xp += examXpEarned;
      if (!userData.personal_subjects_xp[normalizedSubject]) userData.personal_subjects_xp[normalizedSubject] = 0;
      userData.personal_subjects_xp[normalizedSubject] += examXpEarned;

      // Update Public XP
      userData.total_xp += examXpEarned;
      if (!userData.subjects_xp[normalizedSubject]) userData.subjects_xp[normalizedSubject] = 0;
      userData.subjects_xp[normalizedSubject] += examXpEarned;

      // Legacy fields mapping
      if (normalizedSubject === "math") {
        userData.math_xp += examXpEarned;
        if (userData.personal_math_xp === undefined) userData.personal_math_xp = userData.math_xp || 0;
        userData.personal_math_xp += examXpEarned;
      } else if (normalizedSubject === "physics") {
        userData.physics_xp += examXpEarned;
        if (userData.personal_physics_xp === undefined) userData.personal_physics_xp = userData.physics_xp || 0;
        userData.personal_physics_xp += examXpEarned;
      }

      if (userData.dtech_points === undefined) userData.dtech_points = 0;
      userData.dtech_points += pointsEarned;
  }

  // Update weekly XP
  if (userData.last_week !== currentWeek) {
    userData.weekly_xp = 0;
    userData.last_week = currentWeek;
  }
  userData.weekly_xp += examXpEarned;

  // Global stats
  userData.questions_answered += total_questions;
  userData.correct_answers += correct_answers;
  if (body.rewarded_completions !== undefined) {
      userData.rewarded_completions = { ...(userData.rewarded_completions || {}), ...body.rewarded_completions };
  } else if (examXpEarned > 0) {
      if (!userData.rewarded_completions) userData.rewarded_completions = {};
      const historyKey = `${normalizedSubject}_${typeof topic !== 'undefined' ? topic : 'weekly_exam'}`;
      userData.rewarded_completions[historyKey] = (userData.rewarded_completions[historyKey] || 0) + 1;
  }
  userData.accuracy_percentage = userData.questions_answered > 0 ? Math.round((userData.correct_answers / userData.questions_answered) * 100) : 0;
  userData.quizzes_completed += 1;

  const today = new Date().toISOString().split('T')[0];
  userData.last_active_date = today;

  await env.RANK_KV.put(`user:${user_id}`, JSON.stringify(userData));

  if (examXpEarned > 0) {
    await updateLeaderboards(env, userData, currentWeek, examXpEarned, normalizedSubject);
  }

  return jsonResponse({
    message: "Weekly exam submitted successfully",
    xp_earned: examXpEarned,
    bonus_xp: bonusXp,
    score_percentage: scorePercentage
  });
}

async function updateLeaderboards(env, user, currentWeek, publicXpEarned, subject) {
  const updateBoard = async (key, sortByField, isDynamicSubject = false) => {
    if (isDynamicSubject && (subject === "batch" || !subject)) return;
    let boardStr = await env.RANK_KV.get(key) || "[]";
    let board = JSON.parse(boardStr);

    let xpVal = isDynamicSubject ? user.subjects_xp[subject] : user[sortByField];
    if (xpVal === undefined) xpVal = 0;

    const existingIndex = board.findIndex(u => u.user_id === user.user_id);
    const wasInBoard = existingIndex !== -1;
    const existingEntry = wasInBoard ? board[existingIndex] : null;

    // Fast return if the user isn't in the top 1000 and their new XP wouldn't put them there
    if (!wasInBoard && board.length >= 1000 && xpVal <= board[board.length - 1].xp) {
      return;
    }

    // Fast return if the user is in the board but nothing changed (no XP gained, no cosmetic changes relevant here)
    if (wasInBoard && existingEntry.xp === xpVal) {
      // updateLeaderboards is mainly for XP sorting. If XP hasn't changed, updateLeaderboardUser handles profile updates.
      return;
    }

    // Remove existing entry
    board = board.filter(u => u.user_id !== user.user_id);

    // Add new entry
    board.push({
      user_id: user.user_id,
      username: user.username,
      name: user.name,
      surname: user.surname,
      avatar_url: user.avatar_url,
      equipped_cosmetics: user.equipped_cosmetics || {},
      xp: xpVal
    });

    // Sort and keep top (e.g., top 1000)
    board.sort((a, b) => b.xp - a.xp);
    if (board.length > 1000) board = board.slice(0, 1000);

    await env.RANK_KV.put(key, JSON.stringify(board));
  };

  const grade = user.grade || "grade12";

  // Update school leaderboard if user has a school and earned public XP
  let schoolPromise = Promise.resolve();
  if (user.school && publicXpEarned && publicXpEarned > 0) {
    schoolPromise = (async () => {
      const schoolKey = "leaderboard:schools:overall";
      let schoolBoardStr = await env.RANK_KV.get(schoolKey) || "[]";
      let schoolBoard = JSON.parse(schoolBoardStr);

      let schoolEntry = schoolBoard.find(s => s.school_name === user.school);
      if (schoolEntry) {
        schoolEntry.xp += publicXpEarned;
      } else {
        schoolBoard.push({
          school_name: user.school,
          xp: publicXpEarned
        });
      }

      schoolBoard.sort((a, b) => b.xp - a.xp);
      await env.RANK_KV.put(schoolKey, JSON.stringify(schoolBoard));
    })();
  }

  const promises = [
    schoolPromise,
    updateBoard(`leaderboard:${grade}:overall`, "total_xp"),
    updateBoard(`leaderboard:${grade}:weekly:${currentWeek}`, "weekly_xp"),
    updateBoard("leaderboard:allgrades:overall", "total_xp"),
    updateBoard(`leaderboard:allgrades:weekly:${currentWeek}`, "weekly_xp"),
    updateBoard(`leaderboard:${grade}:${subject}`, subject, true),
    updateBoard(`leaderboard:allgrades:${subject}`, subject, true)
  ];

  // For backwards compatibility, update old math/physics paths if needed
  if (subject === "math" || subject === "physics") {
      promises.push(updateBoard(`leaderboard:${grade}:${subject}`, `${subject}_xp`));
      promises.push(updateBoard(`leaderboard:allgrades:${subject}`, `${subject}_xp`));
  }

  await Promise.all(promises);
}

async function handleScheduledSync(env) {
  try {
    let authQuery = "";
    if (env.FIREBASE_WORKER_EMAIL && env.FIREBASE_WORKER_PASSWORD) {
        const token = await getFirebaseAuthToken(env);
        if (token) authQuery = `?auth=${token}`;
    } else if (env.FIREBASE_SECRET) {
        authQuery = `?auth=${env.FIREBASE_SECRET}`;
    }
    const fbResponse = await fetch(`${FIREBASE_DB_URL}/user_commands.json${authQuery}`);
    if (!fbResponse.ok) return;

    const allUsersCommands = await fbResponse.json();
    if (!allUsersCommands) return;

    const today = new Date().toISOString().split("T")[0];
    const currentWeek = getCurrentWeek();

    for (const userId in allUsersCommands) {
      const commandsObj = allUsersCommands[userId];
      if (!commandsObj) continue;

      const userDataString = await env.RANK_KV.get(`user:${userId}`);
      if (!userDataString) continue;

      let userData = JSON.parse(userDataString);
      let xpGained = false;
      let totalXpEarned = 0;
      let subjectsToUpdate = new Set();

      // Convert object to array and sort by timestamp
      const commands = Object.values(commandsObj);
      commands.sort((a, b) => a.timestamp - b.timestamp);

      // Track processed IDs to avoid duplicates
      if (!userData.processed_commands) userData.processed_commands = [];
      const MAX_PROCESSED_HISTORY = 100;

      for (const cmd of commands) {
          if (userData.processed_commands.includes(cmd.unique_id)) continue;

          if (cmd.action === "quiz") {
              userData.personal_total_xp = (userData.personal_total_xp || 0) + (cmd.personalXp || 0);

              const mappedSubject = cmd.subject === "mathematics" ? "math" : cmd.subject;

              if (mappedSubject === "math") userData.personal_math_xp = (userData.personal_math_xp || 0) + (cmd.personalXp || 0);
              else if (mappedSubject === "physics") userData.personal_physics_xp = (userData.personal_physics_xp || 0) + (cmd.personalXp || 0);

              if (!userData.personal_subjects_xp) userData.personal_subjects_xp = {};
              userData.personal_subjects_xp[mappedSubject] = (userData.personal_subjects_xp[mappedSubject] || 0) + (cmd.personalXp || 0);

              if (cmd.passed) {
                  userData.last_quiz_date = cmd.date;
                  userData.last_active_date = cmd.date;

                  userData.daily_xp = (userData.daily_xp || 0) + (cmd.publicXp || 0);
                  if (mappedSubject === "math") userData.math_xp = (userData.math_xp || 0) + (cmd.publicXp || 0);
                  else if (mappedSubject === "physics") userData.physics_xp = (userData.physics_xp || 0) + (cmd.publicXp || 0);

                  if (!userData.subjects_xp) userData.subjects_xp = {};
                  userData.subjects_xp[mappedSubject] = (userData.subjects_xp[mappedSubject] || 0) + (cmd.publicXp || 0);
                  userData.total_xp = (userData.total_xp || 0) + (cmd.publicXp || 0);

                  xpGained = true;
                  totalXpEarned += (cmd.publicXp || 0);
                  subjectsToUpdate.add(mappedSubject);
              }

              userData.questions_answered = (userData.questions_answered || 0) + (cmd.totalQs || 0);
              userData.correct_answers = (userData.correct_answers || 0) + (cmd.correct || 0);
              userData.quizzes_completed = (userData.quizzes_completed || 0) + 1;

              if (cmd.topic && cmd.totalQs) {
                  if (!userData.topic_accuracy) userData.topic_accuracy = {};
                  if (!userData.topic_accuracy[cmd.topic]) {
                      userData.topic_accuracy[cmd.topic] = { correct: 0, total: 0 };
                  }
                  userData.topic_accuracy[cmd.topic].correct += cmd.correct;
                  userData.topic_accuracy[cmd.topic].total += cmd.totalQs;
              }

              if (!userData.quiz_history) userData.quiz_history = {};
              const historyKey = `${mappedSubject}_${cmd.topic}`;
              userData.quiz_history[historyKey] = (userData.quiz_history[historyKey] || 0) + 1;

          } else if (cmd.action === "weekly") {
              if (!userData.completed_weekly_exams) userData.completed_weekly_exams = {};
              if (!userData.completed_weekly_exams[cmd.examKey]) {
                  userData.completed_weekly_exams[cmd.examKey] = {
                      date: new Date().toISOString(),
                      score: cmd.score,
                      total: cmd.totalQs
                  };
                  userData.personal_total_xp = (userData.personal_total_xp || 0) + (cmd.totalXp || 0);
                  if (!userData.personal_subjects_xp) userData.personal_subjects_xp = {};
                  userData.personal_subjects_xp[cmd.subject] = (userData.personal_subjects_xp[cmd.subject] || 0) + (cmd.totalXp || 0);

                  userData.total_xp = (userData.total_xp || 0) + (cmd.totalXp || 0);
                  if (!userData.subjects_xp) userData.subjects_xp = {};
                  userData.subjects_xp[cmd.subject] = (userData.subjects_xp[cmd.subject] || 0) + (cmd.totalXp || 0);

                  xpGained = true;
                  totalXpEarned += (cmd.totalXp || 0);
                  subjectsToUpdate.add(cmd.subject);
              }
              userData.questions_answered = (userData.questions_answered || 0) + (cmd.totalQs || 0);
              userData.correct_answers = (userData.correct_answers || 0) + (cmd.score || 0);
              userData.quizzes_completed = (userData.quizzes_completed || 0) + 1;

          } else if (cmd.action === "points") {
              userData.dtech_points = (userData.dtech_points || 0) + (cmd.points || 0);
          }

          userData.processed_commands.push(cmd.unique_id);
          // Keep processed commands list manageable
          if (userData.processed_commands.length > MAX_PROCESSED_HISTORY) {
              userData.processed_commands.shift();
          }
      }

      if (userData.questions_answered > 0) {
          userData.accuracy_percentage = Math.round((userData.correct_answers / userData.questions_answered) * 100);
      } else {
          userData.accuracy_percentage = 0;
      }

      const oldLevel = userData.level || 1;
      userData.level = Math.floor((userData.personal_total_xp || userData.total_xp || 0) / 100) + 1;

      // Save back to KV
      await env.RANK_KV.put(`user:${userId}`, JSON.stringify(userData));

      // Process sequentially to prevent leaderboard race conditions
      if (xpGained || totalXpEarned > 0) {
          await updateLeaderboards(env, userData, currentWeek, totalXpEarned, "batch");
          for (const subj of subjectsToUpdate) {
              await updateLeaderboards(env, userData, currentWeek, 0, subj);
          }
      }
      await updateLeaderboardUser(env, userId, userData);

      // Safe Delete from Firebase
      // Delete only the successfully processed commands to avoid race condition with new incoming commands
      const patchObj = {};
      for (const cmd of commands) {
          patchObj[cmd.unique_id] = null;
      }
      await fetch(`${FIREBASE_DB_URL}/user_commands/${userId}.json${authQuery}`, {
          method: 'PATCH',
          body: JSON.stringify(patchObj)
      });
    }
  } catch (e) {
    console.error("Scheduled Sync Failed:", e);
  }
}

async function handleBatchSync(request, env, ctx) {
  const body = await request.json();
  const { user_id, queue } = body;

  if (!user_id || !Array.isArray(queue)) {
    return jsonResponse({ error: "Missing user_id or invalid queue" }, 400);
  }

  const userDataString = await env.RANK_KV.get(`user:${user_id}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  let userData = JSON.parse(userDataString);
  let totalXpEarned = 0;
  let totalPointsEarned = 0;
  let xpGained = false; // To know if we should update leaderboard asynchronously
  let today = new Date().toISOString().split("T")[0];
  let subjectsToUpdate = new Set();

  for (const item of queue) {
    if (item.url.includes('/api/submit-quiz')) {
      const { subject, topic, total_questions, correct_answers } = item.data;
      if (!subject || !topic || total_questions === undefined || correct_answers === undefined) continue;

      // Initialize fields
      if (userData.personal_total_xp === undefined) userData.personal_total_xp = userData.total_xp || 0;
      if (userData.personal_math_xp === undefined) userData.personal_math_xp = userData.math_xp || 0;
      if (userData.personal_physics_xp === undefined) userData.personal_physics_xp = userData.physics_xp || 0;
      if (userData.subjects_xp === undefined) userData.subjects_xp = {};
      if (userData.personal_subjects_xp === undefined) userData.personal_subjects_xp = {};

      const mappedSubject = subject === "mathematics" ? "math" : subject;
      const historyKey = `${mappedSubject}_${topic}`;
      const percentage = (correct_answers / total_questions) * 100;
      const passed = percentage >= 50;

      if (userData.quiz_history === undefined) userData.quiz_history = {};
      const attempts = userData.quiz_history[historyKey] || 0;


      let xpEarned = item.data.publicXp !== undefined ? item.data.publicXp : 0;
      let personalXpEarned = item.data.personalXp !== undefined ? item.data.personalXp : (passed ? 50 : 0); // rough fallback
      let pointsEarned = xpEarned > 0 ? Math.floor(xpEarned / 5) : 0; // Fallback heuristic if not provided
      if (item.data.points !== undefined) pointsEarned = item.data.points;

      // Fallback to legacy logic if frontend didn't send publicXp
      if (item.data.publicXp === undefined && passed && attempts < 3) {
        if (attempts === 0) {
          xpEarned = 50;
          pointsEarned = 10;
        } else if (attempts === 1) {
          xpEarned = 25;
          pointsEarned = 5;
        } else if (attempts === 2) {
          xpEarned = 10;
          pointsEarned = 2;
        }
        personalXpEarned = xpEarned;
      }

      if (item.data.publicXp !== undefined || (passed && attempts < 3)) {

        userData.personal_total_xp += personalXpEarned;
        userData.total_xp += xpEarned; // Decouple total_xp from personal_total_xp

        if (mappedSubject === "math") {
          userData.personal_math_xp += personalXpEarned;
          userData.math_xp += xpEarned;
        } else if (mappedSubject === "physics") {
          userData.personal_physics_xp += personalXpEarned;
          userData.physics_xp += xpEarned;
        } else {
          userData.personal_subjects_xp[mappedSubject] = (userData.personal_subjects_xp[mappedSubject] || 0) + personalXpEarned;
          userData.subjects_xp[mappedSubject] = (userData.subjects_xp[mappedSubject] || 0) + xpEarned;
        }


        if (userData.dtech_points === undefined) userData.dtech_points = 0;
        userData.dtech_points += pointsEarned;

        totalXpEarned += xpEarned;
        totalPointsEarned += pointsEarned;
        xpGained = true;
        subjectsToUpdate.add(mappedSubject);
      }

      userData.quiz_history[historyKey] = attempts + 1;
      if (item.data.rewarded_completions !== undefined) {
          userData.rewarded_completions = { ...(userData.rewarded_completions || {}), ...item.data.rewarded_completions };
      } else if (item.data.publicXp > 0) {
          if (!userData.rewarded_completions) userData.rewarded_completions = {};
          userData.rewarded_completions[historyKey] = (userData.rewarded_completions[historyKey] || 0) + 1;
      }

    } else if (item.url.includes('/api/submit-weekly-exam')) {
      const { subject, exam_week, total_questions, correct_answers } = item.data;
      if (!subject || !exam_week || total_questions === undefined || correct_answers === undefined) continue;

      if (userData.completed_weekly_exams === undefined) userData.completed_weekly_exams = {};
      const examKey = `${exam_week}_${subject}`;

      if (userData.completed_weekly_exams[examKey]) continue;

      userData.completed_weekly_exams[examKey] = {
        score: correct_answers,
        total: total_questions,
        date: today
      };

      const percentage = (correct_answers / total_questions) * 100;
      const passed = percentage >= 40;


      let bonusXp = 0;
      let xpEarned = item.data.totalXp !== undefined ? item.data.totalXp : 0;
      let personalXpEarned = item.data.totalXp !== undefined ? item.data.totalXp : 0; // Same for weekly
      let pointsEarned = item.data.points !== undefined ? item.data.points : 0;

      if (item.data.totalXp === undefined && passed) {
        let base_xp = correct_answers * 8;
        if (percentage > 80) {
            if (percentage >= 95) bonusXp = 150;
            else if (percentage >= 90) bonusXp = 100;
            else bonusXp = 50;
        }
        xpEarned = base_xp + bonusXp;
        personalXpEarned = xpEarned;
        pointsEarned = xpEarned * 2;
      }
      if (xpEarned > 0 || pointsEarned > 0 || (item.data.totalXp === undefined && passed)) {

        // Ensure fields
        if (userData.personal_total_xp === undefined) userData.personal_total_xp = userData.total_xp || 0;
        if (userData.personal_math_xp === undefined) userData.personal_math_xp = userData.math_xp || 0;
        if (userData.personal_physics_xp === undefined) userData.personal_physics_xp = userData.physics_xp || 0;
        if (userData.subjects_xp === undefined) userData.subjects_xp = {};
        if (userData.personal_subjects_xp === undefined) userData.personal_subjects_xp = {};

        userData.personal_total_xp += personalXpEarned;
        userData.total_xp += xpEarned;

        const mappedSubject = subject === "mathematics" ? "math" : subject;

        if (mappedSubject === "math") {
          userData.personal_math_xp += personalXpEarned;
          userData.math_xp += xpEarned;
        } else if (mappedSubject === "physics") {
          userData.personal_physics_xp += personalXpEarned;
          userData.physics_xp += xpEarned;
        } else {
          userData.personal_subjects_xp[mappedSubject] = (userData.personal_subjects_xp[mappedSubject] || 0) + personalXpEarned;
          userData.subjects_xp[mappedSubject] = (userData.subjects_xp[mappedSubject] || 0) + xpEarned;
        }


        if (userData.dtech_points === undefined) userData.dtech_points = 0;
        userData.dtech_points += pointsEarned;

        totalXpEarned += xpEarned;
        totalPointsEarned += pointsEarned;
        xpGained = true;
        subjectsToUpdate.add(mappedSubject);
      }
    } else if (item.url.includes('/api/store/sync-points')) {
      const { added_points, ads_clicked, push_claim } = item.data;

      if (userData.last_ad_click_date !== today) {
        userData.last_ad_click_date = today;
        userData.ad_clicks_today = 0;
      }

      if (userData.dtech_points === undefined) userData.dtech_points = 0;

      if (ads_clicked && added_points) {
        let maxAllowedClicks = 30; // Max 30 ad points per day
        let currentClicks = userData.ad_clicks_today || 0;

        let actuallyAddClicks = Math.min(ads_clicked, maxAllowedClicks - currentClicks);

        if (actuallyAddClicks > 0) {
           userData.ad_clicks_today = currentClicks + actuallyAddClicks;
           let pointsFromClicks = actuallyAddClicks * 1;

           let extraBonusPoints = added_points - pointsFromClicks;
           let validExtraBonus = Math.max(0, extraBonusPoints);

           let totalToAdd = pointsFromClicks + validExtraBonus;

           userData.dtech_points += totalToAdd;
           totalPointsEarned += totalToAdd;
        }
      } else if (added_points && !ads_clicked) {
          // just bonus points
          userData.dtech_points += added_points;
          totalPointsEarned += added_points;
      }

      if (push_claim) {
        if (userData.last_push_claim_date !== today) {
           userData.last_push_claim_date = today;
           userData.dtech_points += 100;
           totalPointsEarned += 100;
        }
      }
    }
  }

  // Update level
  const oldLevel = userData.level || 1;
  const newLevel = Math.floor((userData.personal_total_xp || userData.total_xp || 0) / 100) + 1;
  userData.level = newLevel;

  if (userData.last_active_date !== today) {
    userData.last_active_date = today;
  }

  await env.RANK_KV.put(`user:${user_id}`, JSON.stringify(userData));

  const currentWeek = getCurrentWeek();
  // Only update leaderboards if XP was actually gained, to reduce KV writes
  if (xpGained) {
    await updateLeaderboards(env, userData, currentWeek, totalXpEarned || 0, "batch");
    for (const subj of subjectsToUpdate) {
        await updateLeaderboards(env, userData, currentWeek, 0, subj);
    }
  }
  await updateLeaderboardUser(env, user_id, userData);

  return jsonResponse({
    success: true,
    message: "Batch sync successful",
    xpEarned: totalXpEarned,
    pointsEarned: totalPointsEarned,
    newLevel: newLevel,
    leveledUp: newLevel > oldLevel
  }, 200);
}

async function handleGetLeaderboards(request, env) {
  const url = new URL(request.url);
  const grade = url.searchParams.get("grade") || "grade12";
  const subjectsStr = url.searchParams.get("subjects");
  const subjects = subjectsStr ? subjectsStr.split(",") : ["math", "physics"];
  const currentWeek = getCurrentWeek();

  // Common boards
  const overallStr = await env.RANK_KV.get(`leaderboard:${grade}:overall`) || (grade === "grade12" ? await env.RANK_KV.get("leaderboard:overall") : null) || "[]";
  const weeklyStr = await env.RANK_KV.get(`leaderboard:${grade}:weekly:${currentWeek}`) || (grade === "grade12" ? await env.RANK_KV.get(`leaderboard:weekly:${currentWeek}`) : null) || "[]";

  const allOverallStr = await env.RANK_KV.get("leaderboard:allgrades:overall") || "[]";
  const allWeeklyStr = await env.RANK_KV.get(`leaderboard:allgrades:weekly:${currentWeek}`) || "[]";
  const schoolsOverallStr = await env.RANK_KV.get("leaderboard:schools:overall") || "[]";

  const response = {
    overall: JSON.parse(overallStr),
    weekly: JSON.parse(weeklyStr),
    all_overall: JSON.parse(allOverallStr),
    all_weekly: JSON.parse(allWeeklyStr),
    schools_overall: JSON.parse(schoolsOverallStr)
  };

  // Dynamic subject boards
  for (const sub of subjects) {
      const subStr = await env.RANK_KV.get(`leaderboard:${grade}:${sub}`) || (grade === "grade12" ? await env.RANK_KV.get(`leaderboard:${sub}`) : null) || "[]";
      const allSubStr = await env.RANK_KV.get(`leaderboard:allgrades:${sub}`) || "[]";
      response[sub] = JSON.parse(subStr);
      response[`all_${sub}`] = JSON.parse(allSubStr);
  }

  // Backwards compatibility
  if (!subjects.includes("math")) {
      response.math = JSON.parse(await env.RANK_KV.get(`leaderboard:${grade}:math`) || (grade === "grade12" ? await env.RANK_KV.get("leaderboard:math") : null) || "[]");
      response.all_math = JSON.parse(await env.RANK_KV.get("leaderboard:allgrades:math") || "[]");
  }
  if (!subjects.includes("physics")) {
      response.physics = JSON.parse(await env.RANK_KV.get(`leaderboard:${grade}:physics`) || (grade === "grade12" ? await env.RANK_KV.get("leaderboard:physics") : null) || "[]");
      response.all_physics = JSON.parse(await env.RANK_KV.get("leaderboard:allgrades:physics") || "[]");
  }

  return jsonResponse(response, 200, {
    "Cache-Control": "public, max-age=300"
  });
}

async function handleGetSchools(request, env) {
  // Read from the schools leaderboard to get all active schools
  const schoolsOverallStr = await env.RANK_KV.get("leaderboard:schools:overall") || "[]";
  const schoolsBoard = JSON.parse(schoolsOverallStr);
  const schoolsList = schoolsBoard.map(s => s.school_name);

  return jsonResponse({
    schools: schoolsList
  }, 200, {
    "Cache-Control": "public, max-age=86400"
  });
}

async function handleAdminData(request, env) {
  const url = new URL(request.url);
  const secret = url.searchParams.get("secret");
  if (secret !== "admin-secret-123") {
    return jsonResponse({ error: "Unauthorized" }, 401);
  }

  // Iterate over all keys starting with "user:"
  let users = [];
  let cursor = "";
  let listComplete = false;

  while (!listComplete) {
    const listResult = await env.RANK_KV.list({ prefix: "user:", cursor: cursor });

    // Process this batch of keys
    const promises = listResult.keys.map(key => env.RANK_KV.get(key.name));
    const userStrings = await Promise.all(promises);

    for (const userStr of userStrings) {
      if (userStr) {
        users.push(JSON.parse(userStr));
      }
    }

    listComplete = listResult.list_complete;
    cursor = listResult.cursor;
  }

  const today = new Date();
  const todayStr = today.toISOString().split('T')[0];

  // Calculate active thresholds
  const oneWeekAgo = new Date(today);
  oneWeekAgo.setDate(today.getDate() - 7);
  const oneWeekAgoStr = oneWeekAgo.toISOString().split('T')[0];

  const oneMonthAgo = new Date(today);
  oneMonthAgo.setMonth(today.getMonth() - 1);
  const oneMonthAgoStr = oneMonthAgo.toISOString().split('T')[0];

  const oneYearAgo = new Date(today);
  oneYearAgo.setFullYear(today.getFullYear() - 1);
  const oneYearAgoStr = oneYearAgo.toISOString().split('T')[0];

  let activeToday = 0;
  let activeWeek = 0;
  let activeMonth = 0;
  let activeYear = 0;
  let activeAllTime = users.length; // Same as total users

  let totalQuizzes = 0;
  let totalQuestions = 0;
  let totalCorrect = 0;

  let mostActiveUserToday = null;
  let maxQuestionsToday = -1;

  // Prepare user list for the admin panel, omit sensitive fields like password
  const adminUserList = [];

  for (const user of users) {
    const lastActive = user.last_active_date;
    if (lastActive) {
      if (lastActive === todayStr) activeToday++;
      if (lastActive >= oneWeekAgoStr) activeWeek++;
      if (lastActive >= oneMonthAgoStr) activeMonth++;
      if (lastActive >= oneYearAgoStr) activeYear++;
    }

    totalQuizzes += (user.quizzes_completed || 0);
    totalQuestions += (user.questions_answered || 0);
    totalCorrect += (user.correct_answers || 0);

    // Naive "most active today" - could use daily_xp or last_active_date combined with questions answered
    // If they were active today and answered more questions overall (simplification since daily questions aren't strictly tracked in isolation here, but daily_xp is tracked per quiz submission)
    if (lastActive === todayStr) {
        const activityScore = user.daily_xp || 0;
        if (activityScore > maxQuestionsToday) {
            maxQuestionsToday = activityScore;
            mostActiveUserToday = {
                username: user.username,
                xp_today: activityScore
            };
        }
    }

    adminUserList.push({
      user_id: user.user_id,
      username: user.username,
      name: user.name,
      surname: user.surname,
      grade: user.grade || "grade12",
      total_xp: user.total_xp || 0,
      quizzes_completed: user.quizzes_completed || 0,
      questions_answered: user.questions_answered || 0,
      accuracy_percentage: user.accuracy_percentage || 0,
      last_active_date: user.last_active_date || "Never"
    });
  }

  const averageScore = totalQuestions > 0 ? Math.round((totalCorrect / totalQuestions) * 100) : 0;

  // Sort for top 5 users
  const topUsers = [...adminUserList].sort((a, b) => b.total_xp - a.total_xp).slice(0, 5);

  return jsonResponse({
    stats: {
      total_users: users.length,
      active_today: activeToday,
      active_week: activeWeek,
      active_month: activeMonth,
      active_year: activeYear,
      active_all_time: activeAllTime,
      total_quizzes: totalQuizzes,
      total_questions: totalQuestions,
      average_score: averageScore,
      most_active_user_today: mostActiveUserToday,
      last_updated: new Date().toISOString()
    },
    top_users: topUsers,
    users: adminUserList
  });
}

async function handleAdminDeleteUser(request, env, path) {
  const url = new URL(request.url);
  const secret = url.searchParams.get("secret");
  if (secret !== "admin-secret-123") {
    return jsonResponse({ error: "Unauthorized" }, 401);
  }

  const userId = path.split("/").pop();
  if (!userId) {
    return jsonResponse({ error: "User ID required" }, 400);
  }

  const userStr = await env.RANK_KV.get(`user:${userId}`);
  if (!userStr) {
    return jsonResponse({ error: "User not found" }, 404);
  }

  const user = JSON.parse(userStr);
  const username = user.username;
  const grade = user.grade || "grade12";
  const school = user.school;

  // 1. Delete user record and username mapping
  await env.RANK_KV.delete(`user:${userId}`);
  if (username) {
    await env.RANK_KV.delete(`user_by_name:${username}`);
  }

  // 2. Remove user from all relevant leaderboards immediately
  const currentWeek = getCurrentWeek();
  const keysToUpdate = [
    `leaderboard:${grade}:overall`,
    `leaderboard:${grade}:weekly:${currentWeek}`,
    `leaderboard:allgrades:overall`,
    `leaderboard:allgrades:weekly:${currentWeek}`,
    `leaderboard:overall`, // legacy
    `leaderboard:weekly:${currentWeek}` // legacy
  ];

  const subjects = Object.keys(user.subjects_xp || {});
  if (!subjects.includes("math")) subjects.push("math");
  if (!subjects.includes("physics")) subjects.push("physics");

  for (const sub of subjects) {
    keysToUpdate.push(`leaderboard:${grade}:${sub}`);
    keysToUpdate.push(`leaderboard:allgrades:${sub}`);
    keysToUpdate.push(`leaderboard:${sub}`); // legacy
  }

  for (const key of keysToUpdate) {
    let boardStr = await env.RANK_KV.get(key);
    if (boardStr) {
      let board = JSON.parse(boardStr);
      const originalLength = board.length;
      board = board.filter(u => u.user_id !== userId);

      // Only write back if we actually removed someone
      if (board.length !== originalLength) {
        await env.RANK_KV.put(key, JSON.stringify(board));
      }
    }
  }

  return jsonResponse({ message: "User completely deleted" });
}

async function handleAdClick(request, env) {
  const { user_id } = await request.json();
  if (!user_id) return jsonResponse({ error: "user_id required" }, 400);

  const userDataString = await env.RANK_KV.get(`user:${user_id}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);
  const today = new Date().toISOString().split("T")[0];

  if (userData.last_ad_click_date !== today) {
    userData.last_ad_click_date = today;
    userData.ad_clicks_today = 0;
  }

  if (userData.ad_clicks_today >= 30) {
    return jsonResponse({ error: "Daily ad click limit reached" }, 400);
  }

  const pointsEarned = Math.floor(Math.random() * 50) + 1; // 1 to 50

  if (userData.dtech_points === undefined) userData.dtech_points = 0;
  userData.dtech_points += pointsEarned;
  userData.ad_clicks_today += 1;

  await env.RANK_KV.put(`user:${user_id}`, JSON.stringify(userData));

  return jsonResponse({
    success: true,
    points_earned: pointsEarned,
    new_balance: userData.dtech_points,
    clicks_today: userData.ad_clicks_today
  });
}

async function handleSyncPoints(request, env) {
  const { user_id, added_points, ads_clicked, push_claim } = await request.json();
  if (!user_id) return jsonResponse({ error: "user_id required" }, 400);

  const userDataString = await env.RANK_KV.get(`user:${user_id}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);
  const today = new Date().toISOString().split("T")[0];

  if (userData.last_ad_click_date !== today) {
    userData.last_ad_click_date = today;
    userData.ad_clicks_today = 0;
  }

  if (userData.dtech_points === undefined) userData.dtech_points = 0;

  let actualPointsAdded = 0;
  let actualAdsClickedAdded = 0;

  if (ads_clicked && added_points) {
    // Determine how many clicks we can actually add
    const clicksAllowed = Math.max(0, 30 - userData.ad_clicks_today);
    const validClicksToAdd = Math.min(ads_clicked, clicksAllowed);

    if (validClicksToAdd > 0) {
       // Estimate how much of the added points correspond to the valid clicks
       // To be safe, if they clicked more than allowed offline, we cap points
       // proportional to valid clicks. E.g., max 50 pts per click.
       const maxPointsPossible = validClicksToAdd * 50;
       const validPointsToAdd = Math.min(added_points, maxPointsPossible);

       userData.ad_clicks_today += validClicksToAdd;
       userData.dtech_points += validPointsToAdd;
       actualPointsAdded += validPointsToAdd;
       actualAdsClickedAdded += validClicksToAdd;
    }
  }

  if (push_claim) {
      if (userData.last_push_claim_date !== today) {
          userData.last_push_claim_date = today;
          userData.dtech_points += 100;
          actualPointsAdded += 100;
      }
  }

  await env.RANK_KV.put(`user:${user_id}`, JSON.stringify(userData));

  return jsonResponse({
    success: true,
    new_balance: userData.dtech_points,
    clicks_today: userData.ad_clicks_today,
    actual_points_added: actualPointsAdded
  });
}

const STORE_CATALOG = {
  // Fonts (Starts at 100)
  font_serif: { price: 100, type: 'font' },
  font_retro: { price: 200, type: 'font' },
  font_handwriting: { price: 300, type: 'font' },

  // Themes (Starts at 100)
  theme_gold: { price: 100, type: 'theme' },
  theme_dark: { price: 150, type: 'theme' },
  theme_diamond: { price: 250, type: 'theme' },
  theme_forest: { price: 300, type: 'theme' },
  theme_ocean: { price: 400, type: 'theme' },
  theme_neon: { price: 500, type: 'theme' },
  theme_sunset: { price: 600, type: 'theme' },

  // Avatar Borders (Starts at 500)
  border_gold: { price: 500, type: 'avatar_border' },
  border_diamond: { price: 1000, type: 'avatar_border' },
  border_fire: { price: 1500, type: 'avatar_border' },
  border_neon: { price: 2000, type: 'avatar_border' },
  border_cosmic: { price: 2500, type: 'avatar_border' },
  border_rainbow: { price: 3500, type: 'avatar_border' },
  border_glitch: { price: 5000, type: 'avatar_border' },

  // Name Colors (Starts at 800)
  name_red: { price: 800, type: 'name_color' },
  name_blue: { price: 800, type: 'name_color' },
  name_green: { price: 800, type: 'name_color' },
  name_gold: { price: 2000, type: 'name_color' },

  // Quiz Celebrations (Starts at 1000)
  effect_matrix: { price: 1000, type: 'quiz_celebration' },
  effect_emoji: { price: 1500, type: 'quiz_celebration' },
  effect_fireworks: { price: 2500, type: 'quiz_celebration' },

  // Certificate Templates (Starts at 1000)
  cert_dark: { price: 1000, type: 'certificate_template' },
  cert_gold: { price: 2000, type: 'certificate_template' },
  cert_cyber: { price: 3000, type: 'certificate_template' },

  // Profile Banners (Starts at 2000)
  banner_cyber: { price: 2000, type: 'profile_banner' },
  banner_space: { price: 2000, type: 'profile_banner' },
  banner_sunset: { price: 2000, type: 'profile_banner' },

  // Ultimate Bundles (Starts at 10000)
  ultimate_god: { price: 10000, type: 'ultimate_bundle' },
  ultimate_hacker: { price: 10000, type: 'ultimate_bundle' },
  ultimate_rpg: { price: 10000, type: 'ultimate_bundle' },
  ultimate_cyberpunk: { price: 10000, type: 'ultimate_bundle' }
};

async function handleStorePurchase(request, env) {
  const { user_id, item_id } = await request.json();
  if (!user_id || !item_id) return jsonResponse({ error: "Missing parameters" }, 400);

  if (!STORE_CATALOG[item_id]) {
    return jsonResponse({ error: "Invalid item" }, 400);
  }
  const price = STORE_CATALOG[item_id].price;

  const userDataString = await env.RANK_KV.get(`user:${user_id}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);
  if (userData.dtech_points === undefined) userData.dtech_points = 0;
  if (!userData.unlocked_cosmetics) userData.unlocked_cosmetics = [];

  // 1. Fetch pending commands from Firebase
  let pending_points = 0;
  let commandsToDelete = [];
  try {
    let authQuery = "";
    if (env.FIREBASE_WORKER_EMAIL && env.FIREBASE_WORKER_PASSWORD) {
        const token = await getFirebaseAuthToken(env);
        if (token) authQuery = `?auth=${token}`;
    } else if (env.FIREBASE_SECRET) {
        authQuery = `?auth=${env.FIREBASE_SECRET}`;
    }
    const fbResponse = await fetch(`${FIREBASE_DB_URL}/user_commands/${user_id}.json${authQuery}`);
    if (fbResponse.ok) {
      const commands = await fbResponse.json();
      if (commands) {
        for (const key in commands) {
          const cmd = commands[key];
          if (cmd && cmd.action === "points" && typeof cmd.points === "number") {
            pending_points += cmd.points;
            commandsToDelete.push(key);
          }
        }
      }
    }
  } catch (err) {
    console.error("Error fetching pending commands:", err);
  }

  // Mini-Sync: Apply pending points to Master KV balance
  userData.dtech_points += pending_points;

  // 2. Calculate Available Balance
  const available_balance = userData.dtech_points;

  if (available_balance < price) {
    return jsonResponse({ error: "Not enough D-TECH POINTS" }, 400);
  }

  if (userData.unlocked_cosmetics.includes(item_id)) {
    return jsonResponse({ error: "Item already unlocked" }, 400);
  }

  // 3. Proceed with purchase logic, deduct from master KV
  userData.dtech_points -= price;
  userData.unlocked_cosmetics.push(item_id);

  await env.RANK_KV.put(`user:${user_id}`, JSON.stringify(userData));

  // 4. Clear pending commands from Firebase since they are now synced
  try {
    let authQuery = "";
    if (env.FIREBASE_WORKER_EMAIL && env.FIREBASE_WORKER_PASSWORD) {
        const token = await getFirebaseAuthToken(env);
        if (token) authQuery = `?auth=${token}`;
    } else if (env.FIREBASE_SECRET) {
        authQuery = `?auth=${env.FIREBASE_SECRET}`;
    }
    for (const key of commandsToDelete) {
      await fetch(`${FIREBASE_DB_URL}/user_commands/${user_id}/${key}.json${authQuery}`, {
        method: 'DELETE'
      });
    }
  } catch (err) {
    console.error("Error deleting pending commands:", err);
  }

  return jsonResponse({
    success: true,
    new_balance: userData.dtech_points,
    available_balance: userData.dtech_points, // since it was just synced, available_balance is the same
    unlocked_cosmetics: userData.unlocked_cosmetics
  });
}

async function handleStoreEquip(request, env) {
  const { user_id, type, item_id } = await request.json();
  if (!user_id || !type || item_id === undefined) return jsonResponse({ error: "Missing parameters" }, 400);

  if (item_id !== null && !STORE_CATALOG[item_id]) {
    return jsonResponse({ error: "Invalid item" }, 400);
  }

  if (item_id !== null) {
    const catalogType = STORE_CATALOG[item_id].type;
    if (catalogType === 'ultimate_bundle') {
        if (type !== 'ultimate_profile' && type !== 'ultimate_global') {
            return jsonResponse({ error: "Type mismatch for ultimate bundle" }, 400);
        }
    } else if (catalogType !== type) {
        return jsonResponse({ error: "Type mismatch" }, 400);
    }
  }

  const userDataString = await env.RANK_KV.get(`user:${user_id}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);
  if (!userData.unlocked_cosmetics) userData.unlocked_cosmetics = [];
  if (!userData.equipped_cosmetics) userData.equipped_cosmetics = {};

  if (item_id !== null && !userData.unlocked_cosmetics.includes(item_id)) {
    return jsonResponse({ error: "Item not unlocked" }, 400);
  }

  if (item_id === null) {
    delete userData.equipped_cosmetics[type];
  } else {
    userData.equipped_cosmetics[type] = item_id;
    // For ultimate bundles, equipping one mode should clear the other
    if (type === 'ultimate_profile') {
        delete userData.equipped_cosmetics['ultimate_global'];
    } else if (type === 'ultimate_global') {
        delete userData.equipped_cosmetics['ultimate_profile'];
    }
  }

  await env.RANK_KV.put(`user:${user_id}`, JSON.stringify(userData));

  return jsonResponse({
    success: true,
    equipped_cosmetics: userData.equipped_cosmetics
  });
}
