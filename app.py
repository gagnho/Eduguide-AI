# app.py
import streamlit as st
from fpdf import FPDF
import datetime
import math
import json
import os

# -------------------
# Helper functions
# -------------------
def generate_topics_for_subject(exam, subject):
    # Very small sample topic lists; you can expand later.
    topics_db = {
        "JEE": {
            "Physics": [
    "Units and Dimensions",
    "Kinematics",
    "Laws of Motion",
    "Work, Energy and Power",
    "Rotational Motion",
    "Gravitation",
    "Properties of Solids and Fluids",
    "Oscillations",
    "Waves",
    "Heat and Thermodynamics",
    "Electrostatics",
    "Current Electricity",
    "Magnetic Effects of Current and Magnetism",
    "Electromagnetic Induction and Alternating Currents",
    "Electromagnetic Waves",
    "Optics",
    "Dual Nature of Matter and Radiation",
    "Atoms and Nuclei",
    "Electronic Devices",
    "Experimental Skills"
],

"Chemistry": [
    "Some Basic Concepts of Chemistry",
    "Atomic Structure",
    "Chemical Bonding and Molecular Structure",
    "States of Matter: Gaseous and Liquid State",
    "Thermodynamics",
    "Equilibrium",
    "Redox Reactions and Electrochemistry",
    "The Solid State",
    "Solutions",
    "Chemical Kinetics",
    "Surface Chemistry",
    "Classification of Elements and Periodicity in Properties",
    "The p-block Element (Group 13 and 14)",
    "The p-block Element (Group 15, 16, 17 and 18)",
    "The d-block Element (Transition Elements)",
    "The f-block Element (Lanthanides and Actinides)",
    "Coordination Compounds",
    "Hydrogen",
    "The s-block Element (Alkali and Alkaline earth metals)",
    "The p-block Element (Boron and Carbon family)",
    "General Principles and Processes of Isolation of Metals",
    "Organic Chemistry – Basic Principles and Techniques",
    "Hydrocarbons",
    "Haloalkanes and Haloarenes",
    "Alcohols, Phenols and Ethers",
    "Aldehydes, Ketones and Carboxylic Acids",
    "Amines",
    "Biomolecules",
    "Polymers",
    "Chemistry in Everyday Life",
    "Environmental Chemistry"
],

"Maths": [
    "Sets, Relations and Functions",
    "Complex Numbers and Quadratic Equations",
    "Matrices and Determinants",
    "Permutations and Combinations",
    "Mathematical Induction",
    "Binomial Theorem and Its Applications",
    "Sequences and Series",
    "Limit, Continuity and Differentiability",
    "Integral Calculus",
    "Differential Equations",
    "Coordinate Geometry",
    "Three Dimensional Geometry",
    "Vector Algebra",
    "Statistics and Probability",
    "Trigonometry",
    "Mathematical Reasoning"
]

        },
        "NEET": {
"Physics": [
    "Mechanics",
    "Thermodynamics",
    "Oscillations and Waves",
    "Electrodynamics",
    "Optics",
    "Modern Physics",
    "Properties of Matter",
    "Electromagnetic Induction",
    "Current Electricity",
    "Gravitation",
    "Units and Measurements"
],

"Chemistry": [
    "Physical Chemistry",
    "Inorganic Chemistry",
    "Organic Chemistry Basics",
    "Hydrocarbons and Reaction Mechanisms",
    "Biomolecules and Polymers",
    "Chemistry in Everyday Life",
    "Environmental Chemistry"
],

"Biology": [
    "Diversity of the Living World",
    "Structural Organisation in Animals and Plants",
    "Cell Structure and Function",
    "Plant Physiology",
    "Human Physiology",
    "Reproduction",
    "Genetics and Evolution",
    "Biology and Human Welfare",
    "Biotechnology and Its Applications",
    "Ecology and Environment"
]

        },
        "UPSC": {
"History": [
    "Ancient History (NCERT + Culture)",
    "Medieval History",
    "Modern Indian History (18th century to present)",
    "Indian National Movement",
    "World History (Industrial Revolution, World Wars, Colonization, Decolonization, Political Philosophies)"
],

"Geography": [
    "Physical Geography (Geomorphology, Climatology, Oceanography)",
    "Indian Geography (Physiography, Drainage, Climate, Vegetation, Soils)",
    "Economic Geography (Agriculture, Resources, Industries)",
    "Human Geography (Population, Migration, Settlements)",
    "Environment and Ecology",
    "Disaster Management"
],

"Polity": [
    "Indian Constitution – Historical Underpinnings, Evolution, Features",
    "Union and State Government, Executive, Legislature, Judiciary",
    "Federalism, Centre-State Relations",
    "Local Self Government, Panchayati Raj",
    "Rights Issues (Fundamental Rights, DPSP, Fundamental Duties)",
    "Amendments and Constitutional Bodies",
    "Non-Constitutional Bodies",
    "Governance (Transparency, E-Governance, Citizen Charter, Accountability)"
],

"Economy": [
    "Basic Economic Concepts (NCERT)",
    "Indian Economy – Planning, Growth, Development",
    "Agriculture, Land Reforms",
    "Industrial Policy",
    "Infrastructure",
    "Inclusive Growth",
    "Government Budgeting",
    "External Sector – Balance of Payments, Foreign Trade",
    "Monetary Policy, Inflation",
    "Banking and Financial Sector",
    "Economic Survey and Budget"
],

"Science_and_Tech": [
    "NCERT Basics (Physics, Chemistry, Biology)",
    "Biotechnology",
    "Information Technology, Computers, Robotics, Nanotech",
    "Space Technology",
    "Nuclear Technology",
    "Health, Medicine and Diseases",
    "Environment and Climate Change",
    "Renewable Energy, Conservation"
],

"Ethics": [
    "Ethics and Human Interface",
    "Attitude, Emotional Intelligence",
    "Moral Thinkers and Philosophers (Indian and World)",
    "Public/Civil Service Values and Ethics in Public Administration",
    "Probity in Governance",
    "Case Studies"
],

"Essay": [
    "Current Issues",
    "Philosophical Topics",
    "Socio-economic Issues",
    "Science and Tech",
    "Ethics and Values"
],

"Current_Affairs": [
    "National Issues",
    "International Relations",
    "Government Policies and Schemes",
    "Reports, Indices and Organizations",
    "Social Justice (Health, Education, Women, Vulnerable Sections)"
],

"Optional_Subjects": [
    "Literature (Various Languages as per UPSC list)",
    "Humanities (History, Geography, Political Science, Sociology, Philosophy, Psychology, Public Administration, etc.)",
    "Science (Physics, Chemistry, Mathematics, Botany, Zoology, etc.)",
    "Commerce and Management",
    "Engineering (Civil, Mechanical, Electrical, etc.)"
]

        },
        "SSC/Banking": {
"Quant": [
    "Number System",
    "Simplification",
    "HCF and LCM",
    "Ratio and Proportion",
    "Percentage",
    "Average",
    "Problems on Ages",
    "Profit and Loss",
    "Discount",
    "Simple Interest",
    "Compound Interest",
    "Partnership",
    "Mixture and Alligation",
    "Time and Work",
    "Pipes and Cisterns",
    "Time, Speed and Distance",
    "Boats and Streams",
    "Mensuration (2D and 3D)",
    "Geometry",
    "Trigonometry",
    "Heights and Distances",
    "Algebra",
    "Linear and Quadratic Equations",
    "Coordinate Geometry",
    "Statistics",
    "Probability",
    "Data Interpretation (Tables, Graphs, Charts)"
],

"Reasoning": [
    "Analogy",
    "Classification",
    "Series (Number, Alphabet, Figure)",
    "Coding-Decoding",
    "Blood Relations",
    "Direction Sense",
    "Seating Arrangement",
    "Puzzles",
    "Order and Ranking",
    "Syllogism",
    "Venn Diagrams",
    "Clock and Calendar",
    "Decision Making",
    "Statement–Conclusion",
    "Statement–Assumption",
    "Non-Verbal Reasoning (Figure Classification, Mirror and Water Images, Paper Folding and Cutting, Embedded Figures, Cubes and Dice)"
],
        "Olympiads": {
"Mathematics": [
    "Number Theory",
    "Combinatorics",
    "Geometry (Euclidean, Coordinate, Vectors)",
    "Algebra (Polynomials, Inequalities, Equations)",
    "Functional Equations",
    "Sequences and Series",
    "Probability and Statistics",
    "Trigonometry",
    "Mathematical Induction",
    "Inequalities (Cauchy, AM-GM, Hölder, Jensen etc.)",
    "Graph Theory and Logic (basic)"
],

"Physics": [
    "Mechanics (Newtonian, Rotational, Rigid body)",
    "Oscillations and Waves",
    "Fluid Mechanics",
    "Electrostatics and Current Electricity",
    "Magnetism and Electromagnetic Induction",
    "Optics (Wave + Ray)",
    "Modern Physics (Relativity, Quantum basics)",
    "Thermodynamics & Kinetic Theory",
    "Advanced Problem Solving (IPhO level)"
],

"Chemistry": [
    "Physical Chemistry (Thermodynamics, Chemical Kinetics, Electrochemistry)",
    "Inorganic Chemistry (Periodic properties, Coordination Compounds, Qualitative Analysis)",
    "Organic Chemistry (Reaction Mechanisms, Named Reactions, Stereochemistry)",
    "Spectroscopy and Structure Determination",
    "Environmental Chemistry",
    "Practical Chemistry and Lab Techniques"
],

"Astronomy": [
    "Celestial Mechanics (Kepler’s laws, Orbits, Gravitation)",
    "Astronomical Instruments (Telescopes, CCDs, Spectroscopy)",
    "Stellar Physics (Life cycle of stars, HR diagram)",
    "Cosmology (Big Bang, Expansion, Dark Matter/Energy basics)",
    "Astrophysics (Radiation laws, Doppler effect, Blackbody radiation)",
    "Coordinate Systems in Astronomy (Equatorial, Horizontal, Ecliptic)"
],

"Biology": [
    "Cell Biology and Biochemistry",
    "Plant Physiology",
    "Human Physiology",
    "Genetics and Evolution",
    "Ecology and Biosphere",
    "Ethology (Animal Behavior)",
    "Applied Biology (Biotech, Immunology, Microbiology)"
]
        },

"English": [
    "Reading Comprehension",
    "Cloze Test",
    "Para Jumbles",
    "Error Spotting",
    "Sentence Improvement",
    "Fill in the Blanks",
    "One Word Substitution",
    "Idioms and Phrases",
    "Synonyms and Antonyms",
    "Spelling Test",
    "Active and Passive Voice",
    "Direct and Indirect Speech",
    "Vocabulary",
    "Grammar (Tenses, Articles, Prepositions, Conjunctions, Modals, Subject-Verb Agreement)"
],

"General_Awareness": [
    "History (Ancient, Medieval, Modern, Freedom Struggle)",
    "Geography (Physical, Indian, World)",
    "Indian Polity and Constitution",
    "Economics and Finance Basics",
    "Science (Physics, Chemistry, Biology – NCERT level)",
    "Environment and Ecology",
    "Current Affairs (National and International)",
    "Static GK (Important Dates, Books and Authors, Sports, Awards, Capitals and Currencies, Organizations)"
],

"Computer": [
    "Basics of Computers",
    "MS Office (Word, Excel, PowerPoint)",
    "Internet and Email",
    "Input and Output Devices",
    "Memory and Storage",
    "Networking Basics",
    "Cyber Security Basics",
    "Computer Abbreviations and Shortcuts"
]

        },
    }
    return topics_db.get(exam, {}).get(subject, ["Topic 1", "Topic 2", "Topic 3"])

