import json
from datetime import datetime, timedelta
from typing import Dict, List

import streamlit as st

# Optional OpenAI integration.
# The app still works without an API key using built-in logic.
try:
    from openai import OpenAI
except Exception:
    OpenAI = None


# --------------------------------------------------
# BUILT-IN KNOWLEDGE BASE
# --------------------------------------------------
TOPIC_BANK: Dict[str, Dict] = {
    "python": {
        "summary": "Python is a high-level programming language known for readable syntax, flexibility, and strong support for data analysis, web apps, automation, and AI.",
        "key_points": [
            "Uses indentation to define blocks of code.",
            "Common data types include int, float, str, list, tuple, and dict.",
            "Functions are created using def.",
            "if, elif, and else are used for decision-making.",
            "for and while loops repeat actions.",
        ],
        "quiz": [
            {
                "question": "What keyword is used to create a function in Python?",
                "options": ["func", "def", "create", "lambda"],
                "answer": "def",
            },
            {
                "question": "Which data type stores key-value pairs?",
                "options": ["list", "tuple", "dict", "set"],
                "answer": "dict",
            },
            {
                "question": "What does an if statement do?",
                "options": [
                    "Repeats code forever",
                    "Imports a library",
                    "Makes a decision based on a condition",
                    "Creates a database",
                ],
                "answer": "Makes a decision based on a condition",
            },
        ],
    },
    "sql": {
        "summary": "SQL is a language used to manage and query relational databases. It helps store, retrieve, update, and analyze structured data.",
        "key_points": [
            "SELECT reads data from a table.",
            "INSERT adds new rows.",
            "UPDATE changes existing rows.",
            "DELETE removes rows.",
            "WHERE filters records.",
        ],
        "quiz": [
            {
                "question": "Which SQL command is used to read data from a table?",
                "options": ["GET", "SELECT", "READ", "SHOW"],
                "answer": "SELECT",
            },
            {
                "question": "Which clause filters rows in SQL?",
                "options": ["SORT", "WHERE", "GROUP", "LIMIT"],
                "answer": "WHERE",
            },
            {
                "question": "What does INSERT do?",
                "options": [
                    "Deletes a table",
                    "Adds new records",
                    "Sorts records",
                    "Calculates averages",
                ],
                "answer": "Adds new records",
            },
        ],
    },
    "data analysis": {
        "summary": "Data analysis is the process of inspecting, cleaning, organizing, and interpreting data to answer questions and support decisions.",
        "key_points": [
            "Start by understanding the business question.",
            "Clean missing, duplicate, or inconsistent data.",
            "Explore patterns using summary statistics and charts.",
            "Interpret findings in a business context.",
            "Communicate results clearly.",
        ],
        "quiz": [
            {
                "question": "What usually comes first in data analysis?",
                "options": [
                    "Building a dashboard",
                    "Understanding the question",
                    "Deleting all outliers",
                    "Writing conclusions",
                ],
                "answer": "Understanding the question",
            },
            {
                "question": "Why is data cleaning important?",
                "options": [
                    "To make charts colorful",
                    "To improve data quality",
                    "To reduce file size only",
                    "To avoid asking questions",
                ],
                "answer": "To improve data quality",
            },
            {
                "question": "Which is part of analysis communication?",
                "options": [
                    "Hiding results",
                    "Explaining findings clearly",
                    "Ignoring business impact",
                    "Using random metrics",
                ],
                "answer": "Explaining findings clearly",
            },
        ],
    },
    "finance": {
        "summary": "Finance studies how money is managed, invested, borrowed, and used in business and personal decisions.",
        "key_points": [
            "Revenue is money earned.",
            "Expenses are costs incurred.",
            "Profit equals revenue minus expenses.",
            "Risk and return are closely related.",
            "Budgeting helps plan financial resources.",
        ],
        "quiz": [
            {
                "question": "What is profit?",
                "options": [
                    "Revenue + expenses",
                    "Revenue - expenses",
                    "Expenses - revenue",
                    "Assets - liabilities",
                ],
                "answer": "Revenue - expenses",
            },
            {
                "question": "Which concept reflects uncertainty in outcomes?",
                "options": ["Risk", "Revenue", "Budget", "Payroll"],
                "answer": "Risk",
            },
            {
                "question": "What does budgeting help with?",
                "options": [
                    "Ignoring costs",
                    "Planning resources",
                    "Removing income",
                    "Avoiding analysis",
                ],
                "answer": "Planning resources",
            },
        ],
    },
}


