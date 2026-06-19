import re

files_to_fix = ['leaderboard.html', 'global_leaderboard.html']

for file in files_to_fix:
    with open(file, 'r') as f:
        content = f.read()

    # Look for fetchLeaderboards or setup logic to inject applyDeltasAndSort

    # In leaderboard.html
    if 'leaderboard.html' in file:
        content = content.replace(
            'const response = await fetch(`${API_URL}/api/leaderboard?grade=${currentGrade}${queryParams}`);\n            const data = await response.json();',
            'const response = await fetch(`${API_URL}/api/leaderboard?grade=${currentGrade}${queryParams}`);\n            const data = await response.json();\n            \n            if (window.applyDeltasAndSort) {\n                for (const key of Object.keys(data)) {\n                    if (Array.isArray(data[key])) {\n                        data[key] = await window.applyDeltasAndSort(data[key]);\n                    }\n                }\n            }'
        )

    # In global_leaderboard.html
    if 'global_leaderboard.html' in file:
        content = content.replace(
            '.then(data => ({ gradeId, title: `Grade ${i}`, data, subjects: gradeSubjects }))',
            '.then(async data => {\n                            if (window.applyDeltasAndSort) {\n                                for (const key of Object.keys(data)) {\n                                    if (Array.isArray(data[key])) {\n                                        data[key] = await window.applyDeltasAndSort(data[key]);\n                                    }\n                                }\n                            }\n                            return { gradeId, title: `Grade ${i}`, data, subjects: gradeSubjects };\n                        })'
        )
        content = content.replace(
            '.then(data => ({ gradeId: \'all\', title: \'All Grades\', data }))',
            '.then(async data => {\n                        if (window.applyDeltasAndSort) {\n                            for (const key of Object.keys(data)) {\n                                if (Array.isArray(data[key])) {\n                                    data[key] = await window.applyDeltasAndSort(data[key]);\n                                }\n                            }\n                        }\n                        return { gradeId: \'all\', title: \'All Grades\', data };\n                    })'
        )

    with open(file, 'w') as f:
        f.write(content)
