import streamlit as st
from algoritmo import calcola_previsione
from api.api_connector import get_player_stats
from feedback.dashboard_taratura import aggiorna_modello, mostra_affidabilita

st.set_page_config(
    page_title="App Predittiva Tiri Serie A",
    page_icon="⚽",
    layout="wide"
)

st.image("https://upload.wikimedia.org/wikipedia/it/0/05/Serie_A_TIM_2022-2023_logo.png", width=100)
st.title("⚽ App Predittiva Tiri - Serie A")

st.markdown("---")
st.markdown("### 1. Recupera Dati Reali da API-Football")

col1, col2 = st.columns(2)
with col1:
    fixture_id = st.text_input("ID partita (fixture_id)")
with col2:
    player_id = st.text_input("ID giocatore (player_id)")

if st.button("Recupera dati reali"):
    stats = get_player_stats(fixture_id, player_id)
    if stats:
        st.success("Dati trovati!")
        st.write(stats)
    else:
        st.error("Dati non trovati o errore API")

st.markdown("---")
st.markdown("### 2. Calcola Previsione Algoritmo")

col1, col2 = st.columns(2)
with col1:
    giocatore = st.text_input("Nome Giocatore", "Raspadori")
    ruolo = st.selectbox("Ruolo", ["Attaccante", "Centrocampista", "Difensore"])
    modulo = st.selectbox("Modulo", ["4-3-3", "4-4-2", "3-5-2"])
with col2:
    forma = st.selectbox("Forma", ["Alta", "Media", "Bassa"])
    avversario = st.selectbox("Forza Avversario", ["Debole", "Normale", "Forte"])
    motivazione = st.selectbox("Motivazione", ["Alta", "Media", "Bassa"])
    arbitro = st.selectbox("Stile Arbitro", ["Permissivo", "Neutrale", "Fiscalissimo"])

if st.button("Calcola Previsione"):
    tiri, porta = calcola_previsione(giocatore, ruolo, modulo, forma, avversario, motivazione, arbitro)
    st.success(f"**{giocatore}**: {tiri} tiri totali | {porta} in porta")

st.markdown("---")
st.markdown("### 3. 📊 Dashboard Auto-Taratura")
mostra_affidabilita()

if st.button("🔁 Aggiorna algoritmo"):
    risultato = aggiorna_modello()
    if risultato:
        st.success("Algoritmo migliorato!")
    else:
        st.warning("Modifica NON applicata: peggiorava le percentuali.")