def make_roadmap(exam, subjects, weak_subjects, hours_per_day, days_until_exam):
    # Create a list of daily tasks by prioritizing weak subjects
    days = max(7, int(days_until_exam))
    roadmap = {}
    # Weighted subject priority: weak subjects get double weight
    weights = {}
    for s in subjects:
        weights[s] = 2 if s in weak_subjects else 1
    total_weight = sum(weights.values())
    # daily hours distribution
    total_daily = float(hours_per_day)
    for day in range(1, days + 1):
        roadmap[f"Day {day}"] = []
        # for each subject allocate proportional time
        for s in subjects:
            share = weights[s] / total_weight
            hours = round(share * total_daily, 2)
            # pick topic for that subject in round-robin based on day
            topics = generate_topics_for_subject(exam, s)
            topic = topics[(day-1) % len(topics)]
            roadmap[f"Day {day}"].append({"subject": s, "topic": topic, "hours": hours})
    return roadmap

# simple NLP doubt solver: keyword -> answers
SYMBOLIC_FAQ = {
    "how to remember formulas": "Use spaced repetition apps (like Anki) and self-made flashcards. Revise formulas daily for 5–10 mins and test yourself weekly. Also, try deriving important formulas once in a while to strengthen memory.",
    "time management for JEE/NEET": "Divide your day into focused slots (2–3 hours each). Do Physics/Chemistry/Maths (or Biology) daily. Keep mornings for tough topics and evenings for revision. Always include at least one mock test every week.",
    "how to study NCERT effectively": "Underline key points, make margin notes, and solve all NCERT questions (including examples). For NEET, NCERT Biology line-by-line is non-negotiable. For UPSC/SSC, NCERT builds base for History, Geography, Science.",
    "how to improve in numericals": "Break problems into steps instead of rushing. Write given data properly, identify the formula, and solve systematically. Practice past year questions daily, and keep a formula sheet next to you while revising.",
    "how to master organic chemistry": "Focus on reaction mechanisms rather than mugging up. Make a flowchart for each reagent and its behavior. Revise named reactions frequently, and solve lots of mechanism-based questions to develop intuition.",
    "best revision strategy before exams": "Follow the 80/20 rule: revise high-weightage topics first. Use short notes and highlight mistakes from mock tests. Daily mini-revisions + weekly full-length revisions are key for long-term memory.",
    "mock test strategy": "Attempt under real exam conditions. Don’t panic if score is low—analyze mistakes, mark weak topics, and revise them immediately. Keep an error logbook so you never repeat the same mistake.",
    "how to avoid silly mistakes": "Always underline key words in the question. Double-check units, signs, and data before finalizing answers. Practice solving slowly at first, then build speed once accuracy is developed.",
    "how to increase speed in exams": "Use a timer while practicing. Develop shortcuts for repetitive calculations. Avoid getting stuck on one question; mark and move. Solve easy ones first, then return to tough ones.",
    "best timetable for school + coaching": "Wake up early and finish one tough subject in the morning. Use school hours for light revisions. After coaching, revise what was taught the same day. Dedicate weekends for mock tests and backlog clearance.",
    "how to balance boards with JEE/NEET": "Prepare NCERT thoroughly since it overlaps with competitive exams. While studying boards, also mark extra points relevant for JEE/NEET. Boards ensure your basics are solid; apply those concepts to advanced problems.",
    "how to improve focus while studying": "Keep distractions away (no phone during study blocks). Use Pomodoro (50 min study, 10 min break). Meditate for 5 mins daily to improve concentration. Study in a quiet, clutter-free space.",
    "how to remember reactions in chemistry": "Instead of mugging, understand the electron movement. Group reactions by mechanism (nucleophilic substitution, electrophilic addition, etc.). Revise daily with flashcards or a reaction chart on your wall.",
    "how to prepare for inorganic chemistry": "Make NCERT your Bible. Memorize periodic trends (atomic size, ionization energy, etc.). Use mnemonics for exceptions. Revise frequently since inorganic is more about memory than logic.",
    "how to prepare biology for NEET": "NCERT line by line is a must. Highlight and revise diagrams regularly. Make sticky notes for factual data (enzymes, hormones, cycles). Practice 100 MCQs daily to retain information.",
    "best strategy for maths in JEE": "Master basics first. Focus on Algebra, Calculus, and Coordinate Geometry since they carry maximum weight. Solve past year problems chapter-wise. Do mixed problem sets for exam temperament.",
    "how to prepare physics for NEET": "Clear NCERT concepts and practice numerical-based questions. Focus on Mechanics, Modern Physics, Optics, and Electrostatics. Use formula sheets and attempt chapter-wise PYQs.",
    "how to prepare current affairs for UPSC/SSC": "Read one reliable newspaper (The Hindu/Indian Express) and monthly current affairs magazines. Make short notes. Revise current events monthly and link them with static subjects.",
    "best books for JEE": "Physics: HC Verma + DC Pandey, Chemistry: NCERT + OP Tandon + MS Chauhan (Organic), Maths: NCERT + Cengage/ML Khanna. Always complement with PYQs.",
    "best books for NEET": "NCERT (especially Biology). For Physics: DC Pandey or BM Sharma, for Chemistry: NCERT + MS Chauhan (Organic) + N Awasthi (Physical). Practice NEET PYQs religiously.",
    "how to deal with exam stress": "Don’t compare your preparation with others. Take deep breaths and stay positive. Regular exercise or meditation helps. Focus on daily progress instead of final results.",
    "how many hours should I study daily": "Quality > quantity. 6–8 hours of focused study is enough if consistent. During peak preparation, students may go up to 10–12 hrs, but avoid burnout.",
    "is NCERT enough for NEET": "Yes, especially for Biology (almost 90% comes directly/indirectly from NCERT). Physics and Chemistry need NCERT + extra practice from reference books.",
    "is NCERT enough for JEE": "No. NCERT builds basics but you need additional books for JEE-level problems. NCERT is great for Inorganic and basics of Organic but not sufficient for problem-solving.",
    "how to stay consistent daily": "Don’t rely on motivation; rely on habits. Fix daily study slots and follow them. Even on low-energy days, study at least 2 hours so momentum isn’t broken.",
    "how to manage backlog": "Don’t try to finish everything at once. Parallel study: 70% time for current topics, 30% for backlog. Solve only important PYQs from backlog chapters.",
    "how to analyze mock test": "Divide into: silly mistakes, conceptual errors, and time management issues. Revise wrong questions and make error notes. Next test → aim to not repeat same errors.",
    "how to prepare GS for UPSC": "Start with NCERTs (6th–12th) for History, Geography, Polity, Economics. Then move to advanced books like Laxmikant (Polity), Spectrum (History), GC Leong (Geography).",
    "how to improve answer writing for UPSC": "Practice daily answer writing (10–15 mins). Use simple language, write in points, and add diagrams/maps wherever possible. Always stick to the word limit.",
    "how to prepare english for SSC": "Daily grammar practice + vocab building (read newspapers). Practice comprehension and cloze test daily. Mock tests will improve speed and accuracy.",
    "how to prepare reasoning for SSC": "Solve daily puzzles, series, coding-decoding. Time yourself while practicing. Learn shortcuts and common patterns (like blood relations, directions, syllogism).",
    "how to prepare quant for SSC": "Master Arithmetic first (percentages, ratios, profit & loss). Then move to Algebra & Geometry. Practice DI regularly. Solve past 10 years of SSC PYQs.",
    "how to avoid burnout": "Don’t overstudy without breaks. Take small hobbies/exercise breaks daily. Sleep at least 6–7 hrs. Remember, long-term consistency beats one-day overwork.",
    "what to do one day before exam": "Revise only short notes & formula sheets. Don’t start new topics. Sleep well. Keep all essentials (admit card, pens) ready at night. Stay calm and confident.",
    "how to attempt exam paper": "Start with your strongest section. Don’t get stuck—mark and move. Keep last 10 mins for review. Maintain accuracy in first attempt, speed in second.",
    "what to do after a bad mock test": "Don’t panic. Mocks are for learning, not judging. Focus on what went wrong—concepts, silly mistakes, or time management. Correct them before next test." ,
    "what is jee preparation roadmap": "Always start with the basics and lectures. If you do not go to some coaching , watch  lectures first, solve questions after watching every lecture. Then if you have time left, start solving other resources. " ,
    "how to prepare for upsc": "Begin with NCERTs for all subjects (6th–12th), move to standard books (Laxmikanth for Polity, Spectrum for History, GC Leong for Geography, etc.). Practice answer writing and revise current affairs daily.",
    "what is olympiad roadmap": """The Olympiad journey (for Physics, Chemistry, Maths, Biology) generally follows these stages:

1️⃣ **NSE (National Standard Examination)** – Conducted by IAPT (Physics, Chemistry, Biology, Astronomy) or INMO for Mathematics.  
   ↪ Top ~300 students qualify for next stage.

2️⃣ **INO (Indian National Olympiad)** – Subject-specific (INPhO, INChO, INBO, INAO, INMO).  
   ↪ Around 35 students per subject are selected.

3️⃣ **OCSC (Orientation-Cum-Selection Camp)** – A rigorous camp at HBCSE, Mumbai.  
   ↪ Top 4–5 students per subject are chosen for the international team.

4️⃣ **IPhO / IChO / IBO / IMO / IAO** – International Olympiads.  
   ↪ Represent India at the global level.

👉 Pro-tip: Along the way, focus on **NSE → INO → OCSC → IPhO/IChO/IMO/IBO**, while strengthening fundamentals (NCERT + Olympiad-specific books like HC Verma for Physics, OP Tandon for Chemistry, etc.).""",
}


