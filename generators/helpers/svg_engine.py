import math

class SVGEngine:
    """
    SVGEngine dynamically generates inline SVG strings based on curriculum metadata.
    It supports generating diagrams for Mathematics, Sciences, and more.
    """

    @staticmethod
    def generate_svg(svg_type: str, params: dict = None) -> str:
        if params is None:
            params = {}

        svg_type = svg_type.lower()
        if svg_type == 'geometry_shape':
            return SVGEngine._generate_geometry_shape(params)
        elif svg_type == 'coordinate_grid':
            return SVGEngine._generate_coordinate_grid(params)
        elif svg_type == 'electric_circuit':
            return SVGEngine._generate_electric_circuit(params)
        elif svg_type == 'dna_structure':
            return SVGEngine._generate_dna_structure(params)
        elif svg_type == 'pedigree_tree':
            return SVGEngine._generate_pedigree_tree(params)
        else:
            return ""

    @staticmethod
    def _generate_geometry_shape(params: dict) -> str:
        shape = params.get('shape', 'rectangle')
        color = params.get('color', '#333333')
        labels = params.get('labels', {})

        svg_content = f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" width="100%" height="200px" style="max-width: 300px; margin: auto; display: block;">\n'

        if shape == 'rectangle':
            svg_content += f'  <rect x="40" y="50" width="120" height="80" fill="none" stroke="{color}" stroke-width="3"/>\n'
            if 'top' in labels:
                svg_content += f'  <text x="100" y="40" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["top"]}</text>\n'
            if 'right' in labels:
                svg_content += f'  <text x="170" y="95" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["right"]}</text>\n'
            if 'bottom' in labels:
                svg_content += f'  <text x="100" y="150" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["bottom"]}</text>\n'
            if 'left' in labels:
                svg_content += f'  <text x="25" y="95" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["left"]}</text>\n'

        elif shape == 'triangle':
            svg_content += f'  <polygon points="100,40 160,140 40,140" fill="none" stroke="{color}" stroke-width="3"/>\n'
            if 'base' in labels:
                svg_content += f'  <text x="100" y="160" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["base"]}</text>\n'
            if 'left' in labels:
                svg_content += f'  <text x="50" y="90" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["left"]}</text>\n'
            if 'right' in labels:
                svg_content += f'  <text x="150" y="90" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["right"]}</text>\n'

        elif shape == 'circle':
            svg_content += f'  <circle cx="100" cy="100" r="60" fill="none" stroke="{color}" stroke-width="3"/>\n'
            svg_content += f'  <line x1="100" y1="100" x2="160" y2="100" stroke="{color}" stroke-width="2" stroke-dasharray="4"/>\n'
            svg_content += f'  <circle cx="100" cy="100" r="3" fill="{color}"/>\n'
            if 'radius' in labels:
                svg_content += f'  <text x="130" y="95" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["radius"]}</text>\n'

        elif shape == 'intersecting_lines':
            svg_content += f'  <line x1="20" y1="20" x2="180" y2="180" stroke="{color}" stroke-width="3"/>\n'
            svg_content += f'  <line x1="20" y1="180" x2="180" y2="20" stroke="{color}" stroke-width="3"/>\n'

            # Additional parallel lines if needed
            if params.get('parallel', False):
                svg_content += f'  <line x1="50" y1="20" x2="210" y2="180" stroke="{color}" stroke-width="3"/>\n'

            if 'top' in labels:
                svg_content += f'  <text x="100" y="40" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["top"]}</text>\n'
            if 'bottom' in labels:
                svg_content += f'  <text x="100" y="170" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["bottom"]}</text>\n'
            if 'left' in labels:
                svg_content += f'  <text x="50" y="105" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["left"]}</text>\n'
            if 'right' in labels:
                svg_content += f'  <text x="150" y="105" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["right"]}</text>\n'

        elif shape == 'function_graph':
            # Basic Cartesian plane with a function curve
            # Draw axes
            svg_content += f'  <line x1="100" y1="10" x2="100" y2="190" stroke="#999" stroke-width="1"/>\n'
            svg_content += f'  <line x1="10" y1="100" x2="190" y2="100" stroke="#999" stroke-width="1"/>\n'

            # Arrows for axes
            svg_content += f'  <polygon points="100,5 95,15 105,15" fill="#999"/>\n'
            svg_content += f'  <polygon points="195,100 185,95 185,105" fill="#999"/>\n'

            # Axes labels
            svg_content += f'  <text x="190" y="115" font-family="sans-serif" font-size="10" fill="#666">x</text>\n'
            svg_content += f'  <text x="110" y="15" font-family="sans-serif" font-size="10" fill="#666">y</text>\n'

            func_type = params.get('func_type', 'parabola')

            if func_type == 'parabola':
                # y = a(x-h)^2 + k
                a = params.get('a', 1)
                h = params.get('h', 0)
                k = params.get('k', 0)

                pts = []
                for px in range(-80, 81, 5):
                    x_val = px / 20.0 # scale
                    y_val = a * (x_val - h)**2 + k
                    py = -y_val * 20.0 # scale and invert y

                    if -90 <= py <= 90:
                        pts.append(f"{100 + px},{100 + py}")

                if pts:
                    svg_content += f'  <polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>\n'

            elif func_type == 'cubic':
                # y = a(x-r1)(x-r2)(x-r3)
                a = params.get('a', 1)
                r1 = params.get('r1', -2)
                r2 = params.get('r2', 0)
                r3 = params.get('r3', 2)

                pts = []
                for px in range(-90, 91, 5):
                    x_val = px / 20.0
                    y_val = a * (x_val - r1) * (x_val - r2) * (x_val - r3)
                    py = -y_val * 5.0 # smaller y scale for cubic

                    if -90 <= py <= 90:
                        pts.append(f"{100 + px},{100 + py}")

                if pts:
                    svg_content += f'  <polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>\n'

            elif func_type == 'hyperbola':
                # y = a/(x-p) + q
                a = params.get('a', 1)
                p = params.get('p', 0)
                q = params.get('q', 0)

                # Asymptotes
                asymp_x = 100 + p * 20
                asymp_y = 100 - q * 20
                svg_content += f'  <line x1="{asymp_x}" y1="10" x2="{asymp_x}" y2="190" stroke="#ccc" stroke-dasharray="4" stroke-width="1"/>\n'
                svg_content += f'  <line x1="10" y1="{asymp_y}" x2="190" y2="{asymp_y}" stroke="#ccc" stroke-dasharray="4" stroke-width="1"/>\n'

                # Draw two branches
                for branch in [1, -1]:
                    pts = []
                    for px in range(1, 90, 2):
                        dx = px * branch / 20.0
                        if dx == 0: continue
                        y_val = a / dx + q
                        py = -y_val * 20.0
                        if -90 <= py <= 90:
                            pts.append(f"{asymp_x + dx*20},{100 + py}")
                    if pts:
                        svg_content += f'  <polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>\n'

            elif func_type == 'exponential':
                # y = a * b^(x-p) + q
                a = params.get('a', 1)
                b = params.get('b', 2)
                p = params.get('p', 0)
                q_val = params.get('q', 0)

                # Asymptote
                asymp_y = 100 - q_val * 20
                svg_content += f'  <line x1="10" y1="{asymp_y}" x2="190" y2="{asymp_y}" stroke="#ccc" stroke-dasharray="4" stroke-width="1"/>\n'

                pts = []
                for px in range(-90, 91, 5):
                    x_val = px / 20.0
                    try:
                        y_val = a * (b**(x_val - p)) + q_val
                        py = -y_val * 20.0
                        if -90 <= py <= 90:
                            pts.append(f"{100 + px},{100 + py}")
                    except:
                        pass
                if pts:
                    svg_content += f'  <polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>\n'

            # Add general labels for functions
            if labels:
                for lbl_key, lbl_val in labels.items():
                    if lbl_key == 'tp':
                        px = 100 + params.get('tp_x', 0) * 20
                        py = 100 - params.get('tp_y', 0) * 20
                        svg_content += f'  <circle cx="{px}" cy="{py}" r="3" fill="{color}"/>\n'
                        svg_content += f'  <text x="{px+5}" y="{py-5}" font-family="sans-serif" font-size="10" fill="{color}">{lbl_val}</text>\n'
                    elif lbl_key == 'y_int':
                        py = 100 - params.get('y_int_y', 0) * 20
                        svg_content += f'  <circle cx="100" cy="{py}" r="3" fill="{color}"/>\n'
                        svg_content += f'  <text x="105" y="{py-5}" font-family="sans-serif" font-size="10" fill="{color}">{lbl_val}</text>\n'

        elif shape == 'scatter_plot':
            # Basic axes
            svg_content += f'  <line x1="20" y1="10" x2="20" y2="180" stroke="#999" stroke-width="2"/>\n'
            svg_content += f'  <line x1="20" y1="180" x2="190" y2="180" stroke="#999" stroke-width="2"/>\n'

            # Points
            pts = params.get('points', [])
            x_min = min((p['x'] for p in pts), default=0)
            x_max = max((p['x'] for p in pts), default=10)
            y_min = min((p['y'] for p in pts), default=0)
            y_max = max((p['y'] for p in pts), default=10)

            if x_max == x_min: x_max += 1
            if y_max == y_min: y_max += 1

            for p in pts:
                cx = 20 + ((p['x'] - x_min) / (x_max - x_min)) * 160
                cy = 180 - ((p['y'] - y_min) / (y_max - y_min)) * 160
                svg_content += f'  <circle cx="{cx}" cy="{cy}" r="3" fill="#1976d2"/>\n'

            if params.get('regression_line', False):
                # Regression line using y = mx + c
                m = params.get('m', 1)
                c = params.get('c', 0)

                # Plot points for line
                y1 = m * x_min + c
                y2 = m * x_max + c

                cx1 = 20
                cy1 = 180 - ((y1 - y_min) / (y_max - y_min)) * 160

                cx2 = 180
                cy2 = 180 - ((y2 - y_min) / (y_max - y_min)) * 160

                # Clip if needed, but for visualization simple line is fine
                svg_content += f'  <line x1="{cx1}" y1="{cy1}" x2="{cx2}" y2="{cy2}" stroke="#d32f2f" stroke-width="2" stroke-dasharray="4"/>\n'

            if labels:
                if 'x_axis' in labels:
                    svg_content += f'  <text x="100" y="195" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">{labels["x_axis"]}</text>\n'
                if 'y_axis' in labels:
                    svg_content += f'  <text x="5" y="90" font-family="sans-serif" font-size="10" text-anchor="middle" transform="rotate(-90 5,90)" fill="#666">{labels["y_axis"]}</text>\n'

        elif shape == 'box_whisker':
            q_min = params.get('min', 10)
            q1 = params.get('q1', 20)
            q2_raw = params.get('q2', 30)
            q3 = params.get('q3', 40)
            q_max = params.get('max', 50)

            span = q_max - q_min
            if span == 0: span = 1

            def scale_x(val):
                return 20 + ((val - q_min) / span) * 160

            x_min_p = scale_x(q_min)
            x1_p = scale_x(q1)
            # handle cases where q2 is a string like '?'
            q2_val = q2_raw if isinstance(q2_raw, (int, float)) else (q1 + q3) / 2
            x2_p = scale_x(q2_val)
            x3_p = scale_x(q3)
            x_max_p = scale_x(q_max)
            q2_display = q2_raw

            # Number line
            svg_content += f'  <line x1="10" y1="140" x2="190" y2="140" stroke="#999" stroke-width="2"/>\n'

            # Whiskers
            svg_content += f'  <line x1="{x_min_p}" y1="100" x2="{x1_p}" y2="100" stroke="{color}" stroke-width="2"/>\n'
            svg_content += f'  <line x1="{x3_p}" y1="100" x2="{x_max_p}" y2="100" stroke="{color}" stroke-width="2"/>\n'

            # Ends
            svg_content += f'  <line x1="{x_min_p}" y1="90" x2="{x_min_p}" y2="110" stroke="{color}" stroke-width="2"/>\n'
            svg_content += f'  <line x1="{x_max_p}" y1="90" x2="{x_max_p}" y2="110" stroke="{color}" stroke-width="2"/>\n'

            # Box
            svg_content += f'  <rect x="{x1_p}" y="80" width="{x3_p - x1_p}" height="40" fill="none" stroke="{color}" stroke-width="2"/>\n'

            # Median
            svg_content += f'  <line x1="{x2_p}" y1="80" x2="{x2_p}" y2="120" stroke="{color}" stroke-width="2"/>\n'

            # Labels
            svg_content += f'  <text x="{x_min_p}" y="155" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">{q_min}</text>\n'
            svg_content += f'  <text x="{x1_p}" y="155" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">{q1}</text>\n'
            svg_content += f'  <text x="{x2_p}" y="155" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">{q2_display}</text>\n'
            svg_content += f'  <text x="{x3_p}" y="155" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">{q3}</text>\n'
            svg_content += f'  <text x="{x_max_p}" y="155" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">{q_max}</text>\n'

        elif shape == 'tree_diagram':
            # Basic 2-stage tree
            svg_content += f'  <circle cx="20" cy="100" r="4" fill="{color}"/>\n'

            # Stage 1
            svg_content += f'  <line x1="20" y1="100" x2="80" y2="50" stroke="{color}" stroke-width="2"/>\n'
            svg_content += f'  <line x1="20" y1="100" x2="80" y2="150" stroke="{color}" stroke-width="2"/>\n'

            # Stage 2 top branch
            svg_content += f'  <line x1="80" y1="50" x2="160" y2="25" stroke="{color}" stroke-width="2"/>\n'
            svg_content += f'  <line x1="80" y1="50" x2="160" y2="75" stroke="{color}" stroke-width="2"/>\n'

            # Stage 2 bottom branch
            svg_content += f'  <line x1="80" y1="150" x2="160" y2="125" stroke="{color}" stroke-width="2"/>\n'
            svg_content += f'  <line x1="80" y1="150" x2="160" y2="175" stroke="{color}" stroke-width="2"/>\n'

            if labels:
                svg_content += f'  <text x="50" y="65" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#333">{labels.get("p1", "")}</text>\n'
                svg_content += f'  <text x="50" y="145" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#333">{labels.get("p2", "")}</text>\n'

                svg_content += f'  <text x="90" y="45" font-family="sans-serif" font-size="12" font-weight="bold" fill="#333">{labels.get("o1", "")}</text>\n'
                svg_content += f'  <text x="90" y="145" font-family="sans-serif" font-size="12" font-weight="bold" fill="#333">{labels.get("o2", "")}</text>\n'

        elif shape == 'venn_diagram':
            svg_content += f'  <rect x="10" y="10" width="180" height="180" fill="none" stroke="{color}" stroke-width="2"/>\n'

            # Two sets
            svg_content += f'  <circle cx="75" cy="100" r="50" fill="rgba(25, 118, 210, 0.2)" stroke="#1976d2" stroke-width="2"/>\n'
            svg_content += f'  <circle cx="125" cy="100" r="50" fill="rgba(211, 47, 47, 0.2)" stroke="#d32f2f" stroke-width="2"/>\n'

            if labels:
                svg_content += f'  <text x="45" y="105" font-family="sans-serif" font-size="12" text-anchor="middle" fill="#333">{labels.get("A", "")}</text>\n'
                svg_content += f'  <text x="155" y="105" font-family="sans-serif" font-size="12" text-anchor="middle" fill="#333">{labels.get("B", "")}</text>\n'
                svg_content += f'  <text x="100" y="105" font-family="sans-serif" font-size="12" text-anchor="middle" fill="#333">{labels.get("intersect", "")}</text>\n'
                svg_content += f'  <text x="25" y="175" font-family="sans-serif" font-size="12" text-anchor="middle" fill="#333">{labels.get("outer", "")}</text>\n'

        elif shape == 'pattern_diagram':
            pattern_type = params.get('pattern_type', 'dots')
            terms = params.get('terms', 3)

            svg_content += f'  <g transform="translate(10, 100)">\n'

            for i in range(1, terms + 1):
                offset_x = (i - 1) * 60
                svg_content += f'    <text x="{offset_x + 15}" y="40" font-family="sans-serif" font-size="12" text-anchor="middle" fill="#666">T{i}</text>\n'

                if pattern_type == 'dots':
                    # Triangle numbers
                    dots = i * (i + 1) // 2
                    col = 0
                    row = 0
                    for d in range(dots):
                        cx = offset_x + col * 8
                        cy = -row * 8
                        svg_content += f'      <circle cx="{cx}" cy="{cy}" r="3" fill="{color}"/>\n'
                        col += 1
                        if col > row:
                            row += 1
                            col = 0
                elif pattern_type == 'blocks':
                    # Squares
                    blocks = i * i
                    for r in range(i):
                        for c in range(i):
                            x = offset_x + c * 10
                            y = -r * 10
                            svg_content += f'      <rect x="{x}" y="{y}" width="9" height="9" fill="{color}" stroke="none"/>\n'

            svg_content += f'  </g>\n'

        elif shape == 'timeline':
            events = params.get('events', [])

            # Draw line
            svg_content += f'  <line x1="20" y1="100" x2="180" y2="100" stroke="#333" stroke-width="2"/>\n'

            for ev in events:
                x = 20 + ev.get('t', 0) * 160
                lbl = ev.get('label', '')
                val = ev.get('val', '')

                svg_content += f'  <line x1="{x}" y1="95" x2="{x}" y2="105" stroke="#333" stroke-width="2"/>\n'
                if lbl:
                    svg_content += f'  <text x="{x}" y="90" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">{lbl}</text>\n'
                if val:
                    svg_content += f'  <text x="{x}" y="120" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#333">{val}</text>\n'

        elif shape == 'number_line':
            roots = params.get('roots', [])

            # Draw line
            svg_content += f'  <line x1="20" y1="100" x2="180" y2="100" stroke="#333" stroke-width="2"/>\n'
            svg_content += f'  <polygon points="180,95 190,100 180,105" fill="#333"/>\n'
            svg_content += f'  <polygon points="20,95 10,100 20,105" fill="#333"/>\n'

            if roots:
                # scale
                r_min = min(roots)
                r_max = max(roots)
                span = r_max - r_min
                if span == 0: span = 1

                for r in roots:
                    x = 40 + ((r - r_min) / span) * 120
                    svg_content += f'  <line x1="{x}" y1="95" x2="{x}" y2="105" stroke="#333" stroke-width="2"/>\n'
                    svg_content += f'  <text x="{x}" y="120" font-family="sans-serif" font-size="12" text-anchor="middle" fill="#333">{r}</text>\n'

                    # Highlight region
                    region = params.get('region', '')
                    if region == 'between':
                        x1 = 40 + ((min(roots) - r_min) / span) * 120
                        x2 = 40 + ((max(roots) - r_min) / span) * 120
                        svg_content += f'  <line x1="{x1}" y1="100" x2="{x2}" y2="100" stroke="#d32f2f" stroke-width="4"/>\n'
                        svg_content += f'  <circle cx="{x1}" cy="100" r="4" fill="#d32f2f"/>\n'
                        svg_content += f'  <circle cx="{x2}" cy="100" r="4" fill="#d32f2f"/>\n'
                    elif region == 'outside':
                        x1 = 40 + ((min(roots) - r_min) / span) * 120
                        x2 = 40 + ((max(roots) - r_min) / span) * 120
                        svg_content += f'  <line x1="{x1}" y1="100" x2="20" y2="100" stroke="#d32f2f" stroke-width="4"/>\n'
                        svg_content += f'  <line x1="{x2}" y1="100" x2="180" y2="100" stroke="#d32f2f" stroke-width="4"/>\n'
                        svg_content += f'  <circle cx="{x1}" cy="100" r="4" fill="#d32f2f"/>\n'
                        svg_content += f'  <circle cx="{x2}" cy="100" r="4" fill="#d32f2f"/>\n'

        elif shape == 'cyclic_quad':
            svg_content += f'  <circle cx="100" cy="100" r="80" fill="none" stroke="{color}" stroke-width="3"/>\n'

            # Points on circle
            # Let's define some standard angles: 45, 135, 210, 330
            import math
            angles = [45, 135, 210, 330]
            pts = []
            for a in angles:
                rad = math.radians(a)
                x = 100 + 80 * math.cos(rad)
                y = 100 - 80 * math.sin(rad) # SVG y is inverted
                pts.append(f"{x},{y}")

            svg_content += f'  <polygon points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>\n'

            # Extended line for exterior angle
            if params.get('exterior_angle', False):
                # Extend the line from pt 3 (210 deg) to pt 4 (330 deg)
                rad = math.radians(330)
                x = 100 + 80 * math.cos(rad)
                y = 100 - 80 * math.sin(rad)

                # We need the vector from pt3 to pt4
                rad3 = math.radians(210)
                x3 = 100 + 80 * math.cos(rad3)
                y3 = 100 - 80 * math.sin(rad3)

                dx = x - x3
                dy = y - y3
                length = math.sqrt(dx*dx + dy*dy)

                ex = x + (dx/length) * 50
                ey = y + (dy/length) * 50

                svg_content += f'  <line x1="{x}" y1="{y}" x2="{ex}" y2="{ey}" stroke="{color}" stroke-width="2"/>\n'

            # Add labels if provided A, B, C, D
            if 'A' in labels:
                svg_content += f'  <text x="160" y="40" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["A"]}</text>\n'
            if 'B' in labels:
                svg_content += f'  <text x="30" y="40" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["B"]}</text>\n'
            if 'C' in labels:
                svg_content += f'  <text x="20" y="160" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["C"]}</text>\n'
            if 'D' in labels:
                svg_content += f'  <text x="180" y="160" text-anchor="middle" fill="{color}" font-family="sans-serif">{labels["D"]}</text>\n'

        svg_content += '</svg>'
        return svg_content

    @staticmethod
    def _generate_coordinate_grid(params: dict) -> str:
        points = params.get('points', [])
        svg_content = f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" width="100%" height="200px" style="max-width: 300px; margin: auto; display: block; background: #fafafa;">\n'

        # Draw grid
        for i in range(10, 200, 20):
            svg_content += f'  <line x1="{i}" y1="0" x2="{i}" y2="200" stroke="#ddd" stroke-width="1"/>\n'
            svg_content += f'  <line x1="0" y1="{i}" x2="200" y2="{i}" stroke="#ddd" stroke-width="1"/>\n'

        # Draw axes
        svg_content += f'  <line x1="100" y1="0" x2="100" y2="200" stroke="#333" stroke-width="2"/>\n'
        svg_content += f'  <line x1="0" y1="100" x2="200" y2="100" stroke="#333" stroke-width="2"/>\n'

        # Plot points
        for pt in points:
            x = 100 + pt.get('x', 0) * 20
            y = 100 - pt.get('y', 0) * 20
            label = pt.get('label', '')
            svg_content += f'  <circle cx="{x}" cy="{y}" r="4" fill="red"/>\n'
            if label:
                svg_content += f'  <text x="{x+8}" y="{y-8}" fill="#333" font-family="sans-serif" font-size="12">{label}</text>\n'

        svg_content += '</svg>'
        return svg_content

    @staticmethod
    def _generate_electric_circuit(params: dict) -> str:
        state = params.get('state', 'closed') # open or closed switch
        components = params.get('components', ['battery', 'resistor']) # list of components
        color = "#222"

        svg = f'<svg viewBox="0 0 240 160" xmlns="http://www.w3.org/2000/svg" width="100%" height="200px" style="max-width: 300px; margin: auto; display: block;">\n'

        # Top wire
        svg += f'  <line x1="40" y1="40" x2="200" y2="40" stroke="{color}" stroke-width="2"/>\n'
        # Bottom wire with battery
        svg += f'  <line x1="40" y1="120" x2="110" y2="120" stroke="{color}" stroke-width="2"/>\n'
        svg += f'  <line x1="130" y1="120" x2="200" y2="120" stroke="{color}" stroke-width="2"/>\n'
        # Battery symbol
        svg += f'  <line x1="110" y1="110" x2="110" y2="130" stroke="{color}" stroke-width="2"/>\n'
        svg += f'  <line x1="118" y1="105" x2="118" y2="135" stroke="{color}" stroke-width="4"/>\n'
        svg += f'  <line x1="130" y1="110" x2="130" y2="130" stroke="{color}" stroke-width="2"/>\n'

        # Left wire
        svg += f'  <line x1="40" y1="40" x2="40" y2="120" stroke="{color}" stroke-width="2"/>\n'

        # Right wire with switch or resistor
        svg += f'  <line x1="200" y1="40" x2="200" y2="60" stroke="{color}" stroke-width="2"/>\n'
        svg += f'  <line x1="200" y1="100" x2="200" y2="120" stroke="{color}" stroke-width="2"/>\n'

        if 'resistor' in components:
            points = "200,60 210,65 190,75 210,85 190,95 200,100"
            svg += f'  <polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>\n'
            svg += f'  <text x="220" y="85" font-family="sans-serif" font-size="12">R</text>\n'
        else:
            svg += f'  <line x1="200" y1="60" x2="200" y2="100" stroke="{color}" stroke-width="2"/>\n'

        if 'switch' in components:
            svg += f'  <rect x="100" y="38" width="40" height="4" fill="white"/>\n'
            svg += f'  <circle cx="100" cy="40" r="3" fill="{color}"/>\n'
            svg += f'  <circle cx="140" cy="40" r="3" fill="{color}"/>\n'
            if state == 'open':
                svg += f'  <line x1="100" y1="40" x2="135" y2="25" stroke="{color}" stroke-width="2"/>\n'
            else:
                svg += f'  <line x1="100" y1="40" x2="140" y2="40" stroke="{color}" stroke-width="2"/>\n'

        svg += '</svg>'
        return svg

    @staticmethod
    def _generate_dna_structure(params: dict) -> str:
        color1 = "#d32f2f"
        color2 = "#1976d2"
        base_color = "#333"
        pairs = params.get('pairs', 6)

        svg = f'<svg viewBox="0 0 100 200" xmlns="http://www.w3.org/2000/svg" width="100%" height="200px" style="max-width: 150px; margin: auto; display: block;">\n'

        for i in range(pairs):
            y = 20 + i * (160 / (pairs - 1 if pairs > 1 else 1))
            w = 30 * math.sin(i * 1.2)
            x1 = 50 - w
            x2 = 50 + w
            svg += f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{base_color}" stroke-width="3"/>\n'
            svg += f'  <circle cx="{x1}" cy="{y}" r="4" fill="{color1}"/>\n'
            svg += f'  <circle cx="{x2}" cy="{y}" r="4" fill="{color2}"/>\n'

            if i > 0:
                prev_y = 20 + (i-1) * (160 / (pairs - 1))
                prev_w = 30 * math.sin((i-1) * 1.2)
                px1 = 50 - prev_w
                px2 = 50 + prev_w
                svg += f'  <line x1="{px1}" y1="{prev_y}" x2="{x1}" y2="{y}" stroke="{color1}" stroke-width="2"/>\n'
                svg += f'  <line x1="{px2}" y1="{prev_y}" x2="{x2}" y2="{y}" stroke="{color2}" stroke-width="2"/>\n'

        svg += '</svg>'
        return svg

    @staticmethod
    def _generate_pedigree_tree(params: dict) -> str:
        svg = f'<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg" width="100%" height="200px" style="max-width: 300px; margin: auto; display: block;">\n'
        color = "#333"

        # Parent generation
        svg += f'  <rect x="40" y="20" width="30" height="30" fill="none" stroke="{color}" stroke-width="2"/>\n'
        svg += f'  <circle cx="145" cy="35" r="15" fill="none" stroke="{color}" stroke-width="2"/>\n'

        # Marriage line
        svg += f'  <line x1="70" y1="35" x2="130" y2="35" stroke="{color}" stroke-width="2"/>\n'

        # Descent line
        svg += f'  <line x1="100" y1="35" x2="100" y2="70" stroke="{color}" stroke-width="2"/>\n'
        svg += f'  <line x1="60" y1="70" x2="140" y2="70" stroke="{color}" stroke-width="2"/>\n'

        # Children generation
        svg += f'  <line x1="60" y1="70" x2="60" y2="90" stroke="{color}" stroke-width="2"/>\n'
        svg += f'  <circle cx="60" cy="105" r="15" fill="{color}" stroke="{color}" stroke-width="2"/>\n'

        svg += f'  <line x1="140" y1="70" x2="140" y2="90" stroke="{color}" stroke-width="2"/>\n'
        svg += f'  <rect x="125" y="90" width="30" height="30" fill="none" stroke="{color}" stroke-width="2"/>\n'

        svg += '</svg>'
        return svg
