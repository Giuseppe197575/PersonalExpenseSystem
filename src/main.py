import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "spese.db"


# ─────────────────────────────────────────────
#  INIZIALIZZAZIONE DATABASE
# ─────────────────────────────────────────────

def inizializza_db(conn: sqlite3.Connection) -> None:
    """Crea le tabelle se non esistono."""
    cursor = conn.cursor()
    cursor.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS categorie (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT    NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS spese (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            data         TEXT    NOT NULL,
            importo      REAL    NOT NULL CHECK(importo > 0),
            categoria_id INTEGER NOT NULL,
            descrizione  TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorie(id)
        );

        CREATE TABLE IF NOT EXISTS budget (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            mese            TEXT    NOT NULL,
            categoria_id    INTEGER NOT NULL,
            importo_limite  REAL    NOT NULL CHECK(importo_limite > 0),
            UNIQUE(mese, categoria_id),
            FOREIGN KEY (categoria_id) REFERENCES categorie(id)
        );
        """
    )
    conn.commit()


# ─────────────────────────────────────────────
#  MENU PRINCIPALE
# ─────────────────────────────────────────────

def mostra_menu() -> None:
    print("\n-------------------------")
    print(" SISTEMA SPESE PERSONALI")
    print("-------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-------------------------")


def leggi_scelta() -> int:
    try:
        return int(input("Inserisci la tua scelta: "))
    except ValueError:
        return 0


# ─────────────────────────────────────────────
#  FUNZIONI DI INPUT CON VALIDAZIONE
# ─────────────────────────────────────────────

def leggi_stringa_non_vuota(messaggio: str) -> str:
    while True:
        valore = input(messaggio).strip()
        if valore:
            return valore
        print("Errore: il campo non può essere vuoto.")


def leggi_importo_positivo(messaggio: str) -> float:
    while True:
        try:
            importo = float(input(messaggio))
            if importo <= 0:
                print("Errore: l'importo deve essere maggiore di zero.")
                continue
            return importo
        except ValueError:
            print("Errore: inserisci un numero valido.")


def leggi_data_yyyy_mm_dd(messaggio: str) -> str:
    """Legge una data in formato YYYY-MM-DD e la restituisce come stringa."""
    while True:
        data = input(messaggio).strip()
        if len(data) == 10 and data[4] == "-" and data[7] == "-":
            yyyy = data[0:4]
            mm   = data[5:7]
            dd   = data[8:10]
            if yyyy.isdigit() and mm.isdigit() and dd.isdigit():
                if 1 <= int(mm) <= 12 and 1 <= int(dd) <= 31:
                    return data
        print("Errore: usa il formato YYYY-MM-DD.")


def leggi_mese_yyyy_mm(messaggio: str) -> str:
    """Legge un mese in formato YYYY-MM e lo restituisce come stringa."""
    while True:
        mese = input(messaggio).strip()
        if len(mese) == 7 and mese[4] == "-":
            yyyy = mese[0:4]
            mm   = mese[5:7]
            if yyyy.isdigit() and mm.isdigit() and 1 <= int(mm) <= 12:
                return mese
        print("Errore: usa il formato YYYY-MM.")


# ─────────────────────────────────────────────
#  UTILITY DATABASE
# ─────────────────────────────────────────────

def ottieni_id_categoria(cursor: sqlite3.Cursor, nome: str) -> int | None:
    cursor.execute("SELECT id FROM categorie WHERE nome = ?;", (nome,))
    riga = cursor.fetchone()
    return riga[0] if riga else None


# ─────────────────────────────────────────────
#  MODULO 1 — GESTIONE CATEGORIE
# ─────────────────────────────────────────────

def gestione_categorie(conn: sqlite3.Connection) -> None:
    nome = input("Nome categoria: ").strip()
    if not nome:
        print("Errore: il nome non può essere vuoto.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categorie WHERE nome = ?;", (nome,))
    if cursor.fetchone():
        print("La categoria esiste già.")
        return

    try:
        cursor.execute("INSERT INTO categorie (nome) VALUES (?);", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")
    except sqlite3.IntegrityError:
        print("Errore durante l'inserimento.")


# ─────────────────────────────────────────────
#  MODULO 2 — INSERIMENTO SPESA
# ─────────────────────────────────────────────

def inserisci_spesa(conn: sqlite3.Connection) -> None:
    data = leggi_data_yyyy_mm_dd("Data (YYYY-MM-DD): ")
    importo = leggi_importo_positivo("Importo: ")
    nome_categoria = leggi_stringa_non_vuota("Nome categoria: ")
    descrizione = input("Descrizione (opzionale): ").strip()
    if not descrizione:
        descrizione = None

    cursor = conn.cursor()
    categoria_id = ottieni_id_categoria(cursor, nome_categoria)
    if categoria_id is None:
        print("Errore: la categoria non esiste.")
        return

    try:
        cursor.execute(
            """
            INSERT INTO spese (data, importo, categoria_id, descrizione)
            VALUES (?, ?, ?, ?);
            """,
            (data, importo, categoria_id, descrizione),
        )
        conn.commit()
        print("Spesa inserita correttamente.")
    except sqlite3.IntegrityError as err:
        print(f"Errore durante l'inserimento: {err}")


# ─────────────────────────────────────────────
#  MODULO 3 — DEFINIZIONE BUDGET MENSILE
# ─────────────────────────────────────────────

def definisci_budget(conn: sqlite3.Connection) -> None:
    mese = leggi_mese_yyyy_mm("Mese (YYYY-MM): ")
    nome_categoria = leggi_stringa_non_vuota("Nome categoria: ")
    importo_limite = leggi_importo_positivo("Importo limite: ")

    cursor = conn.cursor()
    categoria_id = ottieni_id_categoria(cursor, nome_categoria)
    if categoria_id is None:
        print("Errore: la categoria non esiste.")
        return

    cursor.execute(
        """
        INSERT OR REPLACE INTO budget (mese, categoria_id, importo_limite)
        VALUES (?, ?, ?);
        """,
        (mese, categoria_id, importo_limite),
    )
    conn.commit()
    print("Budget mensile salvato correttamente.")


# ─────────────────────────────────────────────
#  MODULO 4 — REPORT
# ─────────────────────────────────────────────

def report_totale_per_categoria(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT c.nome, SUM(s.importo) AS totale
        FROM spese s
        JOIN categorie c ON s.categoria_id = c.id
        GROUP BY c.id, c.nome
        ORDER BY totale DESC;
        """
    )
    righe = cursor.fetchall()

    if not righe:
        print("Nessuna spesa registrata.")
        return

    print(f"\n{'Categoria':<20}{'Totale Speso':>12}")
    print("-" * 32)
    for nome, totale in righe:
        punti = "." * (20 - len(nome))
        print(f"{nome}{punti}{totale:>12.2f}")


