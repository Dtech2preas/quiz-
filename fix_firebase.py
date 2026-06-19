import re

with open('firebase_config.js', 'r') as f:
    content = f.read()

# Add applyDeltasAndSort and fix getCombinedUserData
new_logic = """
window.applyDeltasAndSort = async function(baseDataArray, sortKey = 'xp') {
    if (!baseDataArray || !Array.isArray(baseDataArray)) return [];

    try {
        const fbResponse = await fetch(`${firebaseConfig.databaseURL}/user_commands.json`);
        if (!fbResponse.ok) return baseDataArray;
        const allCommands = await fbResponse.json();
        if (!allCommands) return baseDataArray;

        for (let i = 0; i < baseDataArray.length; i++) {
            const user = baseDataArray[i];
            if (allCommands[user.user_id]) {
                const userCmds = Object.values(allCommands[user.user_id]);
                let pendingXp = 0;
                for (const cmd of userCmds) {
                    if (cmd && cmd.action === 'quiz' && cmd.passed && cmd.publicXp) {
                         // Very basic mapping for general 'xp'
                         // For subject specific, the logic in worker.js is complex, but generally totalXp Earned
                         // Since we are sorting, we add it to the generic 'xp' property
                         pendingXp += cmd.publicXp;
                    } else if (cmd && cmd.action === 'weekly' && cmd.totalXp) {
                         pendingXp += cmd.totalXp;
                    }
                }
                user.xp = (user.xp || 0) + pendingXp;
            }
        }

        // Re-sort array
        baseDataArray.sort((a, b) => b.xp - a.xp);
        return baseDataArray;

    } catch(e) {
        console.error("Error applying deltas:", e);
        return baseDataArray;
    }
};

window.getCombinedUserData = async function(userId, queryParams = "", isPublic = false) {
    try {
        const endpoint = isPublic ? `/api/public-user/${userId}` : `/api/user/${userId}`;
        const response = await fetch(`${API_URL}${endpoint}${queryParams}`);
        if (!response.ok) return null;
        let userData = await response.json();

        // Fetch pending changes from Firebase and apply them
        try {
            const fbResponse = await fetch(`${firebaseConfig.databaseURL}/user_commands/${userId}.json`);
            if (fbResponse.ok) {
                const commands = await fbResponse.json();
                if (commands) {
                    let pendingTotalXp = 0;
                    let pendingPoints = 0;

                    const cmdsArray = Object.values(commands);
                    for (const cmd of cmdsArray) {
                        if (cmd.action === 'points' && cmd.points) {
                            pendingPoints += cmd.points;
                        } else if (cmd.action === 'quiz' && cmd.passed && cmd.publicXp) {
                            pendingTotalXp += cmd.publicXp;
                        } else if (cmd.action === 'weekly' && cmd.totalXp) {
                            pendingTotalXp += cmd.totalXp;
                        }
                    }

                    userData.total_xp = (userData.total_xp || 0) + pendingTotalXp;
                    userData.dtech_points = (userData.dtech_points || 0) + pendingPoints;

                    // The backend sends available_balance which it calculates itself
                    // No need to override it here if the backend already included it
                }
            }
        } catch(fbErr) {
             console.error("Error fetching pending commands:", fbErr);
        }

        return userData;
    } catch (e) {
        console.error("Error fetching user data:", e);
        return null;
    }
};
"""

content = re.sub(r'window\.getCombinedUserData = async function.*$', new_logic, content, flags=re.DOTALL | re.MULTILINE)

with open('firebase_config.js', 'w') as f:
    f.write(content)
