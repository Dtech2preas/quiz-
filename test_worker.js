import worker from './worker.js';

// Mock Cloudflare Env and Context
const store = new Map();
const env = {
  RANK_KV: {
    get: async (key) => store.get(key) || null,
    put: async (key, value) => { store.set(key, value); },
    delete: async (key) => { store.delete(key); }
  }
};
const ctx = {
  waitUntil: (promise) => promise.catch(console.error)
};

// Helper for sending Requests to the worker
async function dispatchRequest(method, path, body = null) {
  const reqInit = { method };
  if (body) {
    reqInit.body = JSON.stringify(body);
    reqInit.headers = { "Content-Type": "application/json" };
  }
  const request = new Request(`http://localhost${path}`, reqInit);
  const response = await worker.fetch(request, env, ctx);
  let resBody = null;
  try {
    resBody = await response.json();
  } catch(e) {}
  return { status: response.status, body: resBody };
}

async function test() {
  console.log("--- Starting Tests ---");

  // 1. Signup user
  let res = await dispatchRequest("POST", "/api/signup", {
    username: "testuser", password: "Password123!", name: "John", surname: "Doe"
  });
  console.log("Signup:", res.status, res.body);
  const userId = res.body.user_id;

  // 2. Add some dummy data to mock a quiz completion
  const userStr = await env.RANK_KV.get(`user:${userId}`);
  const user = JSON.parse(userStr);
  user.total_xp = 1500;
  user.math_xp = 1000;
  user.physics_xp = 500;
  user.accuracy_percentage = 85;
  user.study_streak_days = 4;
  await env.RANK_KV.put(`user:${userId}`, JSON.stringify(user));

  // Create mock leaderboards
  await env.RANK_KV.put("leaderboard:overall", JSON.stringify([{ user_id: userId, xp: 1500 }]));
  await env.RANK_KV.put("leaderboard:math", JSON.stringify([{ user_id: userId, xp: 1000 }]));
  await env.RANK_KV.put("leaderboard:physics", JSON.stringify([{ user_id: userId, xp: 500 }]));

  // 3. Update Avatar
  const avatarUrl = "https://catbox.moe/test.png";
  res = await dispatchRequest("PUT", `/api/user/${userId}/avatar`, { avatar_url: avatarUrl });
  console.log("Update Avatar:", res.status, res.body);

  // 4. Update Profile
  res = await dispatchRequest("PUT", `/api/user/${userId}/profile`, {
    username: "newuser", name: "Jane", surname: "Smith"
  });
  console.log("Update Profile:", res.status, res.body);

  // 5. Verify old username is deleted
  const oldUsernameKey = await env.RANK_KV.get("user_by_name:testuser");
  console.log("Old username key exists:", oldUsernameKey !== null);

  // 6. Get Public Profile (using new username)
  res = await dispatchRequest("GET", "/api/public-user/newuser");
  console.log("Get Public Profile:", res.status, res.body);

  console.log("--- Tests Completed ---");
}

test();
