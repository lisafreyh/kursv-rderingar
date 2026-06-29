import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# ===== FIGUR 5: ÖVERSIKT =====
st.subheader("Overview (Figure 5)")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df["course"],
    y=df["prop45"],
    marker_color="steelblue"
))

fig.update_layout(
    title="Proportion of students (4–5)",
    xaxis_title="Course",
    yaxis_title="Proportion",
    clickmode='event+select'
)

selected = st.plotly_chart(fig, use_container_width=True)

# ===== STATE: vilken kurs är vald =====
if "selected_course" not in st.session_state:
    st.session_state.selected_course = df["course"].iloc[0]

# ===== FALLBACK: välj via knapp =====
selected_course = st.radio(
    "Select course:",
    df["course"].tolist(),
    index=df["course"].tolist().index(st.session_state.selected_course)
)

st.session_state.selected_course = selected_course

# ===== FIGUR 6: LIKERT =====
st.subheader(f"Course profile: {selected_course}")

course_data = next(d for d in data if d["course"] == selected_course)

rows = []
for q, values in course_data["likert"].items():
    total = sum(values)

    rows.append({
        "Question": q,
        "1–2": -(values[0] + values[1]) / total * 100,
        "3": values[2] / total * 100,
        "4–5": (values[3] + values[4]) / total * 100
    })

likert_df = pd.DataFrame(rows)

# ===== LIKERT SOM I ARTIKELN =====
fig2 = go.Figure()

fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["1–2"],
    name="1–2",
    orientation='h',
    marker_color="red"
))

fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["3"],
    name="3",
    orientation='h',
    marker_color="gray"
))

fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["4–5"],
    name="4–5",
    orientation='h',
    marker_color="green"
))

fig2.update_layout(
    barmode='relative',
    title="Likert profile (%)",
    xaxis_title="Percentage",
    yaxis_title="",
)

st.plotly_chart(fig2, use_container_width=True)
``