# --------------------------------------------------
# CAREER + SKILL FORECAST DATA
# --------------------------------------------------
CAREER_BANK: Dict[str, Dict] = {
    "data analyst": {
        "match_keywords": ["excel", "sql", "python", "power bi", "tableau", "statistics", "analysis"],
        "description": "Data analysts turn raw data into insights for business decisions.",
        "future_demand": "High",
        "salary_band": "$60,000 - $95,000",
        "core_skills": ["Excel", "SQL", "Python", "Power BI", "Statistics", "Data Visualization"],
        "recommended_learning": ["Dashboard design", "Data cleaning", "Business storytelling", "Forecasting"],
        "industries": ["Finance", "Retail", "Healthcare", "Consulting"],
    },
    "business analyst": {
        "match_keywords": ["analysis", "excel", "sql", "requirements", "process", "power bi", "communication"],
        "description": "Business analysts connect business needs with data, systems, and process improvements.",
        "future_demand": "High",
        "salary_band": "$65,000 - $105,000",
        "core_skills": ["Excel", "SQL", "Process Analysis", "Requirements Gathering", "Power BI", "Communication"],
        "recommended_learning": ["Process mapping", "Stakeholder management", "KPI design", "Documentation"],
        "industries": ["Banking", "Technology", "Healthcare", "Operations"],
    },
    "financial analyst": {
        "match_keywords": ["finance", "excel", "valuation", "forecasting", "budgeting", "accounting", "analysis"],
        "description": "Financial analysts evaluate performance, create forecasts, and support investment or budgeting decisions.",
        "future_demand": "High",
        "salary_band": "$65,000 - $110,000",
        "core_skills": ["Excel", "Financial Modeling", "Forecasting", "Accounting", "PowerPoint", "Business Writing"],
        "recommended_learning": ["Valuation", "Scenario analysis", "Variance analysis", "Presentation skills"],
        "industries": ["Banking", "Corporate Finance", "Investment Firms", "Insurance"],
    },
    "data scientist": {
        "match_keywords": ["python", "machine learning", "statistics", "sql", "modeling", "ai", "pandas"],
        "description": "Data scientists build predictive models and extract advanced insights from complex datasets.",
        "future_demand": "Very High",
        "salary_band": "$90,000 - $145,000",
        "core_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "Model Evaluation"],
        "recommended_learning": ["Scikit-learn", "Feature engineering", "Model deployment", "Experiment design"],
        "industries": ["Technology", "Finance", "Healthcare", "E-commerce"],
    },
    "ai product analyst": {
        "match_keywords": ["ai", "product", "analysis", "sql", "python", "metrics", "experimentation"],
        "description": "AI product analysts evaluate product performance, user behavior, and AI feature impact.",
        "future_demand": "Very High",
        "salary_band": "$80,000 - $130,000",
        "core_skills": ["SQL", "Product Metrics", "Python", "Experimentation", "Dashboarding", "Communication"],
        "recommended_learning": ["A/B testing", "LLM evaluation", "User analytics", "Product strategy"],
        "industries": ["Technology", "EdTech", "FinTech", "SaaS"],
    },
}

SKILL_DEMAND: Dict[str, str] = {
    "excel": "High",
    "sql": "Very High",
    "python": "Very High",
    "power bi": "High",
    "tableau": "High",
    "statistics": "High",
    "machine learning": "Very High",
    "financial modeling": "High",
    "forecasting": "High",
    "data visualization": "High",
    "communication": "Very High",
    "requirements gathering": "High",
    "a/b testing": "High",
    "product metrics": "High",
}


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def normalize_topic(topic: str) -> str:
    return topic.strip().lower()


def get_topic_data(topic: str):
    return TOPIC_BANK.get(normalize_topic(topic))


