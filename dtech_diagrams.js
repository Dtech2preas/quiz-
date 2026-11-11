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
             * Config: { fn: true, fg: true, fk: true, fapp: true, angle: 0 }
             */
            free_body(cfg) {
                const c = this.getColors();
                const width = 280;
                const height = 220;
                const cx = 140;
                const cy = 110;

                return `
                <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="dtech-svg">
                    ${this.getDefs()}
                    <!-- Coordinate Axes (Dashed) -->
                    <line x1="30" y1="${cy}" x2="250" y2="${cy}" stroke="${c.border}" stroke-width="1.5" stroke-dasharray="3,3"/>
                    <line x1="${cx}" y1="20" x2="${cx}" y2="200" stroke="${c.border}" stroke-width="1.5" stroke-dasharray="3,3"/>

                    <!-- Central Point of Mass -->
                    <circle cx="${cx}" cy="${cy}" r="6" fill="${c.blue}" stroke="#ffffff" stroke-width="2"/>

                    <!-- Normal Force (Up) -->
                    <line x1="${cx}" y1="${cy}" x2="${cx}" y2="35" stroke="${c.green}" stroke-width="2.5" marker-end="url(#dtech-arrow-green)"/>
                    <text x="${cx + 8}" y="35" fill="${c.green}" font-size="12" font-weight="bold">F_N</text>

                    <!-- Gravity Force (Down) -->
                    <line x1="${cx}" y1="${cy}" x2="${cx}" y2="185" stroke="${c.red}" stroke-width="2.5" marker-end="url(#dtech-arrow-red)"/>
                    <text x="${cx + 8}" y="185" fill="${c.red}" font-size="12" font-weight="bold">F_g (w)</text>

                    <!-- Applied Force (Right) -->
                    <line x1="${cx}" y1="${cy}" x2="225" y2="${cy}" stroke="${c.yellow}" stroke-width="2.5" marker-end="url(#dtech-arrow-yellow)"/>
                    <text x="228" y="${cy - 8}" fill="${c.yellow}" font-size="12" font-weight="bold">F_app</text>

                    <!-- Frictional Force (Left) -->
                    <line x1="${cx}" y1="${cy}" x2="55" y2="${cy}" stroke="${c.cyan}" stroke-width="2.5" marker-end="url(#dtech-arrow-main)"/>
                    <text x="45" y="${cy - 8}" fill="${c.cyan}" font-size="12" font-weight="bold">f_k</text>
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
                    <text x="180" y="29" fill="${c.cyan}" font-size="11" font-weight="bold" text-anchor="middle">${v} V</text>

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
                    <text x="252" y="${(yReact + yProd) / 2 + 4}" fill="${isExo ? c.red : c.green}" font-size="11" font-weight="bold">ΔH ${isExo ? '< 0' : '> 0'}</text>
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
                    <text x="185" y="175" fill="${c.yellow}" font-size="11" font-weight="bold" text-anchor="middle">TP ${tp}</text>

                    <!-- Intercepts -->
                    <circle cx="115" cy="${cy}" r="3.5" fill="${c.green}"/>
                    <circle cx="255" cy="${cy}" r="3.5" fill="${c.green}"/>
                    <circle cx="${cx}" cy="90" r="3.5" fill="${c.red}"/>
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
