import requests

API_KEY = "7bba25feebc705016e0d0627aaf59b47"
HOST = "api-football-v1.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": HOST
}

def get_fixtures_today():
    url = f"https://{HOST}/v3/fixtures"
    params = {"date": "2025-05-03", "league": "135", "season": "2024"}
    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        data = res.json()["response"]
        return [{
            "fixture_id": f["fixture"]["id"],
            "home": f["teams"]["home"]["name"],
            "away": f["teams"]["away"]["name"],
            "home_logo": f["teams"]["home"]["logo"],
            "away_logo": f["teams"]["away"]["logo"]
        } for f in data]
    except Exception as e:
        print("Errore fixtures:", e)
        return []

def get_players_from_fixture(fixture_id):
    url = f"https://{HOST}/v3/players"
    params = {"fixture": fixture_id}
    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        data = res.json()["response"]
        players = []
        for p in data:
            info = p["player"]
            stats = p["statistics"][0]
            players.append({
                "id": info["id"],
                "name": info["name"],
                "team": stats["team"]["name"],
                "position": stats["games"]["position"]
            })
        return players
    except Exception as e:
        print("Errore players:", e)
        return []

def get_player_stats(fixture_id, player_id):
    url = f"https://{HOST}/v3/players"
    params = {"fixture": fixture_id, "id": player_id}
    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        if data["response"]:
            stats = data["response"][0]["statistics"][0]
            return {
                "tiri_totali": stats["shots"]["total"],
                "tiri_in_porta": stats["shots"]["on"],
                "minuti": stats["games"]["minutes"]
            }
    except Exception as e:
        print(f"Errore API: {e}")
    return None