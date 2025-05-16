import streamlit as st
from api.api_connector import get_fixtures_today, get_players_from_fixture, get_player_stats
from algoritmo import calcola_previsione
from feedback.dashboard_taratura import aggiorna_modello, mostra_affidabilita

st.set_page_config(page_title="App Predittiva Tiri Serie A", page_icon="⚽", layout="wide")
st.title("⚽ App Predittiva Tiri - Serie A")

st.markdown("## 1. Seleziona Partita e Giocatore")

fixtures = get_fixtures_today()
match_dict = {f"{f['home']} vs {f['away']}": f for f in fixtures}
selected_match = st.selectbox("Scegli una partita", list(match_dict.keys()))
fixture_data = match_dict[selected_match]
fixture_id = fixture_data["fixture_id"]

col1, col2 = st.columns(2)
with col1:
    st.image(fixture_data["home_logo"], width=100, caption=fixture_data["home"])
with col2:
    st.image(fixture_data["away_logo"], width=100, caption=fixture_data["away"])

selected_team = st.radio("Filtra per squadra", [fixture_data["home"], fixture_data["away"]])

players = get_players_from_fixture(fixture_id)
filtered_players = [p for p in players if p["team"] == selected_team]

role_order = {"G": 0, "D": 1, "M": 2, "F": 3}
role_icons = {"G": "🧤", "D": "🛡️", "M": "🎯", "F": "⚽"}
role_colors = {"G": "blue", "D": "green", "M": "orange", "F": "red"}
filtered_players.sort(key=lambda p: role_order.get(p["position"], 4))

def format_player(p):
    icon = role_icons.get(p["position"], "")
    color = role_colors.get(p["position"], "black")
    return f":{color}[{icon} {p['name']}] ({p['position']})"

player_names = {format_player(p): p["id"] for p in filtered_players}
selected_player = st.selectbox("Scegli un giocatore", list(player_names.keys()))
player_id = player_names[selected_player]

if st.button("Recupera dati reali"):
    stats = get_player_stats(fixture_id, player_id)
    if stats:
        st.success("Dati trovati!")
        st.json(stats)
    else:
        st.error("Errore nel recupero dei dati da API")

st.markdown("---")
st.markdown("## 2. Calcola Previsione Algoritmo")

col1, col2 = st.columns(2)
with col1:
    giocatore = st.text_input("Nome Giocatore", selected_player.split()[1])
    ruolo = st.selectbox("Ruolo", ["Attaccante", "Centrocampista", "Difensore"])
    modulo = st.selectbox("Modulo", ["4-3-3", "4-4-2", "3-5-2"])
with col2:
    forma = st.selectbox("Forma", ["Alta", "Media", "Bassa"])
    avversario = st.selectbox("Forza Avversario", ["Debole", "Normale", "Forte"])
    motivazione = st.selectbox("Motivazione", ["Alta", "Media", "Bassa"])
    arbitro = st.selectbox("Stile Arbitro", ["Permissivo", "Neutrale", "Fiscalissimo"])

if st.button("Calcola Previsione"):
    tiri, porta = calcola_previsione(giocatore, ruolo, modulo, forma, avversario, motivazione, arbitro)
    st.success(f"{giocatore}: {tiri} tiri totali | {porta} in porta")

st.markdown("---")
st.markdown("## 3. 📊 Dashboard Auto-Taratura")
mostra_affidabilita()

if st.button("🔁 Aggiorna algoritmo"):
    risultato = aggiorna_modello()
    if risultato:
        st.success("Algoritmo migliorato!")
    else:
        st.warning("Modifica NON applicata: peggiorava le percentuali.")