from bs4 import BeautifulSoup
import httpx
import pandas as pd


def total_scores(players: list[int], view: str) -> pd.DataFrame:
    names, points_list = [], []
    for player_id in players:
        response = httpx.get(
            f"https://www.kicktipp.de/penny-eishockey/gesamtuebersicht?tippsaisonId=3329281&teilnehmerSucheId={player_id}&ansicht={view}"
        )
        soup = BeautifulSoup(response.content, "lxml")

        player_row = soup.find("table", id="ranking").find("tr", class_="treffer")
        game_days = player_row.find_all("td", class_="spieltag")
        name = player_row.find_all("td")[1].get_text()
        points = [
            int(c) if c else None for c in (cell.get_text() for cell in game_days)
        ]
        names.append(name)
        points_list.append(points)
    df = pd.DataFrame(points_list).T
    df.columns = names
    df.index = range(1, len(df) + 1)
    df.index.name = "Spieltag"
    return df
