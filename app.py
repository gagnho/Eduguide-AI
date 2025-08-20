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
            "Physics": ["Mechanics", "Electrodynamics", "Waves & Optics", "Modern Physics", "Thermal physics"],
            "Chemistry": ["Physical Chemistry", "Organic Basics", "Inorganic Chemistry", "Reaction Mechanisms"],
            "Maths": ["Algebra", "Calculus", "Coordinate Geometry", "Trigonometry"]
        },
        "NEET": {
            "Physics": ["Mechanics", "Thermodynamics", "Electrodynamics", "Modern Physics"],
            "Chemistry": ["Physical Chemistry", "Organic Basics", "Inorganic Trends"],
            "Biology": ["Botany", "Zoology", "Human Physiology", "Genetics"]
        },
        "UPSC": {
            "History": ["Ancient", "Medieval", "Modern"],
            "Geography": ["Physical", "Human", "Indian"],
            "Polity": ["Constitution", "Governance", "Public Policy"],
            "Economics": ["Micro", "Macro", "Indian Economy"]
        },
        "SSC/Banking": {
            "Quant": ["Arithmetic", "Algebra", "Data Interpretation"],
            "Reasoning": ["Verbal", "Non-Verbal", "Puzzle"],
            "English": ["Grammar", "Comprehension", "Vocabulary"]
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
    "how to remember": "Use spaced repetition + flashcards. Revise important formulas daily and do quick weekly revisions.",
    "time management": "Create a weekly timetable; do high-weightage topics first and allocate at least one mock test per week.",
    "numericals": "Practice step-by-step, solve past year problems, and revise concept-wise formula sheet.",
    "organic": "Make reaction maps, practice mechanism questions and revise named reactions frequently.",
    "revision": "Make short notes and solve quizzes. Use the 80/20 rule: revise the 20% topics that give 80% questions.",
    "mock test": "Simulate exam conditions, analyze mistakes, and convert weaknesses into dedicated practice slots."
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

def recommend_resources(exam, subjects):
    rec = {
        "JEE": {
            "Global": ["H.C. Verma (Physics)", "O.P. Tandon (Chemistry)", "R.D. Sharma (Maths)"],
            "Online": ["Khan Academy", "NTA/JEE official resources", "Past year question papers"]
        },
        "NEET": {
            "Global": ["NCERT Biology", "O.P. Tandon (Chemistry)", "Concepts of Physics"],
            "Online": ["Embibe", "BYJU'S (concept videos)", "Past year papers"]
        },
        "UPSC": {
            "Global": ["NCERTs (History/Geography)", "Laxmikanth (Polity)", "Indian Year Book"],
            "Online": ["PRS India", "PIB", "ClearIAS"]
        },
        "SSC/Banking": {
            "Global": ["Quantitative Aptitude (R.S. Aggarwal)", "Reasoning (R.S. Aggarwal)", "Wren & Martin (English)"],
            "Online": ["Gradeup", "Unacademy", "Test series"]
        }
    }
    base = rec.get(exam, {"Global": ["Standard Textbooks"], "Online": ["Online resources"]})
    return base

def save_pdf_report(filename, profile, roadmap, nlp_responses, cv_placeholder, resources, mock_scores):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "EduGuide AI - Personalized Roadmap", ln=True, align="C")
    pdf.ln(4)
    pdf.set_font("Arial", "", 11)
    # profile
    pdf.cell(0, 7, f"Name: {profile.get('name','-')}  |  Exam: {profile.get('exam','-')}  |  Generated: {datetime.datetime.now().date()}", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "Study Plan (First 7 days preview):", ln=True)
    pdf.set_font("Arial", "", 11)
    # show first 7 days
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
    pdf.set_font("Arial", "", 11)
    if mock_scores:
        for m in mock_scores:
            pdf.multi_cell(0, 6, f"- {m['date']}: {m['score']}%")
    else:
        pdf.multi_cell(0, 6, "No mock tests recorded.")
    pdf.ln(6)
    pdf.set_font("Arial", "I", 9)
    pdf.multi_cell(0, 6, "Disclaimer: This roadmap is an educational guideline generated by the EduGuide AI prototype. It is not a substitute for a certified mentor.")
    pdf.output(filename)

# -------------------
# Streamlit UI
# -------------------
st.set_page_config(page_title="EduGuide AI - Smart Exam Mentor", layout="wide")
st.title("🎯 EduGuide AI — Smart Exam Mentor (Prototype)")
st.markdown("Personalized roadmaps, doubt solver, progress tracker. Educational demo.")

# Left - profile & plan
col1, col2 = st.columns([2,1])
with col1:
    st.header("Create your personalized roadmap")
    name = st.text_input("Your name")
    exam = st.selectbox("Which exam are you preparing for?", ["JEE", "NEET", "UPSC", "SSC/Banking", "Other"])
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
    chosen_exam = st.selectbox("Select exam to get recommended resources", ["JEE","NEET","UPSC","SSC/Banking","Other"], index=0)
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

