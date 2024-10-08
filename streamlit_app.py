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
    points_per_gameday_df_orig = total_scores(players=players, view="spieltagspunkte")
    st.write("✅ Punkte")
    gameday_placement_df = total_scores(players=players, view="spieltagsplatzierungen")
    st.write("✅ Spieltagsplatzierungen")
    placement_per_gameday_df = total_scores(players=players, view="platzierungen")
    st.write("✅ Gesamtplatzierungen")

st.subheader("Aktueller Spieltag", anchor=False)
st.dataframe(current_gameday_df, hide_index=True)

st.subheader("Spieltagspunkte", anchor=False)
points_per_gameday_df = points_per_gameday_df_orig.reset_index().melt(
    "Spieltag", var_name="Name", value_name="Punkte"
)
points_per_gameday_chart = (
    alt.Chart(points_per_gameday_df)
    .mark_line(interpolate="basis")
    .encode(x="Spieltag:Q", y="Punkte:Q", color="Name:N")
)
st.altair_chart(points_per_gameday_chart, use_container_width=True)

st.subheader("Spieltagsplatzierung", anchor=False)
gameday_placement_df = gameday_placement_df.reset_index().melt(
    "Spieltag", var_name="Name", value_name="Spieltagsplatzierung"
)
gameday_placement_chart = (
    alt.Chart(gameday_placement_df)
    .mark_line(interpolate="basis")
    .encode(
        x="Spieltag:Q",
        y=alt.Y("Spieltagsplatzierung:Q", scale=alt.Scale(reverse=True)),
        color="Name:N",
    )
)
st.altair_chart(gameday_placement_chart, use_container_width=True)

st.subheader("Gesamtpunkte", anchor=False)
total_points_per_gameday_df = points_per_gameday_df_orig.cumsum()
total_points_per_gameday_df = total_points_per_gameday_df.reset_index().melt(
    "Spieltag", var_name="Name", value_name="Punkte"
)
points_per_gameday_chart = (
    alt.Chart(total_points_per_gameday_df)
    .mark_line(interpolate="basis")
    .encode(x="Spieltag:Q", y="Punkte:Q", color="Name:N")
)
st.altair_chart(points_per_gameday_chart, use_container_width=True)
st.subheader("Gesamtpunkte (Log Scale)", anchor=False)
points_per_gameday_chart = (
    alt.Chart(total_points_per_gameday_df)
    .mark_line(interpolate="basis")
    .encode(
        x="Spieltag:Q", y=alt.Y("Punkte:Q", scale=alt.Scale(type="log")), color="Name:N"
    )
)
st.altair_chart(points_per_gameday_chart, use_container_width=True)

st.subheader("Gesamtplatzierung", anchor=False)
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