def nlp_answer(question):
    q = question.lower()
    responses = []
    for k, v in SYMBOLIC_FAQ.items():
        if k in q:
            responses.append(v)
    # fallback: look for keywords
    if not responses:
        for key in ["remember", "time", "numerical", "organic", "revision", "mock"]:
            if key in q:
                responses.append(SYMBOLIC_FAQ.get("how to remember") if key == "remember" else SYMBOLIC_FAQ.get("time management"))
    if not responses:
        responses = ["I could not find an exact match. Try asking about study strategy, time management, revision, or specific subject topics."]
    return responses

def recommend_resources(exam, subjects=None):
    rec = {
        "JEE": {
            "Books": [
                "H.C. Verma – Concepts of Physics Vol 1 & 2",
                "I.E. Irodov – Problems in General Physics (for practice)",
                "DC Pandey / Physics Galaxy by Ashish Arora Sir (for best theory)",
                "O.P. Tandon – Physical & Organic Chemistry",
                "VK Jaiswal - Problems in Inorganic Chemistry",
                "Vikas Gupta and Pankaj Joshi - Black Book for JEE Mathematics",
                "Pradeep Chemistry (for basics)",
                "M.S. Chauhan – Organic Chemistry",
                "R.D. Sharma (for basics) / Cengage (Advanced Practice) / Arihant – Mathematics"
            ],
            "Online Platforms": [
                "NTA Abhyas App (free mock tests)",
                "Testbook App (free mock tests)",
                "Khan Academy (concept clarity)",
                "Unacademy / Vedantu (live classes & doubt solving)",
                "Past Year JEE Main + Advanced Papers"
            ],
            "Tips": [
                "Prioritize NCERT for Chemistry (esp. Inorganic).",
                "Solve at least 30–40 questions per topic.",
                "Weekly full-length timed mock tests."
            ]
        },

        "NEET": {
            "Books": [
                "NCERT Biology (11th & 12th – absolute must!)",
                "Trueman’s Biology (for detailed practice)",
                "O.P. Tandon – Physical & Organic Chemistry",
                "MTG NCERT at Your Fingertips – Biology, Physics, Chemistry",
                "Concepts of Physics – H.C. Verma (for basics)"
            ],
            "Online Platforms": [
                "Embibe (mock tests + analysis)",
                "Aakash / Allen digital modules",
                "BYJU'S & Khan Academy (concept videos)",
                "Past Year NEET Papers (at least last 10 years)"
            ],
            "Tips": [
                "Do NCERT Biology line by line.",
                "Focus on diagrams, cycles, and exceptions.",
                "Give regular chapter-wise and full syllabus tests."
            ]
        },

        "UPSC": {
            "Books": [
                "NCERTs (6th–12th History, Geography, Polity, Economics, Science)",
                "Laxmikanth – Indian Polity",
                "Spectrum – Modern Indian History",
                "Indian Economy by Ramesh Singh",
                "Environment by Shankar IAS Academy",
                "Indian Year Book (selective reading)"
            ],
            "Online Platforms": [
                "PRS India (Legislative updates)",
                "PIB (Press Information Bureau releases)",
                "ClearIAS, InsightsIAS, VisionIAS",
                "Rajya Sabha TV / Sansad TV debates"
            ],
            "Tips": [
                "Revise NCERTs thoroughly before moving to advanced sources.",
                "Focus on Current Affairs daily (The Hindu/Indian Express).",
                "Practice Mains answer writing + Previous year Prelims MCQs."
            ]
        },

        "SSC/Banking": {
            "Books": [
                "Quantitative Aptitude – R.S. Aggarwal",
                "Magical Book on Quicker Maths – M. Tyra",
                "Analytical Reasoning – M.K. Pandey",
                "A Modern Approach to Verbal & Non-Verbal Reasoning – R.S. Aggarwal",
                "Wren & Martin – English Grammar"
            ],
            "Online Platforms": [
                "Testbook / Adda247 (mocks + quizzes)",
                "Gradeup (BYJU'S Exam Prep)",
                "Oliveboard (for Banking aspirants)",
                "Unacademy SSC Courses"
            ],
            "Tips": [
                "Focus on accuracy + speed with timer-based practice.",
                "Daily current affairs & GK for SSC CGL/CHSL.",
                "Take at least 1 mock daily in exam season."
            ]
        },

        "Olympiads": {
            "Books": [
                "Mathematics: Problem-Solving Strategies (Arthur Engel), Challenge and Thrill of Pre-College Mathematics",
                "Physics: I.E. Irodov – Problems in General Physics, Pathfinder (IAPT), University Physics by Young & Freedman",
                "Chemistry: Atkins Physical Chemistry, Clayden Organic Chemistry, Inorganic by J.D. Lee",
                "Astronomy: Foundations of Astrophysics – Ryden & Peterson, Astronomy: Principles and Practice – Roy & Clarke",
                "Biology: Campbell Biology, Lehninger Biochemistry, Olympiad Biology Problem Books (IAPT)"
            ],
            "Online Platforms": [
                "IAPT Official Website (Indian Olympiads)",
                "Brilliant.org (Olympiad style problem solving)",
                "Art of Problem Solving (AoPS) – Olympiad Math",
                "Olympiads School / Physics Olympiad (IPhO training materials)",
                "HBCSE Olympiad resources (official past papers)"
            ],
            "Tips": [
                "Solve past year Olympiad papers (NSEP, NSEC, NSEB, NSEA, RMO, INMO etc.).",
                "Focus on deep understanding, not rote learning.",
                "Join problem-solving groups and discuss tough problems.",
                "Practice experimental/lab-based questions for Science Olympiads."
            ]
        }
    }

    # return logic
    if exam not in rec:
        return {}
    if subjects:
        return {exam: {sub: rec[exam][sub] for sub in subjects if sub in rec[exam]}}
    return rec[exam]

    # If subjects are given, filter recommendations
    base = rec.get(exam, {"Books": ["Standard Textbooks"], "Online Platforms": ["General resources"], "Tips": ["Stay consistent & practice regularly."]})
    
    if subjects:
        filtered = {key: [] for key in base}
        for subject in subjects:
            for key, items in base.items():
                filtered[key].extend([i for i in items if subject.lower() in i.lower()])
        return filtered if any(filtered.values()) else base
    
    return base


