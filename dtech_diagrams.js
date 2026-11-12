/**
 * DTech Diagram Engine (dtech_diagrams.js)
 * High-precision, zero-dependency, mobile-responsive parametric SVG diagram generator.
 * Tailored for South African DBE CAPS Curriculum (Grades 10–12).
 * Supports: Physics Mechanics, Electric Circuits, Doppler, Chemistry Cells & Profiles,
 * Genetics Pedigrees, Punnett Squares, Endocrine Loops, and Cartesian Graphs.
 */

(function(global) {
    'use strict';

    const DTechDiagrams = {
        /**
         * Render an SVG into a target DOM container
         * @param {Object} config - Diagram specification object
         * @param {HTMLElement|string} container - Container element or selector
         */
        render(config, container) {
            const el = typeof container === 'string' ? document.querySelector(container) : container;
            if (!el) return;
            const svgString = this.getSVG(config);
            if (svgString) {
                el.innerHTML = svgString;
                el.style.display = 'flex';
            } else {
                el.innerHTML = '';
                el.style.display = 'none';
            }
        },

        /**
         * Returns the raw SVG string for a diagram configuration
         * @param {Object} config - Diagram specification object
         * @returns {string} Clean SVG markup
         */
        getSVG(config) {
            if (!config || typeof config !== 'object' || !config.type) {
                return '';
            }

            const handler = this.types[config.type];
            if (typeof handler === 'function') {
                return handler.call(this, config);
            }
            return '';
        },

        // Palette & Defs
        getColors() {
            return {
                bg: 'var(--bg-card, #1e293b)',
                text: 'var(--text-main, #f8fafc)',
                muted: 'var(--text-muted, #94a3b8)',
                blue: 'var(--accent-blue, #3b82f6)',
                green: 'var(--accent-green, #10b981)',
                red: 'var(--accent-red, #ef4444)',
                yellow: 'var(--accent-yellow, #f59e0b)',
                cyan: 'var(--accent-cyan, #06b6d4)',
                border: 'var(--border-color, #334155)',
                plane: '#475569'
            };
        },

        getDefs() {
            const c = this.getColors();
            return `
            <defs>
                <marker id="dtech-arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="${c.blue}"/>
                </marker>
                <marker id="dtech-arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="${c.green}"/>
                </marker>
                <marker id="dtech-arrow-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="${c.red}"/>
                </marker>
                <marker id="dtech-arrow-main" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="${c.text}"/>
                </marker>
                <marker id="dtech-arrow-yellow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="${c.yellow}"/>
                </marker>
                <linearGradient id="dtech-spectrum-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#3b82f6"/>
                    <stop offset="25%" stop-color="#06b6d4"/>
                    <stop offset="50%" stop-color="#10b981"/>
                    <stop offset="75%" stop-color="#f59e0b"/>
                    <stop offset="100%" stop-color="#ef4444"/>
                </linearGradient>
            </defs>`;
        },

        // Diagram Renderers
        types: {
            /**
             * 1. INCLINED PLANE (Newton's Laws & Friction)
             * Config: { angle: 30, mass: 4, friction: true, pulling_force: 25, pulling_dir: 'up' }
             */
            inclined_plane(cfg) {
                const c = this.getColors();
                const angle = cfg.angle || 30;
                const mass = cfg.mass || 5;
                const width = 360;
                const height = 220;

                // Triangle dimensions
                const x0 = 40;
                const y0 = 180;
                const base = 260;
                const rad = (angle * Math.PI) / 180;
                const rampH = Math.min(130, Math.tan(rad) * base);
                const xTop = x0 + base;
                const yTop = y0 - rampH;

                // Position block halfway along hypotenuse
                const hyp = Math.sqrt(base * base + rampH * rampH);
                const t = 0.52; // parameter along incline
                const bx = x0 + base * t;
                const by = y0 - rampH * t;
                const blockW = 44;
                const blockH = 28;

                // Vectors
                const fApp = cfg.pulling_force;
                const hasFric = cfg.friction !== false;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Incline Surface -->
                    <polygon points="${x0},${y0} ${xTop},${y0} ${xTop},${yTop}" fill="rgba(51, 65, 85, 0.4)" stroke="${c.border}" stroke-width="2"/>
                    <line x1="${x0}" y1="${y0}" x2="${xTop}" y2="${yTop}" stroke="${c.text}" stroke-width="3" stroke-linecap="round"/>
                    <line x1="${x0 - 15}" y1="${y0}" x2="${xTop + 15}" y2="${y0}" stroke="${c.muted}" stroke-width="2"/>

                    <!-- Angle Arc & Label -->
                    <path d="M ${x0 + 45} ${y0} A 45 45 0 0 0 ${x0 + 45 * Math.cos(rad)} ${y0 - 45 * Math.sin(rad)}" fill="none" stroke="${c.yellow}" stroke-width="2"/>
                    <text x="${x0 + 55}" y="${y0 - 10}" fill="${c.yellow}" font-size="13" font-weight="bold">${angle}°</text>

                    <!-- Block (Rotated along incline) -->
                    <g transform="translate(${bx}, ${by}) rotate(${-angle})">
                        <rect x="${-blockW / 2}" y="${-blockH}" width="${blockW}" height="${blockH}" rx="4" fill="${c.blue}" stroke="#60a5fa" stroke-width="2"/>
                        <text x="0" y="${-blockH / 2 + 5}" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">${mass} kg</text>

                        <!-- Normal Force (Perpendicular to plane) -->
                        <line x1="0" y1="${-blockH}" x2="0" y2="${-blockH - 45}" stroke="${c.green}" stroke-width="2.5" marker-end="url(#dtech-arrow-green)"/>
                        <text x="12" y="${-blockH - 40}" fill="${c.green}" font-size="11" font-weight="bold">F_N</text>

                        <!-- Parallel Forces -->
                        ${fApp ? `
                        <line x1="${blockW / 2}" y1="${-blockH / 2}" x2="${blockW / 2 + 50}" y2="${-blockH / 2}" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                        <text x="${blockW / 2 + 15}" y="${-blockH / 2 - 8}" fill="${c.yellow}" font-size="11" font-weight="bold">${fApp} N</text>
                        ` : ''}

                        ${hasFric ? `
                        <line x1="${-blockW / 2}" y1="${-4}" x2="${-blockW / 2 - 40}" y2="${-4}" stroke="${c.red}" stroke-width="2" marker-end="url(#dtech-arrow-red)"/>
                        <text x="${-blockW / 2 - 35}" y="${-10}" fill="${c.red}" font-size="11" font-weight="bold">f_k</text>
                        ` : ''}
                    </g>

                    <!-- Gravity Vector (Straight down) -->
                    <line x1="${bx}" y1="${by - blockH / 2}" x2="${bx}" y2="${by + 48}" stroke="${c.red}" stroke-width="2.5" marker-end="url(#dtech-arrow-red)"/>
                    <text x="${bx + 8}" y="${by + 45}" fill="${c.red}" font-size="11" font-weight="bold">F_g = mg</text>
                </svg>`;
            },

            /**
             * 2. ELECTRIC CIRCUIT (Series / Parallel with Voltmeter and Ammeter)
             * Config: { battery: 12, internal_r: 1, r1: 4, r2: 6, config: 'parallel'|'series', ammeter: true, voltmeter: true }
             */
            circuit(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 220;
                const isParallel = cfg.config !== 'series';
                const vVal = cfg.battery || 12;
                const rInt = cfg.internal_r;
                const r1 = cfg.r1 || 4;
                const r2 = cfg.r2 || 6;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Main Circuit Loop -->
                    <!-- Top Wire with Battery & Switch -->
                    <line x1="60" y1="50" x2="130" y2="50" stroke="${c.text}" stroke-width="2.5"/>
                    <!-- Battery Cells -->
                    <line x1="130" y1="36" x2="130" y2="64" stroke="${c.green}" stroke-width="3"/>
                    <line x1="138" y1="42" x2="138" y2="58" stroke="${c.text}" stroke-width="4.5"/>
                    <line x1="146" y1="36" x2="146" y2="64" stroke="${c.green}" stroke-width="3"/>
                    <line x1="154" y1="42" x2="154" y2="58" stroke="${c.text}" stroke-width="4.5"/>
                    <text x="142" y="26" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">${vVal} V${rInt ? ` (r=${rInt}Ω)` : ''}</text>

                    <!-- Top Wire Continuing to Switch -->
                    <line x1="154" y1="50" x2="220" y2="50" stroke="${c.text}" stroke-width="2.5"/>
                    <!-- Switch (Closed) -->
                    <circle cx="220" cy="50" r="3" fill="${c.text}"/>
                    <circle cx="250" cy="50" r="3" fill="${c.text}"/>
                    <line x1="220" y1="50" x2="250" y2="50" stroke="${c.text}" stroke-width="2.5"/>
                    <text x="235" y="40" fill="${c.muted}" font-size="10" text-anchor="middle">S</text>
                    <line x1="250" y1="50" x2="310" y2="50" stroke="${c.text}" stroke-width="2.5"/>

                    <!-- Right Side Drop -->
                    <line x1="310" y1="50" x2="310" y2="90" stroke="${c.text}" stroke-width="2.5"/>

                    ${isParallel ? `
                    <!-- Parallel Junction Top & Bottom -->
                    <circle cx="310" cy="90" r="3.5" fill="${c.blue}"/>
                    <circle cx="60" cy="90" r="3.5" fill="${c.blue}"/>
                    <!-- Branch 1 (Upper) -->
                    <line x1="60" y1="90" x2="140" y2="90" stroke="${c.text}" stroke-width="2"/>
                    <rect x="140" y="81" width="50" height="18" fill="${c.bg}" stroke="${c.blue}" stroke-width="2" rx="3"/>
                    <text x="165" y="94" fill="${c.text}" font-size="11" font-weight="bold" text-anchor="middle">R₁ = ${r1}Ω</text>
                    <line x1="190" y1="90" x2="310" y2="90" stroke="${c.text}" stroke-width="2"/>

                    <!-- Branch 2 (Lower) -->
                    <line x1="60" y1="90" x2="60" y2="150" stroke="${c.text}" stroke-width="2"/>
                    <line x1="310" y1="90" x2="310" y2="150" stroke="${c.text}" stroke-width="2"/>
                    <line x1="60" y1="150" x2="140" y2="150" stroke="${c.text}" stroke-width="2"/>
                    <rect x="140" y="141" width="50" height="18" fill="${c.bg}" stroke="${c.blue}" stroke-width="2" rx="3"/>
                    <text x="165" y="154" fill="${c.text}" font-size="11" font-weight="bold" text-anchor="middle">R₂ = ${r2}Ω</text>
                    <line x1="190" y1="150" x2="310" y2="150" stroke="${c.text}" stroke-width="2"/>

                    <!-- Return Path Bottom -->
                    <line x1="60" y1="90" x2="60" y2="185" stroke="${c.text}" stroke-width="2.5"/>
                    <line x1="310" y1="150" x2="310" y2="185" stroke="${c.text}" stroke-width="2.5"/>
                    <line x1="310" y1="185" x2="210" y2="185" stroke="${c.text}" stroke-width="2.5"/>
                    ` : `
                    <!-- Series Resistors -->
                    <line x1="310" y1="90" x2="310" y2="185" stroke="${c.text}" stroke-width="2.5"/>
                    <line x1="310" y1="185" x2="250" y2="185" stroke="${c.text}" stroke-width="2.5"/>
                    <rect x="200" y="176" width="50" height="18" fill="${c.bg}" stroke="${c.blue}" stroke-width="2" rx="3"/>
                    <text x="225" y="189" fill="${c.text}" font-size="11" font-weight="bold" text-anchor="middle">R₁ = ${r1}Ω</text>
                    <line x1="200" y1="185" x2="160" y2="185" stroke="${c.text}" stroke-width="2.5"/>
                    <rect x="110" y="176" width="50" height="18" fill="${c.bg}" stroke="${c.blue}" stroke-width="2" rx="3"/>
                    <text x="135" y="189" fill="${c.text}" font-size="11" font-weight="bold" text-anchor="middle">R₂ = ${r2}Ω</text>
                    <line x1="110" y1="185" x2="60" y2="185" stroke="${c.text}" stroke-width="2.5"/>
                    `}

                    <!-- Ammeter in Series (Bottom Left) -->
                    <circle cx="95" cy="185" r="13" fill="${c.bg}" stroke="${c.yellow}" stroke-width="2"/>
                    <text x="95" y="190" fill="${c.yellow}" font-size="12" font-weight="bold" text-anchor="middle">A</text>
                    <line x1="60" y1="185" x2="82" y2="185" stroke="${c.text}" stroke-width="2.5"/>
                    <line x1="108" y1="185" x2="140" y2="185" stroke="${c.text}" stroke-width="2.5"/>

                    <!-- Left Return to Top -->
                    <line x1="60" y1="185" x2="60" y2="50" stroke="${c.text}" stroke-width="2.5"/>

                    <!-- Voltmeter across battery or branch -->
                    <line x1="115" y1="50" x2="115" y2="15" stroke="${c.muted}" stroke-width="1.5" stroke-dasharray="2,2"/>
                    <line x1="170" y1="50" x2="170" y2="15" stroke="${c.muted}" stroke-width="1.5" stroke-dasharray="2,2"/>
                    <line x1="115" y1="15" x2="130" y2="15" stroke="${c.muted}" stroke-width="1.5"/>
                    <line x1="155" y1="15" x2="170" y2="15" stroke="${c.muted}" stroke-width="1.5"/>
                    <circle cx="142" cy="15" r="11" fill="${c.bg}" stroke="${c.cyan}" stroke-width="2"/>
                    <text x="142" y="19" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">V</text>
                </svg>`;
            },

            /**
             * 3. ATWOOD MACHINE / PULLEY SYSTEM
             * Config: { m1: 3, m2: 5, type: 'vertical'|'table' }
             */
            pulley_atwood(cfg) {
                const c = this.getColors();
                const m1 = cfg.m1 || 2;
                const m2 = cfg.m2 || 5;
                const width = 320;
                const height = 220;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Ceiling -->
                    <line x1="110" y1="20" x2="210" y2="20" stroke="${c.muted}" stroke-width="3"/>
                    <!-- Ceiling mount bracket -->
                    <line x1="160" y1="20" x2="160" y2="45" stroke="${c.text}" stroke-width="3"/>

                    <!-- Pulley Wheel -->
                    <circle cx="160" cy="55" r="20" fill="${c.bg}" stroke="${c.cyan}" stroke-width="3"/>
                    <circle cx="160" cy="55" r="4" fill="${c.cyan}"/>

                    <!-- Cords -->
                    <line x1="140" y1="55" x2="140" y2="110" stroke="${c.text}" stroke-width="2.5"/>
                    <line x1="180" y1="55" x2="180" y2="140" stroke="${c.text}" stroke-width="2.5"/>

                    <!-- Tension Arrows -->
                    <line x1="140" y1="105" x2="140" y2="80" stroke="${c.green}" stroke-width="2" marker-end="url(#dtech-arrow-green)"/>
                    <text x="126" y="92" fill="${c.green}" font-size="11" font-weight="bold">T</text>
                    <line x1="180" y1="135" x2="180" y2="110" stroke="${c.green}" stroke-width="2" marker-end="url(#dtech-arrow-green)"/>
                    <text x="187" y="122" fill="${c.green}" font-size="11" font-weight="bold">T</text>

                    <!-- Mass 1 (Left, lighter, higher) -->
                    <rect x="122" y="110" width="36" height="36" rx="4" fill="${c.blue}" stroke="#60a5fa" stroke-width="2"/>
                    <text x="140" y="132" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">${m1} kg</text>
                    <!-- Gravity 1 -->
                    <line x1="140" y1="146" x2="140" y2="175" stroke="${c.red}" stroke-width="2" marker-end="url(#dtech-arrow-red)"/>
                    <text x="148" y="170" fill="${c.red}" font-size="10">m₁g</text>

                    <!-- Mass 2 (Right, heavier, lower) -->
                    <rect x="158" y="140" width="44" height="44" rx="4" fill="${c.yellow}" stroke="#fbbf24" stroke-width="2"/>
                    <text x="180" y="166" fill="#000000" font-size="12" font-weight="bold" text-anchor="middle">${m2} kg</text>
                    <!-- Gravity 2 -->
                    <line x1="180" y1="184" x2="180" y2="214" stroke="${c.red}" stroke-width="2.5" marker-end="url(#dtech-arrow-red)"/>
                    <text x="188" y="210" fill="${c.red}" font-size="10">m₂g</text>
                </svg>`;
            },

            /**
             * 4. FREE BODY DIAGRAM (FBD)
             * Config: { fn: true, fg: true, fk: true, fapp: 40, angle: 30, mass: 8 }
             */
            free_body(cfg) {
                const c = this.getColors();
                const width = 300;
                const height = 220;
                const cx = 130;
                const cy = 115;
                const angle = cfg.angle || 0;
                const rad = (angle * Math.PI) / 180;
                const fLen = 85;
                const fx = cx + fLen * Math.cos(rad);
                const fy = cy - fLen * Math.sin(rad);

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Coordinate Axes (Dashed) -->
                    <line x1="20" y1="${cy}" x2="270" y2="${cy}" stroke="${c.border}" stroke-width="1.5" stroke-dasharray="3,3"/>
                    <line x1="${cx}" y1="20" x2="${cx}" y2="205" stroke="${c.border}" stroke-width="1.5" stroke-dasharray="3,3"/>

                    <!-- Central Point of Mass -->
                    <circle cx="${cx}" cy="${cy}" r="6" fill="${c.blue}" stroke="#ffffff" stroke-width="2"/>
                    ${cfg.mass ? `<text x="${cx - 10}" y="${cy - 10}" fill="${c.muted}" font-size="10">${cfg.mass} kg</text>` : ''}

                    <!-- Normal Force (Up) -->
                    <line x1="${cx}" y1="${cy}" x2="${cx}" y2="35" stroke="${c.green}" stroke-width="2.5" marker-end="url(#dtech-arrow-green)"/>
                    <text x="${cx + 8}" y="35" fill="${c.green}" font-size="12" font-weight="bold">F_N</text>

                    <!-- Gravity Force (Down) -->
                    <line x1="${cx}" y1="${cy}" x2="${cx}" y2="190" stroke="${c.red}" stroke-width="2.5" marker-end="url(#dtech-arrow-red)"/>
                    <text x="${cx + 8}" y="190" fill="${c.red}" font-size="12" font-weight="bold">F_g = mg</text>

                    <!-- Applied Force (At Angle theta if specified) -->
                    <line x1="${cx}" y1="${cy}" x2="${fx}" y2="${fy}" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="${fx + 5}" y="${fy}" fill="${c.yellow}" font-size="11" font-weight="bold">F_app${cfg.fapp ? ` = ${cfg.fapp}N` : ''}</text>
                    ${angle > 0 ? `
                    <path d="M ${cx + 35} ${cy} A 35 35 0 0 0 ${cx + 35 * Math.cos(rad)} ${cy - 35 * Math.sin(rad)}" fill="none" stroke="${c.yellow}" stroke-width="1.5"/>
                    <text x="${cx + 42}" y="${cy - 8}" fill="${c.yellow}" font-size="10">${angle}°</text>
                    ` : ''}

                    <!-- Frictional Force (Left) -->
                    <line x1="${cx}" y1="${cy}" x2="45" y2="${cy}" stroke="${c.cyan}" stroke-width="2.5" marker-end="url(#dtech-arrow-main)"/>
                    <text x="35" y="${cy - 8}" fill="${c.cyan}" font-size="12" font-weight="bold">f_k</text>
                </svg>`;
            },

            /**
             * 5. DOPPLER EFFECT (Wavefront Compression)
             * Config: { source_speed: 'v_s', dir: 'right' }
             */
            doppler_wave(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 180;
                const cy = 90;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Sound Wavefront Circles (Shifted centers towards right) -->
                    <circle cx="160" cy="${cy}" r="75" fill="none" stroke="${c.blue}" stroke-width="1.5" opacity="0.4"/>
                    <circle cx="180" cy="${cy}" r="55" fill="none" stroke="${c.blue}" stroke-width="1.8" opacity="0.6"/>
                    <circle cx="195" cy="${cy}" r="35" fill="none" stroke="${c.blue}" stroke-width="2" opacity="0.8"/>
                    <circle cx="205" cy="${cy}" r="18" fill="none" stroke="${c.blue}" stroke-width="2.5"/>

                    <!-- Moving Source (S) -->
                    <circle cx="212" cy="${cy}" r="7" fill="${c.red}"/>
                    <text x="212" y="${cy - 12}" fill="${c.red}" font-size="11" font-weight="bold" text-anchor="middle">Source (v_s)</text>
                    <line x1="212" y1="${cy}" x2="238" y2="${cy}" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>

                    <!-- Listener A (Approaching side: High f, compressed lambda) -->
                    <circle cx="310" cy="${cy}" r="8" fill="${c.green}"/>
                    <text x="310" y="${cy + 22}" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">Listener A</text>
                    <text x="310" y="${cy + 36}" fill="${c.yellow}" font-size="10" text-anchor="middle">(Higher f_L)</text>

                    <!-- Listener B (Receding side: Low f, stretched lambda) -->
                    <circle cx="50" cy="${cy}" r="8" fill="${c.cyan}"/>
                    <text x="50" y="${cy + 22}" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">Listener B</text>
                    <text x="50" y="${cy + 36}" fill="${c.muted}" font-size="10" text-anchor="middle">(Lower f_L)</text>
                </svg>`;
            },

            /**
             * 6. GALVANIC ELECTROCHEMICAL CELL
             * Config: { anode: 'Zn', cathode: 'Cu', voltage: 1.10 }
             */
            galvanic_cell(cfg) {
                const c = this.getColors();
                const anode = cfg.anode || 'Zn';
                const cathode = cfg.cathode || 'Cu';
                const v = cfg.voltage || '1.10';
                const width = 360;
                const height = 210;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Beaker 1 (Anode / Oxidation) -->
                    <rect x="50" y="80" width="90" height="90" rx="4" fill="rgba(59, 130, 246, 0.15)" stroke="${c.border}" stroke-width="2"/>
                    <rect x="75" y="55" width="16" height="85" fill="#94a3b8" stroke="#cbd5e1" stroke-width="1.5"/>
                    <text x="83" y="45" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">${anode}</text>
                    <text x="95" y="155" fill="${c.blue}" font-size="10" text-anchor="middle">${anode}²⁺ (aq)</text>
                    <text x="95" y="195" fill="${c.red}" font-size="11" font-weight="bold" text-anchor="middle">Anode (-)</text>

                    <!-- Beaker 2 (Cathode / Reduction) -->
                    <rect x="220" y="80" width="90" height="90" rx="4" fill="rgba(16, 185, 129, 0.15)" stroke="${c.border}" stroke-width="2"/>
                    <rect x="269" y="55" width="16" height="85" fill="#d97706" stroke="#f59e0b" stroke-width="1.5"/>
                    <text x="277" y="45" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">${cathode}</text>
                    <text x="265" y="155" fill="${c.green}" font-size="10" text-anchor="middle">${cathode}²⁺ (aq)</text>
                    <text x="265" y="195" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">Cathode (+)</text>

                    <!-- U-Tube Salt Bridge -->
                    <path d="M 115 125 L 115 70 Q 115 60 125 60 L 235 60 Q 245 60 245 70 L 245 125" fill="none" stroke="${c.yellow}" stroke-width="12" stroke-linecap="round" opacity="0.85"/>
                    <text x="180" y="52" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">Salt Bridge (KNO₃)</text>

                    <!-- External Circuit & Voltmeter -->
                    <path d="M 83 55 L 83 25 L 160 25" fill="none" stroke="${c.text}" stroke-width="2"/>
                    <path d="M 277 55 L 277 25 L 200 25" fill="none" stroke="${c.text}" stroke-width="2"/>
                    <!-- Voltmeter -->
                    <circle cx="180" cy="25" r="14" fill="${c.bg}" stroke="${c.cyan}" stroke-width="2"/>
                    <text x="180" y="29" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">${cfg.show_voltage ? `${v} V` : 'V'}</text>

                    <!-- Electron Flow Arrow -->
                    <line x1="110" y1="16" x2="140" y2="16" stroke="${c.yellow}" stroke-width="2" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="125" y="10" fill="${c.yellow}" font-size="9" text-anchor="middle">e⁻ flow</text>
                </svg>`;
            },

            /**
             * 7. REACTION ENERGY PROFILE
             * Config: { type_reaction: 'exothermic'|'endothermic', ea: 80, delta_h: -40, catalyzed: true }
             */
            energy_profile(cfg) {
                const c = this.getColors();
                const isExo = cfg.type_reaction !== 'endothermic';
                const hasCat = cfg.catalyzed !== false;
                const width = 340;
                const height = 210;

                const yReact = 120;
                const yPeak = 45;
                const yCatPeak = 70;
                const yProd = isExo ? 160 : 80;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Axes -->
                    <line x1="45" y1="190" x2="310" y2="190" stroke="${c.text}" stroke-width="2" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="45" y1="190" x2="45" y2="20" stroke="${c.text}" stroke-width="2" marker-end="url(#dtech-arrow-main)"/>
                    <text x="175" y="206" fill="${c.muted}" font-size="11" text-anchor="middle">Reaction Coordinate</text>
                    <text x="25" y="100" fill="${c.muted}" font-size="11" transform="rotate(-90, 25, 100)" text-anchor="middle">Potential Energy (kJ)</text>

                    <!-- Reactants Line -->
                    <line x1="45" y1="${yReact}" x2="95" y2="${yReact}" stroke="${c.blue}" stroke-width="3"/>
                    <text x="70" y="${yReact - 8}" fill="${c.blue}" font-size="11" font-weight="bold" text-anchor="middle">Reactants</text>

                    <!-- Uncatalyzed Curve -->
                    <path d="M 95 ${yReact} C 120 ${yReact}, 140 ${yPeak}, 175 ${yPeak} C 210 ${yPeak}, 230 ${yProd}, 260 ${yProd}" fill="none" stroke="${c.red}" stroke-width="2.5"/>

                    ${hasCat ? `
                    <!-- Catalyzed Curve (Dashed Green) -->
                    <path d="M 95 ${yReact} C 120 ${yReact}, 140 ${yCatPeak}, 175 ${yCatPeak} C 210 ${yCatPeak}, 230 ${yProd}, 260 ${yProd}" fill="none" stroke="${c.green}" stroke-width="2" stroke-dasharray="4,4"/>
                    <text x="175" y="${yCatPeak - 6}" fill="${c.green}" font-size="10" font-weight="bold" text-anchor="middle">With Catalyst</text>
                    ` : ''}

                    <!-- Products Line -->
                    <line x1="260" y1="${yProd}" x2="305" y2="${yProd}" stroke="${c.cyan}" stroke-width="3"/>
                    <text x="282" y="${yProd - 8}" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">Products</text>

                    <!-- Ea Double Arrow -->
                    <line x1="120" y1="${yReact}" x2="120" y2="${yPeak}" stroke="${c.yellow}" stroke-width="1.8" marker-end="url(#dtech-arrow-yellow)" marker-start="url(#dtech-arrow-yellow)"/>
                    <text x="130" y="${(yReact + yPeak) / 2 + 4}" fill="${c.yellow}" font-size="10" font-weight="bold">E_a</text>

                    <!-- Delta H Arrow -->
                    <line x1="240" y1="${yReact}" x2="240" y2="${yProd}" stroke="${c.text}" stroke-width="1.8" stroke-dasharray="2,2"/>
                    <line x1="240" y1="${yReact}" x2="240" y2="${yProd}" stroke="${isExo ? c.red : c.green}" stroke-width="2" marker-end="${isExo ? 'url(#dtech-arrow-red)' : 'url(#dtech-arrow-green)'}"/>
                    <text x="252" y="${(yReact + yProd) / 2 + 4}" fill="${isExo ? c.red : c.green}" font-size="11" font-weight="bold">${cfg.delta_h_label || 'ΔH'}</text>
                </svg>`;
            },

            /**
             * 8. GENETICS PEDIGREE CHART
             * Config: { generations: 3, affected: ['I-1', 'II-2', 'III-1'], trait_name: 'Huntington' }
             */
            pedigree(cfg) {
                const c = this.getColors();
                const aff = new Set(cfg.affected || ['I-1', 'II-2']);
                const width = 340;
                const height = 210;

                const isAff = (id) => aff.has(id);

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    <!-- Generation I -->
                    <text x="35" y="48" fill="${c.muted}" font-size="12" font-weight="bold">I</text>
                    <!-- I-1 (Male Square) -->
                    <rect x="90" y="32" width="26" height="26" fill="${isAff('I-1') ? c.red : c.bg}" stroke="${c.text}" stroke-width="2"/>
                    <text x="103" y="24" fill="${c.muted}" font-size="10" text-anchor="middle">1</text>
                    <!-- Marriage Line -->
                    <line x1="116" y1="45" x2="190" y2="45" stroke="${c.text}" stroke-width="2"/>
                    <!-- I-2 (Female Circle) -->
                    <circle cx="203" cy="45" r="13" fill="${isAff('I-2') ? c.red : c.bg}" stroke="${c.text}" stroke-width="2"/>
                    <text x="203" y="24" fill="${c.muted}" font-size="10" text-anchor="middle">2</text>

                    <!-- Descent Line to Gen II -->
                    <line x1="153" y1="45" x2="153" y2="75" stroke="${c.text}" stroke-width="2"/>
                    <line x1="90" y1="75" x2="250" y2="75" stroke="${c.text}" stroke-width="2"/>

                    <!-- Generation II -->
                    <text x="35" y="118" fill="${c.muted}" font-size="12" font-weight="bold">II</text>
                    <!-- II-1 (Female) -->
                    <line x1="90" y1="75" x2="90" y2="102" stroke="${c.text}" stroke-width="2"/>
                    <circle cx="90" cy="115" r="13" fill="${isAff('II-1') ? c.red : c.bg}" stroke="${c.text}" stroke-width="2"/>
                    <text x="90" y="138" fill="${c.muted}" font-size="10" text-anchor="middle">1</text>

                    <!-- II-2 (Male Affected) -->
                    <line x1="170" y1="75" x2="170" y2="102" stroke="${c.text}" stroke-width="2"/>
                    <rect x="157" y="102" width="26" height="26" fill="${isAff('II-2') ? c.red : c.bg}" stroke="${c.text}" stroke-width="2"/>
                    <text x="170" y="138" fill="${c.muted}" font-size="10" text-anchor="middle">2</text>
                    <!-- II-2 marries II-3 -->
                    <line x1="183" y1="115" x2="225" y2="115" stroke="${c.text}" stroke-width="2"/>
                    <circle cx="238" cy="115" r="13" fill="${isAff('II-3') ? c.red : c.bg}" stroke="${c.text}" stroke-width="2"/>
                    <text x="238" y="138" fill="${c.muted}" font-size="10" text-anchor="middle">3</text>

                    <!-- II-4 (Female) -->
                    <line x1="250" y1="75" x2="250" y2="102" stroke="${c.text}" stroke-width="2"/>
                    <circle cx="250" cy="115" r="13" fill="${isAff('II-4') ? c.red : c.bg}" stroke="${c.text}" stroke-width="2"/>
                    <text x="250" y="138" fill="${c.muted}" font-size="10" text-anchor="middle">4</text>

                    <!-- Generation III -->
                    <text x="35" y="185" fill="${c.muted}" font-size="12" font-weight="bold">III</text>
                    <line x1="210" y1="115" x2="210" y2="155" stroke="${c.text}" stroke-width="2"/>
                    <line x1="175" y1="155" x2="245" y2="155" stroke="${c.text}" stroke-width="2"/>

                    <!-- III-1 (Male) -->
                    <line x1="175" y1="155" x2="175" y2="172" stroke="${c.text}" stroke-width="2"/>
                    <rect x="162" y="172" width="26" height="26" fill="${isAff('III-1') ? c.red : c.bg}" stroke="${c.text}" stroke-width="2"/>
                    <text x="175" y="206" fill="${c.muted}" font-size="10" text-anchor="middle">1</text>

                    <!-- III-2 (Female) -->
                    <line x1="245" y1="155" x2="245" y2="172" stroke="${c.text}" stroke-width="2"/>
                    <circle cx="245" cy="185" r="13" fill="${isAff('III-2') ? c.red : c.bg}" stroke="${c.text}" stroke-width="2"/>
                    <text x="245" y="206" fill="${c.muted}" font-size="10" text-anchor="middle">2</text>

                    <!-- Legend -->
                    <rect x="270" y="15" width="12" height="12" fill="${c.bg}" stroke="${c.text}" stroke-width="1.5"/>
                    <text x="288" y="25" fill="${c.text}" font-size="10">Male</text>
                    <circle cx="276" cy="38" r="6" fill="${c.bg}" stroke="${c.text}" stroke-width="1.5"/>
                    <text x="288" y="42" fill="${c.text}" font-size="10">Female</text>
                    <rect x="270" y="52" width="12" height="12" fill="${c.red}" stroke="${c.text}" stroke-width="1.5"/>
                    <text x="288" y="62" fill="${c.red}" font-size="10">Affected</text>
                </svg>`;
            },

            /**
             * 9. ENDOCRINE NEGATIVE FEEDBACK LOOP
             * Config: { stimulus: 'High Blood Glucose', gland: 'Beta Cells (Pancreas)', hormone: 'Insulin', target: 'Liver & Cells', effect: 'Glucose -> Glycogen' }
             */
            endocrine_feedback(cfg) {
                const c = this.getColors();
                const stim = cfg.stimulus || 'High Blood Glucose';
                const gland = cfg.gland || 'Pancreas (Beta Cells)';
                const horm = cfg.hormone || 'Insulin Secretion';
                const target = cfg.target || 'Liver & Muscle Cells';
                const effect = cfg.effect || 'Absorb Glucose / Synthesize Glycogen';
                const width = 360;
                const height = 210;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Box 1: Stimulus (Top Left) -->
                    <rect x="20" y="20" width="140" height="36" rx="6" fill="${c.bg}" stroke="${c.yellow}" stroke-width="2"/>
                    <text x="90" y="42" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="middle">${stim}</text>

                    <line x1="160" y1="38" x2="200" y2="38" stroke="${c.text}" stroke-width="2" marker-end="url(#dtech-arrow-main)"/>

                    <!-- Box 2: Gland Sensor (Top Right) -->
                    <rect x="200" y="20" width="140" height="36" rx="6" fill="${c.bg}" stroke="${c.cyan}" stroke-width="2"/>
                    <text x="270" y="42" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">${gland}</text>

                    <line x1="270" y1="56" x2="270" y2="88" stroke="${c.text}" stroke-width="2" marker-end="url(#dtech-arrow-main)"/>

                    <!-- Box 3: Hormone Secretion (Middle Right) -->
                    <rect x="200" y="88" width="140" height="36" rx="6" fill="${c.bg}" stroke="${c.green}" stroke-width="2"/>
                    <text x="270" y="110" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">${horm}</text>

                    <line x1="270" y1="124" x2="270" y2="155" stroke="${c.text}" stroke-width="2" marker-end="url(#dtech-arrow-main)"/>

                    <!-- Box 4: Effector Response (Bottom Right) -->
                    <rect x="180" y="155" width="165" height="42" rx="6" fill="${c.bg}" stroke="${c.blue}" stroke-width="2"/>
                    <text x="262" y="173" fill="${c.blue}" font-size="10" font-weight="bold" text-anchor="middle">${target}</text>
                    <text x="262" y="188" fill="${c.text}" font-size="9" text-anchor="middle">${effect}</text>

                    <!-- Negative Feedback Return Loop (Leftward & Up) -->
                    <path d="M 180 176 L 90 176 L 90 64" fill="none" stroke="${c.red}" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#dtech-arrow-red)"/>
                    <text x="80" y="125" fill="${c.red}" font-size="10" font-weight="bold" transform="rotate(-90, 80, 125)" text-anchor="middle">Negative Feedback (Inhibition)</text>
                </svg>`;
            },

            /**
             * 10. CARTESIAN GRAPH (Functions, Kinematics, Parabolas)
             * Config: { graph_type: 'parabola'|'hyperbola', turning_point: '(2; -4)', y_intercept: '-3', title: 'f(x) = x² - 4x' }
             */
            cartesian_graph(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const cx = 140;
                const cy = 110;
                const tp = cfg.turning_point || '(2; -4)';
                const title = cfg.title || 'f(x)';
                const tpLabel = cfg.show_coords ? `TP ${tp}` : (cfg.tp_label || 'Turning Point P');

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Axes -->
                    <line x1="20" y1="${cy}" x2="320" y2="${cy}" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="${cx}" y1="195" x2="${cx}" y2="20" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="315" y="${cy - 8}" fill="${c.text}" font-size="11" font-weight="bold">x</text>
                    <text x="${cx + 8}" y="25" fill="${c.text}" font-size="11" font-weight="bold">y</text>
                    <text x="${cx - 12}" y="${cy + 15}" fill="${c.muted}" font-size="11">0</text>

                    <!-- Title -->
                    <text x="240" y="35" fill="${c.cyan}" font-size="12" font-weight="bold">${title}</text>

                    <!-- Parabola Curve -->
                    <path d="M 60 40 Q 190 220 280 40" fill="none" stroke="${c.blue}" stroke-width="2.5"/>

                    <!-- Turning Point (Minimum) -->
                    <circle cx="185" cy="155" r="4.5" fill="${c.yellow}"/>
                    <text x="185" y="175" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="middle">${tpLabel}</text>

                    <!-- Intercepts -->
                    <circle cx="115" cy="${cy}" r="3.5" fill="${c.green}"/>
                    <circle cx="255" cy="${cy}" r="3.5" fill="${c.green}"/>
                    <circle cx="${cx}" cy="90" r="3.5" fill="${c.red}"/>
                </svg>`;
            },
            /**
             * 11. PUNNETT SQUARE (Monohybrid & Dihybrid Crosses)
             * Config: { p1: ['I^A', 'i'], p2: ['I^B', 'i'], cross_label: 'Father (IAi) × Mother (IBi)', phenotype: 'Blood Groups: AB, A, B, O' }
             */
            punnett_square(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 230;
                const p1 = cfg.p1 || ['B', 'b'];
                const p2 = cfg.p2 || ['B', 'b'];
                const label = cfg.cross_label || `${p1.join('')} × ${p2.join('')}`;
                const showOffspring = cfg.hide_offspring !== true;

                const c00 = showOffspring ? `${p1[0]}${p2[0]}` : '?';
                const c01 = showOffspring ? `${p1[1]}${p2[0]}` : '?';
                const c10 = showOffspring ? `${p1[0]}${p2[1]}` : '?';
                const c11 = showOffspring ? `${p1[1]}${p2[1]}` : '?';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <text x="170" y="22" fill="${c.cyan}" font-size="12" font-weight="bold" text-anchor="middle">Punnett Square: ${label}</text>
                    
                    <!-- Gametes Parent 1 (Top / Male) -->
                    <text x="160" y="50" fill="${c.yellow}" font-size="12" font-weight="bold" text-anchor="middle">${p1[0]}</text>
                    <text x="250" y="50" fill="${c.yellow}" font-size="12" font-weight="bold" text-anchor="middle">${p1[1]}</text>
                    <text x="70" y="50" fill="${c.muted}" font-size="10" text-anchor="middle">Gametes ♂</text>

                    <!-- Gametes Parent 2 (Left / Female) -->
                    <text x="85" y="100" fill="${c.green}" font-size="12" font-weight="bold" text-anchor="middle">${p2[0]}</text>
                    <text x="85" y="160" fill="${c.green}" font-size="12" font-weight="bold" text-anchor="middle">${p2[1]}</text>
                    <text x="85" y="190" fill="${c.muted}" font-size="9" text-anchor="middle">Gametes ♀</text>

                    <!-- 2x2 Offspring Grid -->
                    <rect x="115" y="65" width="90" height="60" rx="4" fill="rgba(59, 130, 246, 0.15)" stroke="${c.border}" stroke-width="1.5"/>
                    <text x="160" y="102" fill="${c.text}" font-size="13" font-weight="bold" text-anchor="middle">${c00}</text>

                    <rect x="205" y="65" width="90" height="60" rx="4" fill="rgba(59, 130, 246, 0.1)" stroke="${c.border}" stroke-width="1.5"/>
                    <text x="250" y="102" fill="${c.text}" font-size="13" font-weight="bold" text-anchor="middle">${c01}</text>

                    <rect x="115" y="125" width="90" height="60" rx="4" fill="rgba(59, 130, 246, 0.1)" stroke="${c.border}" stroke-width="1.5"/>
                    <text x="160" y="162" fill="${c.text}" font-size="13" font-weight="bold" text-anchor="middle">${c10}</text>

                    <rect x="205" y="125" width="90" height="60" rx="4" fill="rgba(59, 130, 246, 0.2)" stroke="${c.border}" stroke-width="1.5"/>
                    <text x="250" y="162" fill="${c.text}" font-size="13" font-weight="bold" text-anchor="middle">${c11}</text>

                    ${cfg.show_phenotype && cfg.phenotype ? `<text x="170" y="215" fill="${c.muted}" font-size="10" text-anchor="middle">${cfg.phenotype}</text>` : ''}
                </svg>`;
            },

            /**
             * 12. REDSHIFT / BLUESHIFT SPECTRAL ABSORPTION LINES
             * Config: { shift: 'red'|'blue' }
             */
            red_blue_shift(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 190;
                const isRed = cfg.shift !== 'blue';
                const shiftDx = isRed ? 22 : -22;
                const shiftLabel = isRed ? 'Redshift (Receding Galaxy, λ increases)' : 'Blueshift (Approaching, λ decreases)';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <text x="180" y="20" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">Spectral Lines: ${shiftLabel}</text>
                    
                    <!-- Laboratory Reference Spectrum -->
                    <text x="40" y="42" fill="${c.muted}" font-size="10">Laboratory Standard (Stationary):</text>
                    <rect x="40" y="48" width="280" height="32" rx="4" fill="url(#dtech-spectrum-grad)" stroke="${c.border}" stroke-width="1.5"/>
                    <line x1="90" y1="48" x2="90" y2="80" stroke="#000000" stroke-width="2.5"/>
                    <line x1="150" y1="48" x2="150" y2="80" stroke="#000000" stroke-width="2.5"/>
                    <line x1="215" y1="48" x2="215" y2="80" stroke="#000000" stroke-width="2.5"/>
                    <line x1="270" y1="48" x2="270" y2="80" stroke="#000000" stroke-width="2.5"/>
                    
                    <!-- Observed Star / Galaxy Spectrum -->
                    <text x="40" y="108" fill="${c.muted}" font-size="10">Observed Star/Galaxy Spectrum:</text>
                    <rect x="40" y="114" width="280" height="32" rx="4" fill="url(#dtech-spectrum-grad)" stroke="${c.border}" stroke-width="1.5"/>
                    <line x1="${90 + shiftDx}" y1="114" x2="${90 + shiftDx}" y2="146" stroke="#000000" stroke-width="2.5"/>
                    <line x1="${150 + shiftDx}" y1="114" x2="${150 + shiftDx}" y2="146" stroke="#000000" stroke-width="2.5"/>
                    <line x1="${215 + shiftDx}" y1="114" x2="${215 + shiftDx}" y2="146" stroke="#000000" stroke-width="2.5"/>
                    <line x1="${270 + shiftDx}" y1="114" x2="${270 + shiftDx}" y2="146" stroke="#000000" stroke-width="2.5"/>

                    <!-- Shift Arrow -->
                    <line x1="215" y1="97" x2="${215 + shiftDx}" y2="97" stroke="${isRed ? c.red : c.blue}" stroke-width="2" marker-end="${isRed ? 'url(#dtech-arrow-red)' : 'url(#dtech-arrow-blue)'}"/>
                    
                    <text x="45" y="165" fill="#60a5fa" font-size="10">Blue (400 nm)</text>
                    <text x="315" y="165" fill="#ef4444" font-size="10" text-anchor="end">Red (700 nm)</text>
                    <text x="180" y="180" fill="${isRed ? c.red : c.blue}" font-size="10" font-weight="bold" text-anchor="middle">${isRed ? 'Shifted towards longer wavelength (Red)' : 'Shifted towards shorter wavelength (Blue)'}</text>
                </svg>`;
            },

            /**
             * 13. VERTICAL PROJECTILE MOTION (Velocity-Time Graph)
             * Config: { v0: 20, t_top: 2.04 }
             */
            kinematics_graph(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const v0 = cfg.v0 || 20;
                const tTop = cfg.t_top || (v0 / 9.8).toFixed(1);
                const tTotal = (tTop * 2).toFixed(1);
                const tApexLabel = cfg.show_time_values ? `${tTop} s (Apex)` : 't_apex (v = 0)';
                const tTotalLabel = cfg.show_time_values ? `${tTotal} s` : 't_total';
                const slopeLabel = cfg.show_accel_value ? 'Slope = a = -9.8 m/s²' : 'Slope = a (gravity)';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="45" y1="110" x2="315" y2="110" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="55" y1="195" x2="55" y2="25" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="310" y="102" fill="${c.text}" font-size="11" font-weight="bold">t (s)</text>
                    <text x="65" y="30" fill="${c.text}" font-size="11" font-weight="bold">v (m/s)</text>
                    <text x="45" y="122" fill="${c.muted}" font-size="10">0</text>

                    <!-- Initial velocity +v0 -->
                    <circle cx="55" cy="50" r="3.5" fill="${c.green}"/>
                    <text x="42" y="54" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="end">+${v0}</text>

                    <!-- Velocity-time curve -->
                    <line x1="55" y1="50" x2="265" y2="170" stroke="${c.blue}" stroke-width="2.5"/>

                    <!-- Apex (v = 0) -->
                    <circle cx="160" cy="110" r="4" fill="${c.yellow}"/>
                    <line x1="160" y1="110" x2="160" y2="125" stroke="${c.yellow}" stroke-width="1"/>
                    <text x="160" y="138" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">${tApexLabel}</text>

                    <!-- Return to ground -v0 -->
                    <circle cx="265" cy="170" r="3.5" fill="${c.red}"/>
                    <line x1="265" y1="110" x2="265" y2="170" stroke="${c.muted}" stroke-width="1" stroke-dasharray="2,2"/>
                    <text x="265" y="102" fill="${c.muted}" font-size="10" text-anchor="middle">${tTotalLabel}</text>
                    <text x="42" y="174" fill="${c.red}" font-size="11" font-weight="bold" text-anchor="end">-${v0}</text>
                    <line x1="55" y1="170" x2="265" y2="170" stroke="${c.muted}" stroke-width="1" stroke-dasharray="2,2"/>

                    <text x="210" y="60" fill="${c.cyan}" font-size="10" font-weight="bold">${slopeLabel}</text>
                </svg>`;
            },

            /**
             * 14. TWO CONNECTED BODIES ON HORIZONTAL SURFACE
             * Config: { m1: 3, m2: 5, force: 30 }
             */
            two_body_horizontal(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 180;
                const m1 = cfg.m1 || 3;
                const m2 = cfg.m2 || 5;
                const f = cfg.force || 30;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="25" y1="130" x2="335" y2="130" stroke="${c.text}" stroke-width="2.5"/>
                    <line x1="25" y1="135" x2="335" y2="135" stroke="${c.muted}" stroke-width="1" stroke-dasharray="4,4"/>

                    <!-- Block 1 (Left) -->
                    <rect x="55" y="82" width="55" height="48" rx="4" fill="${c.blue}" stroke="#60a5fa" stroke-width="2"/>
                    <text x="82" y="111" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">${m1} kg</text>

                    <!-- Connecting String with Tension -->
                    <line x1="110" y1="106" x2="180" y2="106" stroke="${c.text}" stroke-width="2.5"/>
                    <line x1="120" y1="106" x2="138" y2="106" stroke="${c.green}" stroke-width="2" marker-end="url(#dtech-arrow-green)"/>
                    <line x1="170" y1="106" x2="152" y2="106" stroke="${c.green}" stroke-width="2" marker-end="url(#dtech-arrow-green)"/>
                    <text x="145" y="98" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">T</text>

                    <!-- Block 2 (Right) -->
                    <rect x="180" y="74" width="65" height="56" rx="4" fill="${c.yellow}" stroke="#fbbf24" stroke-width="2"/>
                    <text x="212" y="107" fill="#000000" font-size="13" font-weight="bold" text-anchor="middle">${m2} kg</text>

                    <!-- Pulling Force -->
                    <line x1="245" y1="102" x2="315" y2="102" stroke="${c.yellow}" stroke-width="3" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="280" y="90" fill="${c.yellow}" font-size="12" font-weight="bold" text-anchor="middle">F = ${f} N</text>

                    <!-- Normal & Weight -->
                    <line x1="82" y1="82" x2="82" y2="45" stroke="${c.green}" stroke-width="2" marker-end="url(#dtech-arrow-green)"/>
                    <line x1="82" y1="130" x2="82" y2="165" stroke="${c.red}" stroke-width="2" marker-end="url(#dtech-arrow-red)"/>
                </svg>`;
            },

            /**
             * 15. COULOMB'S LAW (Point Charges)
             * Config: { q1: '+4 µC', q2: '-2 µC', distance: '0.3 m' }
             */
            coulomb_charges(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 180;
                const q1 = String(cfg.q1 || '+4 µC');
                const q2 = String(cfg.q2 || '-2 µC');
                const dist = cfg.distance || '0.3 m';
                const isAttract = cfg.force_dir !== 'repel' && (!q1.startsWith('+') || !q2.startsWith('+')) && (!q1.startsWith('-') || !q2.startsWith('-'));

                const q1Color = q1.includes('-') ? c.blue : c.red;
                const q2Color = q2.includes('-') ? c.blue : c.red;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <circle cx="80" cy="80" r="24" fill="${q1Color}" opacity="0.2" stroke="${q1Color}" stroke-width="2.5"/>
                    <text x="80" y="86" fill="${c.text}" font-size="14" font-weight="bold" text-anchor="middle">${q1.includes('-') ? '−' : '+'}</text>
                    <text x="80" y="46" fill="${q1Color}" font-size="11" font-weight="bold" text-anchor="middle">q₁ = ${q1}</text>

                    <circle cx="260" cy="80" r="24" fill="${q2Color}" opacity="0.2" stroke="${q2Color}" stroke-width="2.5"/>
                    <text x="260" y="86" fill="${c.text}" font-size="14" font-weight="bold" text-anchor="middle">${q2.includes('-') ? '−' : '+'}</text>
                    <text x="260" y="46" fill="${q2Color}" font-size="11" font-weight="bold" text-anchor="middle">q₂ = ${q2}</text>

                    ${isAttract ? `
                    <line x1="105" y1="80" x2="150" y2="80" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="125" y="72" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">F₁₂</text>
                    <line x1="235" y1="80" x2="190" y2="80" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="215" y="72" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">F₂₁</text>
                    ` : `
                    <line x1="55" y1="80" x2="20" y2="80" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="35" y="72" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">F₁₂</text>
                    <line x1="285" y1="80" x2="320" y2="80" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="305" y="72" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">F₂₁</text>
                    `}

                    <line x1="80" y1="120" x2="260" y2="120" stroke="${c.muted}" stroke-width="1.5" stroke-dasharray="3,3"/>
                    <line x1="80" y1="112" x2="80" y2="128" stroke="${c.muted}" stroke-width="1.5"/>
                    <line x1="260" y1="112" x2="260" y2="128" stroke="${c.muted}" stroke-width="1.5"/>
                    <text x="170" y="140" fill="${c.muted}" font-size="11" font-weight="bold" text-anchor="middle">r = ${dist}</text>
                    <text x="170" y="162" fill="${c.cyan}" font-size="10" text-anchor="middle">Coulomb's Law: F = k|q₁q₂| / r²</text>
                </svg>`;
            },

            /**
             * 16. BATTERY INTERNAL RESISTANCE (V vs I Graph)
             * Config: { emf: 12, r: 1.5 }
             */
            internal_resistance_graph(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const emf = cfg.emf || 12;
                const r = cfg.r || 1.5;
                const emfLabel = cfg.show_emf_value ? `E = ${emf}V` : 'Emf (ε)';
                const slopeLabel = cfg.show_r_value ? `Slope = -r (${r} Ω)` : 'Slope = -r';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="45" y1="180" x2="315" y2="180" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="55" y1="190" x2="55" y2="25" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="310" y="198" fill="${c.text}" font-size="11" font-weight="bold">I (A)</text>
                    <text x="65" y="30" fill="${c.text}" font-size="11" font-weight="bold">V (Volts)</text>

                    <!-- Emf Intercept -->
                    <circle cx="55" cy="45" r="4" fill="${c.yellow}"/>
                    <text x="42" y="49" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="end">${emfLabel}</text>

                    <!-- Terminal Voltage Line -->
                    <line x1="55" y1="45" x2="265" y2="165" stroke="${c.blue}" stroke-width="2.5"/>

                    <!-- Slope / r Indicator -->
                    <polygon points="140,94 200,94 200,128" fill="rgba(59, 130, 246, 0.15)" stroke="${c.muted}" stroke-width="1" stroke-dasharray="2,2"/>
                    <text x="215" y="115" fill="${c.cyan}" font-size="11" font-weight="bold">${slopeLabel}</text>

                    <text x="180" y="45" fill="${c.green}" font-size="11" font-weight="bold">V_load = E - Ir</text>
                </svg>`;
            },

            /**
             * 17. PHOTOELECTRIC EFFECT (Ek vs Frequency Graph)
             * Config: { metal: 'Cesium', f0: '4.8 × 10¹⁴' }
             */
            photoelectric_graph(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const metal = cfg.metal || 'Potassium';
                const f0 = cfg.f0 || '5.5';
                const f0Label = cfg.show_f0_value ? `f₀ (${f0})` : 'f₀ (Threshold)';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="40" y1="140" x2="315" y2="140" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="90" y1="195" x2="90" y2="25" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="310" y="132" fill="${c.text}" font-size="11" font-weight="bold">f (Hz)</text>
                    <text x="100" y="30" fill="${c.text}" font-size="11" font-weight="bold">E_k(max) (J)</text>

                    <!-- Work function -W0 -->
                    <line x1="90" y1="140" x2="90" y2="185" stroke="${c.muted}" stroke-width="1.5" stroke-dasharray="3,3"/>
                    <circle cx="90" cy="185" r="3.5" fill="${c.red}"/>
                    <text x="80" y="188" fill="${c.red}" font-size="11" font-weight="bold" text-anchor="end">-W₀</text>
                    <line x1="90" y1="185" x2="165" y2="140" stroke="${c.muted}" stroke-width="1.5" stroke-dasharray="3,3"/>

                    <!-- Threshold freq f0 -->
                    <circle cx="165" cy="140" r="4" fill="${c.yellow}"/>
                    <text x="165" y="158" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="middle">${f0Label}</text>

                    <!-- Line with slope h -->
                    <line x1="165" y1="140" x2="285" y2="45" stroke="${c.blue}" stroke-width="2.5"/>
                    <text x="240" y="40" fill="${c.cyan}" font-size="11" font-weight="bold">Slope = h (Planck)</text>
                    <text x="240" y="55" fill="${c.muted}" font-size="10">${metal}</text>
                </svg>`;
            },

            /**
             * 18. ACID-BASE TITRATION CURVE
             * Config: { eq_ph: '7.0', eq_vol: 25 }
             */
            titration_curve(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const eqPh = cfg.eq_ph || '7.0';
                const eqVol = cfg.eq_vol || 25;
                const volLabel = cfg.show_eq_values ? `${eqVol} cm³` : 'V_equiv';
                const eqLabel = cfg.show_eq_values ? `Equivalence Pt (pH=${eqPh})` : 'Equivalence Point';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="45" y1="180" x2="315" y2="180" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="55" y1="190" x2="55" y2="20" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="310" y="195" fill="${c.text}" font-size="11" font-weight="bold">V_base (cm³)</text>
                    <text x="65" y="25" fill="${c.text}" font-size="11" font-weight="bold">pH</text>

                    <text x="45" y="183" fill="${c.muted}" font-size="10" text-anchor="end">0</text>
                    <line x1="50" y1="105" x2="55" y2="105" stroke="${c.muted}" stroke-width="1"/>
                    <text x="45" y="108" fill="${c.muted}" font-size="10" text-anchor="end">7</text>
                    <line x1="50" y1="35" x2="55" y2="35" stroke="${c.muted}" stroke-width="1"/>
                    <text x="45" y="38" fill="${c.muted}" font-size="10" text-anchor="end">14</text>
                    <line x1="55" y1="105" x2="300" y2="105" stroke="${c.muted}" stroke-width="1" stroke-dasharray="3,3" opacity="0.5"/>

                    <!-- Sigmoidal Curve -->
                    <path d="M 55 168 C 100 165, 145 155, 165 140 C 172 130, 175 80, 185 70 C 205 55, 250 48, 295 45" fill="none" stroke="${c.green}" stroke-width="2.5"/>

                    <!-- Equivalence Point -->
                    <circle cx="175" cy="105" r="4.5" fill="${c.yellow}"/>
                    <line x1="175" y1="105" x2="175" y2="180" stroke="${c.yellow}" stroke-width="1" stroke-dasharray="2,2"/>
                    <text x="175" y="195" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">${volLabel}</text>
                    <text x="190" y="102" fill="${c.yellow}" font-size="11" font-weight="bold">${eqLabel}</text>
                </svg>`;
            },

            /**
             * 19. ELECTROLYTIC CELL (Electroplating & Refining)
             * Config: { anode: 'Copper (Cu)', cathode: 'Object to plate', electrolyte: 'CuSO₄ (aq)' }
             */
            electrolytic_cell(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 210;
                const anode = cfg.anode || 'Copper (Cu)';
                const cathode = cfg.cathode || 'Object to plate';
                const electrolyte = cfg.electrolyte || 'CuSO₄ (aq)';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <rect x="60" y="75" width="240" height="105" rx="4" fill="rgba(59, 130, 246, 0.15)" stroke="${c.border}" stroke-width="2"/>
                    <text x="180" y="170" fill="${c.blue}" font-size="11" font-weight="bold" text-anchor="middle">${electrolyte}</text>

                    <!-- Anode (+) -->
                    <rect x="95" y="50" width="18" height="95" fill="#d97706" stroke="#f59e0b" stroke-width="1.5"/>
                    <text x="104" y="42" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="middle">Anode (+)</text>
                    <text x="104" y="195" fill="${c.muted}" font-size="10" text-anchor="middle">${anode}</text>

                    <!-- Cathode (-) -->
                    <rect x="245" y="50" width="18" height="95" fill="#94a3b8" stroke="#cbd5e1" stroke-width="1.5"/>
                    <text x="254" y="42" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">Cathode (-)</text>
                    <text x="254" y="195" fill="${c.muted}" font-size="10" text-anchor="middle">${cathode}</text>

                    <!-- Circuit to DC Power -->
                    <line x1="104" y1="50" x2="104" y2="22" stroke="${c.text}" stroke-width="2"/>
                    <line x1="254" y1="50" x2="254" y2="22" stroke="${c.text}" stroke-width="2"/>
                    <line x1="104" y1="22" x2="165" y2="22" stroke="${c.text}" stroke-width="2"/>
                    <line x1="195" y1="22" x2="254" y2="22" stroke="${c.text}" stroke-width="2"/>

                    <line x1="165" y1="12" x2="165" y2="32" stroke="${c.yellow}" stroke-width="3"/>
                    <line x1="173" y1="16" x2="173" y2="28" stroke="${c.text}" stroke-width="4"/>
                    <line x1="187" y1="12" x2="187" y2="32" stroke="${c.yellow}" stroke-width="3"/>
                    <line x1="195" y1="16" x2="195" y2="28" stroke="${c.text}" stroke-width="4"/>
                    <text x="180" y="42" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">DC Power</text>

                    <line x1="135" y1="115" x2="215" y2="115" stroke="${c.cyan}" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#dtech-arrow-main)"/>
                    <text x="175" y="108" fill="${c.cyan}" font-size="10" text-anchor="middle">Cu²⁺ migration</text>
                </svg>`;
            },

            /**
             * 20. HYPERBOLA GRAPH (Asymptotes & Branches)
             * Config: { p: 2, q: 1, title: 'f(x) = 3/(x - 2) + 1' }
             */
            hyperbola_graph(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const p = cfg.p !== undefined ? cfg.p : 2;
                const q = cfg.q !== undefined ? cfg.q : 1;
                const title = cfg.title || `y = a/(x - ${p}) + ${q}`;
                const xLabel = cfg.show_asymptote_values ? `x = ${p}` : 'x = p';
                const yLabel = cfg.show_asymptote_values ? `y = ${q}` : 'y = q';

                const cx = 130;
                const cy = 110;
                const asymX = cx + Math.min(80, Math.max(-80, p * 18));
                const asymY = cy - Math.min(80, Math.max(-80, q * 18));

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="20" y1="${cy}" x2="320" y2="${cy}" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="${cx}" y1="195" x2="${cx}" y2="20" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="315" y="${cy - 8}" fill="${c.text}" font-size="11" font-weight="bold">x</text>
                    <text x="${cx + 8}" y="25" fill="${c.text}" font-size="11" font-weight="bold">y</text>
                    <text x="${cx - 12}" y="${cy + 15}" fill="${c.muted}" font-size="11">0</text>

                    <!-- Asymptotes -->
                    <line x1="${asymX}" y1="20" x2="${asymX}" y2="195" stroke="${c.yellow}" stroke-width="1.5" stroke-dasharray="4,4"/>
                    <text x="${asymX + 4}" y="35" fill="${c.yellow}" font-size="10" font-weight="bold">${xLabel}</text>

                    <line x1="20" y1="${asymY}" x2="320" y2="${asymY}" stroke="${c.yellow}" stroke-width="1.5" stroke-dasharray="4,4"/>
                    <text x="295" y="${asymY - 6}" fill="${c.yellow}" font-size="10" font-weight="bold">${yLabel}</text>

                    <!-- Branches -->
                    <path d="M ${asymX + 12} ${asymY - 65} Q ${asymX + 22} ${asymY - 22} ${asymX + 65} ${asymY - 12}" fill="none" stroke="${c.blue}" stroke-width="2.5"/>
                    <path d="M ${asymX - 12} ${asymY + 65} Q ${asymX - 22} ${asymY + 22} ${asymX - 65} ${asymY + 12}" fill="none" stroke="${c.blue}" stroke-width="2.5"/>

                    <text x="240" y="22" fill="${c.cyan}" font-size="11" font-weight="bold">${title}</text>
                </svg>`;
            },

            /**
             * 21. MENSTRUAL CYCLE (28-Day Hormonal & Uterine Cycle)
             * Config: { highlight_hormone: 'LH'|'FSH'|'Estrogen'|'Progesterone'|'all', highlight_day: 14 }
             */
            menstrual_cycle(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 220;
                const highDay = cfg.highlight_day || 14;
                const highHormone = cfg.highlight_hormone || 'all';
                const dayToX = (d) => 50 + d * 10;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <text x="180" y="18" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">28-Day Menstrual Cycle: Hormones & Endometrium</text>

                    <!-- Phase Bands -->
                    <!-- Menstruation (Days 1-5) -->
                    <rect x="50" y="30" width="50" height="150" fill="rgba(239, 68, 68, 0.12)"/>
                    <text x="75" y="42" fill="${c.red}" font-size="9" font-weight="bold" text-anchor="middle">Menstruation</text>

                    <!-- Follicular Phase (Days 6-13) -->
                    <rect x="100" y="30" width="80" height="150" fill="rgba(59, 130, 246, 0.08)"/>
                    <text x="140" y="42" fill="${c.blue}" font-size="9" font-weight="bold" text-anchor="middle">Follicular Phase</text>

                    <!-- Ovulation Day 14 Line -->
                    <line x1="${dayToX(14)}" y1="30" x2="${dayToX(14)}" y2="180" stroke="${c.yellow}" stroke-width="2" stroke-dasharray="3,3"/>
                    <circle cx="${dayToX(14)}" cy="55" r="4" fill="${c.yellow}"/>
                    <text x="${dayToX(14)}" y="44" fill="${c.yellow}" font-size="9" font-weight="bold" text-anchor="middle">Ovulation (Day 14)</text>

                    <!-- Luteal Phase (Days 15-28) -->
                    <rect x="190" y="30" width="140" height="150" fill="rgba(16, 185, 129, 0.08)"/>
                    <text x="260" y="42" fill="${c.green}" font-size="9" font-weight="bold" text-anchor="middle">Luteal / Secretory Phase</text>

                    <!-- Hormone Curves -->
                    <!-- LH: Sharp surge at Day 14 -->
                    <path d="M 50 115 Q 150 115 180 110 Q 188 60 190 55 Q 192 60 200 110 Q 260 118 330 118" fill="none" stroke="${c.yellow}" stroke-width="${highHormone === 'LH' ? 3.5 : 2}"/>
                    <text x="202" y="65" fill="${c.yellow}" font-size="10" font-weight="bold">LH Surge</text>

                    <!-- FSH: Small bump at Day 14 -->
                    <path d="M 50 100 Q 110 95 180 90 Q 190 75 200 95 Q 260 110 330 110" fill="none" stroke="${c.blue}" stroke-width="${highHormone === 'FSH' ? 3.5 : 1.8}"/>
                    <text x="65" y="94" fill="${c.blue}" font-size="9" font-weight="bold">FSH</text>

                    <!-- Estrogen: Peak Day 12-13, drops, small rise Day 21 -->
                    <path d="M 50 120 Q 120 120 165 75 Q 185 110 210 105 Q 260 92 330 125" fill="none" stroke="${c.green}" stroke-width="${highHormone === 'Estrogen' ? 3.5 : 2}"/>
                    <text x="145" y="70" fill="${c.green}" font-size="9" font-weight="bold">Estrogen</text>

                    <!-- Progesterone: Low until Day 14, peaks Day 21 -->
                    <path d="M 50 128 L 180 128 Q 210 125 250 75 Q 290 85 330 128" fill="none" stroke="${c.red}" stroke-width="${highHormone === 'Progesterone' ? 3.5 : 2.2}"/>
                    <text x="250" y="70" fill="${c.red}" font-size="9" font-weight="bold">Progesterone</text>

                    <!-- Endometrium Thickness Layer -->
                    <path d="M 50 175 Q 75 180 100 180 Q 140 176 190 168 Q 260 156 330 175 L 330 182 L 50 182 Z" fill="rgba(239, 68, 68, 0.25)" stroke="${c.red}" stroke-width="1.5"/>
                    <text x="100" y="176" fill="${c.muted}" font-size="8">Endometrium</text>

                    <!-- Time Axis Days -->
                    <line x1="50" y1="182" x2="330" y2="182" stroke="${c.text}" stroke-width="2"/>
                    <text x="50" y="196" fill="${c.muted}" font-size="9" text-anchor="middle">Day 1</text>
                    <text x="100" y="196" fill="${c.muted}" font-size="9" text-anchor="middle">5</text>
                    <text x="${dayToX(14)}" y="196" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">14</text>
                    <text x="260" y="196" fill="${c.muted}" font-size="9" text-anchor="middle">21</text>
                    <text x="330" y="196" fill="${c.muted}" font-size="9" text-anchor="middle">28</text>
                    <text x="190" y="210" fill="${c.muted}" font-size="10" text-anchor="middle">Time (Days of Cycle)</text>
                </svg>`;
            },

            /**
             * 22. AC/DC GENERATOR & MOTOR (Armature Loop & Commutators)
             * Config: { type: 'ac'|'dc', show_rotation: true, loop_label: 'ABCD' }
             */
            generator_motor(cfg) {
                const c = this.getColors();
                const isDC = cfg.motor_type === 'dc' || cfg.type_engine === 'dc' || cfg.type === 'dc';
                const width = 360;
                const height = 220;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <text x="180" y="20" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">${isDC ? 'DC Motor / Dynamo (Split-Ring Commutator)' : 'AC Generator (Slip Rings)'}</text>

                    <!-- North Magnetic Pole (Red) -->
                    <rect x="25" y="55" width="45" height="90" rx="4" fill="#dc2626" stroke="#ef4444" stroke-width="2"/>
                    <text x="47" y="110" fill="#ffffff" font-size="24" font-weight="bold" text-anchor="middle">N</text>

                    <!-- South Magnetic Pole (Blue) -->
                    <rect x="290" y="55" width="45" height="90" rx="4" fill="#2563eb" stroke="#3b82f6" stroke-width="2"/>
                    <text x="312" y="110" fill="#ffffff" font-size="24" font-weight="bold" text-anchor="middle">S</text>

                    <!-- Magnetic Field Lines (B) -->
                    <line x1="72" y1="75" x2="288" y2="75" stroke="${c.green}" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#dtech-arrow-green)"/>
                    <line x1="72" y1="100" x2="288" y2="100" stroke="${c.green}" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#dtech-arrow-green)"/>
                    <line x1="72" y1="125" x2="288" y2="125" stroke="${c.green}" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#dtech-arrow-green)"/>
                    <text x="180" y="68" fill="${c.green}" font-size="10" font-weight="bold" text-anchor="middle">Magnetic Field (B)</text>

                    <!-- Armature Rectangular Coil (Perspective ABCD) -->
                    <polygon points="120,68 230,80 210,135 100,123" fill="rgba(245, 158, 11, 0.12)" stroke="${c.yellow}" stroke-width="2.5"/>
                    <text x="115" y="64" fill="${c.yellow}" font-size="11" font-weight="bold">A</text>
                    <text x="235" y="78" fill="${c.yellow}" font-size="11" font-weight="bold">B</text>
                    <text x="215" y="148" fill="${c.yellow}" font-size="11" font-weight="bold">C</text>
                    <text x="95" y="135" fill="${c.yellow}" font-size="11" font-weight="bold">D</text>

                    <!-- Central Axle of Rotation -->
                    <line x1="165" y1="40" x2="165" y2="165" stroke="${c.muted}" stroke-width="2" stroke-dasharray="4,4"/>
                    <!-- Rotation Arrow -->
                    <path d="M 152 48 A 15 10 0 1 1 178 48" fill="none" stroke="${c.cyan}" stroke-width="2" marker-end="url(#dtech-arrow-main)"/>
                    <text x="188" y="46" fill="${c.cyan}" font-size="10" font-weight="bold">ω</text>

                    ${isDC ? `
                    <!-- Split-Ring Commutator -->
                    <path d="M 156 160 A 9 9 0 0 1 174 160" fill="none" stroke="${c.yellow}" stroke-width="4"/>
                    <path d="M 156 165 A 9 9 0 0 0 174 165" fill="none" stroke="${c.yellow}" stroke-width="4"/>
                    <text x="220" y="166" fill="${c.yellow}" font-size="10" font-weight="bold">Split-Ring Commutator</text>
                    ` : `
                    <!-- Slip Rings (Two Separate Rings) -->
                    <ellipse cx="165" cy="155" rx="8" ry="4" fill="none" stroke="${c.yellow}" stroke-width="3"/>
                    <ellipse cx="165" cy="165" rx="8" ry="4" fill="none" stroke="${c.yellow}" stroke-width="3"/>
                    <text x="220" y="162" fill="${c.yellow}" font-size="10" font-weight="bold">Slip Rings</text>
                    `}

                    <!-- Carbon Brushes -->
                    <rect x="150" y="152" width="4" height="15" fill="#475569"/>
                    <rect x="176" y="152" width="4" height="15" fill="#475569"/>
                    <text x="110" y="164" fill="${c.muted}" font-size="9">Carbon Brushes</text>

                    <!-- External Circuit with Meter / Resistor -->
                    <path d="M 150 160 L 120 160 L 120 195 L 155 195" fill="none" stroke="${c.text}" stroke-width="1.8"/>
                    <path d="M 180 160 L 210 160 L 210 195 L 175 195" fill="none" stroke="${c.text}" stroke-width="1.8"/>
                    <circle cx="165" cy="195" r="11" fill="${c.bg}" stroke="${c.cyan}" stroke-width="2"/>
                    <text x="165" y="199" fill="${c.cyan}" font-size="10" font-weight="bold" text-anchor="middle">${isDC ? 'DC' : 'G'}</text>
                </svg>`;
            },

            /**
             * 23. AC SINE WAVE VOLTAGE / CURRENT GRAPH
             * Config: { vmax: 311, show_rms: true, title: 'AC Voltage vs Time' }
             */
            ac_wave_graph(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const vmax = cfg.vmax || 311;
                const title = cfg.title || 'AC Voltage vs Time';
                const cy = 110;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="30" y1="${cy}" x2="315" y2="${cy}" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="45" y1="195" x2="45" y2="25" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="310" y="${cy - 8}" fill="${c.text}" font-size="11" font-weight="bold">t (s)</text>
                    <text x="55" y="30" fill="${c.text}" font-size="11" font-weight="bold">V (Volts)</text>
                    <text x="35" y="${cy + 15}" fill="${c.muted}" font-size="10">0</text>

                    <!-- Title -->
                    <text x="210" y="25" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">${title}</text>

                    <!-- Peak Voltage Lines -->
                    <line x1="45" y1="45" x2="110" y2="45" stroke="${c.muted}" stroke-width="1" stroke-dasharray="2,2"/>
                    <text x="40" y="49" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="end">+V_max</text>
                    <circle cx="110" cy="45" r="3.5" fill="${c.yellow}"/>

                    <line x1="45" y1="175" x2="240" y2="175" stroke="${c.muted}" stroke-width="1" stroke-dasharray="2,2"/>
                    <text x="40" y="179" fill="${c.red}" font-size="10" font-weight="bold" text-anchor="end">-V_max</text>
                    <circle cx="240" cy="175" r="3.5" fill="${c.red}"/>

                    <!-- Vrms Reference Line -->
                    <line x1="45" y1="64" x2="290" y2="64" stroke="${c.green}" stroke-width="1.2" stroke-dasharray="3,3"/>
                    <text x="295" y="67" fill="${c.green}" font-size="9" font-weight="bold">V_rms = V_max / √2</text>

                    <!-- Sine Wave Curve -->
                    <path d="M 45 ${cy} C 75 45, 80 45, 110 45 C 140 45, 145 ${cy}, 175 ${cy} C 205 ${cy}, 210 175, 240 175 C 270 175, 275 ${cy}, 305 ${cy}" fill="none" stroke="${c.blue}" stroke-width="2.5"/>

                    <!-- Period T markers -->
                    <text x="175" y="${cy + 15}" fill="${c.muted}" font-size="10" text-anchor="middle">T/2</text>
                    <text x="305" y="${cy + 15}" fill="${c.muted}" font-size="10" text-anchor="middle">T</text>
                </svg>`;
            },

            /**
             * 24. MOMENTUM & IMPULSE (Collisions: Before & After)
             * Config: { m1: 1500, v1: 20, m2: 1000, v2: 0, vf: '?', type: 'inelastic' }
             */
            momentum_collision(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 220;
                const m1 = cfg.m1 || 1500;
                const m2 = cfg.m2 || 1000;
                const v1 = cfg.v1 !== undefined ? cfg.v1 : 20;
                const v2 = cfg.v2 !== undefined ? cfg.v2 : 0;
                const vfLabel = cfg.vf !== undefined ? cfg.vf : 'v_f = ?';
                const isInelastic = cfg.collision_type !== 'elastic' && cfg.type !== 'elastic';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Stage 1: Before Collision -->
                    <text x="25" y="24" fill="${c.cyan}" font-size="11" font-weight="bold">BEFORE COLLISION:</text>
                    <line x1="25" y1="88" x2="335" y2="88" stroke="${c.muted}" stroke-width="2"/>

                    <!-- Trolley 1 -->
                    <rect x="50" y="48" width="55" height="35" rx="3" fill="${c.blue}" stroke="#60a5fa" stroke-width="1.8"/>
                    <circle cx="62" cy="85" r="4" fill="${c.text}"/>
                    <circle cx="92" cy="85" r="4" fill="${c.text}"/>
                    <text x="77" y="70" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">${m1} kg</text>
                    <!-- Velocity arrow 1 -->
                    <line x1="110" y1="65" x2="160" y2="65" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="135" y="56" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">v₁ = ${v1} m/s</text>

                    <!-- Trolley 2 -->
                    <rect x="210" y="48" width="55" height="35" rx="3" fill="${c.green}" stroke="#34d399" stroke-width="1.8"/>
                    <circle cx="222" cy="85" r="4" fill="${c.text}"/>
                    <circle cx="252" cy="85" r="4" fill="${c.text}"/>
                    <text x="237" y="70" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">${m2} kg</text>
                    ${v2 === 0 ? `
                    <text x="237" y="42" fill="${c.muted}" font-size="10" text-anchor="middle">At rest (v₂ = 0)</text>
                    ` : `
                    <line x1="270" y1="65" x2="305" y2="65" stroke="${c.green}" stroke-width="2" marker-end="url(#dtech-arrow-green)"/>
                    <text x="287" y="56" fill="${c.green}" font-size="10" text-anchor="middle">${v2} m/s</text>
                    `}

                    <!-- Divider -->
                    <line x1="25" y1="108" x2="335" y2="108" stroke="${c.border}" stroke-width="1" stroke-dasharray="4,4"/>

                    <!-- Stage 2: After Collision -->
                    <text x="25" y="130" fill="${c.yellow}" font-size="11" font-weight="bold">AFTER COLLISION (${isInelastic ? 'Inelastic: Bodies Stick Together' : 'Elastic: Separate'}):</text>
                    <line x1="25" y1="195" x2="335" y2="195" stroke="${c.muted}" stroke-width="2"/>

                    ${isInelastic ? `
                    <!-- Coupled Trolleys -->
                    <rect x="115" y="155" width="55" height="35" rx="3" fill="${c.blue}" stroke="#60a5fa" stroke-width="1.8"/>
                    <text x="142" y="177" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">${m1} kg</text>
                    <rect x="170" y="155" width="55" height="35" rx="3" fill="${c.green}" stroke="#34d399" stroke-width="1.8"/>
                    <text x="197" y="177" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">${m2} kg</text>
                    <circle cx="127" cy="192" r="4" fill="${c.text}"/>
                    <circle cx="157" cy="192" r="4" fill="${c.text}"/>
                    <circle cx="182" cy="192" r="4" fill="${c.text}"/>
                    <circle cx="212" cy="192" r="4" fill="${c.text}"/>
                    <!-- Combined final velocity -->
                    <line x1="230" y1="172" x2="285" y2="172" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="257" y="162" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="middle">${vfLabel}</text>
                    ` : `
                    <rect x="75" y="155" width="55" height="35" rx="3" fill="${c.blue}" stroke="#60a5fa" stroke-width="1.8"/>
                    <rect x="195" y="155" width="55" height="35" rx="3" fill="${c.green}" stroke="#34d399" stroke-width="1.8"/>
                    <line x1="255" y1="172" x2="295" y2="172" stroke="${c.green}" stroke-width="2" marker-end="url(#dtech-arrow-green)"/>
                    <text x="275" y="162" fill="${c.green}" font-size="10" text-anchor="middle">${vfLabel}</text>
                    `}
                    <text x="180" y="214" fill="${c.cyan}" font-size="10" text-anchor="middle">Conservation of Linear Momentum: Σp_before = Σp_after</text>
                </svg>`;
            },

            /**
             * 25. MAXWELL-BOLTZMANN DISTRIBUTION (Reaction Rates)
             * Config: { compare_temp: true, catalyst: false, ea_label: 'E_a' }
             */
            maxwell_boltzmann(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const hasCatalyst = cfg.catalyst === true;
                const compareT = cfg.compare_temp !== false;
                const eaX = hasCatalyst ? 200 : 230;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="40" y1="185" x2="315" y2="185" stroke="${c.text}" stroke-width="2" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="40" y1="185" x2="40" y2="25" stroke="${c.text}" stroke-width="2" marker-end="url(#dtech-arrow-main)"/>
                    <text x="310" y="198" fill="${c.text}" font-size="10" font-weight="bold">Kinetic Energy</text>
                    <text x="25" y="100" fill="${c.muted}" font-size="10" transform="rotate(-90, 25, 100)" text-anchor="middle">Number of Molecules</text>

                    <!-- Shaded Reaction Zone -->
                    <path d="M ${eaX} 185 Q 260 180 300 185 L 300 185 L ${eaX} 185 Z" fill="rgba(245, 158, 11, 0.25)"/>

                    <!-- Curve 1: Lower Temperature T1 -->
                    <path d="M 40 185 Q 90 35 125 45 Q 165 60 220 150 Q 260 180 300 185" fill="none" stroke="${c.blue}" stroke-width="2.5"/>
                    <text x="125" y="40" fill="${c.blue}" font-size="10" font-weight="bold" text-anchor="middle">T₁ (Lower temp)</text>

                    ${compareT ? `
                    <!-- Curve 2: Higher Temperature T2 -->
                    <path d="M 40 185 Q 110 75 155 80 Q 205 88 245 145 Q 275 175 305 185" fill="none" stroke="${c.red}" stroke-width="2.2" stroke-dasharray="4,2"/>
                    <text x="180" y="95" fill="${c.red}" font-size="10" font-weight="bold">T₂ (Higher temp)</text>
                    ` : ''}

                    <!-- Activation Energy Line Ea -->
                    <line x1="${eaX}" y1="35" x2="${eaX}" y2="185" stroke="${c.yellow}" stroke-width="2" stroke-dasharray="3,3"/>
                    <text x="${eaX}" y="30" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="middle">${cfg.ea_label || 'E_a'}</text>

                    ${hasCatalyst ? `
                    <line x1="240" y1="35" x2="240" y2="185" stroke="${c.muted}" stroke-width="1.5" stroke-dasharray="2,2"/>
                    <text x="240" y="30" fill="${c.muted}" font-size="10" text-anchor="middle">E_a (uncat)</text>
                    <text x="${eaX}" y="45" fill="${c.green}" font-size="9" text-anchor="middle">Catalyzed E_a</text>
                    ` : `
                    <text x="${eaX + 25}" y="140" fill="${c.yellow}" font-size="9">E ≥ E_a</text>
                    `}
                </svg>`;
            },

            /**
             * 26. TRIGONOMETRIC FUNCTION GRAPH
             * Config: { func: 'sin'|'cos', a: 1, k: 1, title: 'f(x) = sin(x)' }
             */
            trig_graph(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const isCos = cfg.func === 'cos';
                const amp = cfg.a !== undefined ? cfg.a : 1;
                const title = cfg.title || (isCos ? `y = ${amp === 1 ? '' : amp}cos(x)` : `y = ${amp === 1 ? '' : amp}sin(x)`);
                const cy = 110;

                const yPeak = cy - 55;
                const yTrough = cy + 55;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="30" y1="${cy}" x2="325" y2="${cy}" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="50" y1="195" x2="50" y2="25" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="320" y="${cy - 8}" fill="${c.text}" font-size="11" font-weight="bold">x</text>
                    <text x="60" y="30" fill="${c.text}" font-size="11" font-weight="bold">y</text>
                    <text x="40" y="${cy + 15}" fill="${c.muted}" font-size="10">0°</text>

                    <!-- Degree Marks on X Axis -->
                    <text x="115" y="${cy + 15}" fill="${c.muted}" font-size="9" text-anchor="middle">90°</text>
                    <text x="180" y="${cy + 15}" fill="${c.muted}" font-size="9" text-anchor="middle">180°</text>
                    <text x="245" y="${cy + 15}" fill="${c.muted}" font-size="9" text-anchor="middle">270°</text>
                    <text x="310" y="${cy + 15}" fill="${c.muted}" font-size="9" text-anchor="middle">360°</text>

                    <!-- Amplitude Markers -->
                    <line x1="45" y1="${yPeak}" x2="55" y2="${yPeak}" stroke="${c.text}" stroke-width="1.5"/>
                    <text x="40" y="${yPeak + 4}" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="end">${amp}</text>
                    <line x1="45" y1="${yTrough}" x2="55" y2="${yTrough}" stroke="${c.text}" stroke-width="1.5"/>
                    <text x="40" y="${yTrough + 4}" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="end">-${amp}</text>

                    <!-- Title -->
                    <text x="220" y="30" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">${title}</text>

                    ${isCos ? `
                    <path d="M 50 ${yPeak} C 85 ${yPeak}, 95 ${cy}, 115 ${cy} C 135 ${cy}, 150 ${yTrough}, 180 ${yTrough} C 210 ${yTrough}, 225 ${cy}, 245 ${cy} C 265 ${cy}, 280 ${yPeak}, 310 ${yPeak}" fill="none" stroke="${c.blue}" stroke-width="2.5"/>
                    <circle cx="50" cy="${yPeak}" r="4" fill="${c.yellow}"/>
                    <circle cx="180" cy="${yTrough}" r="4" fill="${c.yellow}"/>
                    <circle cx="310" cy="${yPeak}" r="4" fill="${c.yellow}"/>
                    ` : `
                    <path d="M 50 ${cy} C 75 ${cy}, 90 ${yPeak}, 115 ${yPeak} C 140 ${yPeak}, 155 ${cy}, 180 ${cy} C 205 ${cy}, 220 ${yTrough}, 245 ${yTrough} C 270 ${yTrough}, 290 ${cy}, 310 ${cy}" fill="none" stroke="${c.blue}" stroke-width="2.5"/>
                    <circle cx="115" cy="${yPeak}" r="4" fill="${c.yellow}"/>
                    <circle cx="245" cy="${yTrough}" r="4" fill="${c.yellow}"/>
                    `}
                </svg>`;
            },

            /**
             * 27. ANALYTICAL GEOMETRY (Line Segments, Angles, Circles)
             * Config: { shape: 'segment'|'circle', p1: 'A(2; 5)', p2: 'B(8; -3)', midpoint: 'M' }
             */
            analytical_geometry(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const isCircle = cfg.shape === 'circle';
                const p1Label = cfg.p1 || 'A(2; 5)';
                const p2Label = cfg.p2 || 'B(8; 1)';
                const midLabel = cfg.midpoint || 'M';

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="25" y1="150" x2="315" y2="150" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <line x1="75" y1="195" x2="75" y2="25" stroke="${c.text}" stroke-width="1.8" marker-end="url(#dtech-arrow-main)"/>
                    <text x="310" y="142" fill="${c.text}" font-size="11" font-weight="bold">x</text>
                    <text x="85" y="30" fill="${c.text}" font-size="11" font-weight="bold">y</text>
                    <text x="63" y="165" fill="${c.muted}" font-size="10">0</text>

                    ${isCircle ? `
                    <!-- Circle centered at (175, 110) -->
                    <circle cx="175" cy="110" r="50" fill="none" stroke="${c.blue}" stroke-width="2.5"/>
                    <circle cx="175" cy="110" r="3.5" fill="${c.yellow}"/>
                    <text x="175" y="100" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">O(0; 0)</text>
                    <!-- Tangent Line at P -->
                    <circle cx="210" cy="75" r="4" fill="${c.red}"/>
                    <text x="220" y="70" fill="${c.red}" font-size="11" font-weight="bold">P(x₁; y₁)</text>
                    <!-- Radius to Tangent -->
                    <line x1="175" y1="110" x2="210" y2="75" stroke="${c.green}" stroke-width="1.8"/>
                    <!-- Tangent Line perpendicular -->
                    <line x1="170" y1="35" x2="250" y2="115" stroke="${c.yellow}" stroke-width="2"/>
                    <text x="245" y="130" fill="${c.yellow}" font-size="10">Tangent Line</text>
                    ` : `
                    <!-- Line Segment AB -->
                    <line x1="105" y1="60" x2="265" y2="140" stroke="${c.blue}" stroke-width="2.5"/>
                    <circle cx="105" cy="60" r="4.5" fill="${c.green}"/>
                    <text x="105" y="48" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">${p1Label}</text>

                    <circle cx="265" cy="140" r="4.5" fill="${c.green}"/>
                    <text x="265" y="130" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">${p2Label}</text>

                    <!-- Midpoint M -->
                    <circle cx="185" cy="100" r="4" fill="${c.yellow}"/>
                    <text x="195" y="94" fill="${c.yellow}" font-size="10" font-weight="bold">${midLabel}</text>

                    <!-- Inclination Angle Theta -->
                    <line x1="105" y1="60" x2="290" y2="60" stroke="${c.muted}" stroke-width="1" stroke-dasharray="3,3"/>
                    <text x="150" y="55" fill="${c.cyan}" font-size="10">Inclination angle θ</text>
                    `}
                </svg>`;
            },

            /**
             * 28. HUMAN EYE ANATOMY (Accommodation & Vision Defect)
             * Config: { show_names: false }
             */
            eye_anatomy(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 220;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <text x="180" y="18" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">Structure of the Human Eye</text>

                    <!-- Eyeball Outer Wall (Sclera) -->
                    <path d="M 100 65 A 85 85 0 1 1 100 155 Q 70 110 100 65" fill="rgba(30, 41, 59, 0.4)" stroke="${c.border}" stroke-width="2.5"/>

                    <!-- Cornea -->
                    <path d="M 100 65 Q 60 110 100 155" fill="none" stroke="${c.cyan}" stroke-width="2.5"/>
                    <text x="65" y="60" fill="${c.cyan}" font-size="10" font-weight="bold">A (Cornea)</text>
                    <line x1="75" y1="65" x2="88" y2="90" stroke="${c.cyan}" stroke-width="1"/>

                    <!-- Iris & Pupil -->
                    <line x1="105" y1="75" x2="115" y2="92" stroke="${c.yellow}" stroke-width="3"/>
                    <line x1="105" y1="145" x2="115" y2="128" stroke="${c.yellow}" stroke-width="3"/>
                    <text x="95" y="168" fill="${c.yellow}" font-size="10" font-weight="bold">B (Iris & Pupil)</text>

                    <!-- Ciliary Body & Suspensory Ligaments -->
                    <circle cx="125" cy="80" r="5" fill="${c.red}"/>
                    <circle cx="125" cy="140" r="5" fill="${c.red}"/>
                    <line x1="125" y1="85" x2="132" y2="95" stroke="${c.muted}" stroke-width="1.5"/>
                    <line x1="125" y1="135" x2="132" y2="125" stroke="${c.muted}" stroke-width="1.5"/>
                    <text x="145" y="68" fill="${c.red}" font-size="10" font-weight="bold">C (Ciliary Body)</text>

                    <!-- Biconvex Lens -->
                    <ellipse cx="134" cy="110" rx="9" ry="18" fill="rgba(59, 130, 246, 0.3)" stroke="${c.blue}" stroke-width="2.2"/>
                    <text x="140" y="138" fill="${c.blue}" font-size="10" font-weight="bold">D (Lens)</text>

                    <!-- Retina -->
                    <path d="M 140 50 A 75 75 0 0 1 245 110 A 75 75 0 0 1 140 170" fill="none" stroke="${c.yellow}" stroke-width="2.5"/>
                    <text x="240" y="55" fill="${c.yellow}" font-size="10" font-weight="bold">E (Retina)</text>

                    <!-- Yellow Spot / Fovea -->
                    <circle cx="250" cy="110" r="4" fill="${c.green}"/>
                    <text x="258" y="108" fill="${c.green}" font-size="9" font-weight="bold">Fovea</text>

                    <!-- Optic Nerve -->
                    <path d="M 235 125 L 295 145 L 295 160 L 230 140" fill="${c.border}" stroke="${c.text}" stroke-width="1.5"/>
                    <text x="300" y="156" fill="${c.text}" font-size="10" font-weight="bold">F (Optic Nerve)</text>
                </svg>`;
            },

            /**
             * 29. HUMAN EAR ANATOMY (Hearing & Balance)
             * Config: { show_names: false }
             */
            ear_anatomy(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 220;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <text x="180" y="18" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">Structure of the Human Ear</text>

                    <!-- Pinna -->
                    <path d="M 55 45 C 25 70, 25 145, 55 170 C 65 180, 75 165, 70 150 C 50 140, 50 80, 70 70 Z" fill="rgba(59, 130, 246, 0.15)" stroke="${c.blue}" stroke-width="2"/>
                    <text x="45" y="40" fill="${c.blue}" font-size="10" font-weight="bold">A (Pinna)</text>

                    <!-- Auditory Canal -->
                    <path d="M 70 95 L 145 95 M 70 120 L 145 120" stroke="${c.text}" stroke-width="2"/>
                    <text x="105" y="90" fill="${c.muted}" font-size="9" text-anchor="middle">Auditory Canal</text>

                    <!-- Tympanum -->
                    <line x1="145" y1="90" x2="152" y2="125" stroke="${c.red}" stroke-width="3"/>
                    <text x="125" y="142" fill="${c.red}" font-size="10" font-weight="bold">B (Tympanum)</text>

                    <!-- Ossicles -->
                    <path d="M 152 105 L 165 100 L 175 105 L 182 108" fill="none" stroke="${c.yellow}" stroke-width="3"/>
                    <text x="175" y="92" fill="${c.yellow}" font-size="10" font-weight="bold" text-anchor="middle">C (Ossicles)</text>

                    <!-- Semicircular Canals -->
                    <circle cx="215" cy="80" r="16" fill="none" stroke="${c.green}" stroke-width="2.5"/>
                    <circle cx="225" cy="72" r="14" fill="none" stroke="${c.green}" stroke-width="2.5"/>
                    <text x="250" y="68" fill="${c.green}" font-size="10" font-weight="bold">D (Semicircular Canals)</text>

                    <!-- Cochlea -->
                    <path d="M 215 110 C 235 110, 245 125, 235 140 C 225 150, 210 145, 210 135 C 210 125, 222 125, 222 132" fill="none" stroke="${c.cyan}" stroke-width="3"/>
                    <text x="255" y="136" fill="${c.cyan}" font-size="10" font-weight="bold">E (Cochlea)</text>

                    <!-- Auditory Nerve -->
                    <line x1="240" y1="125" x2="315" y2="125" stroke="${c.text}" stroke-width="3" stroke-dasharray="4,2"/>
                    <text x="315" y="120" fill="${c.text}" font-size="10" font-weight="bold">Auditory Nerve</text>

                    <!-- Eustachian Tube -->
                    <line x1="175" y1="125" x2="195" y2="175" stroke="${c.muted}" stroke-width="2.5"/>
                    <text x="210" y="180" fill="${c.muted}" font-size="9">Eustachian Tube</text>
                </svg>`;
            },

            /**
             * 30. DNA NUCLEOTIDE & BASE-PAIRING (Phosphate, Sugar, Base)
             * Config: { base1: 'A', base2: 'T', bonds: 2 }
             */
            dna_nucleotide(cfg) {
                const c = this.getColors();
                const width = 340;
                const height = 210;
                const b1 = cfg.base1 || 'Adenine (A)';
                const b2 = cfg.base2 || 'Thymine (T)';
                const bonds = cfg.bonds || 2;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <text x="170" y="20" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">DNA Nucleotide Pair & Hydrogen Bonding</text>

                    <!-- Nucleotide 1 (Left) -->
                    <!-- Phosphate Group (P) -->
                    <circle cx="50" cy="65" r="16" fill="${c.yellow}" stroke="#fbbf24" stroke-width="2"/>
                    <text x="50" y="70" fill="#000000" font-size="12" font-weight="bold" text-anchor="middle">P</text>
                    <text x="50" y="42" fill="${c.yellow}" font-size="9" text-anchor="middle">Phosphate</text>

                    <!-- Deoxyribose Pentose Sugar (S) -->
                    <polygon points="90,85 110,65 130,85 122,112 98,112" fill="${c.blue}" stroke="#60a5fa" stroke-width="2"/>
                    <text x="110" y="94" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">S</text>
                    <line x1="66" y1="65" x2="90" y2="80" stroke="${c.text}" stroke-width="2"/>
                    <text x="110" y="128" fill="${c.blue}" font-size="9" text-anchor="middle">Deoxyribose</text>

                    <!-- Base 1 -->
                    <rect x="130" y="73" width="45" height="26" rx="3" fill="#dc2626" stroke="#ef4444" stroke-width="1.8"/>
                    <text x="152" y="90" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">${b1.charAt(0)}</text>

                    <!-- Hydrogen Bonds in Middle -->
                    ${bonds === 3 ? `
                    <line x1="178" y1="78" x2="198" y2="78" stroke="${c.cyan}" stroke-width="2" stroke-dasharray="3,2"/>
                    <line x1="178" y1="86" x2="198" y2="86" stroke="${c.cyan}" stroke-width="2" stroke-dasharray="3,2"/>
                    <line x1="178" y1="94" x2="198" y2="94" stroke="${c.cyan}" stroke-width="2" stroke-dasharray="3,2"/>
                    <text x="188" y="112" fill="${c.cyan}" font-size="8" text-anchor="middle">3 H-bonds</text>
                    ` : `
                    <line x1="178" y1="81" x2="198" y2="81" stroke="${c.cyan}" stroke-width="2" stroke-dasharray="3,2"/>
                    <line x1="178" y1="91" x2="198" y2="91" stroke="${c.cyan}" stroke-width="2" stroke-dasharray="3,2"/>
                    <text x="188" y="112" fill="${c.cyan}" font-size="8" text-anchor="middle">2 H-bonds</text>
                    `}

                    <!-- Base 2 (Right) -->
                    <rect x="201" y="73" width="45" height="26" rx="3" fill="#16a34a" stroke="#22c55e" stroke-width="1.8"/>
                    <text x="223" y="90" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">${b2.charAt(0)}</text>

                    <!-- Sugar 2 (Right) -->
                    <polygon points="286,85 266,65 246,85 254,112 278,112" fill="${c.blue}" stroke="#60a5fa" stroke-width="2"/>
                    <text x="266" y="94" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">S</text>

                    <!-- Phosphate 2 (Right) -->
                    <circle cx="310" cy="115" r="16" fill="${c.yellow}" stroke="#fbbf24" stroke-width="2"/>
                    <text x="310" y="120" fill="#000000" font-size="12" font-weight="bold" text-anchor="middle">P</text>
                    <line x1="282" y1="105" x2="295" y2="112" stroke="${c.text}" stroke-width="2"/>

                    <!-- Footer Note -->
                    <text x="170" y="180" fill="${c.muted}" font-size="10" text-anchor="middle">Complementary Base Pairing Rule: A = T and G ≡ C</text>
                </svg>`;
            },

            /**
             * 31. REFLEX ARC (Spinal Cord & Neurons)
             * Config: { stimulus: 'Heat/Pinprick', effector: 'Biceps Muscle' }
             */
            reflex_arc(cfg) {
                const c = this.getColors();
                const width = 360;
                const height = 220;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <text x="180" y="18" fill="${c.text}" font-size="12" font-weight="bold" text-anchor="middle">Neural Pathway of a Reflex Arc</text>

                    <!-- Spinal Cord Cross Section -->
                    <rect x="185" y="45" width="145" height="135" rx="20" fill="rgba(51, 65, 85, 0.4)" stroke="${c.border}" stroke-width="2"/>
                    <path d="M 210 80 Q 235 95 245 110 Q 235 125 210 140 Q 225 110 210 80" fill="rgba(148, 163, 184, 0.5)"/>
                    <path d="M 305 80 Q 280 95 270 110 Q 280 125 305 140 Q 290 110 305 80" fill="rgba(148, 163, 184, 0.5)"/>
                    <line x1="245" y1="110" x2="270" y2="110" stroke="rgba(148, 163, 184, 0.5)" stroke-width="6"/>
                    <text x="257" y="64" fill="${c.muted}" font-size="9" text-anchor="middle">Spinal Cord</text>

                    <!-- Interneuron -->
                    <line x1="230" y1="88" x2="230" y2="132" stroke="${c.green}" stroke-width="2.5"/>
                    <circle cx="230" cy="110" r="3.5" fill="${c.green}"/>
                    <text x="255" y="128" fill="${c.green}" font-size="9" font-weight="bold">Interneuron</text>

                    <!-- Receptor -->
                    <rect x="25" y="70" width="35" height="24" rx="4" fill="${c.red}" opacity="0.3" stroke="${c.red}" stroke-width="1.5"/>
                    <text x="42" y="85" fill="${c.red}" font-size="9" font-weight="bold" text-anchor="middle">Receptor</text>

                    <!-- Sensory Neuron -->
                    <path d="M 60 82 Q 130 75 160 70 Q 170 65 185 88 L 228 88" fill="none" stroke="${c.blue}" stroke-width="2" marker-end="url(#dtech-arrow-blue)"/>
                    <circle cx="155" cy="68" r="6" fill="${c.blue}"/>
                    <text x="120" y="60" fill="${c.blue}" font-size="9" font-weight="bold">Sensory Neuron</text>
                    <text x="155" y="52" fill="${c.muted}" font-size="8" text-anchor="middle">Ganglion</text>

                    <!-- Motor Neuron -->
                    <path d="M 228 132 L 185 132 Q 140 145 75 145" fill="none" stroke="${c.yellow}" stroke-width="2" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="125" y="140" fill="${c.yellow}" font-size="9" font-weight="bold">Motor Neuron</text>

                    <!-- Effector -->
                    <ellipse cx="45" cy="145" rx="20" ry="12" fill="${c.green}" opacity="0.4" stroke="${c.green}" stroke-width="1.8"/>
                    <text x="45" y="148" fill="${c.green}" font-size="9" font-weight="bold" text-anchor="middle">Effector</text>

                    <text x="180" y="205" fill="${c.cyan}" font-size="9" text-anchor="middle">Receptor → Sensory Neuron → Interneuron → Motor Neuron → Effector</text>
                </svg>`;
            },

            /**
             * 32. WORK-ENERGY TRACK / ROLLER COASTER (Mechanical Energy Conservation)
             * Config: { h1: 20, h2: 12, mass: 50, track_label: 'Frictionless Track' }
             */
            work_energy_track(cfg) {
                const c = this.getColors();
                const width = 350;
                const height = 210;
                const h1 = cfg.h1 || 20;
                const h2 = cfg.h2 || 12;
                const m = cfg.mass || 50;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <line x1="20" y1="180" x2="330" y2="180" stroke="${c.text}" stroke-width="2"/>
                    <text x="325" y="195" fill="${c.muted}" font-size="10">Ground (h = 0)</text>

                    <!-- Track Curve -->
                    <path d="M 35 50 Q 80 50 120 120 Q 150 180 175 180 Q 210 180 240 130 Q 260 100 280 100 Q 305 100 325 150" fill="none" stroke="${c.blue}" stroke-width="3"/>

                    <!-- Point A (Peak) -->
                    <circle cx="50" cy="50" r="5" fill="${c.yellow}"/>
                    <rect x="42" y="38" width="16" height="12" rx="2" fill="${c.yellow}"/>
                    <text x="50" y="32" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="middle">A (${m} kg)</text>
                    <line x1="50" y1="50" x2="50" y2="180" stroke="${c.yellow}" stroke-width="1.2" stroke-dasharray="3,3"/>
                    <text x="60" y="115" fill="${c.yellow}" font-size="10" font-weight="bold">h₁ = ${h1}m</text>

                    <!-- Point B (Bottom) -->
                    <circle cx="175" cy="180" r="5" fill="${c.green}"/>
                    <text x="175" y="172" fill="${c.green}" font-size="11" font-weight="bold" text-anchor="middle">B (v_max)</text>

                    <!-- Point C (Second Crest) -->
                    <circle cx="280" cy="100" r="5" fill="${c.cyan}"/>
                    <text x="280" y="92" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">C</text>
                    <line x1="280" y1="100" x2="280" y2="180" stroke="${c.cyan}" stroke-width="1.2" stroke-dasharray="3,3"/>
                    <text x="290" y="145" fill="${c.cyan}" font-size="10" font-weight="bold">h₂ = ${h2}m</text>

                    <text x="180" y="20" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">Conservation of Mechanical Energy: E_mech = E_k + E_p</text>
                </svg>`;
            }

        }
    };

    // Attach to global window and module exports
    if (typeof window !== 'undefined') {
        window.DTechDiagrams = DTechDiagrams;
    }
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = DTechDiagrams;
    }
    if (typeof global !== 'undefined') {
        global.DTechDiagrams = DTechDiagrams;
    }
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));
