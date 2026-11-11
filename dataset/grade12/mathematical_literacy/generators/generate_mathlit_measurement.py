import json
import os
import random
import math
import time

def build_measurement_dataset():
    questions = []
    seen_questions = set()
    
    target_easy = 300
    target_med = 500
    target_hard = 200
    counts = {"easy": 0, "medium": 0, "hard": 0}
    
    def add_q(subtopic, difficulty, q_text, correct_ans, distractors, explanation):
        if counts[difficulty] >= (target_easy if difficulty == "easy" else target_med if difficulty == "medium" else target_hard):
            return False
        if q_text in seen_questions:
            return False
            
        c_str = str(correct_ans).strip()
        clean_dist = []
        seen_d = {c_str}
        for d in distractors:
            d_str = str(d).strip()
            if d_str and d_str not in seen_d:
                seen_d.add(d_str)
                clean_dist.append(d_str)
                
        if len(clean_dist) < 6:
            return False
            
        seen_questions.add(q_text)
        counts[difficulty] += 1
        q_id = f"ML12_P2_MEAS_{len(questions) + 1:04d}"
        
        questions.append({
            "id": q_id,
            "topic": "Measurement",
            "subtopic": subtopic,
            "paper": "paper2",
            "difficulty": difficulty,
            "question": q_text,
            "correct_answer": c_str,
            "wrong_answers_pool": clean_dist[:8],
            "explanation": explanation
        })
        return True

    # -------------------------------------------------------------------------
    # 1. EASY QUESTIONS (Target: 300)
    # -------------------------------------------------------------------------
    conv_lengths = [
        (450, "mm to cm", 45.0, "cm", 10.0, "/"),
        (1250, "mm to m", 1.25, "m", 1000.0, "/"),
        (350, "cm to m", 3.5, "m", 100.0, "/"),
        (4.8, "m to cm", 480.0, "cm", 100.0, "*"),
        (7200, "m to km", 7.2, "km", 1000.0, "/"),
        (14.5, "km to m", 14500.0, "m", 1000.0, "*"),
        (2500, "g to kg", 2.5, "kg", 1000.0, "/"),
        (4.75, "kg to g", 4750.0, "g", 1000.0, "*"),
        (3500, "kg to tonnes", 3.5, "tonnes", 1000.0, "/"),
        (2.8, "tonnes to kg", 2800.0, "kg", 1000.0, "*"),
        (1500, "mℓ to litres", 1.5, "litres", 1000.0, "/"),
        (4.25, "litres to mℓ", 4250.0, "mℓ", 1000.0, "*"),
        (6500, "litres to kℓ", 6.5, "kℓ", 1000.0, "/"),
        (12.0, "kℓ to litres", 12000.0, "litres", 1000.0, "*"),
        (3.5, "m³ to litres", 3500.0, "litres", 1000.0, "*"),
        (8200, "litres to m³", 8.2, "m³", 1000.0, "/")
    ]
    for val, label, ans_val, unit_str, factor, op in conv_lengths:
        for mult in [1, 2, 3, 4, 5, 6, 8, 10, 12]:
            inp = round(val * mult, 2)
            res = round(inp / factor if op == "/" else inp * factor, 2)
            from_u = label.split()[0]
            to_u = label.split()[2]
            q_conv = f"Convert {inp} {from_u} into {to_u}."
            c_conv = f"{res} {unit_str}"
            d_conv = [
                f"{res * 10} {unit_str}",
                f"{res / 10} {unit_str}",
                f"{res * 100} {unit_str}",
                f"{res / 100} {unit_str}",
                f"{round(res * 1.15, 2)} {unit_str}",
                f"{round(res * 0.85, 2)} {unit_str}",
                f"{round(inp, 2)} {unit_str}"
            ]
            exp_conv = f"{inp} {from_u} {'÷' if op == '/' else '×'} {factor} = {res} {unit_str}."
            add_q("Metric Conversions & Temperature", "easy", q_conv, c_conv, d_conv, exp_conv)

    c_temps = [-15, -10, -5, 0, 10, 15, 20, 25, 30, 35, 37, 40, 100, 160, 180, 200, 220]
    for tc in c_temps:
        tf = round((tc * 1.8) + 32, 1)
        q_c2f = f"A recipe specifies a baking temperature of {tc}°C. Convert this temperature to degrees Fahrenheit (°F) using the formula: °F = (°C × 1.8) + 32."
        c_c2f = f"{tf}°F"
        d_c2f = [
            f"{round(tc + 32, 1)}°F",
            f"{round(tc * 1.8, 1)}°F",
            f"{round(tf + 18, 1)}°F",
            f"{round(tf - 18, 1)}°F",
            f"{round(tf * 1.10, 1)}°F",
            f"{round(tf * 0.90, 1)}°F",
            f"{round((tc - 32) / 1.8, 1)}°F"
        ]
        exp_c2f = f"°F = ({tc} × 1.8) + 32 = {tc * 1.8:.1f} + 32 = {tf}°F."
        add_q("Metric Conversions & Temperature", "easy", q_c2f, c_c2f, d_c2f, exp_c2f)

        q_f2c = f"A clinical thermometer imported from the USA displays a body temperature of {tf}°F. Convert this temperature to degrees Celsius (°C) using the formula: °C = (°F - 32) ÷ 1.8."
        c_f2c = f"{tc}°C"
        d_f2c = [
            f"{round(tf - 32, 1)}°C",
            f"{round(tf / 1.8, 1)}°C",
            f"{round(tc + 5, 1)}°C",
            f"{round(tc - 5, 1)}°C",
            f"{round(tc * 1.15, 1)}°C",
            f"{round(tc * 0.85, 1)}°C",
            f"{round(tf * 1.8 + 32, 1)}°C"
        ]
        exp_f2c = f"°C = ({tf} - 32) ÷ 1.8 = {tf - 32:.1f} ÷ 1.8 = {tc}°C."
        add_q("Metric Conversions & Temperature", "easy", q_f2c, c_f2c, d_f2c, exp_f2c)

    # 1c. Circular Perimeter & Area (Easy)
    for radius in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.5]:
        circ = round(2 * 3.142 * radius, 2)
        area_c = round(3.142 * (radius ** 2), 2)
        q_circ = f"A circular flowerbed in a municipal park has a radius of {radius} m. Calculate the circumference (boundary perimeter) of the flowerbed. (Use π ≈ 3.142 and round to 2 decimal places)."
        c_circ = f"{circ} m"
        d_circ = [
            f"{area_c} m",
            f"{round(3.142 * radius, 2)} m",
            f"{round(circ * 1.15, 2)} m",
            f"{round(circ * 0.85, 2)} m",
            f"{round(circ + 3.0, 2)} m",
            f"{round(circ - 3.0, 2)} m",
            f"{round(2 * radius, 2)} m"
        ]
        exp_circ = f"Circumference = 2 × π × r = 2 × 3.142 × {radius} = {circ} m."
        add_q("2D Perimeter & Area of Composite Shapes", "easy", q_circ, c_circ, d_circ, exp_circ)

        q_ac = f"Calculate the surface area of the circular flowerbed having a radius of {radius} m. (Use π ≈ 3.142 and round to 2 decimal places)."
        c_ac = f"{area_c} m²"
        d_ac = [
            f"{circ} m²",
            f"{round(2 * 3.142 * radius, 2)} m²",
            f"{round(area_c * 1.15, 2)} m²",
            f"{round(area_c * 0.85, 2)} m²",
            f"{round(area_c + 5.0, 2)} m²",
            f"{round(area_c - 5.0, 2)} m²",
            f"{round(3.142 * radius, 2)} m²"
        ]
        exp_ac = f"Area = π × r² = 3.142 × ({radius})² = 3.142 × {radius**2:.2f} = {area_c} m²."
        add_q("2D Perimeter & Area of Composite Shapes", "easy", q_ac, c_ac, d_ac, exp_ac)

    # 1d. Triangular Area (Gables)
    for b_tri in [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]:
        for h_tri in [1.8, 2.2, 2.5, 3.0, 3.5]:
            a_tri = round(0.5 * b_tri * h_tri, 2)
            q_tri = f"A triangular roof gable on a residential building has a horizontal base of {b_tri} m and a perpendicular height of {h_tri} m. Calculate the area of the triangular gable."
            c_tri = f"{a_tri} m²"
            d_tri = [
                f"{round(b_tri * h_tri, 2)} m²",
                f"{round(a_tri * 1.20, 2)} m²",
                f"{round(a_tri * 0.80, 2)} m²",
                f"{round(a_tri + 3.5, 2)} m²",
                f"{round(a_tri - 3.5 if a_tri > 4 else a_tri + 1.5, 2)} m²",
                f"{round(b_tri + h_tri, 2)} m²",
                f"{round(a_tri * 2.0, 2)} m²"
            ]
            exp_tri = f"Area = ½ × base × height = 0.5 × {b_tri} × {h_tri} = {a_tri} m²."
            add_q("2D Perimeter & Area of Composite Shapes", "easy", q_tri, c_tri, d_tri, exp_tri)

    
    # Speed, Distance, Time basic calculations (Easy)
    speed_cases = [
        (60, 2.5), (80, 1.5), (100, 3.0), (120, 2.0), (90, 4.0), (70, 3.5),
        (110, 2.5), (85, 2.0), (95, 3.0), (65, 4.0), (105, 1.5), (75, 2.5)
    ]
    for spd, hrs in speed_cases:
        for factor in [0.8, 1.0, 1.2, 1.4]:
            s = round(spd * factor)
            t = round(hrs, 1)
            dist = round(s * t, 1)
            q_spd = f"A delivery vehicle travels at a constant average speed of {s} km/h for {t} hours. Calculate the total distance travelled in kilometres (km). Use formula: Distance = Speed × Time."
            c_spd = f"{dist} km"
            d_spd = [
                f"{round(s / t, 1)} km",
                f"{round(t / s, 1)} km",
                f"{round(dist * 1.15, 1)} km",
                f"{round(dist * 0.85, 1)} km",
                f"{round(dist + 25.0, 1)} km",
                f"{round(dist - 25.0, 1)} km",
                f"{round(s + t, 1)} km"
            ]
            exp_spd = f"Distance = Speed × Time = {s} km/h × {t} hours = {dist} km."
            add_q("Metric Conversions & Temperature", "easy", q_spd, c_spd, d_spd, exp_spd)

    # Everyday South African perimeter and area contexts (Easy)
    rect_contexts = [
        ("school soccer field", 100.0, 64.0),
        ("netball court", 30.5, 15.25),
        ("residential brick paving driveway", 18.0, 3.5),
        ("rooftop solar panel array", 14.0, 6.0),
        ("spaza shop retail floor", 8.5, 5.0),
        ("double garage concrete floor", 6.0, 6.0),
        ("highway billboard advertisement banner", 12.0, 3.0),
        ("hospital clinic emergency ramp", 15.0, 2.5)
    ]
    for r_name, rl, rb in rect_contexts:
        for mult in [0.8, 1.0, 1.2, 1.5]:
            l = round(rl * mult, 1)
            b = round(rb * mult, 1)
            p = round(2 * (l + b), 1)
            a = round(l * b, 1)
            q_p = f"Calculate the boundary perimeter of a {r_name} measuring {l} m in length and {b} m in width."
            c_p = f"{p} m"
            d_p = [
                f"{a} m",
                f"{round(l + b, 1)} m",
                f"{round(p * 1.15, 1)} m",
                f"{round(p * 0.85, 1)} m",
                f"{round(p + 10.0, 1)} m",
                f"{round(p - 10.0, 1)} m",
                f"{round(2 * l, 1)} m"
            ]
            exp_p = f"Perimeter = 2({l} + {b}) = {p} m."
            add_q("2D Perimeter & Area of Composite Shapes", "easy", q_p, c_p, d_p, exp_p)

