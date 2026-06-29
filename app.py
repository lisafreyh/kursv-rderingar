import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Course Evaluation Dashboard")

# ===== DATA =====
data = [
    {
        "course": "Course A",
        "prop45": 0.82,
        "likert": {
            "Q2": [5, 10, 20, 40, 25],
            "Q3": [3, 7, 15, 50, 25],
            "Q4": [2, 8, 20, 50, 20]
        }
    },
    {
        "course": "Course B",
        "prop45": 0.65,
        "likert": {
            "Q2": [10, 20, 20, 30, 20],
            "Q3": [8, 15, 25, 30, 22],
            "Q4": [5, 15, 20, 35, 25]
        }
    },
    {
        "course": "Course C",
        "prop45": 0.90,
        "likert": {
            "Q2": [2, 5, 15, 50, 28],
            "Q3": [3, 6, 12, 55, 24],
            "Q4": [1, 4, 10, 60, 25]
        }
    }
]

df = pd.DataFrame(data)

# ===== FIGUR 5 (klickbar lista istället för stapel-click) =====
st.subheader("Overview (Figure 5)")

fig = px.bar(df, x="course", y="prop45",
             labels={"prop45": "Proportion (4–5)", "course": "Course"})

st.plotly_chart(fig, use_container_width=True)

# KLICKBAR!
selected_course = st.radio(
    "Select a course to view details:",
    df["course"].tolist()
)

# ===== FIGUR 6 =====
st.subheader(f"Course profile for {selected_course} (Figure 6)")

course_data = next(d for d in data if d["course"] == selected_course)

rows = []
for q, values in course_data["likert"].items():
    rows.append({
        "Question": q,
        "Low (1–2)": values[0] + values[1],
        "Mid (3)": values[2],
        "High (4–5)": values[3] + values[4]
    })

likert_df = pd.DataFrame(rows)

fig2 = px.bar(
    likert_df,
    x="Question",
    y=["Low (1–2)", "Mid (3)", "High (4–5)"],
    barmode="stack",
    title="Likert profile"
)

st.plotly_chart(fig2, use_container_width=True)
