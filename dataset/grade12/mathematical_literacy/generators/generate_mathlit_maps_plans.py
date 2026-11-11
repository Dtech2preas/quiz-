import json
import os
import random
import math
import time

def build_maps_plans_dataset():
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
        q_id = f"ML12_P2_MAPS_{len(questions) + 1:04d}"
        
        questions.append({
            "id": q_id,
            "topic": "Maps, Plans and Representations",
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
    map_terms = [
        ("Number scale (Ratio scale)", "A scale expressed as a numerical ratio (e.g. 1 : 50 000), where one unit on the map represents that same number of units in reality.",
         ["A graphic bar scale drawn at the bottom corner of a map.", "A compass rose indicating magnetic north variations.", "An alphanumeric grid reference identifying towns on a road atlas.", "The ratio of contour line intervals on a topographic map.", "The conversion factor between degrees Celsius and degrees Fahrenheit.", "The percentage discount applied to municipal electricity tariffs."]),
        ("Bar scale (Graphic scale)", "A line or bar divided into segments that physically show the equivalent ground distances corresponding to ruler measurements.",
         ["A ratio scale written strictly in the form 1 : x.", "A table displaying travel times between national highway toll plazas.", "A diagram illustrating the swing direction of an exterior security gate.", "A chart showing the elevation profile of a mountain hiking trail.", "An architectural drawing showing the roof pitch angle.", "A schedule showing window glass specifications."]),
        ("Advantage of a bar scale", "The bar scale remains mathematically accurate and valid even when a plan is enlarged, reduced, or photocopied, because the scale line resizes proportionally with the image.",
         ["It requires no ruler measurements to determine distances.", "It displays the exact GPS latitude and longitude coordinates.", "It can only be used on maps with a scale larger than 1 : 10 000.", "It eliminates the need for calculating fuel consumption.", "It shows the compass bearing toward true north automatically.", "It is exclusively approved for building plans submitted to municipalities."]),
        ("Floor plan", "A scaled 2D orthographic drawing showing a view from above (bird's-eye view) of the rooms, walls, doors, and windows of a building as if sliced horizontally.",
         ["A scaled drawing showing the vertical side view of a building from the outside.", "A 3D perspective artistic rendering of furniture in a room.", "A technical diagram showing the plumbing drainage gradient underground.", "A map displaying the national highway network and toll gates.", "An engineering drawing of the foundation concrete reinforcement mesh.", "A land surveyor's cadastral boundary diagram."]),
        ("Elevation plan", "A scaled 2D drawing showing the exterior vertical facade or side view of a building (e.g. North, South, East, or West elevation).",
         ["A horizontal top view showing the layout of interior rooms.", "A cross-sectional view cutting through the foundation slab.", "A site plan displaying municipal boundary setbacks and building lines.", "A contour map depicting topographical slope gradients.", "A detailed exploded diagram showing furniture assembly.", "A schematic diagram of domestic electrical wiring circuits."]),
        ("North-facing orientation in South Africa", "In the Southern Hemisphere, North-facing rooms receive the maximum amount of direct sunlight and natural warmth throughout the year, especially during winter.",
         ["North-facing rooms remain permanently shaded and coldest during winter months.", "North-facing rooms only receive sunlight at sunrise in the morning.", "North-facing rooms receive the most rain during coastal winter storms.", "North-facing rooms must always have smaller window openings to comply with building regulations.", "North-facing rooms face away from the equator in South Africa.", "North-facing rooms require 50% more heating in winter than South-facing rooms."])
    ]
    for term, c_def, w_defs in map_terms:
        q = f"In Mathematical Literacy maps and plans, define or explain '{term}'."
        add_q("Scale Concepts (Number Scale vs Bar Scale)", "easy", q, c_def, w_defs, f"Official CAPS concept: {term}: {c_def}")

    symbols = [
        ("an arc connected to a straight line perpendicular to an opening in a wall", "A single interior swing door showing the direction of swing", ["A double sliding patio door", "A casement window with sill", "A built-in cupboard with folding doors", "A staircase with handrail", "An electrical distribution board", "A municipal sewer inspection eye"]),
        ("two parallel thin lines set inside a thicker exterior wall boundary", "A standard glazed window", ["A solid structural brick column", "A cavity wall insulation barrier", "A sliding shower screen", "A kitchen double-sink drainage board", "A water closet cistern", "A timber ceiling beam"]),
        ("a square with an X drawn through it on an architectural plan", "An open void, double-volume space, or vertical service shaft duct", ["A reinforced concrete column", "A built-in electrical stove", "A hot water geyser cylinder", "A bathroom shower cubicle", "A master bedroom walk-in closet", "A refuse bin storage area"]),
        ("a circle with two parallel lines projecting outwards on an electrical plan", "A standard 16A double electrical wall socket outlet", ["A ceiling mounted incandescent light fitting", "A single-pole wall light switch", "A television aerial antenna point", "A telephone data outlet socket", "A solar inverter control unit", "An earth leakage circuit breaker"]),
        ("a triangle inside a circle on an electrical layout", "A telephone or high-speed data network point", ["A fluorescent tube light fitting", "A single convenience outlet", "A ceiling smoke detector sensor", "A geyser isolating switch", "A municipal water meter", "A prepaid electricity meter"]),
        ("a circle with a cross (X) inside it on a ceiling lighting plan", "A ceiling-mounted lighting point (luminaire)", ["An extractor fan ventilation duct", "A wall bracket spotlight", "A distribution fuse board", "A two-way light switch", "A TV antenna wall jack", "A panic button sensor"])
    ]
    for desc, c_sym, w_syms in symbols:
        q = f"On a South African SANS-compliant building plan, what does {desc} represent?"
        add_q("Floor Plans & Room Dimensions", "easy", q, c_sym, w_syms, f"Architectural convention: {desc} represents {c_sym}.")

    # Direct scale conversions across multiple scales (Easy)
    scale_benchmarks = [
        ("1 : 20", 20, 0.2),
        ("1 : 25", 25, 0.25),
        ("1 : 50", 50, 0.5),
        ("1 : 75", 75, 0.75),
        ("1 : 100", 100, 1.0),
        ("1 : 150", 150, 1.5),
        ("1 : 200", 200, 2.0),
        ("1 : 250", 250, 2.5),
        ("1 : 500", 500, 5.0),
        ("1 : 1 000", 1000, 10.0),
        ("1 : 2 500", 2500, 25.0),
        ("1 : 5 000", 5000, 50.0)
    ]
    for sc_label, sc_val, m_per_cm in scale_benchmarks:
        for cm_len in [2.0, 3.5, 4.0, 5.0, 6.5, 8.0, 10.0, 12.5, 15.0, 18.0]:
            real_m = round(cm_len * m_per_cm, 2)
            q_sc = f"On a building plan with a scale of {sc_label}, a measurement on paper is {cm_len} cm. Calculate the actual ground distance in metres (m)."
            c_sc = f"{real_m} m"
            d_sc = [
                f"{real_m * 10} m",
                f"{real_m / 10} m",
                f"{round(real_m * 1.15, 2)} m",
                f"{round(real_m * 0.85, 2)} m",
                f"{round(real_m + 3.0, 2)} m",
                f"{round(real_m - 3.0 if real_m > 4 else real_m + 1.5, 2)} m",
                f"{round(cm_len * sc_val, 1)} m"
            ]
            exp_sc = f"Actual metres = {cm_len} cm × {m_per_cm} m/cm = {real_m} m."
            add_q("Calculating Real Distances & Map Dimensions", "easy", q_sc, c_sc, d_sc, exp_sc)

    # Relative Compass Bearings between SA Towns (Easy)
    sa_town_relations = [
        ("Polokwane", "Pretoria", "North (N)", ["South (S)", "East (E)", "West (W)", "North-West (NW)", "South-East (SE)", "South-West (SW)"]),
        ("Pretoria", "Johannesburg", "North (N)", ["South (S)", "East (E)", "West (W)", "North-East (NE)", "South-East (SE)", "South-West (SW)"]),
        ("Durban", "Johannesburg", "South-East (SE)", ["North-West (NW)", "North-East (NE)", "South-West (SW)", "South (S)", "East (E)", "West (W)"]),
        ("Cape Town", "Bloemfontein", "South-West (SW)", ["North-East (NE)", "North-West (NW)", "South-East (SE)", "South (S)", "West (W)", "East (E)"]),
        ("Nelspruit (Mbombela)", "Pretoria", "East (E)", ["West (W)", "North (N)", "South (S)", "North-East (NE)", "South-East (SE)", "South-West (SW)"]),
        ("Kimberley", "Bloemfontein", "West (W)", ["East (E)", "North (N)", "South (S)", "North-West (NW)", "South-West (SW)", "South-East (SE)"]),
        ("Gqeberha (Port Elizabeth)", "East London", "South-West (SW)", ["North-East (NE)", "North-West (NW)", "South-East (SE)", "East (E)", "West (W)", "North (N)"]),
        ("Rustenburg", "Pretoria", "West (W)", ["East (E)", "North (N)", "South (S)", "North-West (NW)", "North-East (NE)", "South-East (SE)"]),
        ("Upington", "Kimberley", "West (W)", ["East (E)", "North (N)", "South (S)", "South-West (SW)", "North-West (NW)", "South-East (SE)"]),
        ("Mthatha", "Durban", "South-West (SW)", ["North-East (NE)", "North-West (NW)", "South-East (SE)", "North (N)", "South (S)", "East (E)"]),
        ("Mahikeng", "Johannesburg", "West (W)", ["East (E)", "South (S)", "North (N)", "South-East (SE)", "North-East (NE)", "South-West (SW)"]),
        ("Musina", "Polokwane", "North (N)", ["South (S)", "East (E)", "West (W)", "North-West (NW)", "North-East (NE)", "South-East (SE)"])
    ]
    for from_city, to_city, c_dir, w_dirs in sa_town_relations:
        q_rel = f"When consulting a map of South Africa, in which general compass direction does {from_city} lie relative to {to_city}?"
        add_q("Elevations & Compass Bearings", "easy", q_rel, c_dir, w_dirs, f"Geographical orientation: {from_city} lies {c_dir} of {to_city}.")

    
    # Additional Compass and Map Conversions (Easy)
    for sc_name, sc_ratio, sc_factor in [('1 : 20', 20, 0.2), ('1 : 25', 25, 0.25), ('1 : 40', 40, 0.4), ('1 : 80', 80, 0.8), ('1 : 125', 125, 1.25), ('1 : 250', 250, 2.5), ('1 : 400', 400, 4.0), ('1 : 800', 800, 8.0), ('1 : 30', 30, 0.3), ('1 : 60', 60, 0.6), ('1 : 120', 120, 1.2), ('1 : 300', 300, 3.0), ('1 : 600', 600, 6.0), ('1 : 35', 35, 0.35), ('1 : 90', 90, 0.9)]:
        for mm_len in [25, 40, 50, 60, 75, 80, 100, 120, 150, 180, 200, 250]:
            cm_len = mm_len / 10.0
            real_m = round(cm_len * sc_factor, 2)
            q_mm = f"On a technical detail drawing drawn to a scale of {sc_name}, a component measures {mm_len} mm ({cm_len} cm). Calculate the actual length in metres (m)."
            c_mm = f"{real_m} m"
            d_mm = [
                f"{real_m * 10} m",
                f"{real_m / 10} m",
                f"{round(real_m * 1.15, 2)} m",
                f"{round(real_m * 0.85, 2)} m",
                f"{round(real_m + 1.2, 2)} m",
                f"{round(real_m - 1.2 if real_m > 1.5 else real_m + 0.6, 2)} m",
                f"{round(mm_len * sc_factor, 1)} m"
            ]
            exp_mm = f"Real length = {cm_len} cm × {sc_factor} m/cm = {real_m} m."
            add_q("Calculating Real Distances & Map Dimensions", "easy", q_mm, c_mm, d_mm, exp_mm)

    # -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    map_distances_cm = [
        2.5, 3.2, 3.8, 4.4, 5.0, 5.6, 6.2, 6.8, 7.4, 8.0, 8.6, 9.2, 10.0, 10.8, 11.5, 12.4, 13.2, 14.0, 15.2, 16.5, 17.8, 19.0, 20.5, 22.4, 24.0
    ]
    sa_landmarks = [
        ("a secondary school and a community clinic", "topographical map sheet"),
        ("a municipal water reservoir and a police station", "district 1 : 50 000 map"),
        ("a regional grain silo and a rail freight junction", "provincial infrastructure map"),
        ("a nature reserve entrance gate and a game ranger outpost", "wildlife sanctuary map"),
        ("a river bridge weir and a mountain radio telemetry tower", "surveyor topographical sheet"),
        ("a rural police station and a magistrate court building", "local municipality map"),
        ("a sports stadium complex and a municipal bus terminus", "urban spatial development plan"),
        ("a forestry lookout tower and a fire break boundary", "provincial forestry map"),
        ("a solar energy power plant and a municipal sub-station", "energy development atlas"),
        ("a coastal lighthouse and a commercial harbour pier", "marine navigation chart")
    ]
    for lm_desc, map_kind in sa_landmarks:
        for m_cm in map_distances_cm:
            act_km = round(m_cm * 0.5, 2)
            act_m = int(act_km * 1000)
            
            q_topo1 = (f"On a South African 1 : 50 000 topographical map ({map_kind}), "
                       f"the straight-line distance measured with a ruler between {lm_desc} is {m_cm} cm. "
                       f"Calculate the actual ground distance between the two locations in kilometres (km).")
            c_topo1 = f"{act_km} km"
            d_topo1 = [
                f"{round(m_cm * 5.0, 2)} km",
                f"{round(m_cm * 0.05, 2)} km",
                f"{round(act_km * 1.15, 2)} km",
                f"{round(act_km * 0.85, 2)} km",
                f"{round(act_km + 1.5, 2)} km",
                f"{round(act_km - 1.5 if act_km > 2 else act_km + 0.8, 2)} km",
                f"{m_cm} km"
            ]
            exp_topo1 = (f"Actual distance = Map distance × Scale = {m_cm} cm × 50 000 = {m_cm * 50000:,.0f} cm. "
                         f"Converting to km: {m_cm * 50000:,.0f} cm ÷ 100 000 = {act_km} km.")
            add_q("Calculating Real Distances & Map Dimensions", "medium", q_topo1, c_topo1, d_topo1, exp_topo1)

            q_topo2 = (f"Two agricultural depots situated along a provincial feeder road are actually {act_km} km apart. "
                       f"Determine how many centimetres (cm) apart these depots will appear when plotted on a 1 : 50 000 map sheet.")
            c_topo2 = f"{m_cm} cm"
            d_topo2 = [
                f"{round(act_km * 5.0, 1)} cm",
                f"{round(act_km / 5.0, 1)} cm",
                f"{round(m_cm * 1.15, 1)} cm",
                f"{round(m_cm * 0.85, 1)} cm",
                f"{round(m_cm + 2.0, 1)} cm",
                f"{round(m_cm - 2.0 if m_cm > 3 else m_cm + 1.0, 1)} cm",
                f"{act_km} cm"
            ]
            exp_topo2 = (f"Actual distance in cm = {act_km} km × 100 000 = {act_km * 100000:,.0f} cm. "
                         f"Map distance = Actual cm ÷ 50 000 = {act_km * 100000:,.0f} ÷ 50 000 = {m_cm} cm.")
            add_q("Calculating Real Distances & Map Dimensions", "medium", q_topo2, c_topo2, d_topo2, exp_topo2)

    # Walking travel times on street maps (Medium)
    walk_cases = [
        ("commuter train station to a high school", 1.8),
        ("taxi rank to a municipal civic clinic", 2.4),
        ("shopping centre to a community sports ground", 3.2),
        ("residential township zone to an industrial park", 4.0),
        ("provincial hospital to a central post office", 1.5)
    ]
    for w_desc, km_dist in walk_cases:
        for mult in [0.75, 1.0, 1.25, 1.5, 2.0]:
            dist = round(km_dist * mult, 2)
            walk_speed = 5.0 # km/h
            walk_hours = round(dist / walk_speed, 2)
            walk_mins = int(round(walk_hours * 60))
            q_walk = (f"A commuter walks from the {w_desc} along a pedestrian pathway (actual route distance: {dist} km). "
                      f"Assuming a brisk average walking speed of 5 km/h, calculate the walking travel time in minutes.")
            c_walk = f"{walk_mins} minutes"
            d_walk = [
                f"{int(walk_hours * 100)} minutes",
                f"{walk_mins + 12} minutes",
                f"{walk_mins - 12 if walk_mins > 15 else walk_mins + 6} minutes",
                f"{int(dist * 10)} minutes",
                f"{int(walk_mins * 1.25)} minutes",
                f"{int(walk_mins * 0.75)} minutes",
                f"{int(dist * 60)} minutes"
            ]
            exp_walk = f"Time in hours = Distance ÷ Speed = {dist} km ÷ 5 km/h = {walk_hours} hours. In minutes = {walk_hours} × 60 = {walk_mins} minutes."
            add_q("Strip Maps & Travel Planning", "medium", q_walk, c_walk, d_walk, exp_walk)

    # Architectural floor plan rooms and area calculations (Medium)
    plan_rooms = [
        ("principal's executive office suite", 100, 6.5, 4.5),
        ("school multi-media computer laboratory", 100, 9.0, 6.0),
        ("community healthcare maternity ward", 100, 8.2, 5.4),
        ("municipal library digital resource center", 100, 7.0, 5.0),
        ("master bedroom with en-suite bathroom", 50, 10.4, 8.0),
        ("open plan commercial bakery kitchen", 50, 9.2, 7.0),
        ("secondary school science physical laboratory", 100, 10.0, 7.5),
        ("community police station holding facility", 50, 8.0, 5.5),
        ("post office customer parcels hall", 100, 8.5, 6.2),
        ("vocational training automotive workshop", 100, 12.0, 8.0)
    ]
    for r_title, sc_factor, pl_l, pl_b in plan_rooms:
        for scale in [0.70, 0.75, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35, 1.45]:
            cl = round(pl_l * scale, 1)
            cb = round(pl_b * scale, 1)
            real_l_m = round(cl * (sc_factor / 100.0), 2)
            real_b_m = round(cb * (sc_factor / 100.0), 2)
            real_area_m2 = round(real_l_m * real_b_m, 2)
            real_perim_m = round(2 * (real_l_m + real_b_m), 2)
            
            q_fa = (f"On an architectural working plan drawn to a scale of 1 : {sc_factor}, a {r_title} has plan dimensions of {cl} cm in length and {cb} cm in width. "
                    f"Calculate the actual floor area of the {r_title} in square metres (m²).")
            c_fa = f"{real_area_m2} m²"
            d_fa = [
                f"{real_perim_m} m²",
                f"{round(cl * cb, 2)} m²",
                f"{round(real_area_m2 * 1.15, 2)} m²",
                f"{round(real_area_m2 * 0.85, 2)} m²",
                f"{round(real_area_m2 + 6.0, 2)} m²",
                f"{round(real_area_m2 - 6.0, 2)} m²",
                f"{round(real_l_m + real_b_m, 2)} m²"
            ]
            exp_fa = (f"Real Length = {cl} cm × {sc_factor} ÷ 100 = {real_l_m} m. "
                      f"Real Width = {cb} cm × {sc_factor} ÷ 100 = {real_b_m} m. "
                      f"Actual Floor Area = {real_l_m} m × {real_b_m} m = {real_area_m2} m².")
            add_q("Floor Plans & Room Dimensions", "medium", q_fa, c_fa, d_fa, exp_fa)

    
    # Seating plan calculations (Medium)
    seating_venues = [
        ("Johannesburg Civic Theatre Main Auditorium", 28, 32, 180.00),
        ("Cape Town International Convention Centre Hall", 35, 40, 250.00),
        ("Durban Playhouse Opera Theatre", 25, 30, 150.00),
        ("Bloemfontein Sand du Plessis Theatre", 22, 28, 160.00),
        ("Pretoria State Theatre Drama Stage", 26, 30, 175.00),
        ("Gqeberha Opera House", 20, 25, 140.00),
        ("Polokwane Community Civic Centre", 18, 24, 120.00), ("FNB Stadium Executive Business Lounge", 15, 20, 450.00), ("Kings Park Stadium Corporate Pavilion", 16, 25, 380.00), ("DHL Stadium Seated Suites", 18, 22, 420.00), ("Loftus Versfeld Presidential Suite", 14, 18, 480.00), ("Mangaung Civic Hall", 20, 30, 110.00)
    ]
    for v_name, num_rows, seats_per_row, ticket_p in seating_venues:
        for scale in [0.8, 0.9, 1.0, 1.1, 1.2]:
            nr = int(round(num_rows * scale))
            sr = int(round(seats_per_row * scale))
            tot_seats = nr * sr
            tot_revenue = round(tot_seats * ticket_p, 2)
            
            q_seat = (f"A seating plan for the {v_name} consists of {nr} rows (labeled Row A to Row {chr(ord('A') + nr - 1)}), "
                      f"with each row containing exactly {sr} seats. All tickets are priced at R{ticket_p:,.2f}. "
                      f"Calculate the total capacity (total number of seats) in this venue.")
            c_seat = f"{tot_seats:,} seats"
            d_seat = [
                f"{tot_seats + 50:,} seats",
                f"{tot_seats - 50:,} seats",
                f"{int(tot_seats * 1.15):,} seats",
                f"{int(tot_seats * 0.85):,} seats",
                f"{nr + sr:,} seats",
                f"{int(tot_revenue / 100):,} seats",
                f"{tot_seats * 2:,} seats"
            ]
            exp_seat = f"Total seats = Number of rows × Seats per row = {nr} × {sr} = {tot_seats:,} seats."
            add_q("Seating Plans & Grid References", "medium", q_seat, c_seat, d_seat, exp_seat)

            q_rev = (f"For a sold-out show at the {v_name} ({tot_seats:,} seats at R{ticket_p:,.2f} per ticket): "
                     f"Calculate the total gross ticket revenue generated from ticket sales.")
            c_rev = f"R{tot_revenue:,.2f}"
            d_rev = [
                f"R{round(tot_revenue * 1.15, 2):,.2f}",
                f"R{round(tot_revenue * 0.85, 2):,.2f}",
                f"R{round(tot_revenue + 15000, 2):,.2f}",
                f"R{round(tot_revenue - 15000, 2):,.2f}",
                f"R{round(tot_seats * 100, 2):,.2f}",
                f"R{round(ticket_p * 100, 2):,.2f}",
                f"R{round(tot_revenue / 2.0, 2):,.2f}"
            ]
            exp_rev = f"Revenue = Total Seats × Ticket Price = {tot_seats:,} × R{ticket_p:,.2f} = R{tot_revenue:,.2f}."
            add_q("Seating Plans & Grid References", "medium", q_rev, c_rev, d_rev, exp_rev)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    strip_routes = [
        ("N1 Johannesburg to Cape Town", 1400, 110, 4.0, [("Grasmere Plaza", 24.50), ("Vaal Plaza", 74.00), ("Verkeerdevlei Plaza", 68.50), ("Huguenot Tunnel", 47.50)], 7.8, 22.80),
        ("N3 Johannesburg to Durban", 570, 100, 1.5, [("De Hoek Plaza", 63.00), ("Wilge Plaza", 86.00), ("Tugela Plaza", 91.00), ("Mooi River Plaza", 64.00)], 7.2, 22.80),
        ("N4 Pretoria to Mbombela (Nelspruit)", 330, 110, 1.0, [("Diamond Hill Plaza", 45.00), ("Middelburg Plaza", 75.00), ("Machado Plaza", 112.00), ("Nkomazi Plaza", 84.00)], 6.8, 22.80),
        ("N2 Port Elizabeth/Gqeberha to Cape Town", 750, 100, 2.0, [("Tsitsikamma Plaza", 62.50)], 7.4, 22.80),
        ("N12 Johannesburg to Kimberley", 480, 105, 1.5, [("Grasmere Plaza", 24.50)], 7.0, 22.80),
        ("N1 Polokwane to Pretoria", 260, 110, 0.5, [("Capricorn Plaza", 56.00), ("Kranskop Plaza", 58.00), ("Carousel Plaza", 67.00), ("Pumulani Plaza", 14.50)], 6.9, 22.80),
        ("N7 Cape Town to Springbok (Namibia corridor)", 550, 100, 1.5, [], 7.5, 22.80),
        ("N14 Pretoria to Upington", 820, 105, 2.0, [("Pelindaba Plaza", 8.50)], 7.6, 22.80),
        ("N2 Durban to Richards Bay and Pongola", 340, 100, 1.0, [("Tongaat Plaza", 14.50), ("Mvoti Plaza", 16.50), ("Mtunzini Plaza", 54.00)], 7.1, 22.80),
        ("N10 Gqeberha to Middelburg and De Aar", 520, 105, 1.5, [], 7.3, 22.80),
        ("N8 Kimberley to Bloemfontein to Maseru", 310, 100, 1.0, [], 6.7, 22.80),
        ("N11 Ladysmith to Newcastle to Ermelo", 290, 95, 0.75, [], 7.4, 22.80)
    ]
    
    for route_name, base_dist, avg_spd, rest_hrs, tolls, cons_rate, fuel_p in strip_routes:
        for scale in [0.85, 0.95, 1.0, 1.05, 1.15, 1.25]:
            tot_dist = round(base_dist * scale, 1)
            drive_time_hrs = round(tot_dist / avg_spd, 2)
            total_journey_hrs = round(drive_time_hrs + rest_hrs, 2)
            
            hrs_part = int(total_journey_hrs)
            mins_part = int(round((total_journey_hrs - hrs_part) * 60))
            if mins_part >= 60:
                hrs_part += 1
                mins_part -= 60
                
            litres_fuel = round((tot_dist / 100.0) * cons_rate, 2)
            cost_fuel = round(litres_fuel * fuel_p, 2)
            tot_tolls = sum(t_fee for _, t_fee in tolls)
            tot_trip_cost = round(cost_fuel + tot_tolls, 2)
            
            q_trip1 = (f"A logistics courier drives along the {route_name} (total trip distance: {tot_dist} km). "
                       f"The vehicle maintains an average driving speed of {avg_spd} km/h. "
                       f"The route schedule mandates driver rest stops totaling {rest_hrs} hours. "
                       f"Calculate the total journey duration (driving time plus rest stops), in hours and minutes.")
            c_trip1 = f"{hrs_part} hours {mins_part} minutes"
            d_trip1 = [
                f"{int(drive_time_hrs)} hours {int(round((drive_time_hrs - int(drive_time_hrs)) * 60))} minutes",
                f"{hrs_part + 1} hours {mins_part} minutes",
                f"{hrs_part - 1 if hrs_part > 1 else hrs_part + 2} hours {mins_part} minutes",
                f"{hrs_part} hours {mins_part + 15} minutes",
                f"{hrs_part} hours {mins_part - 15 if mins_part > 15 else mins_part + 20} minutes",
                f"{int(tot_dist / 100)} hours 0 minutes",
                f"{hrs_part} hours {int(drive_time_hrs * 10 % 10 * 6)} minutes"
            ]
            exp_trip1 = (f"Driving Time = Distance ÷ Speed = {tot_dist} km ÷ {avg_spd} km/h = {drive_time_hrs} hours. "
                         f"Total Journey Time = {drive_time_hrs} + {rest_hrs} = {total_journey_hrs} hours = {hrs_part} hours {mins_part} minutes.")
            add_q("Strip Maps & Travel Planning", "hard", q_trip1, c_trip1, d_trip1, exp_trip1)

            toll_str = ", ".join([f"{t_name} (R{t_fee:.2f})" for t_name, t_fee in tolls]) if tolls else "None (toll-free route)"
            q_trip2 = (f"Continuing with the trip along the {route_name} ({tot_dist} km): "
                       f"The bakkie consumes diesel at a rate of {cons_rate} litres per 100 km, and fuel costs R{fuel_p:.2f} per litre. "
                       f"The route tolls are: {toll_str} (Total toll fees = R{tot_tolls:,.2f}). "
                       f"Calculate the total operating travel cost for fuel and tolls combined.")
            c_trip2 = f"R{tot_trip_cost:,.2f}"
            d_trip2 = [
                f"R{cost_fuel:,.2f}",
                f"R{tot_tolls:,.2f}",
                f"R{round(tot_trip_cost * 1.15, 2):,.2f}",
                f"R{round(tot_trip_cost * 0.85, 2):,.2f}",
                f"R{round(tot_trip_cost + 150, 2):,.2f}",
                f"R{round(tot_trip_cost - 150, 2):,.2f}",
                f"R{round(litres_fuel * 10, 2):,.2f}"
            ]
            exp_trip2 = (f"Fuel Litres = ({tot_dist} ÷ 100) × {cons_rate} = {litres_fuel} litres. "
                         f"Fuel Cost = {litres_fuel} × R{fuel_p:.2f} = R{cost_fuel:,.2f}. "
                         f"Total Travel Cost = Fuel + Tolls = R{cost_fuel:,.2f} + R{tot_tolls:,.2f} = R{tot_trip_cost:,.2f}.")
            add_q("Fuel Consumption & Travel Budgeting", "hard", q_trip2, c_trip2, d_trip2, exp_trip2)

    # 3b. Assembly hardware & Sequence Principles
    furniture_models = [
        ("ErgoTech Executive Corner Desk", "Fasten metal cam-lock pins into pre-drilled pilot holes in the desktop before aligning with the vertical modesty pedestal panels.",
         ["Apply PVC glue directly inside the cam sockets before inserting locking cams.", "Screw the plastic glide feet into the middle of the keyboard tray.", "Nail the back panel across the front of the desk drawers.", "Attach the main desktop before fastening the leg support braces.", "Tighten cam locks using a high-torque pneumatic drill.", "Leave the modesty brace off to maximize legroom."]),
        ("Nordic Pine 5-Tier Bookcase", "Measure diagonal distances between opposite corners with a steel tape to verify the frame is square (equal diagonals) before tacking the backboard.",
         ["Nail the thin masonite backboard while the frame is resting twisted on an uneven rug.", "Attach the top crown molding before securing the fixed middle structural shelf.", "Glue the adjustable shelf pins permanently into all pre-drilled holes.", "Insert shelves before checking if the side uprights are parallel.", "Fasten the wall safety anchor bracket only to the thin backing board.", "Discard the L-shaped corner brackets supplied with the kit."]),
        ("Heavy-Duty Galvanized Steel Garden Bench", "Loosely thread all M8 bolts through the cast-iron side frames and wooden slats by hand before final tightening with an Allen wrench.",
         ["Tighten the first bolt completely to maximum torque before inserting any remaining bolts.", "Hammer the threaded bolts through misaligned slat holes with a heavy claw hammer.", "Omit the spring lock washers and flat washers from the exterior joints.", "Assemble the backrest slats upside down to alter the contour seating angle.", "Apply exterior clear varnish over wet morning dew immediately after assembly.", "Paint over the nylon lock nuts before threading them onto the bolts."]),
        ("Modular Medical Examination Couch", "Secure the adjustable headrest ratchet mechanism using high-tensile steel clevis pins and split cotter rings before attaching vinyl upholstery.",
         ["Glue the vinyl foam padding directly over the moving hinge teeth.", "Replace the steel clevis pins with soft aluminum wood screws.", "Mount the headrest adjustment lever in the reverse locking direction.", "Weld the movable joint permanently in the flat horizontal position.", "Discard the protective rubber non-slip ferrules on the couch legs.", "Assemble the couch without testing the multi-position locking detents."]),
        ("Timber Patio Braai Preparation Station", "Install the galvanized heat-shield baffle plate with a minimum 25 mm air gap clearance between the charcoal braai tub and the timber framing.",
         ["Fasten the timber side slats flush against the hot metal firebox without insulation.", "Seal all wood surfaces with flammable petroleum-based solvents directly around the braai grill.", "Omit the lockable caster wheel brakes on sloping patio surfaces.", "Attach the heavy granite prep slab using double-sided adhesive tape only.", "Secure the grease drip cup directly above the open storage shelf.", "Drill drainage holes directly through the center of the wooden prep cutting board."])
    ]
    for prod_name, c_step, w_steps in furniture_models:
        for phase_title in ["Initial Component Preparation", "Frame Alignment and Rigidity", "Hardware Fastening and Torque", "Load-bearing Structural Verification", "Final Safety and Stability Clearance"]:
            q_asm = (f"A technical assembly manual for a {prod_name} details safety precautions for '{phase_title}'. "
                     f"In accordance with standard workshop assembly practices and structural ergonomics, "
                     f"which procedure must be followed to ensure safe assembly and load-bearing stability?")
            add_q("Assembly Diagrams & Working Models", "hard", q_asm, c_step, w_steps, f"Assembly guideline for {prod_name} during {phase_title}: {c_step}")

    
    # Additional Industrial Assembly and Return-trip Logistics (Hard)
    extra_furniture = [
        ("Solar Photovoltaic Roof Mounting Framework", "Torque all stainless steel T-bolt rail clamps to 15 Nm using a calibrated torque wrench to ensure aerodynamic wind-uplift compliance.",
         ["Fasten aluminum rails with wood screws directly through the waterproof underlay.", "Omit spring washers on roof bracket anchor bolts.", "Tighten bolts with an uncalibrated hand pliers until stripped.", "Mount panels with less than 50 mm clearance above corrugated iron.", "Use zinc-plated screws in coastal corrosive environments.", "Discard the manufacturer earth grounding bonding clips."]),
        ("Mobile Aluminum Scaffolding Access Tower", "Engage and lock all four caster wheel brake levers and fully deploy the four outrigger stabilizer legs at 45° angles before ascending the tower.",
         ["Climb the exterior braces of the tower instead of using the internal trapdoor ladder.", "Leave two caster brakes unlocked to facilitate moving while standing on the top platform.", "Erect the tower on soft uncompacted mud without base spreader soleplates.", "Remove horizontal diagonal cross-braces to allow materials to be hoisted through the middle.", "Exceed the maximum platform working load by 50%.", "Omit the 150 mm kickboard toe-guards around the working platform."]),
        ("Commercial Stainless Steel Kitchen Extraction Canopy", "Anchor ceiling suspension drop rods securely into structural concrete soffit anchors using M10 expansion drop-in anchors tested to a 300 kg pull-out load.",
         ["Secure the 200 kg extraction hood into drywall hollow plasterboard using plastic plugs.", "Fasten ductwork joints with standard duct tape without stainless steel self-tapping screws.", "Mount the grease baffle filters in the reverse airflow orientation.", "Omit the removable oil collection drip tray.", "Route electrical wiring exposed directly through the grease extraction air stream.", "Seal the hood perimeter with combustible silicone sealant."])
    ]
    for prod_name, c_step, w_steps in extra_furniture:
        for phase_title in ["Pre-installation Site Assessment", "Structural Anchoring and Torque Validation", "Component Alignment and Fitment", "Safety Interlock and Rigidity Testing"]:
            q_asm = (f"A technical installation specification for a {prod_name} provides mandatory protocols for '{phase_title}'. "
                     f"Which procedure must be executed to ensure compliance with SANS technical regulations and structural integrity?")
            add_q("Assembly Diagrams & Working Models", "hard", q_asm, c_step, w_steps, f"Safety guideline for {prod_name} during {phase_title}: {c_step}")

    
    # Round-trip journey expenses (Hard)
    for route_name, base_dist, avg_spd, rest_hrs, tolls, cons_rate, fuel_p in strip_routes:
        for scale in [0.9, 1.0, 1.1, 1.2]:
            one_way_dist = round(base_dist * scale, 1)
            round_dist = round(one_way_dist * 2.0, 1)
            litres_round = round((round_dist / 100.0) * cons_rate, 2)
            fuel_cost_round = round(litres_round * fuel_p, 2)
            tot_tolls_one = sum(t_fee for _, t_fee in tolls)
            tot_tolls_round = round(tot_tolls_one * 2.0, 2)
            total_round_trip = round(fuel_cost_round + tot_tolls_round, 2)
            
            q_round = (f"A logistics contractor undertakes a full ROUND TRIP (both ways) along the {route_name} "
                       f"(one-way distance: {one_way_dist} km, total round-trip distance: {round_dist} km). "
                       f"The vehicle consumes fuel at {cons_rate} litres/100 km, fuel is R{fuel_p:.2f}/litre, "
                       f"and one-way toll fees total R{tot_tolls_one:,.2f} (paid in both directions: R{tot_tolls_round:,.2f}). "
                       f"Calculate the complete budget for the round trip (fuel and tolls combined).")
            c_round = f"R{total_round_trip:,.2f}"
            d_round = [
                f"R{fuel_cost_round:,.2f}",
                f"R{tot_tolls_round:,.2f}",
                f"R{round(total_round_trip * 1.15, 2):,.2f}",
                f"R{round(total_round_trip * 0.85, 2):,.2f}",
                f"R{round(total_round_trip + 250, 2):,.2f}",
                f"R{round(total_round_trip - 250, 2):,.2f}",
                f"R{round(one_way_dist * fuel_p, 2):,.2f}"
            ]
            exp_round = (f"Round-trip Distance = {one_way_dist} × 2 = {round_dist} km. "
                         f"Round-trip Fuel = ({round_dist} ÷ 100) × {cons_rate} = {litres_round} litres = R{fuel_cost_round:,.2f}. "
                         f"Round-trip Tolls = R{tot_tolls_one:,.2f} × 2 = R{tot_tolls_round:,.2f}. "
                         f"Total Budget = R{fuel_cost_round:,.2f} + R{tot_tolls_round:,.2f} = R{total_round_trip:,.2f}.")
            add_q("Fuel Consumption & Travel Budgeting", "hard", q_round, c_round, d_round, exp_round)

    print(f"Generated Maps & Plans: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/mathematical_literacy"
    out_file = os.path.join(out_dir, "paper2_mathlit12_maps_plans.json")
    dataset = build_maps_plans_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()

# Additional modules for Maps & Plans