def save_pdf_report(filename, profile, roadmap, nlp_responses, cv_placeholder, resources, mock_scores):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "EduGuide AI - Personalized Roadmap", ln=True, align="C")
    pdf.ln(4)

    # profile
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Name: {profile.get('name','-')}  |  Exam: {profile.get('exam','-')}  |  Generated: {datetime.datetime.now().date()}", ln=True)
    pdf.ln(3)

    # study plan
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "Study Plan (First 7 days preview):", ln=True)
    pdf.set_font("Arial", "", 11)
    days = list(roadmap.keys())
    for d in days[:7]:
        pdf.multi_cell(0, 6, d + ":")
        for item in roadmap[d]:
            pdf.multi_cell(0, 6, f"  - {item['subject']}: {item['topic']} ({item['hours']} hrs)")
    pdf.ln(3)

    # NLP
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "AI Suggestions (from your doubts):", ln=True)
    pdf.set_font("Arial", "", 11)
    for r in nlp_responses:
        pdf.multi_cell(0, 6, f"- {r}")
    pdf.ln(3)

    # resources
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "Recommended Resources:", ln=True)
    pdf.set_font("Arial", "", 11)
    for r in resources.get("Global", []):
        pdf.multi_cell(0, 6, f"- {r}")
    pdf.ln(2)
    for r in resources.get("Online", []):
        pdf.multi_cell(0, 6, f"- {r}")
    pdf.ln(3)

    # mock scores summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "Mock Test Scores (history):", ln=True)

    def feedback(score):
        if score < 40:
            return ("Needs serious improvement. Focus on weak areas and revise basics.", (255, 0, 0))  # Red
        elif score < 60:
            return ("Average performance. Revise mistakes and practice more PYQs.", (255, 140, 0))  # Orange
        elif score < 80:
            return ("Good progress! Work on time management and accuracy.", (0, 0, 255))  # Blue
        elif score < 90:
            return ("Very good! Just polish concepts and focus on silly mistakes.", (0, 100, 0))  # Dark Green
        else:
            return ("Excellent performance! Maintain consistency and keep practicing.", (0, 200, 0))  # Bright Green

    pdf.set_font("Arial", "", 11)
    if mock_scores:
        for m in mock_scores:
            msg, color = feedback(m['score'])
            pdf.set_text_color(*color)
            pdf.multi_cell(0, 6, f"- {m['date']}: {m['score']}% → {msg}")
            pdf.set_text_color(0, 0, 0)  # reset back to black
    else:
        pdf.multi_cell(0, 6, "No mock tests recorded.")

    # disclaimer
    pdf.ln(6)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, "Disclaimer: This roadmap is an educational guideline generated by the EduGuide AI. It is not a substitute for a certified mentor.")
    pdf.set_text_color(0, 0, 0)

    pdf.output(filename)