def report_spese_vs_budget(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT b.mese, c.nome,
               b.importo_limite,
               COALESCE(SUM(s.importo), 0) AS speso
        FROM budget b
        JOIN categorie c ON b.categoria_id = c.id
        LEFT JOIN spese s
            ON s.categoria_id = b.categoria_id
            AND strftime('%Y-%m', s.data) = b.mese
        GROUP BY b.mese, b.categoria_id, c.nome, b.importo_limite
        ORDER BY b.mese, c.nome;
        """
    )
    righe = cursor.fetchall()

    if not righe:
        print("Nessun budget definito.")
        return

    for mese, categoria, budget, speso in righe:
        stato = "SUPERAMENTO BUDGET" if speso > budget else "NEL BUDGET"
        print(f"\nMese: {mese}")
        print(f"Categoria: {categoria}")
        print(f"Budget: {budget:.2f}")
        print(f"Speso:  {speso:.2f}")
        print(f"Stato:  {stato}")


def report_elenco_spese(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '-')
        FROM spese s
        JOIN categorie c ON s.categoria_id = c.id
        ORDER BY s.data;
        """
    )
    righe = cursor.fetchall()

    if not righe:
        print("Nessuna spesa registrata.")
        return

    print(f"\n{'Data':<12} {'Categoria':<18} {'Importo':>8}  {'Descrizione'}")
    print("-" * 62)
    for data, categoria, importo, descrizione in righe:
        print(f"{data:<12} {categoria:<18} {importo:>8.2f}  {descrizione}")


def visualizza_report(conn: sqlite3.Connection) -> None:
    while True:
        print("\n--- MENU REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        print("-------------------")

        scelta = leggi_scelta()

        if scelta == 1:
            report_totale_per_categoria(conn)
        elif scelta == 2:
            report_spese_vs_budget(conn)
        elif scelta == 3:
            report_elenco_spese(conn)
        elif scelta == 4:
            break
        else:
            print("Scelta non valida. Riprovare.")


# ─────────────────────────────────────────────
#  CICLO PRINCIPALE
# ─────────────────────────────────────────────

def main() -> None:
    print("Benvenuto nel Personal Expense System!")
    print()
    print("Questo sistema ti aiuterà a tenere traccia delle tue spese personali,")
    print("gestire le categorie di spesa e definire budget mensili.")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        inizializza_db(conn)

        while True:
            mostra_menu()
            scelta = leggi_scelta()

            if scelta == 1:
                gestione_categorie(conn)
            elif scelta == 2:
                inserisci_spesa(conn)
            elif scelta == 3:
                definisci_budget(conn)
            elif scelta == 4:
                visualizza_report(conn)
            elif scelta == 5:
                print("Arrivederci!")
                break
            else:
                print("Scelta non valida. Riprovare.")


if __name__ == "__main__":
    main()
