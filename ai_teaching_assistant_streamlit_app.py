import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st


st.set_page_config(page_title="AI Learning Twin", page_icon="🧠", layout="wide")


# -----------------------------
# Demo data and core logic
# -----------------------------
SKILL_CATALOG = {
    "Analytical Thinking": {"category": "Core", "future_weight": 0.95},
    "AI Literacy": {"category": "Tech", "future_weight": 0.98},
    "Data Analysis": {"category": "Tech", "future_weight": 0.92},
    "Python": {"category": "Tech", "future_weight": 0.88},
    "Cloud Tools": {"category": "Tech", "future_weight": 0.84},
    "Communication": {"category": "Human", "future_weight": 0.90},
    "Critical Thinking": {"category": "Human", "future_weight": 0.93},
    "Adaptability": {"category": "Human", "future_weight": 0.96},
    "Leadership": {"category": "Human", "future_weight": 0.82},
    "Project Management": {"category": "Business", "future_weight": 0.80},
    "Digital Marketing": {"category": "Business", "future_weight": 0.72},
    "Business Analysis": {"category": "Business", "future_weight": 0.86},
}

CAREER_ROLES = {
    "Business Analyst": {
        "salary_band": "$70k-$110k",
        "automation_risk": 0.30,
        "required": {
            "Business Analysis": 80,
            "Data Analysis": 75,
            "Communication": 72,
            "Critical Thinking": 76,
            "Project Management": 60,
            "AI Literacy": 55,
        },
    },
    "Data Analyst": {
        "salary_band": "$75k-$120k",
        "automation_risk": 0.28,
        "required": {
            "Data Analysis": 85,
            "Python": 75,
            "AI Literacy": 68,
            "Analytical Thinking": 80,
            "Communication": 65,
            "Critical Thinking": 75,
        },
    },
    "Product Manager": {
        "salary_band": "$95k-$145k",
        "automation_risk": 0.22,
        "required": {
            "Communication": 82,
            "Leadership": 75,
            "Project Management": 78,
            "Business Analysis": 70,
            "Critical Thinking": 80,
            "Adaptability": 78,
        },
    },
    "AI Strategy Analyst": {
        "salary_band": "$90k-$140k",
        "automation_risk": 0.18,
        "required": {
            "AI Literacy": 88,
            "Analytical Thinking": 82,
            "Business Analysis": 74,
            "Communication": 72,
            "Critical Thinking": 84,
            "Data Analysis": 78,
        },
    },
}

COURSE_LIBRARY = {
    "AI Literacy": ["Intro to AI for Business", "Prompting and AI Tools", "AI Ethics and Governance"],
    "Data Analysis": ["Excel Analytics", "SQL Fundamentals", "Data Visualization with Power BI"],
    "Python": ["Python Basics", "Python for Analytics", "Automating Reports with Python"],
    "Communication": ["Business Communication", "Presentation Design", "Professional Writing"],
    "Critical Thinking": ["Decision Analysis", "Problem Solving Workshop"],
    "Adaptability": ["Change Management", "Learning How to Learn"],
    "Leadership": ["Leading Teams", "Conflict Resolution"],
    "Project Management": ["Agile Project Management", "Project Planning Essentials"],
    "Business Analysis": ["Requirements Gathering", "Business Process
