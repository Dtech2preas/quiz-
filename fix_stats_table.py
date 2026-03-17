with open('stats.html', 'r') as f:
    content = f.read()

css_replacement = """            /* Two column grid for General Information table */
            .stat-group .table:first-of-type tr, .stat-group .table:nth-of-type(2) tr {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.5rem;
                padding: 1rem;
            }
            .stat-group .table:first-of-type th,
            .stat-group .table:first-of-type td,
            .stat-group .table:nth-of-type(2) th,
            .stat-group .table:nth-of-type(2) td {
                display: block;
                padding: 0.5rem;
                border: none;
                text-align: left;
            }
            .stat-group .table:first-of-type th,
            .stat-group .table:nth-of-type(2) th {
                background: transparent;
                color: var(--text-muted);
                font-size: 0.9rem;
            }
            .stat-group .table:first-of-type td,
            .stat-group .table:nth-of-type(2) td {
                font-weight: 600;
                color: var(--text-main);
                font-size: 1.1rem;
            }

            /* Topic table specific grid */
            .stat-group .table:nth-of-type(3) tr {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.5rem;
                padding: 1rem;
            }
            .stat-group .table:nth-of-type(3) td {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                border: none;
                padding: 0.5rem;
            }
            .stat-group .table:nth-of-type(3) td::before {
                margin-right: 0;
                margin-bottom: 0.2rem;
            }"""

content = content.replace("""            /* Two column grid for General Information table */
            .stat-group .table:first-of-type tr {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.5rem;
                padding: 1rem;
            }
            .stat-group .table:first-of-type th,
            .stat-group .table:first-of-type td {
                display: block;
                padding: 0.5rem;
                border: none;
                text-align: left;
            }
            .stat-group .table:first-of-type th {
                background: transparent;
                color: var(--text-muted);
                font-size: 0.9rem;
            }
            .stat-group .table:first-of-type td {
                font-weight: 600;
                color: var(--text-main);
                font-size: 1.1rem;
            }
            .stat-group .table:first-of-type tr:hover td {
                background-color: transparent;
            }""", css_replacement)

with open('stats.html', 'w') as f:
    f.write(content)
