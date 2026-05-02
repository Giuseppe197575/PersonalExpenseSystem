-- ============================================================
--  Personal Expense System — Script SQL completo
--  Creazione del database, vincoli di integrità e dati di esempio
-- ============================================================

PRAGMA foreign_keys = ON;

-- ── Cancella le tabelle se esistono già (utile in fase di sviluppo) ──
-- L'ordine è importante: si eliminano prima le tabelle dipendenti
DROP TABLE IF EXISTS spese;
DROP TABLE IF EXISTS budget;
DROP TABLE IF EXISTS categorie;

-- ============================================================
--  TABELLA: categorie
--  Contiene le categorie di spesa definite dall'utente
-- ============================================================
CREATE TABLE categorie (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chiave primaria, assegnata automaticamente
    nome TEXT    NOT NULL UNIQUE              -- Nome obbligatorio e univoco
);

-- ============================================================
--  TABELLA: spese
--  Contiene ogni singola spesa registrata
-- ============================================================
CREATE TABLE spese (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    data         TEXT    NOT NULL,                          -- Formato YYYY-MM-DD
    importo      REAL    NOT NULL CHECK(importo > 0),       -- Deve essere positivo
    categoria_id INTEGER NOT NULL,                          -- Riferimento alla categoria
    descrizione  TEXT,                                      -- Campo opzionale
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)    -- Chiave esterna
);

-- ============================================================
--  TABELLA: budget
--  Contiene i limiti di spesa mensili per categoria
-- ============================================================
CREATE TABLE budget (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    mese            TEXT    NOT NULL,                               -- Formato YYYY-MM
    categoria_id    INTEGER NOT NULL,                               -- Riferimento alla categoria
    importo_limite  REAL    NOT NULL CHECK(importo_limite > 0),     -- Deve essere positivo
    UNIQUE(mese, categoria_id),                                     -- Un solo budget per mese/categoria
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)            -- Chiave esterna
);

-- ============================================================
--  DATI DI ESEMPIO — Categorie
-- ============================================================
INSERT INTO categorie (nome) VALUES ('Alimentari');
INSERT INTO categorie (nome) VALUES ('Trasporti');
INSERT INTO categorie (nome) VALUES ('Svago');
INSERT INTO categorie (nome) VALUES ('Salute');
INSERT INTO categorie (nome) VALUES ('Abbigliamento');

-- ============================================================
--  DATI DI ESEMPIO — Spese
-- ============================================================
-- Gennaio 2026
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-01-05', 85.50,  1, 'Spesa settimanale');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-01-08', 20.00,  2, 'Abbonamento bus mensile');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-01-10', 45.00,  3, 'Cinema e cena');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-01-15', 120.00, 1, 'Spesa mensile supermercato');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-01-18', 35.00,  4, 'Farmacia');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-01-22', 60.00,  5, 'Scarpe invernali');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-01-28', 95.00,  1, 'Spesa fine mese');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-01-30', 15.00,  2, 'Taxi');

-- Febbraio 2026
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-02-03', 75.00,  1, 'Spesa settimanale');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-02-07', 20.00,  2, 'Abbonamento bus mensile');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-02-14', 80.00,  3, 'Cena di San Valentino');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-02-18', 110.00, 1, 'Spesa mensile supermercato');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-02-20', 50.00,  4, 'Visita medica');
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES ('2026-02-25', 40.00,  5, 'Maglione');

-- ============================================================
--  DATI DI ESEMPIO — Budget mensili
-- ============================================================
-- Gennaio 2026
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-01', 1, 280.00);  -- Alimentari: 280 €
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-01', 2,  50.00);  -- Trasporti:   50 €
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-01', 3,  40.00);  -- Svago:       40 €
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-01', 4,  50.00);  -- Salute:      50 €
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-01', 5,  80.00);  -- Abbigliamento: 80 €

-- Febbraio 2026
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-02', 1, 250.00);  -- Alimentari: 250 €
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-02', 2,  50.00);  -- Trasporti:   50 €
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-02', 3,  60.00);  -- Svago:       60 €
INSERT INTO budget (mese, categoria_id, importo_limite) VALUES ('2026-02', 4,  40.00);  -- Salute:      40 €
