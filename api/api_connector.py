import requests

API_KEY = "7bba25feebc705016e0d0627aaf59b47"
HOST = "api-football-v1.p.rapidapi.com"

def get_player_stats(fixture_id, player_id):
    url = f"https://{HOST}/v3/players"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": HOST
    }
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