import json
import os
import random
import math
import time

def build_p2_probability_dataset():
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
        q_id = f"ML12_P2_PROB_{len(questions) + 1:04d}"
        
        questions.append({
            "id": q_id,
            "topic": "Probability",
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
    p2_terms = [
        ("Manufacturing tolerance", "The permissible limit or allowable range of variation in a physical dimension or mass of a manufactured product.",
         ["The total cost of production including raw materials and factory overheads.", "The maximum warranty period offered on consumer appliances.", "The percentage discount applied to bulk retail orders.", "The probability that a product will be damaged during transport.", "The volume of paint required to cover two coats on an exterior wall.", "The ratio scale of an architectural elevation drawing."]),
        ("Quality control batch sample", "A representative subset of items randomly selected from a production run to test for compliance with technical specifications.",
         ["The total inventory remaining in a warehouse at the financial year-end.", "A list of defective items returned by dissatisfied customers.", "The maximum load capacity of a freight delivery truck.", "An accounting reconciliation between bank balance and cash book.", "A scheduled maintenance checklist for industrial machinery.", "The total number of units required to reach the break-even sales volume."]),
        ("Failure rate (Reliability)", "The frequency or probability with which an engineered system or mechanical component fails, expressed as failures per unit of time or trials.",
         ["The interest rate charged by banks on overdraft credit facilities.", "The speed at which a delivery vehicle travels along a national highway.", "The percentage of water lost due to evaporation in open reservoirs.", "The ratio of fixed operating costs to variable production costs.", "The angle of inclination of a residential roof truss gable.", "The proportion of gross salary deducted for pension contributions."]),
        ("Risk assessment in construction", "The systematic evaluation of the likelihood and potential impact of hazards, accidents, or weather delays occurring on a building site.",
         ["The calculation of total concrete volume required for foundation footings.", "The pricing of ceramic floor tiles per square metre including 10% wastage.", "The architectural drawing showing interior electrical outlet positions.", "The calculation of personal income tax rebates for elderly workers.", "The determination of the shortest driving route on a strip map.", "The measurement of ceiling height clearance for door frames."]),
        ("Independent operational events", "Two industrial or logistical events where the occurrence of one event has no effect on the probability of the other event occurring.",
         ["Two consecutive operations carried out by the same worker on a single machine.", "Two components that are wired in series on an electrical circuit.", "Events that both cause a production shutdown simultaneously.", "Events whose probabilities always add up to exactly 100%.", "The selection of items from a container without replacement.", "Two measurements of the same room with different scales."])
    ]
    for term, c_def, w_defs in p2_terms:
        q = f"In Mathematical Literacy Paper 2 applied contexts, define or explain '{term}'."
        add_q("Quality Control & Manufacturing Tolerances", "easy", q, c_def, w_defs, f"CAPS operational concept: {term}: {c_def}")

    batch_tests = [
        ("bakery packaging 700g sandwich bread loaves", 1000, 960, "compliant mass (695g - 705g)"),
        ("dairy bottling plant filling 2-litre milk jugs", 2500, 2425, "acceptable volume (1 980 mℓ - 2 020 mℓ)"),
        ("brick manufacturing kiln producing clay paving bricks", 5000, 4850, "SABS compressive strength specification"),
        ("pharmaceutical lab pressing 500mg paracetamol tablets", 10000, 9820, "correct chemical dosage tolerance"),
        ("solar panel plant assembling 400W photovoltaic modules", 800, 768, "rated electrical output efficiency"),
        ("beverage can cannery sealing 330ml soft drinks", 4000, 3920, "hermetic seal pressure test"),
        ("agricultural seed packager filling 50kg grain bags", 1200, 1164, "statutory trade weight tolerance"),
        ("concrete batching plant casting test cubes", 500, 475, "28-day curing strength benchmark"),
        ("flour mill packing 10kg cake flour bags", 2000, 1940, "acceptable filling weight margin"),
        ("paint factory canning 5-litre PVA emulsion cans", 1500, 1455, "nominal volume tolerance"),
        ("cable manufacturer extruding 100m electrical rolls", 1800, 1746, "electrical resistance standard"),
        ("steel pipe foundry manufacturing galvanized conduit", 2200, 2134, "wall thickness tolerance")
    ]
    for b_title, tot_tested, pass_cnt, spec_desc in batch_tests:
        for factor in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
            tot_t = int(tot_tested * factor)
            p_cnt = int(pass_cnt * factor)
            f_cnt = tot_t - p_cnt
            p_pct = round((p_cnt / tot_t) * 100.0, 1)
            f_pct = round((f_cnt / tot_t) * 100.0, 1)
            
            q_pass = (f"A quality assurance audit tests a sample of {tot_t:,} units from a {b_title}. "
                      f"Exactly {p_cnt:,} units met the {spec_desc}. "
                      f"Calculate the percentage probability that an item randomly selected from this batch is compliant.")
            c_pass = f"{p_pct}%"
            d_pass = [
                f"{f_pct}%",
                f"{round(p_pct * 1.10, 1)}%",
                f"{round(p_pct * 0.90, 1)}%",
                f"{round(p_cnt / 100.0, 1)}%",
                f"{round(p_pct + 4.0, 1)}%",
                f"{round(p_pct - 4.0, 1)}%",
                f"{round((p_cnt / f_cnt) * 10.0, 1)}%"
            ]
            exp_pass = f"P(Compliant) = ({p_cnt:,} ÷ {tot_t:,}) × 100% = {p_pct}%."
            add_q("Quality Control & Manufacturing Tolerances", "easy", q_pass, c_pass, d_pass, exp_pass)

            q_fail = f"From the same audit of {tot_t:,} units ({b_title}), determine the percentage probability of randomly selecting a DEFECTIVE (non-compliant) item."
            c_fail = f"{f_pct}%"
            d_fail = [
                f"{p_pct}%",
                f"{round(f_pct * 1.5, 1)}%",
                f"{round(f_pct * 0.5, 1)}%",
                f"{round(f_cnt / 10.0, 1)}%",
                f"{round(f_pct + 2.5, 1)}%",
                f"{round(f_pct - 2.5 if f_pct > 3 else f_pct + 1.2, 1)}%",
                f"{round((f_cnt / p_cnt) * 10.0, 1)}%"
            ]
            exp_fail = f"P(Defective) = ({f_cnt:,} ÷ {tot_t:,}) × 100% = {f_pct}%."
            add_q("Quality Control & Manufacturing Tolerances", "easy", q_fail, c_fail, d_fail, exp_fail)

    # Road safety & PPE Compliance (Easy)
    ppe_scenarios = [
        ("construction scaffolding team", "wearing certified safety harnesses", 60, 54),
        ("steel fabrication workshop", "wearing auto-darkening welding helmets", 45, 42),
        ("commercial forestry chainsaw operators", "wearing cut-resistant safety chaps", 50, 48),
        ("underground gold mine stope workers", "carrying functioning self-contained rescuers", 80, 78),
        ("chemical handling depot personnel", "wearing organic vapour respirators", 40, 38),
        ("asbestos abatement demolition crew", "fitted with P3 particulate respirators", 35, 35)
    ]
    for team_name, ppe_item, n_workers, n_comp in ppe_scenarios:
        for factor in [1, 2, 3, 4]:
            nw = n_workers * factor
            nc = n_comp * factor
            p_comp = round((nc / nw) * 100.0, 1)
            q_ppe = f"A site safety inspector audits a {team_name} ({nw} workers total). Exactly {nc} workers are {ppe_item}. What is the percentage probability that a randomly audited worker is fully compliant with PPE regulations?"
            c_ppe = f"{p_comp}%"
            d_ppe = [
                f"{round(100 - p_comp, 1)}%",
                f"{round(p_comp * 1.10, 1)}%",
                f"{round(p_comp * 0.90, 1)}%",
                f"{round(nc / 10.0, 1)}%",
                f"{round(p_comp + 5.0, 1)}%",
                f"{round(p_comp - 5.0, 1)}%",
                f"{round((nw - nc) / 10.0, 1)}%"
            ]
            exp_ppe = f"P(Compliant) = ({nc} ÷ {nw}) × 100% = {p_comp}%."
            add_q("Workplace Health & Safety Probabilities", "easy", q_ppe, c_ppe, d_ppe, exp_ppe)

    
    # Vehicle Roadworthy Safety Audits (Easy)
    vehicle_safety_tests = [
        ("minibus taxi brake testing", 200, 170, "statutory brake balance and stopping distance standard"),
        ("freight truck tyre tread depth audit", 300, 276, "minimum 1.6 mm legal tread depth requirement"),
        ("commuter bus emergency exit inspection", 150, 144, "functioning emergency release mechanism"),
        ("agricultural tractor lighting check", 80, 68, "operational rear red reflector and indicator lights"),
        ("courier delivery motorcycle roadworthy audit", 250, 230, "certified helmet and front disc brake standard"),
        ("school transport bus seatbelt inspection", 120, 114, "operational 3-point lap and diagonal seatbelts"),
        ("municipal refuse truck hydraulic safety audit", 90, 81, "fail-safe bin lifting hydraulic interlock"),
        ("traffic police patrol car fleet inspection", 100, 97, "pursuit-rated tyre speed rating compliance"),
        ("hospital patient transfer van road test", 80, 76, "dual-circuit ABS braking certification"),
        ("mining personnel carrier vehicle check", 110, 102, "roll-over protective structure ROPS certification")
    ]
    for test_title, n_tested, n_pass, spec_str in vehicle_safety_tests:
        for factor in [0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]:
            nt = int(round(n_tested * factor))
            np = int(round(n_pass * factor))
            nf = nt - np
            pass_p = round((np / nt) * 100.0, 1)
            fail_p = round((nf / nt) * 100.0, 1)
            
            q_vtest = (f"A municipal traffic safety officer inspects {nt} vehicles during a {test_title}. "
                       f"Exactly {np} vehicles met the {spec_str}. "
                       f"Calculate the percentage probability that an inspected vehicle is compliant.")
            c_vtest = f"{pass_p}%"
            d_vtest = [
                f"{fail_p}%",
                f"{round(pass_p * 1.10, 1)}%",
                f"{round(pass_p * 0.90, 1)}%",
                f"{round(np / 10.0, 1)}%",
                f"{round(pass_p + 5.0, 1)}%",
                f"{round(pass_p - 5.0, 1)}%",
                f"{round((np / nf) * 10.0, 1)}%"
            ]
            exp_vtest = f"P(Compliant) = ({np} ÷ {nt}) × 100% = {pass_p}%."
            add_q("Workplace Health & Safety Probabilities", "easy", q_vtest, c_vtest, d_vtest, exp_vtest)

            q_vfail = f"From the same vehicle audit ({test_title}: {nt} vehicles inspected), determine the percentage probability that a vehicle FAILS the inspection."
            c_vfail = f"{fail_p}%"
            d_vfail = [
                f"{pass_p}%",
                f"{round(fail_p * 1.5, 1)}%",
                f"{round(fail_p * 0.5, 1)}%",
                f"{round(nf / 10.0, 1)}%",
                f"{round(fail_p + 3.0, 1)}%",
                f"{round(fail_p - 3.0 if fail_p > 3.5 else fail_p + 1.5, 1)}%",
                f"{round((nf / np) * 100.0, 1)}%"
            ]
            exp_vfail = f"P(Failed) = ({nf} ÷ {nt}) × 100% = {fail_p}%."
            add_q("Workplace Health & Safety Probabilities", "easy", q_vfail, c_vfail, d_vfail, exp_vfail)

# -------------------------------------------------------------------------
    # 2. MEDIUM QUESTIONS (Target: 500)
    # -------------------------------------------------------------------------
    op_tables = [
        ("Drinking Water SANS 241 Quality Compliance", "Water Source", ["Municipal Mains", "Borehole Wells"], "Standard", ["Fully Compliant", "Non-Compliant"], [[190, 10], [140, 60]]),
        ("Commercial Vehicle Roadworthy Testing", "Vehicle Category", ["Minibus Taxis", "Freight Trucks"], "Test Result", ["Passed First Time", "Failed Inspection"], [[110, 90], [135, 65]]),
        ("Courier Dispatch Performance", "Service Tier", ["Overnight Express", "Standard Economy"], "Delivery Status", ["Delivered On-Time", "Delayed Arrival"], [[220, 30], [195, 55]]),
        ("Construction Concrete Test Cubes", "Mix Grade", ["Grade 25 MPa", "Grade 30 MPa"], "Strength", ["Exceeds Spec", "Below Spec"], [[170, 30], [185, 15]]),
        ("Factory Safety Equipment Inspections", "Department", ["Fabrication Bay", "Assembly Line"], "Condition", ["Certified Safe", "Requires Repair"], [[145, 25], [160, 20]]),
        ("Hospital Standby Power Generator Readiness", "Facility Type", ["Regional Hospital", "District Clinic"], "Readiness", ["Auto-Start Ready", "Battery Deficient"], [[85, 15], [60, 40]]),
        ("Agricultural Irrigation Pumps", "Power Source", ["Grid Powered", "Solar Powered"], "Operational Status", ["Fully Operational", "Maintenance Alert"], [[130, 20], [115, 35]]),
        ("Municipal Traffic Camera Speed Enforcement", "Road Type", ["Freeway Corridor", "Urban Arterial"], "Compliance", ["Within Speed Limit", "Speeding Violation"], [[420, 80], [350, 150]]),
        ("Commercial Building Fire Extinguisher Audits", "Extinguisher Type", ["Dry Chemical Powder", "CO2 Gas"], "Service Tag", ["Valid Inspection Tag", "Expired Service Tag"], [[180, 20], [130, 30]]),
        ("Cold Storage Food Safety Compliance", "Storage Area", ["Walk-in Freezers", "Chilled Prep Rooms"], "HACCP Check", ["Temperature Compliant", "Temperature Deviation"], [[165, 15], [140, 20]])
    ]
    for o_title, r_lbl, rows, c_lbl, cols, matrix in op_tables:
        for mult in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            m = [[val * mult for val in row] for row in matrix]
            r0_tot = sum(m[0])
            r1_tot = sum(m[1])
            c0_tot = m[0][0] + m[1][0]
            c1_tot = m[0][1] + m[1][1]
            grand_tot = r0_tot + r1_tot
            
            p_r0 = round((r0_tot / grand_tot) * 100.0, 1)
            q_ot1 = (f"The table below shows operational inspection data for {o_title} (Grand Total = {grand_tot}):\n"
                     f"• {rows[0]}: {cols[0]} = {m[0][0]}, {cols[1]} = {m[0][1]} (Row Total = {r0_tot})\n"
                     f"• {rows[1]}: {cols[0]} = {m[1][0]}, {cols[1]} = {m[1][1]} (Row Total = {r1_tot})\n"
                     f"Calculate the percentage probability that a randomly audited item is '{rows[0]}'. (Round to 1 decimal place).")
            c_ot1 = f"{p_r0}%"
            d_ot1 = [
                f"{round((r1_tot / grand_tot) * 100.0, 1)}%",
                f"{round((m[0][0] / grand_tot) * 100.0, 1)}%",
                f"{round((c0_tot / grand_tot) * 100.0, 1)}%",
                f"{round(p_r0 * 1.15, 1)}%",
                f"{round(p_r0 * 0.85, 1)}%",
                f"{round(p_r0 + 10.0, 1)}%",
                f"{round(p_r0 - 10.0, 1)}%"
            ]
            exp_ot1 = f"P({rows[0]}) = Row Total ÷ Grand Total = {r0_tot} ÷ {grand_tot} × 100% = {p_r0}%."
            add_q("Quality Control & Manufacturing Tolerances", "medium", q_ot1, c_ot1, d_ot1, exp_ot1)

            p_cond_fail = round((m[1][1] / r1_tot) * 100.0, 1)
            q_ot2 = (f"Using the operational audit data for {o_title} (Grand Total = {grand_tot}):\n"
                     f"GIVEN that an item is from the '{rows[1]}' category, calculate the conditional probability that it is '{cols[1]}', expressed as a percentage.")
            c_ot2 = f"{p_cond_fail}%"
            d_ot2 = [
                f"{round((m[1][1] / grand_tot) * 100.0, 1)}%",
                f"{round((m[1][1] / c1_tot) * 100.0, 1)}%",
                f"{round((m[1][0] / r1_tot) * 100.0, 1)}%",
                f"{round(p_cond_fail * 1.20, 1)}%",
                f"{round(p_cond_fail * 0.80, 1)}%",
                f"{round(p_cond_fail + 8.0, 1)}%",
                f"{round(p_cond_fail - 8.0 if p_cond_fail > 9 else p_cond_fail + 4.0, 1)}%"
            ]
            exp_ot2 = f"P({cols[1]} | {rows[1]}) = Cell count ÷ Row Total = {m[1][1]} ÷ {r1_tot} × 100% = {p_cond_fail}%."
            add_q("Quality Control & Manufacturing Tolerances", "medium", q_ot2, c_ot2, d_ot2, exp_ot2)

            p_joint = round((m[0][0] / grand_tot) * 100.0, 1)
            q_ot3 = (f"From the audit dataset for {o_title} (Grand Total = {grand_tot}):\n"
                     f"Determine the probability that a randomly audited item is BOTH '{rows[0]}' AND '{cols[0]}', expressed as a percentage.")
            c_ot3 = f"{p_joint}%"
            d_ot3 = [
                f"{p_r0}%",
                f"{round((c0_tot / grand_tot) * 100.0, 1)}%",
                f"{round((m[0][1] / grand_tot) * 100.0, 1)}%",
                f"{round((m[1][0] / grand_tot) * 100.0, 1)}%",
                f"{round(p_joint * 1.20, 1)}%",
                f"{round(p_joint * 0.80, 1)}%",
                f"{round(p_joint + 8.5, 1)}%"
            ]
            exp_ot3 = f"P({rows[0]} and {cols[0]}) = Cell count ÷ Grand Total = {m[0][0]} ÷ {grand_tot} × 100% = {p_joint}%."
            add_q("Quality Control & Manufacturing Tolerances", "medium", q_ot3, c_ot3, d_ot3, exp_ot3)

    # 2b. Multi-Stage Supply Chain and Logistics Tree Diagrams (Medium)
    tree_chains = [
        ("Two-leg national courier express transit", "Leg 1 (JHB to DBN on-time)", 0.88, "Leg 2 (DBN local courier dispatch on-time)", 0.92),
        ("Water treatment chlorination and filtration stages", "Stage 1 (Primary coagulation compliant)", 0.95, "Stage 2 (UV bacterial sterilization compliant)", 0.96),
        ("Automated bottling line packaging sequence", "Capping torque within spec", 0.94, "Label application aligned within spec", 0.90),
        ("Air cargo perishable cold chain storage", "Cold storage transfer Hub 1", 0.92, "Refrigerated road link Hub 2", 0.85),
        ("Solar microgrid battery storage charging", "Daytime solar charge full", 0.86, "Inverter overnight battery conversion", 0.90),
        ("Emergency healthcare hospital trauma intake", "Triage stabilization within 15 min", 0.85, "Operating theatre transfer readiness", 0.90),
        ("Mining environmental air ventilation scrubber", "Primary particulate dust filter operational", 0.96, "Secondary toxic gas scrubber operational", 0.94),
        ("Bulk grain export rail transport sequence", "Grain elevator load out on schedule", 0.88, "Harbour bulk berth ship loading on schedule", 0.84)
    ]
    for chain_title, st1_name, p1_base, st2_name, p2_base in tree_chains:
        for d1 in [-0.08, -0.04, 0.0, 0.04, 0.06]:
            for d2 in [-0.08, -0.04, 0.0, 0.04]:
                p1 = round(p1_base + d1, 2)
                p2 = round(p2_base + d2, 2)
                p_success = round(p1 * p2, 4)
                p_success_pct = round(p_success * 100.0, 2)
                p_failure = round(1.0 - p_success, 4)
                p_failure_pct = round(p_failure * 100.0, 2)
                
                q_tc1 = (f"A two-stage operational flow models {chain_title}. "
                         f"The probability of {st1_name} is {p1:.2f} ({p1*100:.0f}%), and the probability of {st2_name} is {p2:.2f} ({p2*100:.0f}%). "
                         f"Assuming the two stages operate independently, calculate the probability that the ENTIRE operational process succeeds without defects, expressed as a percentage.")
                c_tc1 = f"{p_success_pct}%"
                d_tc1 = [
                    f"{p_failure_pct}%",
                    f"{round((p1 + p2) * 50.0, 2)}%",
                    f"{round(p1 * 100.0, 2)}%",
                    f"{round(p2 * 100.0, 2)}%",
                    f"{round(p_success_pct * 1.15, 2)}%",
                    f"{round(p_success_pct * 0.85, 2)}%",
                    f"{round(p_success_pct + 8.5, 2)}%"
                ]
                exp_tc1 = f"P(Overall Success) = P(Stage 1) × P(Stage 2) = {p1:.2f} × {p2:.2f} = {p_success:.4f} = {p_success_pct}%."
                add_q("Transport Logistics & Route Reliability", "medium", q_tc1, c_tc1, d_tc1, exp_tc1)

                q_tc2 = (f"From the same operational model ({chain_title}: P(Stage 1) = {p1:.2f}, P(Stage 2) = {p2:.2f}): "
                         f"Determine the probability that AT LEAST ONE stage experiences a delay or defect, expressed as a percentage.")
                c_tc2 = f"{p_failure_pct}%"
                d_tc2 = [
                    f"{p_success_pct}%",
                    f"{round((1 - p1) * (1 - p2) * 100.0, 2)}%",
                    f"{round((1 - p1) * 100.0, 2)}%",
                    f"{round((1 - p2) * 100.0, 2)}%",
                    f"{round(p_failure_pct * 1.20, 2)}%",
                    f"{round(p_failure_pct * 0.80, 2)}%",
                    f"{round(p_failure_pct + 5.5, 2)}%"
                ]
                exp_tc2 = f"P(At least one defect) = 100% - P(Both succeed) = 100% - {p_success_pct}% = {p_failure_pct}%."
                add_q("Transport Logistics & Route Reliability", "medium", q_tc2, c_tc2, d_tc2, exp_tc2)

    # -------------------------------------------------------------------------
    # 3. HARD QUESTIONS (Target: 200)
    # -------------------------------------------------------------------------
    harvest_cases = [
        ("suburban family home in Durban", 220, 75, 0.85, 26.50, 8500),
        ("primary school hall in Nelspruit", 480, 85, 0.85, 28.00, 14500),
        ("community agricultural packing shed in George", 350, 65, 0.80, 25.00, 11000),
        ("provincial health clinic in Polokwane", 280, 60, 0.85, 27.50, 9500),
        ("vocational technical workshop in Cape Town", 400, 70, 0.85, 31.00, 12500),
        ("commercial shopping mall canopy in Johannesburg", 650, 80, 0.85, 29.50, 22000),
        ("secondary school boarding hostel in Bloemfontein", 320, 55, 0.85, 24.00, 10500),
        ("community library rooftop in Kimberley", 260, 50, 0.80, 23.50, 9000),
        ("dairy milking parlour roof in Mooi River", 500, 90, 0.85, 27.00, 16000),
        ("hotel resort pavilion roof in Rustenburg", 380, 65, 0.85, 26.00, 13000)
    ]
    for h_desc, roof_m2, rain_mm, coeff, tariff_kl, tank_inv in harvest_cases:
        for factor in [0.75, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35]:
            r_area = round(roof_m2 * factor, 1)
            r_mm = round(rain_mm * factor, 1)
            litres_h = round(r_area * r_mm * coeff, 1)
            kl_h = round(litres_h / 1000.0, 2)
            monthly_saving = round(kl_h * tariff_kl, 2)
            annual_saving = round(monthly_saving * 4, 2)
            payback_years = round(tank_inv / annual_saving, 1)
            
            q_harv1 = (f"A property owner evaluates rainwater harvesting for a {h_desc} (roof catchment area: {r_area} m², runoff coefficient: {coeff}). "
                       f"During a typical wet summer month, rainfall probability models predict an average of {r_mm} mm of rain. "
                       f"Municipal water in this consumption bracket costs R{tariff_kl:,.2f} per kℓ (including VAT). "
                       f"Calculate the monthly monetary saving on the municipal water bill resulting from this harvested rainwater.")
            c_harv1 = f"R{monthly_saving:,.2f}"
            d_harv1 = [
                f"R{round(litres_h * tariff_kl, 2):,.2f}",
                f"R{annual_saving:,.2f}",
                f"R{round(monthly_saving * 1.15, 2):,.2f}",
                f"R{round(monthly_saving * 0.85, 2):,.2f}",
                f"R{round(monthly_saving + 120, 2):,.2f}",
                f"R{round(monthly_saving - 120, 2):,.2f}",
                f"R{round(kl_h * 10, 2):,.2f}"
            ]
            exp_harv1 = (f"Step 1: Harvested Litres = {r_area} m² × {r_mm} mm × {coeff} = {litres_h:,.1f} ℓ. "
                         f"Step 2: Volume in kℓ = {litres_h:,.1f} ÷ 1,000 = {kl_h} kℓ. "
                         f"Step 3: Monthly Saving = {kl_h} kℓ × R{tariff_kl:,.2f} = R{monthly_saving:,.2f}.")
            add_q("Environmental & Water Resource Risk", "hard", q_harv1, c_harv1, d_harv1, exp_harv1)

            q_harv2 = (f"Using the rainwater harvesting data for the {h_desc} (total capital installation cost: R{tank_inv:,.2f}): "
                       f"Assuming an annual savings of R{annual_saving:,.2f} over the rainy season, "
                       f"calculate the estimated payback period for this investment in years (rounded to 1 decimal place).")
            c_harv2 = f"{payback_years} years"
            d_harv2 = [
                f"{round(tank_inv / monthly_saving, 1)} years",
                f"{round(payback_years * 1.25, 1)} years",
                f"{round(payback_years * 0.75, 1)} years",
                f"{round(payback_years + 2.0, 1)} years",
                f"{round(payback_years - 2.0 if payback_years > 3 else payback_years + 1.0, 1)} years",
                f"{round(annual_saving / 1000, 1)} years",
                f"{round(payback_years * 2.0, 1)} years"
            ]
            exp_harv2 = f"Payback Period = Capital Cost ÷ Annual Savings = R{tank_inv:,.2f} ÷ R{annual_saving:,.2f} = {payback_years} years."
            add_q("Integrated Cost-Risk Decisions", "hard", q_harv2, c_harv2, d_harv2, exp_harv2)

    # 3b. Solar PV vs Diesel Generator Operational Risk & Break-Even
    solar_cases = [
        ("small rural clinic", 12.0, 3.5, 24.50, 68000),
        ("community spaza refrigeration unit", 18.0, 3.8, 24.50, 85000),
        ("agricultural water borehole pump", 24.0, 4.0, 24.50, 115000),
        ("school computer lab backup system", 15.0, 3.6, 24.50, 78000),
        ("police radio communication station", 10.0, 3.4, 24.50, 58000),
        ("community bakery dough mixer station", 20.0, 3.8, 24.50, 92000)
    ]
    for sol_desc, daily_kwh, l_per_kwh, diesel_p, sol_inv in solar_cases:
        for scale in [0.8, 0.9, 1.0, 1.1, 1.2, 1.35]:
            dk = round(daily_kwh * scale, 1)
            diesel_litres_day = round(dk * 0.35, 2)
            daily_fuel_cost = round(diesel_litres_day * diesel_p, 2)
            monthly_fuel_cost = round(daily_fuel_cost * 30, 2)
            annual_diesel_cost = round(monthly_fuel_cost * 12, 2)
            solar_payback_years = round(sol_inv / annual_diesel_cost, 1)
            
            q_sol = (f"An administrator compares backup power options for a {sol_desc} requiring {dk} kWh of electricity per day during loadshedding. "
                     f"A diesel generator consumes 0.35 litres of diesel per kWh, with diesel priced at R{diesel_p:.2f} per litre. "
                     f"Calculate the monthly fuel operating cost (30-day month) of running the diesel generator.")
            c_sol = f"R{monthly_fuel_cost:,.2f}"
            d_sol = [
                f"R{daily_fuel_cost:,.2f}",
                f"R{round(monthly_fuel_cost * 1.15, 2):,.2f}",
                f"R{round(monthly_fuel_cost * 0.85, 2):,.2f}",
                f"R{round(monthly_fuel_cost + 800, 2):,.2f}",
                f"R{round(monthly_fuel_cost - 800, 2):,.2f}",
                f"R{round(diesel_litres_day * 100, 2):,.2f}",
                f"R{round(dk * diesel_p, 2):,.2f}"
            ]
            exp_sol = (f"Daily diesel = {dk} kWh × 0.35 L/kWh = {diesel_litres_day} litres. "
                       f"Daily fuel cost = {diesel_litres_day} L × R{diesel_p:.2f} = R{daily_fuel_cost:,.2f}. "
                       f"Monthly fuel cost (30 days) = R{daily_fuel_cost:,.2f} × 30 = R{monthly_fuel_cost:,.2f}.")
            add_q("Integrated Cost-Risk Decisions", "hard", q_sol, c_sol, d_sol, exp_sol)

            q_pay = (f"Continuing with the {sol_desc} backup power analysis: "
                     f"Installing an off-grid solar photovoltaic (PV) system with lithium battery storage costs R{sol_inv:,.2f} upfront (with negligible running costs). "
                     f"If the diesel generator fuel cost is R{annual_diesel_cost:,.2f} per year, calculate the payback period of the solar investment in years (rounded to 1 decimal place).")
            c_pay = f"{solar_payback_years} years"
            d_pay = [
                f"{round(sol_inv / monthly_fuel_cost, 1)} years",
                f"{round(solar_payback_years * 1.25, 1)} years",
                f"{round(solar_payback_years * 0.75, 1)} years",
                f"{round(solar_payback_years + 1.5, 1)} years",
                f"{round(solar_payback_years - 1.5 if solar_payback_years > 2 else solar_payback_years + 0.8, 1)} years",
                f"{round(annual_diesel_cost / 1000, 1)} years",
                f"{round(solar_payback_years * 2.0, 1)} years"
            ]
            exp_pay = f"Payback Period = Solar Investment ÷ Annual Diesel Fuel Cost = R{sol_inv:,.2f} ÷ R{annual_diesel_cost:,.2f} = {solar_payback_years} years."
            add_q("Integrated Cost-Risk Decisions", "hard", q_pay, c_pay, d_pay, exp_pay)

    print(f"Generated Paper 2 Probability & Integrated Contexts: Easy={counts['easy']}, Medium={counts['medium']}, Hard={counts['hard']}, Total={len(questions)}")
    return questions

def run():
    t0 = time.time()
    out_dir = "/data/data/com.termux/files/home/quiz-/dataset/grade12/mathematical_literacy"
    out_file = os.path.join(out_dir, "paper2_mathlit12_probability.json")
    dataset = build_p2_probability_dataset()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(dataset)} questions to {out_file} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run()