# -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    cyl_tanks = [
        ("standard household rainwater harvesting tank", 0.90, 2.10),
        ("agricultural irrigation storage tank", 1.20, 2.50),
        ("community clinic emergency water tank", 1.00, 2.20),
        ("commercial food factory mixing vat", 0.75, 1.80),
        ("dairy farm milk holding silo", 1.10, 2.40),
        ("school boarding hostel water tank", 1.25, 2.80),
        ("municipal park watering bowser", 0.85, 2.00),
        ("poultry farm automatic drinker reservoir", 0.95, 2.30),
        ("bakery liquid sugar storage cylinder", 0.80, 1.90),
        ("fire station rapid response buffer tank", 1.30, 3.00)
    ]
    for t_desc, r_base, h_base in cyl_tanks:
        for scale in [0.75, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35, 1.45, 1.55]:
            r = round(r_base * scale, 2)
            h = round(h_base * scale, 2)
            v_m3 = round(3.142 * (r ** 2) * h, 3)
            cap_litres = int(round(v_m3 * 1000))
            sa_curved = round(2 * 3.142 * r * h, 2)
            sa_total = round(2 * 3.142 * (r ** 2) + sa_curved, 2)
            
            q_v = (f"A cylindrical JoJo water tank ({t_desc}) has a radius of {r} m and a height of {h} m. "
                   f"Calculate the volume of the tank in cubic metres (m³). (Use π ≈ 3.142 and round to 3 decimal places).")
            c_v = f"{v_m3} m³"
            d_v = [
                f"{round(3.142 * r * (h ** 2), 3)} m³",
                f"{round(2 * 3.142 * r * h, 3)} m³",
                f"{round(v_m3 * 1.15, 3)} m³",
                f"{round(v_m3 * 0.85, 3)} m³",
                f"{round(v_m3 + 0.5, 3)} m³",
                f"{round(v_m3 - 0.5, 3)} m³",
                f"{round(3.142 * (r ** 2), 3)} m³"
            ]
            exp_v = f"Volume = π × r² × h = 3.142 × ({r})² × {h} = 3.142 × {r**2:.4f} × {h} = {v_m3} m³."
            add_q("Volume & Capacity of Tanks & Prisms", "medium", q_v, c_v, d_v, exp_v)

            q_cap = (f"Using the calculated volume of {v_m3} m³ for the cylindrical water tank ({t_desc}): "
                     f"Calculate the total capacity of the tank in litres (ℓ), knowing that 1 m³ = 1,000 ℓ.")
            c_cap = f"{cap_litres:,} ℓ"
            d_cap = [
                f"{int(cap_litres / 10):,} ℓ",
                f"{int(cap_litres * 10):,} ℓ",
                f"{int(cap_litres * 1.15):,} ℓ",
                f"{int(cap_litres * 0.85):,} ℓ",
                f"{int(cap_litres + 500):,} ℓ",
                f"{int(cap_litres - 500):,} ℓ",
                f"{int(cap_litres / 100):,} ℓ"
            ]
            exp_cap = f"Capacity = Volume in m³ × 1,000 = {v_m3} × 1,000 = {cap_litres:,} ℓ."
            add_q("Volume & Capacity of Tanks & Prisms", "medium", q_cap, c_cap, d_cap, exp_cap)

            q_sa = (f"The exterior of the closed cylindrical water tank ({t_desc}: radius = {r} m, height = {h} m) needs to be coated with UV-protective sealant. "
                    f"Calculate the total exterior surface area of the closed cylinder. Use formula: Total SA = 2πr² + 2πrh. (Use π ≈ 3.142 and round to 2 decimal places).")
            c_sa = f"{sa_total} m²"
            d_sa = [
                f"{sa_curved} m²",
                f"{round(3.142 * (r ** 2) + sa_curved, 2)} m²",
                f"{round(sa_total * 1.15, 2)} m²",
                f"{round(sa_total * 0.85, 2)} m²",
                f"{round(sa_total + 4.5, 2)} m²",
                f"{round(sa_total - 4.5, 2)} m²",
                f"{v_m3} m²"
            ]
            exp_sa = f"Total SA = 2πr² + 2πrh = 2(3.142)({r}²) + 2(3.142)({r})({h}) = {2*3.142*r**2:.2f} + {sa_curved:.2f} = {sa_total} m²."
            add_q("Surface Area of Prisms & Cylinders", "medium", q_sa, c_sa, d_sa, exp_sa)

            # Q4: Filling Time calculation
            flow_rates = [20, 25, 30, 40]
            for fr in flow_rates:
                mins_fill = round(cap_litres / fr, 1)
                hrs_fill = round(mins_fill / 60.0, 1)
                q_fill = (f"The {t_desc} (capacity {cap_litres:,} ℓ) is being filled from a borehole pump at a constant rate of {fr} litres per minute. "
                          f"Calculate the time required to fill the tank from empty to full capacity, in hours and minutes (or rounded to 1 decimal place in hours).")
                c_fill = f"{hrs_fill} hours"
                d_fill = [
                    f"{round(hrs_fill * 1.25, 1)} hours",
                    f"{round(hrs_fill * 0.75, 1)} hours",
                    f"{round(hrs_fill + 2.5, 1)} hours",
                    f"{round(hrs_fill - 2.5 if hrs_fill > 3 else hrs_fill + 1.2, 1)} hours",
                    f"{round(mins_fill / 100.0, 1)} hours",
                    f"{round(cap_litres / 1000.0, 1)} hours",
                    f"{round(hrs_fill * 2.0, 1)} hours"
                ]
                exp_fill = f"Time in minutes = {cap_litres} ℓ ÷ {fr} ℓ/min = {mins_fill} minutes. Time in hours = {mins_fill} ÷ 60 = {hrs_fill} hours."
                add_q("Volume & Capacity of Tanks & Prisms", "medium", q_fill, c_fill, d_fill, exp_fill)

    # 2b. Tiling Calculations
    tiling_rooms = [
        ("lounge and dining area", 6.5, 4.8, 0.50, 0.50, 6, 285.00),
        ("master bedroom and dressing area", 5.2, 4.0, 0.40, 0.40, 8, 240.00),
        ("school science laboratory", 8.4, 6.0, 0.60, 0.60, 4, 320.00),
        ("clinic waiting room floor", 7.2, 5.0, 0.50, 0.50, 6, 290.00),
        ("office reception area", 5.8, 4.5, 0.45, 0.45, 7, 265.00),
        ("community library reading room", 9.0, 6.5, 0.50, 0.50, 6, 295.00),
        ("church vestry hall", 7.5, 5.5, 0.40, 0.40, 8, 250.00),
        ("restaurant kitchen floor", 6.0, 4.5, 0.30, 0.30, 11, 210.00)
    ]
    for r_title, l_room, b_room, l_t, b_t, tiles_per_box, box_price in tiling_rooms:
        for factor in [0.85, 0.95, 1.05, 1.15, 1.25, 1.35]:
            lr = round(l_room * factor, 2)
            br = round(b_room * factor, 2)
            floor_a = round(lr * br, 2)
            tile_a = round(l_t * b_t, 4)
            raw_tiles = math.ceil(floor_a / tile_a)
            tot_tiles_wastage = math.ceil(raw_tiles * 1.10)
            boxes_needed = math.ceil(tot_tiles_wastage / tiles_per_box)
            cost_tiles = round(boxes_needed * box_price, 2)
            
            q_tile1 = (f"A contractor needs to tile a {r_title} with floor dimensions of {lr} m by {br} m. "
                       f"Each square ceramic tile measures {int(l_t*100)} cm by {int(b_t*100)} cm ({l_t} m × {b_t} m). "
                       f"Contract regulations require adding 10% extra tiles for cutting and breakage wastage. "
                       f"Calculate the total number of tiles that must be ordered (rounded up to the next whole tile).")
            c_tile1 = f"{tot_tiles_wastage} tiles"
            d_tile1 = [
                f"{raw_tiles} tiles",
                f"{int(raw_tiles * 1.15)} tiles",
                f"{int(raw_tiles * 1.05)} tiles",
                f"{tot_tiles_wastage + 15} tiles",
                f"{tot_tiles_wastage - 15} tiles",
                f"{boxes_needed} tiles",
                f"{int(floor_a)} tiles"
            ]
            exp_tile1 = (f"Floor Area = {lr} m × {br} m = {floor_a} m². Tile Area = {l_t} m × {b_t} m = {tile_a} m². "
                         f"Raw tiles needed = {floor_a} ÷ {tile_a} = {floor_a / tile_a:.2f} ≈ {raw_tiles} tiles. "
                         f"Adding 10% wastage = {raw_tiles} × 1.10 = {raw_tiles * 1.10:.2f} ≈ {tot_tiles_wastage} tiles.")
            add_q("Tiling Calculations & 10% Wastage", "medium", q_tile1, c_tile1, d_tile1, exp_tile1)

            q_tile2 = (f"Continuing with the {r_title} tiling project (requiring {tot_tiles_wastage} tiles): "
                       f"Tiles are only sold in full boxes of {tiles_per_box} tiles at R{box_price:,.2f} per box. "
                       f"Calculate the total cost to purchase the required boxes of tiles.")
            c_tile2 = f"R{cost_tiles:,.2f}"
            d_tile2 = [
                f"R{round((tot_tiles_wastage / tiles_per_box) * box_price, 2):,.2f}",
                f"R{round(cost_tiles * 1.15, 2):,.2f}",
                f"R{round(cost_tiles * 0.85, 2):,.2f}",
                f"R{round(cost_tiles + box_price, 2):,.2f}",
                f"R{round(cost_tiles - box_price, 2):,.2f}",
                f"R{round(tot_tiles_wastage * box_price, 2):,.2f}",
                f"R{round(boxes_needed * 100, 2):,.2f}"
            ]
            exp_tile2 = (f"Boxes needed = {tot_tiles_wastage} ÷ {tiles_per_box} = {tot_tiles_wastage / tiles_per_box:.2f} ≈ {boxes_needed} full boxes. "
                         f"Total cost = {boxes_needed} boxes × R{box_price:,.2f} = R{cost_tiles:,.2f}.")
            add_q("Tiling Calculations & 10% Wastage", "medium", q_tile2, c_tile2, d_tile2, exp_tile2)

    # 2c. Painting Calculations
    paint_rooms = [
        ("bedroom", 4.5, 3.5, 2.7, 1, 0.9, 2.0, 1, 1.5, 1.2, 8.0, 5, 480.00),
        ("classroom", 8.0, 6.0, 3.0, 1, 1.0, 2.1, 3, 1.8, 1.5, 9.0, 5, 520.00),
        ("clinic consulting room", 5.0, 4.0, 2.8, 1, 0.9, 2.1, 2, 1.2, 1.2, 8.5, 5, 495.00),
        ("community library study room", 7.0, 5.0, 3.0, 1, 1.0, 2.1, 2, 2.0, 1.5, 8.0, 5, 510.00),
        ("police charge office", 6.5, 4.5, 2.9, 1, 1.0, 2.1, 2, 1.6, 1.2, 8.0, 5, 490.00),
        ("staff meeting boardroom", 7.5, 5.5, 3.0, 1, 1.2, 2.1, 3, 2.0, 1.4, 9.0, 5, 530.00)
    ]
    for r_title, l_r, b_r, h_r, nd, dw, dh, nw, ww, wh, spread, can_sz, can_pr in paint_rooms:
        for scale in [0.85, 0.95, 1.05, 1.15, 1.25]:
            l = round(l_r * scale, 2)
            b = round(b_r * scale, 2)
            h = round(h_r, 2)
            gross_wall = round(2 * (l * h) + 2 * (b * h), 2)
            door_a = round(nd * dw * dh, 2)
            win_a = round(nw * ww * wh, 2)
            net_wall = round(gross_wall - door_a - win_a, 2)
            two_coats_a = round(net_wall * 2, 2)
            litres_req = round(two_coats_a / spread, 2)
            cans_needed = math.ceil(litres_req / can_sz)
            cost_paint = round(cans_needed * can_pr, 2)
            
            q_pnt1 = (f"A painter prepares to paint the 4 interior walls of a {r_title} ({l} m long, {b} m wide, {h} m high). "
                      f"The room contains {nd} door ({dw} m × {dh} m) and {nw} window(s) ({ww} m × {wh} m) that will NOT be painted. "
                      f"Calculate the net wall surface area (in m²) that will be painted.")
            c_pnt1 = f"{net_wall} m²"
            d_pnt1 = [
                f"{gross_wall} m²",
                f"{two_coats_a} m²",
                f"{round(gross_wall - door_a, 2)} m²",
                f"{round(net_wall * 1.15, 2)} m²",
                f"{round(net_wall * 0.85, 2)} m²",
                f"{round(net_wall + 6.0, 2)} m²",
                f"{round(net_wall - 6.0, 2)} m²"
            ]
            exp_pnt1 = (f"Gross Wall Area = 2({l} × {h}) + 2({b} × {h}) = {2*l*h:.2f} + {2*b*h:.2f} = {gross_wall} m². "
                        f"Deductions: Doors = {door_a} m², Windows = {win_a} m² (Total = {door_a + win_a:.2f} m²). "
                        f"Net Area = {gross_wall} - {door_a + win_a:.2f} = {net_wall} m².")
            add_q("Painting Calculations & Spread Rates", "medium", q_pnt1, c_pnt1, d_pnt1, exp_pnt1)

            q_pnt2 = (f"Continuing with the {r_title} (Net wall area = {net_wall} m²): "
                      f"Two coats of paint are required. The paint has a spread rate of {spread} m² per litre and is sold in {can_sz}-litre cans at R{can_pr:,.2f} per can. "
                      f"Calculate the total cost to buy the required cans of paint.")
            c_pnt2 = f"R{cost_paint:,.2f}"
            d_pnt2 = [
                f"R{round((litres_req / can_sz) * can_pr, 2):,.2f}",
                f"R{round(cost_paint * 1.20, 2):,.2f}",
                f"R{round(cost_paint * 0.80, 2):,.2f}",
                f"R{round(cost_paint + can_pr, 2):,.2f}",
                f"R{round(cost_paint - can_pr, 2):,.2f}",
                f"R{round(litres_req * can_pr, 2):,.2f}",
                f"R{round(cans_needed * 100, 2):,.2f}"
            ]
            exp_pnt2 = (f"Total painting area for 2 coats = {net_wall} m² × 2 = {two_coats_a} m². "
                        f"Litres needed = {two_coats_a} ÷ {spread} = {litres_req} litres. "
                        f"Number of {can_sz}L cans = {litres_req} ÷ {can_sz} = {litres_req / can_sz:.2f} ≈ {cans_needed} cans. "
                        f"Total Cost = {cans_needed} × R{can_pr:,.2f} = R{cost_paint:,.2f}.")
            add_q("Painting Calculations & Spread Rates", "medium", q_pnt2, c_pnt2, d_pnt2, exp_pnt2)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    # 3a. Packaging Optimization
    pack_items = [
        ("soap bar boxes", 10, 6, 4, "master shipping carton", 60, 40, 30),
        ("cereal boxes", 20, 8, 28, "retail distribution crate", 80, 60, 56),
        ("shoe boxes", 30, 20, 12, "freight container pallet", 120, 100, 120),
        ("canned soup trays", 40, 30, 15, "standard warehouse pallet", 120, 100, 150),
        ("tissue box packs", 24, 12, 10, "export shipping carton", 72, 48, 50),
        ("pharmaceutical medicine packs", 12, 8, 5, "insulated cooler box", 48, 40, 35),
        ("fruit punnets", 18, 12, 8, "ventilated transport crate", 54, 36, 40)
    ]
    for item_name, il, iw, ih, cont_name, cl, cw, ch in pack_items:
        for scale in [0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8]:
            L = int(cl * scale)
            W = int(cw * scale)
            H = int(ch * scale)
            
            n1 = (L // il) * (W // iw) * (H // ih)
            n2 = (L // iw) * (W // il) * (H // ih)
            best_n = max(n1, n2)
            
            vol_item = il * iw * ih
            vol_cont = L * W * H
            used_vol = best_n * vol_item
            wasted_vol = vol_cont - used_vol
            pct_wasted = round((wasted_vol / vol_cont) * 100.0, 1)
            
            q_pack = (f"A packaging engineer needs to pack rectangular {item_name} (dimensions: {il} cm × {iw} cm × {ih} cm) into a {cont_name} (internal dimensions: {L} cm × {W} cm × {H} cm). "
                      f"The boxes must all be packed in the same upright orientation (height along height). "
                      f"Calculate the MAXIMUM number of {item_name} that can fit into the {cont_name}.")
            c_pack = f"{best_n} boxes"
            d_pack = [
                f"{min(n1, n2)} boxes",
                f"{int(vol_cont // vol_item)} boxes",
                f"{best_n + 8} boxes",
                f"{best_n - 8 if best_n > 10 else best_n + 4} boxes",
                f"{int(best_n * 1.15)} boxes",
                f"{int(best_n * 0.85)} boxes",
                f"{int(vol_cont / vol_item * 0.90)} boxes"
            ]
            exp_pack = (f"Orientation 1 (Lengthwise): ({L} ÷ {il}) × ({W} ÷ {iw}) × ({H} ÷ {ih}) = {L // il} × {W // iw} × {H // ih} = {n1} boxes. "
                        f"Orientation 2 (Widthwise): ({L} ÷ {iw}) × ({W} ÷ {il}) × ({H} ÷ {ih}) = {L // iw} × {W // il} × {H // ih} = {n2} boxes. "
                        f"Maximum boxes packed = {best_n} boxes. (Note: Theoretical volume allows {vol_cont // vol_item}, but physical dimensions restrict it to {best_n}).")
            add_q("Packaging & Dimension Optimization", "hard", q_pack, c_pack, d_pack, exp_pack)

            q_wvol = (f"Using the packaging details for the {item_name} packed into the {cont_name} (maximum {best_n} boxes fitted): "
                      f"Calculate the percentage of empty/wasted space remaining inside the {cont_name}. (Round to 1 decimal place).")
            c_wvol = f"{pct_wasted}%"
            d_wvol = [
                f"{round(100 - pct_wasted, 1)}%",
                f"{round(pct_wasted * 1.15, 1)}%",
                f"{round(pct_wasted * 0.85, 1)}%",
                f"{round(pct_wasted + 5.5, 1)}%",
                f"{round(pct_wasted - 5.5 if pct_wasted > 6 else pct_wasted + 2.5, 1)}%",
                f"{round(wasted_vol / 1000.0, 1)}%",
                f"{round(used_vol / 1000.0, 1)}%"
            ]
            exp_wvol = (f"Container Volume = {L} × {W} × {H} = {vol_cont:,} cm³. "
                        f"Used Volume = {best_n} × ({il} × {iw} × {ih}) = {best_n} × {vol_item:,} = {used_vol:,} cm³. "
                        f"Wasted Space = {vol_cont:,} - {used_vol:,} = {wasted_vol:,} cm³. "
                        f"Percentage Wasted = ({wasted_vol:,} ÷ {vol_cont:,}) × 100% = {pct_wasted}%.")
            add_q("Packaging & Dimension Optimization", "hard", q_wvol, c_wvol, d_wvol, exp_wvol)

    # 3b. Body Mass Index (BMI) & Clinical Growth Evaluation
    bmi_profiles = [
        ("Kagiso", 1.78, 62.0),
        ("Lindiwe", 1.62, 74.5),
        ("Bongani", 1.85, 108.0),
        ("Fatima", 1.55, 41.0),
        ("Sipho", 1.72, 88.0),
        ("Nomsa", 1.68, 60.0),
        ("Devan", 1.80, 84.0),
        ("Precious", 1.60, 50.0),
        ("Tshepo", 1.75, 95.0),
        ("Zanele", 1.65, 52.0)
    ]
    for name, h_m, m_kg in bmi_profiles:
        for offset in [-8.0, -5.0, -2.0, 0.0, 3.0, 6.0, 9.0, 12.0]:
            mass = round(m_kg + offset, 1)
            bmi_val = round(mass / (h_m ** 2), 1)
            category = "Underweight (< 18.5)" if bmi_val < 18.5 else "Normal weight (18.5 - 24.9)" if bmi_val <= 24.9 else "Overweight (25.0 - 29.9)" if bmi_val <= 29.9 else "Obese (≥ 30.0)"
            
            q_bmi = (f"{name} has a height of {h_m} m and a body mass of {mass} kg. "
                     f"Calculate {name}'s Body Mass Index (BMI) using the formula: BMI = mass (kg) ÷ [height (m)]² (rounded to 1 decimal place), "
                     f"and identify the correct WHO health category.")
            c_bmi = f"{bmi_val} ({category.split('(')[0].strip()})"
            d_bmi = [
                f"{round(mass / h_m, 1)} (Overweight)",
                f"{round(bmi_val * 1.15, 1)} (Obese)",
                f"{round(bmi_val * 0.85, 1)} (Normal weight)",
                f"{round(bmi_val + 4.0, 1)} (Overweight)",
                f"{round(bmi_val - 4.0, 1)} (Underweight)",
                f"{round(mass / (h_m * 2), 1)} (Underweight)",
                f"{round(bmi_val + 2.0, 1)} (Obese)"
            ]
            exp_bmi = f"BMI = {mass} ÷ ({h_m})² = {mass} ÷ {h_m**2:.4f} = {bmi_val}. Category: {category}."
            add_q("Body Mass Index (BMI) & Growth Monitoring", "hard", q_bmi, c_bmi, d_bmi, exp_bmi)

    # 3c. Sloping Swimming Pool Volume
    pool_scenarios = [
        ("community municipal pool", 25.0, 12.0, 1.0, 2.2),
        ("residential backyard swimming pool", 10.0, 4.5, 1.1, 1.9),
        ("hotel resort recreational pool", 18.0, 8.0, 1.2, 2.4),
        ("school swimming team training pool", 20.0, 10.0, 1.0, 2.0),
        ("fitness centre hydrotherapy pool", 12.0, 6.0, 0.9, 1.6)
    ]
    for p_title, L_p, W_p, d1, d2 in pool_scenarios:
        for scale in [0.75, 0.9, 1.0, 1.15, 1.3, 1.5]:
            l = round(L_p * scale, 1)
            w = round(W_p * scale, 1)
            avg_d = round((d1 + d2) / 2.0, 2)
            vol_p = round(l * w * avg_d, 2)
            
            q_pool = (f"A {p_title} is {l} m long and {w} m wide. The bottom slopes steadily from a shallow end depth of {d1} m to a deep end depth of {d2} m. "
                      f"Calculate the volume of the pool in cubic metres (m³) using the trapezoidal volume formula: V = length × width × [(shallow depth + deep depth) ÷ 2].")
            c_pool = f"{vol_p} m³"
            d_pool = [
                f"{round(l * w * d2, 2)} m³",
                f"{round(l * w * d1, 2)} m³",
                f"{round(vol_p * 1.15, 2)} m³",
                f"{round(vol_p * 0.85, 2)} m³",
                f"{round(vol_p + 25.0, 2)} m³",
                f"{round(vol_p - 25.0, 2)} m³",
                f"{round(l * w * (d1 + d2), 2)} m³"
            ]
            exp_pool = f"Average Depth = ({d1} + {d2}) ÷ 2 = {avg_d} m. Volume = {l} m × {w} m × {avg_d} m = {vol_p} m³."
            add_q("Volume & Capacity of Tanks & Prisms", "hard", q_pool, c_pool, d_pool, exp_pool)

    # 3d. Rainwater Harvesting Catchment & Savings (Hard)
    rain_scenarios = [
        ("suburban pitched corrugated roof", 180, 65, 0.85), # roof_area_m2, rainfall_mm, runoff_coeff
        ("school assembly hall roof", 450, 80, 0.85),
        ("agricultural packing shed roof", 600, 55, 0.80),
        ("community clinic clinic roof", 240, 75, 0.85)
    ]
    for r_desc, roof_a, rain_mm, coeff in rain_scenarios:
        for factor in [0.8, 1.0, 1.2, 1.5]:
            r_area = round(roof_a * factor, 1)
            r_mm = round(rain_mm * factor, 1)
            # Harvested Litres = Roof Area (m2) * Rainfall (mm) * Runoff coefficient
            harvested_l = round(r_area * r_mm * coeff, 1)
            m3_val = round(harvested_l / 1000.0, 2)
            
            q_rain = (f"A rainwater harvesting calculation is carried out for a {r_desc} with a catchment area of {r_area} m². "
                      f"During a storm event, {r_mm} mm of rainfall is recorded. The roof material has a runoff efficiency coefficient of {coeff}. "
                      f"Calculate the total volume of rainwater harvested into storage tanks, in litres (ℓ). Use formula: Litres = Area (m²) × Rainfall (mm) × Runoff coefficient.")
            c_rain = f"{harvested_l:,.1f} ℓ"
            d_rain = [
                f"{round(r_area * r_mm, 1):,.1f} ℓ",
                f"{m3_val:,.1f} ℓ",
                f"{round(harvested_l * 1.15, 1):,.1f} ℓ",
                f"{round(harvested_l * 0.85, 1):,.1f} ℓ",
                f"{round(harvested_l + 1200, 1):,.1f} ℓ",
                f"{round(harvested_l - 1200, 1):,.1f} ℓ",
                f"{round(harvested_l / 10.0, 1):,.1f} ℓ"
            ]
            exp_rain = f"Harvested Litres = {r_area} m² × {r_mm} mm × {coeff} = {harvested_l:,.1f} ℓ."
            add_q("Volume & Capacity of Tanks & Prisms", "hard", q_rain, c_rain, d_rain, exp_rain)

    print(f"Generated Measurement: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/mathematical_literacy"
    out_file = os.path.join(out_dir, "paper2_mathlit12_measurement.json")
    dataset = build_measurement_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
