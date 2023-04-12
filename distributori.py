import pandas as pd

def importa_dati_fuga(file_path, df_master, artisti_percentuali):
    # Carica il CSV
    df_fuga = pd.read_csv(file_path)

    # Filtra le colonne necessarie
    colonne_selezionate = ["Sale Start date", "Sale End date", "Product Artist", "Product Title", "Reported Royalty", "Sale ID"]
    df_fuga = df_fuga[colonne_selezionate]

    # Rimuovi i duplicati in base al Sale ID
    df_fuga.drop_duplicates(subset="Sale ID", keep="first", inplace=True)

    # Aggiungi una colonna per il distributore
    df_fuga["Distributore"] = "Fuga Music"

    # Unisci il dataframe di Fuga con il dataframe master
    df_master = pd.concat([df_master, df_fuga], ignore_index=True)


    # Aggiorna la lista degli artisti e le percentuali di royalties
    artisti_nuovi = set(df_fuga["Product Artist"]) - set(artisti_percentuali.keys())
    for artista in artisti_nuovi:
        artisti_percentuali[artista] = 0

    return df_master, artisti_percentuali


def importa_dati_artist_first(file_path):
    # Funzione vuota, da completare in seguito
    pass

def importa_dati_universal(file_path):
    # Funzione vuota, da completare in seguito
    pass

# Aggiungi ulteriori funzioni per elaborare i dati dei distributori, se necessario
