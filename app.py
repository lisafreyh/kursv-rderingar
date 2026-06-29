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

# ===== DATAFRAME =====
df = pd.DataFrame(data)

# ===== FIGUR 5 =====
st.subheader("Overview (Figure 5)")

# sortera (snyggare)
df = df.sort_values("prop45")

fig = go.Figure()

colors = ["firebrick" if x < 0.7 else "steelblue" for x in df["prop45"]]

fig.add_trace(go.Bar(
    x=df["course"],
    y=df["prop45"],
    marker_color=colors
))

# threshold-linje
fig.add_hline(y=0.7, line_dash="dash", line_color="black")

fig.update_layout(
    title="Proportion of students (4–5)",
    xaxis_title="Course",
    yaxis_title="Proportion",
)

st.plotly_chart(fig, use_container_width=True)

# ===== VAL AV KURS =====
st.markdown("### Select a course")

selected_course = st.radio(
    "",
    df["course"].tolist()
)

# ===== HÄMTA DATA SÄKERT =====
course_data = next((d for d in data if d["course"] == selected_course), None)

if course_data is None:
    st.error("No data found for selected course")
    st.stop()

# ===== FIGUR 6 =====
st.subheader(f"Course profile: {selected_course} (Figure 6)")

rows = []

for q, values in course_data["likert"].items():
    total = sum(values)

    if total == 0:
        total = 1  # skydd mot crash

    rows.append({
        "Question": q,
        "low": -(values[0] + values[1]) / total * 100,
        "mid": values[2] / total * 100,
        "high": (values[3] + values[4]) / total * 100
    })

likert_df = pd.DataFrame(rows)

fig2 = go.Figure()

# vänster (negativt)
fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["low"],
    name="1–2",
    orientation='h',
    marker_color="firebrick"
))

# mitten
fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["mid"],
    name="3",
    orientation='h',
    marker_color="lightgray"
))

# höger
fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["high"],
    name="4–5",
    orientation='h',
    marker_color="seagreen"
))

fig2.update_layout(
    barmode='relative',
    title="Likert profile (%)",
    xaxis=dict(range=[-100, 100]),
    xaxis_title="Percentage",
    yaxis_title="",
)

st.plotly_chart(fig2, use_container_width=True)