def explain_topic(topic: str, difficulty: str) -> str:
    topic_data = get_topic_data(topic)
    if not topic_data:
        return (
            f"I do not have a built-in lesson for '{topic}' yet. "
            "You can still use the custom AI mode with an API key, or add this topic to the knowledge base."
        )

    summary = topic_data["summary"]
    key_points = topic_data["key_points"]

    if difficulty == "Beginner":
        intro = f"Here is a beginner-friendly explanation of {topic.title()}:\n\n{summary}\n\n"
    elif difficulty == "Intermediate":
        intro = f"Here is an intermediate explanation of {topic.title()}:\n\n{summary}\n\n"
    else:
        intro = f"Here is an advanced review of {topic.title()}:\n\n{summary}\n\n"

    bullet_text = "\n".join([f"- {point}" for point in key_points])
    return intro + "Key points:\n" + bullet_text


def generate_quiz(topic: str) -> List[Dict]:
    topic_data = get_topic_data(topic)
    if not topic_data:
        return []
    return topic_data["quiz"]


def grade_quiz(quiz: List[Dict], responses: Dict[str, str]) -> Dict:
    score = 0
    feedback = []

    for idx, item in enumerate(quiz, start=1):
        user_answer = responses.get(f"q_{idx}")
        correct_answer = item["answer"]
        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1
        feedback.append(
            {
                "question": item["question"],
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "result": "Correct" if is_correct else "Incorrect",
            }
        )

    total = len(quiz)
    percent = round((score / total) * 100, 1) if total else 0.0

    if percent >= 80:
        level_feedback = "Strong understanding. You are doing very well."
    elif percent >= 60:
        level_feedback = "Decent understanding, but some review would help."
    else:
        level_feedback = "You should review the topic again before moving on."

    return {
        "score": score,
        "total": total,
        "percent": percent,
        "level_feedback": level_feedback,
        "details": feedback,
    }


def build_study_plan(topic: str, hours_per_week: int, exam_date: datetime) -> List[Dict]:
    today = datetime.today().date()
    days_left = max((exam_date.date() - today).days, 1)
    weeks_left = max(round(days_left / 7), 1)

    steps = [
        f"Understand the core concepts of {topic.title()}",
        f"Review examples and worked problems in {topic.title()}",
        f"Practice short questions on {topic.title()}",
        f"Take a self-quiz and correct mistakes in {topic.title()}",
        "Revise weak areas and summarize notes",
    ]

    plan = []
    for week in range(1, weeks_left + 1):
        task = steps[(week - 1) % len(steps)]
        plan.append(
            {
                "week": week,
                "focus": task,
                "recommended_hours": hours_per_week,
            }
        )
    return plan


def clean_skill_list(skills_text: str) -> List[str]:
    raw_skills = [item.strip().lower() for item in skills_text.split(",") if item.strip()]
    return raw_skills


def career_skill_forecast(skills_text: str, major: str, interests: str) -> Dict:
    skills = clean_skill_list(skills_text)
    scored_roles = []

    for role, data in CAREER_BANK.items():
        matched_skills = [skill for skill in skills if skill in [k.lower() for k in data["match_keywords"]] or skill in [c.lower() for c in data["core_skills"]]]
        score = len(set(matched_skills))

        if major.strip():
            if "business" in major.lower() and role in {"business analyst", "financial analyst", "data analyst", "ai product analyst"}:
                score += 1
            if "computer" in major.lower() or "information" in major.lower() or "cis" in major.lower():
                if role in {"data analyst", "business analyst", "data scientist", "ai product analyst"}:
                    score += 1
            if "finance" in interests.lower() and role in {"financial analyst", "data analyst", "business analyst"}:
                score += 1
            if "ai" in interests.lower() and role in {"data scientist", "ai product analyst"}:
                score += 1

        scored_roles.append(
            {
                "role": role,
                "score": score,
                "matched_skills": matched_skills,
                "details": data,
            }
        )

    scored_roles.sort(key=lambda item: item["score"], reverse=True)
    top_roles = scored_roles[:3]

    all_missing_skills = []
    for role_data in top_roles:
        for skill in role_data["details"]["core_skills"]:
            if skill.lower() not in skills:
                all_missing_skills.append(skill)

    unique_missing = []
    for skill in all_missing_skills:
        if skill not in unique_missing:
            unique_missing.append(skill)

    prioritized_skills = sorted(
        unique_missing,
        key=lambda skill: {"Very High": 3, "High": 2}.get(SKILL_DEMAND.get(skill.lower(), "Moderate"), 1),
        reverse=True,
    )

    return {
        "top_roles": top_roles,
        "priority_skills": prioritized_skills[:6],
        "current_skills": skills,
    }


