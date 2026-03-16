const { createServer } = require('http');
const fs = require('fs');
const path = require('path');

async function importWorker() {
    return await import('./worker.js');
}

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

// Populate store
const userId = '69939f08-ae17-4e4a-9ad3-82498c948e6c';
store.set(`user:${userId}`, JSON.stringify({
    user_id: userId,
    username: 'testuser',
    name: 'John',
    surname: 'Doe',
    avatar_url: 'https://catbox.moe/test.png',
    total_xp: 1500,
    math_xp: 1000,
    physics_xp: 500,
    accuracy_percentage: 85,
    study_streak_days: 4,
    ranks: { overall: 1, math: 1, physics: 1 }
}));
store.set(`user_by_name:testuser`, userId);
store.set("leaderboard:overall", JSON.stringify([{ user_id: userId, username: 'testuser', name: 'John', surname: 'Doe', xp: 1500, avatar_url: 'https://catbox.moe/test.png' }]));

importWorker().then(worker => {
    const server = createServer(async (req, res) => {
        // Handle CORS
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

        if (req.method === 'OPTIONS') {
            res.writeHead(200);
            res.end();
            return;
        }

        const url = new URL(req.url, `http://${req.headers.host}`);
        let body = [];
        req.on('data', chunk => body.push(chunk));
        req.on('end', async () => {
            const bodyStr = Buffer.concat(body).toString();

            const reqInit = {
                method: req.method,
                headers: req.headers
            };
            if (req.method !== 'GET' && req.method !== 'HEAD' && bodyStr) {
                reqInit.body = bodyStr;
            }

            const request = new Request(url, reqInit);
            const response = await worker.default.fetch(request, env, ctx);

            res.writeHead(response.status, { 'Content-Type': 'application/json' });
            res.end(await response.text());
        });
    });

    server.listen(8787, () => {
        console.log('Mock Worker running on port 8787');
    });
});
