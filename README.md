# Personal Expense System

Sistema di gestione delle spese personali su console, scritto in Python con SQLite.

## Requisiti per l'esecuzione

**Interprete necessario**
- Python 3.0 o superiore (sviluppato e testato con Python 3.14.4)
- Download: https://www.python.org/downloads/

**Librerie utilizzate**
- `sqlite3` — gestione del database SQLite (inclusa nella libreria standard di Python)
- `pathlib` — gestione dei percorsi file (inclusa nella libreria standard di Python)

Nessuna installazione aggiuntiva richiesta. Tutte le librerie fanno parte della libreria standard di Python.

## Istruzioni per l'esecuzione

**Compilazione**
Python è un linguaggio interpretato: non è richiesta nessuna compilazione. Il programma si avvia direttamente tramite l'interprete.

**Avvio del programma**

1. Aprire un terminale
2. Spostarsi nella cartella radice del progetto:

```bash
cd PersonalExpenseSystem
```

3. Avviare il programma con il comando:

```bash
python3 src/main.py
```

Il database `spese.db` viene creato automaticamente nella cartella radice del progetto alla prima esecuzione.

## Struttura del progetto

```
PersonalExpenseSystem/
├── src/
│   └── main.py          # codice sorgente principale
├── sql/
│   └── database.sql     # script SQL: creazione tabelle e dati di esempio
├── demo/
│   └── (video dimostrativo)
└── README.md
```

## Funzionalità

1. **Gestione categorie** — aggiunge categorie di spesa, rileva duplicati
2. **Inserimento spesa** — registra una spesa con data, importo, categoria e descrizione opzionale
3. **Budget mensile** — imposta o aggiorna un limite di spesa per mese e categoria
4. **Report** — tre report consultabili da sottomenu:
   - Totale spese per categoria
   - Spese mensili vs budget (con stato NEL BUDGET / SUPERAMENTO BUDGET)
   - Elenco completo delle spese ordinato per data

## Note tecniche

- Il database SQLite viene inizializzato automaticamente all'avvio se non esiste
- I vincoli di integrità referenziale sono attivati tramite `PRAGMA foreign_keys = ON`
- Gli input utente sono validati prima di qualsiasi operazione sul database
- Le query usano parametri `?` per prevenire SQL injection
