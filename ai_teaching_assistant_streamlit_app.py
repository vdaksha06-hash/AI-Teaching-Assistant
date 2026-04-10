import math
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Learning Twin", layout="wide")

CAREER_MODELS = {
    "Data Analyst": {
        "Analytics": 92,
        "Technology": 85,
        "Communication": 72,
        "Adaptability": 78,
        "Leadership": 48,
        "Creativity": 66,
    },
    "Product Manager": {
        "Analytics": 74,
        "Technology": 68,
        "Communication": 88,
        "Adaptability": 84,
        "Leadership": 80,
        "Creativity": 76,
    },
    "AI Business Strategist": {
        "Analytics": 90,
        "Technology": 88,
        "Communication": 79,
        "Adaptability": 90,
        "Leadership": 70,
        "Creativity": 71,
    },
    "UX Researcher": {
        "Analytics": 65,
        "Technology": 54,
        "Communication": 84,
        "Adaptability": 74,
        "Leadership": 52,
        "Creativity": 90,
    },
}

LEARNING_RESOURCES = {
    "Analytics": ["Excel & Power BI", "SQL Foundations", "Applied Statistics"],
    "Technology": ["Python for Business", "AI Literacy", "Cloud & Data Tools"],
    "Communication": ["Business Communication", "Presentation Skills", "Stakeholder Storytelling"],
    "Adaptability": ["Agile Problem Solving", "Scenario Planning", "Change Readiness"],
    "Leadership": ["Project Leadership", "Team Management Basics", "Decision-Making in Uncertainty"],
    "Creativity": ["Design Thinking", "Innovation Strategy", "Product Ideation Workshop"],
}


def clamp(value: float) -> int:
    return max(0, min(100, round(value)))


def build_student_profile(
    gpa: float,
    study_hours: int,
    ai_literacy: int,
    communication: int,
    stress_management: int,
    teamwork: int,
) -> dict:
    return {
        "Analytics": clamp(gpa * 18 + study_hours * 2 + ai_literacy * 0.15),
        "Technology": clamp(ai_literacy * 0.85 + study_hours * 1.8),
        "Communication": clamp(communication),
        "Adaptability": clamp((stress_management + teamwork) / 2 + study_hours * 0.7),
        "Leadership": clamp(teamwork * 0.75 + communication * 0.25),
        "Creativity": clamp((communication * 0.35 + stress_management * 0.25 + ai_literacy * 0.3) * 0.9),
    }


def calculate_readiness(student_profile: dict, target_profile: dict) -> tuple[int, list[dict]]:
    keys = list(target_profile.keys())
    readiness = round(
        sum(min(student_profile[k] / target_profile[k], 1) for k in keys) / len(keys) * 100
    )

    gaps = []
    for key in keys:
        gap = max(0, target_profile[key] - student_profile[key])
        gaps.append(
            {
                "Skill": key,
                "Current": student_profile[key],
                "Target": target_profile[key],
                "Gap": gap,
            }
        )

    gaps.sort(key=lambda item: item["Gap"], reverse=True)
    return readiness, gaps


def build_action_plan(gaps: list[dict]) -> list[str]:
    top_gaps = [gap for gap in gaps if gap["Gap"] > 0][:3]
    if not top_gaps:
        return [
            "Maintain your current profile with advanced projects.",
            "Add an industry certification to strengthen employability.",
            "Build a portfolio to demonstrate workforce readiness.",
        ]

    phases = []
    for index, gap in enumerate(top_gaps, start=1):
        resource = LEARNING_RESOURCES[gap["Skill"]][0]
        phases.append(f"Phase {index}: Improve {gap['Skill']} through {resource}.")
    return phases


st.title("🧠 AI Learning Twin")
st.caption("A Streamlit prototype for predicting future skill gaps and career readiness.")

with st.sidebar:
    st.header("Student Input")
    name = st.text_input("Name", value="Daksha")
    career = st.selectbox("Target Career", list(CAREER_MODELS.keys()), index=2)
    gpa = st.slider("GPA", 0.0, 4.3, 3.8, 0.1)
    study_hours = st.slider("Weekly Study Hours", 0, 40, 18)
    ai_literacy = st.slider("AI / Tech Literacy", 0, 100, 72)
    communication = st.slider("Communication", 0, 100, 76)
    stress_management = st.slider("Stress Management", 0, 100, 68)
    teamwork = st.slider("Teamwork", 0, 100, 80)

student_profile = build_student_profile(
    gpa=gpa,
    study_hours=study_hours,
    ai_literacy=ai_literacy,
    communication=communication,
    stress_management=stress_management,
    teamwork=teamwork,
)

target_profile = CAREER_MODELS[career]
readiness, gaps = calculate_readiness(student_profile, target_profile)
action_plan = build_action_plan(gaps)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Student", name if name.strip() else "Learner")
col2.metric("Target Career", career)
col3.metric("Readiness Score", f"{readiness}%")
col4.metric("Top Skill Gap", gaps[0]["Skill"] if gaps else "None")

st.divider()

left, right = st.columns([1.2, 1])

with left:
    st.subheader("Profile Comparison")
    compare_df = pd.DataFrame(
        {
            "Skill": list(student_profile.keys()),
            "Student": list(student_profile.values()),
            "Target Role": [target_profile[k] for k in student_profile.keys()],
        }
    )

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    x = range(len(compare_df))
    width = 0.35
    ax1.bar([i - width / 2 for i in x], compare_df["Student"], width=width, label="Student")
    ax1.bar([i + width / 2 for i in x], compare_df["Target Role"], width=width, label="Target Role")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(compare_df["Skill"], rotation=20)
    ax1.set_ylim(0, 100)
    ax1.set_ylabel("Score")
    ax1.legend()
    ax1.set_title("Current Profile vs Future Role")
    st.pyplot(fig1)

    st.subheader("Skill Gap Analysis")
    gap_df = pd.DataFrame(gaps)
    st.dataframe(gap_df, use_container_width=True, hide_index=True)

with right:
    st.subheader("Recommended Learning Path")
    top_recommendations = []
    for gap in gaps[:3]:
        if gap["Gap"] > 0:
            for item in LEARNING_RESOURCES[gap["Skill"]][:2]:
                top_recommendations.append((gap["Skill"], item))

    if top_recommendations:
        for idx, (skill, item) in enumerate(top_recommendations, start=1):
            st.markdown(f"**Recommendation {idx}:** {item}  ")
            st.caption(f"Linked skill area: {skill}")
    else:
        st.success("No critical gaps found. Focus on advanced projects and leadership experience.")

    st.subheader("Action Plan & Milestones")
    for milestone in action_plan:
        st.write(f"- {milestone}")

    st.subheader("Project Summary")
    st.write(
        "This prototype shows how an AI Learning Twin can build a student profile, compare it to a future career model, "
        "forecast skill gaps, and generate a personalized development path."
    )

st.divider()

st.subheader("Workforce Readiness Report")
if readiness >= 80:
    st.success(f"{name} is strongly aligned with the {career} pathway.")
elif readiness >= 60:
    st.warning(f"{name} is moderately aligned with the {career} pathway and would benefit from targeted upskilling.")
else:
    st.error(f"{name} currently has significant gaps for the {career} pathway and needs structured intervention.")

st.download_button(
    label="Download Readiness Report (CSV)",
    data=gap_df.to_csv(index=False),
    file_name="ai_learning_twin_report.csv",
    mime="text/csv",
)