def build_career_roadmap(forecast_result: Dict) -> List[Dict]:
    roadmap = []
    priority_skills = forecast_result["priority_skills"]

    steps = [
        "Build foundations in core analytical tools",
        "Practice with hands-on projects and portfolios",
        "Develop communication and business storytelling",
        "Apply skills in a domain-specific case study",
        "Prepare for internships, networking, and interviews",
    ]

    for idx, step in enumerate(steps, start=1):
        skill_focus = priority_skills[idx - 1] if idx - 1 < len(priority_skills) else "Project refinement"
        roadmap.append(
            {
                "phase": idx,
                "goal": step,
                "skill_focus": skill_focus,
            }
        )
    return roadmap


def ask_openai(api_key: str, prompt: str, mode: str) -> str:
    if OpenAI is None:
        return "OpenAI package is not installed. Install it with: pip install openai"

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are an AI teaching assistant and career intelligence coach. Explain concepts clearly, "
        "use structured answers, and adapt to student-friendly language."
    )

    if mode == "Teach":
        user_prompt = f"Teach this topic clearly with examples: {prompt}"
    elif mode == "Quiz":
        user_prompt = (
            f"Create 5 multiple-choice quiz questions with answers for this topic: {prompt}. "
            "Return valid JSON as a list of objects with keys question, options, answer."
        )
    elif mode == "Study Plan":
        user_prompt = f"Make a concise study plan for this topic: {prompt}"
    else:
        user_prompt = (
            "Act like an AI skill forecasting platform for students. "
            f"Use this information: {prompt}. "
            "Recommend 3 suitable career paths, the top in-demand skills to learn next, why they fit, and a short roadmap."
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------
st.set_page_config(page_title="AI Teaching & Skill Forecast Assistant", page_icon="🎓", layout="wide")

st.title("🎓 AI Teaching & Skill Forecast Assistant")
st.caption(
    "An interactive learning platform that explains topics, builds quizzes and study plans, and recommends future career skills."
)

with st.sidebar:
    st.header("How it works")
    st.write("1. Pick a mode.")
    st.write("2. Enter a topic or skill profile.")
    st.write("3. Use built-in logic or optional AI mode with an API key.")
    st.markdown("---")
    st.subheader("Learning modes")
    st.write("- Teach")
    st.write("- Quiz")
    st.write("- Study Plan")
    st.write("- Career & Skill Forecast")
    st.markdown("---")
    st.subheader("Built-in topics")
    st.write("- Python")
    st.write("- SQL")
    st.write("- Data Analysis")
    st.write("- Finance")

mode = st.selectbox(
    "Choose mode",
    ["Teach", "Quiz", "Study Plan", "Career & Skill Forecast"],
)

use_ai = st.toggle("Use OpenAI API for custom AI responses", value=False)
api_key = ""
if use_ai:
    api_key = st.text_input("Enter OpenAI API key", type="password")

if mode in {"Teach", "Quiz", "Study Plan"}:
    col1, col2 = st.columns([2, 1])

    with col1:
        topic = st.text_input("Enter a topic", value="Python")

    with col2:
        difficulty = st.selectbox("Difficulty level", ["Beginner", "Intermediate", "Advanced"])

    if mode == "Teach":
        if st.button("Explain Topic", type="primary"):
            if use_ai and api_key:
                result = ask_openai(api_key, f"Topic: {topic}. Difficulty: {difficulty}", "Teach")
                st.markdown("### AI Explanation")
                st.write(result)
            else:
                lesson = explain_topic(topic, difficulty)
                st.markdown("### Lesson")
                st.write(lesson)

    elif mode == "Quiz":
        if st.button("Generate Quiz", type="primary"):
            if use_ai and api_key:
                raw = ask_openai(api_key, topic, "Quiz")
                st.session_state["quiz_source"] = "ai"
                st.session_state["ai_quiz_raw"] = raw
            else:
                quiz = generate_quiz(topic)
                st.session_state["quiz_source"] = "built_in"
                st.session_state["quiz_data"] = quiz

        if st.session_state.get("quiz_source") == "built_in":
            quiz_data = st.session_state.get("quiz_data", [])
            if quiz_data:
                st.markdown("### Quiz")
                responses = {}
                for idx, item in enumerate(quiz_data, start=1):
                    responses[f"q_{idx}"] = st.radio(
                        f"Q{idx}. {item['question']}",
                        item["options"],
                        key=f"quiz_{idx}",
                    )

                if st.button("Submit Quiz"):
                    result = grade_quiz(quiz_data, responses)
                    st.success(f"Score: {result['score']} / {result['total']} ({result['percent']}%)")
                    st.write(result["level_feedback"])
                    with st.expander("Detailed Feedback"):
                        st.json(result["details"])
            else:
                st.info("No built-in quiz found for that topic. Use AI mode for custom quizzes.")

        elif st.session_state.get("quiz_source") == "ai":
            st.markdown("### AI Quiz Output")
            st.code(st.session_state.get("ai_quiz_raw", ""), language="json")
            st.caption("You can keep this as JSON output or extend the app to render the AI quiz as interactive questions.")

    else:
        col3, col4 = st.columns([1, 1])
        with col3:
            hours_per_week = st.slider("Study hours per week", 1, 20, 5)
        with col4:
            exam_date = st.date_input("Exam date", value=datetime.today() + timedelta(days=21))

        if st.button("Build Study Plan", type="primary"):
            if use_ai and api_key:
                result = ask_openai(
                    api_key,
                    f"Topic: {topic}. Difficulty: {difficulty}. Hours per week: {hours_per_week}. Exam date: {exam_date}",
                    "Study Plan",
                )
                st.markdown("### AI Study Plan")
                st.write(result)
            else:
                plan = build_study_plan(topic, hours_per_week, datetime.combine(exam_date, datetime.min.time()))
                st.markdown("### Weekly Study Plan")
                for item in plan:
                    st.markdown(
                        f"**Week {item['week']}** — {item['focus']}  \\nRecommended study time: **{item['recommended_hours']} hours**"
                    )

else:
    st.markdown("### Student Profile")
    c1, c2 = st.columns(2)
    with c1:
        major = st.text_input("Major", value="Computer Information Systems")
        current_skills = st.text_area(
            "Current skills (comma-separated)",
            value="Excel, SQL, Python, Power BI, communication",
        )
    with c2:
        interests = st.text_input("Career interests", value="business analytics, finance, AI")
        target_role = st.text_input("Dream role (optional)", value="Business Analyst")

    if st.button("Forecast Career Paths", type="primary"):
        if use_ai and api_key:
            ai_prompt = (
                f"Major: {major}. Current skills: {current_skills}. Interests: {interests}. Target role: {target_role}."
            )
            result = ask_openai(api_key, ai_prompt, "Career & Skill Forecast")
            st.markdown("### AI Career Forecast")
            st.write(result)
        else:
            forecast = career_skill_forecast(current_skills, major, interests)
            roadmap = build_career_roadmap(forecast)

            st.markdown("### Recommended Career Paths")
            for idx, role_data in enumerate(forecast["top_roles"], start=1):
                details = role_data["details"]
                st.markdown(f"**{idx}. {role_data['role'].title()}**")
                st.write(details["description"])
                st.write(f"**Demand:** {details['future_demand']}")
                st.write(f"**Estimated salary band:** {details['salary_band']}")
                st.write(f"**Best-fit industries:** {', '.join(details['industries'])}")
                st.write(f"**Matched skills:** {', '.join(role_data['matched_skills']) if role_data['matched_skills'] else 'No direct matches yet'}")
                st.write(f"**Core skills for this role:** {', '.join(details['core_skills'])}")
                st.write(f"**Recommended next learning areas:** {', '.join(details['recommended_learning'])}")
                st.markdown("---")

            st.markdown("### Top Skills to Learn Next")
            for skill in forecast["priority_skills"]:
                st.write(f"- {skill} ({SKILL_DEMAND.get(skill.lower(), 'Moderate')} demand)")

            st.markdown("### Suggested Career Roadmap")
            for item in roadmap:
                st.markdown(
                    f"**Phase {item['phase']}** — {item['goal']}  \\nSkill focus: **{item['skill_focus']}**"
                )

            st.markdown("### Innovation Insight")
            st.info(
                "This feature simulates an AI skill forecasting platform by matching current student skills to future-ready career paths and identifying the highest-priority skills to learn next."
            )

st.markdown("---")
st.markdown(
    """
**Run locally**
```bash
pip install streamlit openai
streamlit run ai_teaching_assistant_streamlit_app.py
```
"""
)