# -------------------
# Streamlit UI
# -------------------
st.set_page_config(page_title="EduGuide AI - Smart Exam Mentor", layout="wide")
st.title("                     ヾ(•ω•`)o EduGuide AI —                     ")
st.markdown("Your Personal Mentor, Here to assist your every need possible.")

# Left - profile & plan
col1, col2 = st.columns([2,1])
with col1:
    st.header("Create your personalized roadmap")
    name = st.text_input("Your name")
    exam = st.selectbox("Which exam are you preparing for?", ["JEE", "NEET", "UPSC", "SSC/Banking", "Olympiads", "Other"])
    subjects_input = st.text_input("Subjects (comma separated). e.g. Physics,Chemistry,Maths")
    subjects = [s.strip() for s in subjects_input.split(",") if s.strip()] if subjects_input else []
    weak_input = st.text_input("Weak subjects/topics (comma separated). e.g. Organic,Algebra")
    weak_subjects = [s.strip() for s in weak_input.split(",") if s.strip()]
    hours_per_day = st.number_input("Available hours per day", min_value=1.0, max_value=16.0, value=4.0, step=0.5)
    days_until = st.number_input("Days until exam (approx)", min_value=7, max_value=365, value=90, step=1)

    if st.button("Generate Roadmap"):
        if not subjects:
            st.error("Please enter at least one subject.")
        else:
            roadmap = make_roadmap(exam, subjects, weak_subjects, hours_per_day, days_until)
            st.success("Roadmap generated! Scroll down to view a preview.")
            st.session_state["roadmap"] = roadmap
            st.session_state["profile"] = {"name": name, "exam": exam, "subjects": subjects, "weak": weak_subjects, "hours": hours_per_day, "days_until": days_until}
    # preview
    if "roadmap" in st.session_state:
        st.subheader("Roadmap preview (first 7 days)")
        roadmap = st.session_state["roadmap"]
        for d in list(roadmap.keys())[:7]:
            st.markdown(f"{d}")
            for item in roadmap[d]:
                st.markdown(f"- {item['subject']} — {item['topic']} ({item['hours']} hrs)")

