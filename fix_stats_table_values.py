with open('stats.html', 'r') as f:
    content = f.read()

# Fix the duplicate data-labels
content = content.replace('            /* Use data attributes for labels on mobile */\n            .table td::before {\n                content: attr(data-label);\n                font-weight: 600;\n                color: var(--text-muted);\n                margin-right: 1rem;\n            }', '')

content = content.replace("""            .stat-group .table:nth-of-type(1) th,
            .stat-group .table:nth-of-type(1) td,
            .stat-group:nth-of-type(2) .table th,
            .stat-group:nth-of-type(2) .table td {
                display: block;
                padding: 0.5rem;
                border: none;
                text-align: left;
            }""", """            .stat-group .table:nth-of-type(1) th,
            .stat-group .table:nth-of-type(1) td,
            .stat-group:nth-of-type(2) .table th,
            .stat-group:nth-of-type(2) .table td {
                display: block;
                padding: 0.5rem;
                border: none;
                text-align: left;
            }
            /* Reset the default mobile table styles for the grid-based tables */
            .stat-group .table:nth-of-type(1) td,
            .stat-group:nth-of-type(2) .table td {
                justify-content: flex-start;
            }""")

with open('stats.html', 'w') as f:
    f.write(content)
