with open('stats.html', 'r') as f:
    content = f.read()

# Make sure we add the data-labels back to the other tables
content = content.replace('            /* Reset the default mobile table styles for the grid-based tables */\n            .stat-group .table:nth-of-type(1) td,\n            .stat-group:nth-of-type(2) .table td {\n                justify-content: flex-start;\n            }', '            /* Use data attributes for labels on mobile */\n            .table td::before {\n                content: attr(data-label);\n                font-weight: 600;\n                color: var(--text-muted);\n                margin-right: 1rem;\n                display: block;\n            }\n            /* Reset the default mobile table styles for the grid-based tables */\n            .stat-group .table:nth-of-type(1) td,\n            .stat-group:nth-of-type(2) .table td {\n                justify-content: flex-start;\n            }\n            .stat-group .table:nth-of-type(1) td::before,\n            .stat-group:nth-of-type(2) .table td::before {\n                display: none;\n            }')

with open('stats.html', 'w') as f:
    f.write(content)
