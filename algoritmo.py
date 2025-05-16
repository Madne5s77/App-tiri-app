def calcola_previsione(giocatore, ruolo, modulo, forma, avversario, motivazione, arbitro):
    pesi = {
        "ruolo": {"Attaccante": 1.2, "Centrocampista": 0.8, "Difensore": 0.4},
        "forma": {"Alta": 1.3, "Media": 1.0, "Bassa": 0.7},
        "modulo": {"4-3-3": 1.1, "3-5-2": 1.0, "4-4-2": 0.9},
        "motivazione": {"Alta": 1.2, "Media": 1.0, "Bassa": 0.8},
        "arbitro": {"Permissivo": 1.1, "Neutrale": 1.0, "Fiscalissimo": 0.9},
        "avversario": {"Debole": 1.2, "Normale": 1.0, "Forte": 0.8}
    }
    base_tiri = 2.5
    tiri = base_tiri * pesi["ruolo"].get(ruolo, 1) * pesi["forma"].get(forma, 1)
    tiri *= pesi["modulo"].get(modulo, 1) * pesi["motivazione"].get(motivazione, 1)
    tiri *= pesi["arbitro"].get(arbitro, 1) * pesi["avversario"].get(avversario, 1)
    return round(tiri, 2), round(tiri * 0.4, 2)