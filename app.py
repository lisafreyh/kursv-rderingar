rows = []
for q, values in course_data["likert"].items():
    total = sum(values)
    if total == 0:
        total = 1

    rows.append({
        "Question": q,
        "low": -(values[0] + values[1]) / total * 100,
        "mid": values[2] / total * 100,
        "high": (values[3] + values[4]) / total * 100
    })

likert_df = pd.DataFrame(rows)

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["low"],
    name="1–2",
    orientation='h',
    marker_color="red"
))

fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["mid"],
    name="3",
    orientation='h',
    marker_color="gray"
))

fig2.add_trace(go.Bar(
    y=likert_df["Question"],
    x=likert_df["high"],
    name="4–5",
    orientation='h',
    marker_color="green"
))

fig2.update_layout(
    barmode='relative',
    xaxis=dict(range=[-100, 100]),
    title="Likert profile (%)"
)
