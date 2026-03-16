const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default {
  async fetch(request, env, ctx) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
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
      if (request.method === "GET" && path === "/api/leaderboard") {
        return await handleGetLeaderboards(request, env);
      }

      return jsonResponse({ error: "Not Found" }, 404);
    } catch (err) {
      return jsonResponse({ error: "Internal Server Error", message: err.message }, 500);
    }
  },
};

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...CORS_HEADERS,
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
  const { username, password, name, surname } = body;

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
    avatar_url: "",
    math_xp: 0,
    physics_xp: 0,
    total_xp: 0,
    weekly_xp: 0,
    questions_answered: 0,
    correct_answers: 0,
    accuracy_percentage: 0,
    study_streak_days: 0,
    quizzes_completed: 0,
    last_quiz_date: null,
    topic_accuracy: {}
  };

  await env.RANK_KV.put(`user:${userId}`, JSON.stringify(newUser));
  await env.RANK_KV.put(`user_by_name:${username}`, userId); // Map username to user_id

  return jsonResponse({ message: "Signup successful", user_id: userId });
}

async function handleLogin(request, env) {
  const body = await request.json();
  const { username, password } = body;

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

  return jsonResponse({ message: "Login successful", user_id: userId });
}

async function handleGetUser(request, env, path) {
  const userId = path.split("/").pop();
  if (!userId) return jsonResponse({ error: "User ID required" }, 400);

  const userDataString = await env.RANK_KV.get(`user:${userId}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);

  // Exclude password hash from response
  delete userData.password_hash;

  // Calculate ranks
  const mathLeaderboardStr = await env.RANK_KV.get("leaderboard:math") || "[]";
  const physicsLeaderboardStr = await env.RANK_KV.get("leaderboard:physics") || "[]";
  const overallLeaderboardStr = await env.RANK_KV.get("leaderboard:overall") || "[]";

  const mathLeaderboard = JSON.parse(mathLeaderboardStr);
  const physicsLeaderboard = JSON.parse(physicsLeaderboardStr);
  const overallLeaderboard = JSON.parse(overallLeaderboardStr);

  const findRank = (board) => {
    const index = board.findIndex(u => u.user_id === userId);
    return index !== -1 ? index + 1 : "-";
  };

  userData.ranks = {
    overall: findRank(overallLeaderboard),
    math: findRank(mathLeaderboard),
    physics: findRank(physicsLeaderboard)
  };

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
  const { name, surname, username, password } = body;

  const userDataString = await env.RANK_KV.get(`user:${userId}`);
  if (!userDataString) return jsonResponse({ error: "User not found" }, 404);

  const userData = JSON.parse(userDataString);

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
  const keys = ["leaderboard:overall", "leaderboard:math", "leaderboard:physics", `leaderboard:weekly:${currentWeek}`];

  for (const key of keys) {
    let boardStr = await env.RANK_KV.get(key) || "[]";
    let board = JSON.parse(boardStr);

    let updated = false;
    for (let i = 0; i < board.length; i++) {
      if (board[i].user_id === userId) {
        board[i].username = userData.username;
        board[i].name = userData.name;
        board[i].surname = userData.surname;
        board[i].avatar_url = userData.avatar_url;
        updated = true;
        break;
      }
    }

    if (updated) {
      await env.RANK_KV.put(key, JSON.stringify(board));
    }
  }
}

async function handleGetPublicUser(request, env, path) {
  const username = path.split("/").pop();
  if (!username) return jsonResponse({ error: "Username required" }, 400);

  const userId = await env.RANK_KV.get(`user_by_name:${username}`);
  if (!userId) return jsonResponse({ error: "User not found" }, 404);

  const userDataString = await env.RANK_KV.get(`user:${userId}`);
  if (!userDataString) return jsonResponse({ error: "User data not found" }, 500);

  const userData = JSON.parse(userDataString);

  // Exclude sensitive info
  const publicData = {
    username: userData.username,
    name: userData.name,
    surname: userData.surname,
    avatar_url: userData.avatar_url || "",
    total_xp: userData.total_xp,
    questions_answered: userData.questions_answered,
    accuracy_percentage: userData.accuracy_percentage,
    study_streak_days: userData.study_streak_days
  };

  // Calculate ranks
  const mathLeaderboardStr = await env.RANK_KV.get("leaderboard:math") || "[]";
  const physicsLeaderboardStr = await env.RANK_KV.get("leaderboard:physics") || "[]";
  const overallLeaderboardStr = await env.RANK_KV.get("leaderboard:overall") || "[]";

  const mathLeaderboard = JSON.parse(mathLeaderboardStr);
  const physicsLeaderboard = JSON.parse(physicsLeaderboardStr);
  const overallLeaderboard = JSON.parse(overallLeaderboardStr);

  const findRank = (board) => {
    const index = board.findIndex(u => u.user_id === userId);
    return index !== -1 ? index + 1 : "-";
  };

  publicData.ranks = {
    overall: findRank(overallLeaderboard),
    math: findRank(mathLeaderboard),
    physics: findRank(physicsLeaderboard)
  };

  return jsonResponse(publicData);
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

  // Calculate XP
  const xpEarned = (correct_answers * 10) + 50; // +10 per correct, +50 completion

  // Check daily cap (basic implementation based on date string)
  const today = new Date().toISOString().split('T')[0];
  if (userData.last_quiz_date !== today) {
    userData.daily_xp = 0;
    userData.last_quiz_date = today;

    // Manage streak
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

  let actualXpEarned = xpEarned;
  if ((userData.daily_xp || 0) + xpEarned > 500) {
    actualXpEarned = Math.max(0, 500 - (userData.daily_xp || 0));
  }
  userData.daily_xp = (userData.daily_xp || 0) + actualXpEarned;

  if (subject === "mathematics") {
    userData.math_xp += actualXpEarned;
  } else if (subject === "physics") {
    userData.physics_xp += actualXpEarned;
  }
  userData.total_xp += actualXpEarned;

  // Update weekly XP (reset if new week)
  const currentWeek = getCurrentWeek();
  if (userData.last_week !== currentWeek) {
    userData.weekly_xp = 0;
    userData.last_week = currentWeek;
  }
  userData.weekly_xp += actualXpEarned;

  userData.questions_answered += total_questions;
  userData.correct_answers += correct_answers;
  userData.accuracy_percentage = Math.round((userData.correct_answers / userData.questions_answered) * 100);
  userData.quizzes_completed += 1;

  // Topic accuracy
  if (!userData.topic_accuracy[topic]) {
    userData.topic_accuracy[topic] = { correct: 0, total: 0 };
  }
  userData.topic_accuracy[topic].correct += correct_answers;
  userData.topic_accuracy[topic].total += total_questions;

  await env.RANK_KV.put(`user:${user_id}`, JSON.stringify(userData));

  // Update leaderboards async
  ctx.waitUntil(updateLeaderboards(env, userData, currentWeek));

  return jsonResponse({ message: "Quiz submitted successfully", xp_earned: actualXpEarned });
}

async function updateLeaderboards(env, user, currentWeek) {
  const updateBoard = async (key, sortByField) => {
    let boardStr = await env.RANK_KV.get(key) || "[]";
    let board = JSON.parse(boardStr);

    // Remove existing entry
    board = board.filter(u => u.user_id !== user.user_id);

    // Add new entry
    board.push({
      user_id: user.user_id,
      username: user.username,
      name: user.name,
      surname: user.surname,
      avatar_url: user.avatar_url,
      xp: user[sortByField]
    });

    // Sort and keep top (e.g., top 1000)
    board.sort((a, b) => b.xp - a.xp);
    if (board.length > 1000) board = board.slice(0, 1000);

    await env.RANK_KV.put(key, JSON.stringify(board));
  };

  await Promise.all([
    updateBoard("leaderboard:overall", "total_xp"),
    updateBoard("leaderboard:math", "math_xp"),
    updateBoard("leaderboard:physics", "physics_xp"),
    updateBoard(`leaderboard:weekly:${currentWeek}`, "weekly_xp")
  ]);
}

async function handleGetLeaderboards(request, env) {
  const mathStr = await env.RANK_KV.get("leaderboard:math") || "[]";
  const physicsStr = await env.RANK_KV.get("leaderboard:physics") || "[]";
  const overallStr = await env.RANK_KV.get("leaderboard:overall") || "[]";

  const currentWeek = getCurrentWeek();
  const weeklyStr = await env.RANK_KV.get(`leaderboard:weekly:${currentWeek}`) || "[]";

  return jsonResponse({
    overall: JSON.parse(overallStr),
    math: JSON.parse(mathStr),
    physics: JSON.parse(physicsStr),
    weekly: JSON.parse(weeklyStr)
  });
}