with col2:
    st.header("Doubt Solver")
    question = st.text_area("Ask a study question (e.g. 'How to manage time for JEE?')", height=120)
    if st.button("Get Suggestion"):
        if question.strip() == "":
            st.info("Type a question about strategy, revision, mock tests, or subject problems.")
        else:
            answers = nlp_answer(question)
            st.session_state["nlp_answers"] = answers
    if "nlp_answers" in st.session_state:
        st.subheader("Suggestions")
        for a in st.session_state["nlp_answers"]:
            st.write("-", a)

# Resources & progress
st.markdown("---")
col3, col4 = st.columns([2,1])
with col3:
    st.header("Recommended Resources")
    chosen_exam = st.selectbox("Select exam to get recommended resources", ["JEE","NEET","UPSC","SSC/Banking","Olympiads","Other"], index=0)
    recs = recommend_resources(chosen_exam, [])
    st.write("*Books / Offline*")
    for r in recs.get("Global", []):
        st.write("-", r)
    st.write("*Online resources*")
    for r in recs.get("Online", []):
        st.write("-", r)

with col4:
    st.header("Mock Test Tracker")
    if "mock_scores" not in st.session_state:
        st.session_state["mock_scores"] = []
    score = st.number_input("Enter mock test score (%)", min_value=0, max_value=100, step=1)
    if st.button("Add Score"):
        st.session_state["mock_scores"].append({"date": str(datetime.date.today()), "score": score})
        st.success("Score added.")
    st.subheader("History")
    for m in st.session_state["mock_scores"]:
        st.write(f"- {m['date']}: {m['score']}%")

# Export PDF
st.markdown("---")
st.header("Export personalized PDF")
if st.button("Generate PDF Report"):
    profile = st.session_state.get("profile", {"name": name or "Student", "exam": exam})
    roadmap = st.session_state.get("roadmap", make_roadmap(exam, subjects or ["General"], weak_subjects or [], hours_per_day, days_until))
    nlp_ans = st.session_state.get("nlp_answers", [])
    recs = recommend_resources(profile.get("exam", exam), subjects)
    mock_scores = st.session_state.get("mock_scores", [])
    filename = "EduGuide_Personal_Roadmap.pdf"
    save_pdf_report(filename, profile, roadmap, nlp_ans, None, recs, mock_scores)
    st.success(f"PDF saved as {filename} in the project folder.")
    st.markdown("Open the file in your project folder to print or submit.")







