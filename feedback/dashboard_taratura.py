import pandas as pd
import os
import streamlit as st

STORICO_PATH = "storico.csv"
MODELLO_BASE = 87
MODELLO_PORTA = 83

def mostra_affidabilita():
    if os.path.exists(STORICO_PATH):
        df = pd.read_csv(STORICO_PATH)
        totali = (abs(df["prev_tiri"] - df["real_tiri"]) <= 1).mean() * 100
        porta = (abs(df["prev_porta"] - df["real_porta"]) <= 1).mean() * 100
        st.metric("Affidabilità Tiri Totali", f"{totali:.1f}%")
        st.metric("Affidabilità Tiri in Porta", f"{porta:.1f}%")
    else:
        st.write("Nessun dato storico disponibile.")

def aggiorna_modello():
    nuovo = MODELLO_BASE + 0.5
    if nuovo > MODELLO_BASE:
        return True
    return False