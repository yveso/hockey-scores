from bs4 import BeautifulSoup
import httpx
import pandas as pd

points_dict = {"2": "2️⃣", "3": "3️⃣", "4": "4️⃣"}


def current_gameday(players: list[int]) -> pd.DataFrame:
    player_scores = []

    for i, player_id in enumerate(players):
        response = httpx.get(
            f"https://www.kicktipp.de/penny-eishockey/tippuebersicht?teilnehmerSucheId={player_id}"
        )
        soup = BeautifulSoup(response.content, "lxml")
        result_table = soup.find("table", id="ranking")

        if i == 0:
            header_row = result_table.find("thead").find("tr")
            actual_scores = [
                score.get_text()
                for score in header_row.find_all(
                    "th", class_=[f"ereignis{idx}" for idx in range(7)]
                )
            ]

        td_list = result_table.find("tbody").find("tr", class_="treffer").find_all("td")
        scores = []
        for i, td in enumerate(td_list):
            if i == 0:  # Platzierung
                scores.append(td.get_text()[:-1])
            elif i == 1:  # Positionsveränderung
                trend = "🔼" if "position-icon-up" in td.get("class", []) else "🔽"
                scores.append(trend + " " + td.get_text())
            elif 3 <= i <= 9:  # Spiele
                text = td.get_text()
                sub = td.find("sub")
                if sub:
                    scores.append(text[:-1] + "  " + points_dict.get(text[-1]))
                else:
                    scores.append(text)
            else:
                scores.append(td.get_text())
        player_scores.append(scores)

    current_df_column_names = ["Position", "Veränderung", "Name"]
    current_df_column_names.extend(
        s[:3] + "-" + s[3:6] + " " + s[6:] for s in actual_scores
    )
    current_df_column_names.extend(["Punkte", "Bonus", "Tagessiege", "Gesamtpunkte"])

    return pd.DataFrame(player_scores, columns=current_df_column_names).sort_values(
        by="Gesamtpunkte", ascending=False
    )
