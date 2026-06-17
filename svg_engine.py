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
