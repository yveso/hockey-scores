import altair as alt
import streamlit as st

from current_gameday import current_gameday  # noqa
from total_scores import total_scores  # noqa

st.set_page_config(page_title="Hockey Punkte", page_icon="🏒", layout="wide")

st.title("🏒 Hockey Punkte 🏒", anchor=False)

players = [69707878, 69683358, 69662381]

with st.status("Daten herunterladen..."):
    current_gameday_df = current_gameday(players)
    st.write("✅ Aktueller Spieltag")
    points_per_gameday_df = total_scores(players=players, view="spieltagspunkte")
    st.write("✅ Spieltagspunkte")
    placement_per_gameday_df = total_scores(players=players, view="platzierungen")
    st.write("✅ Platzierung pro Spieltag")

st.subheader("Aktueller Spieltag", anchor=False)
st.dataframe(current_gameday_df, hide_index=True)

st.subheader("Punkte pro Spieltag", anchor=False)
points_per_gameday_df = points_per_gameday_df.reset_index().melt(
    "Spieltag", var_name="Name", value_name="Punkte"
)
points_per_gameday_chart = (
    alt.Chart(points_per_gameday_df)
    .mark_line(interpolate="basis")
    .encode(x="Spieltag:Q", y="Punkte:Q", color="Name:N")
)
st.altair_chart(points_per_gameday_chart, use_container_width=True)


st.subheader("Platzierung pro Spieltag", anchor=False)
placement_per_gameday_df = placement_per_gameday_df.reset_index().melt(
    "Spieltag", var_name="Name", value_name="Platzierung"
)
placement_per_gameday_chart = (
    alt.Chart(placement_per_gameday_df)
    .mark_line(interpolate="basis")
    .encode(
        x="Spieltag:Q",
        y=alt.Y("Platzierung:Q", scale=alt.Scale(reverse=True)),
        color="Name:N",
    )
)
st.altair_chart(placement_per_gameday_chart, use_container_width=True)
