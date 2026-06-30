# Masterblog

Einfache Flask-Blog-Anwendung mit JSON-Datei als Datenspeicher.

## Features

- **Startseite:** Alle Blogbeiträge aus `posts.json` anzeigen
- **Beitrag hinzufügen:** Formular unter `/add` (GET) und Speichern per POST
- **Persistenz:** Beiträge werden in `posts.json` gelesen und geschrieben
- **Eindeutige IDs:** Neue Beiträge erhalten automatisch die nächste freie ID

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

## Ausführung

```bash
python app.py
```

Die App läuft unter **http://localhost:5001**

> Auf macOS ist Port 5000 oft durch AirPlay belegt — deshalb wird Port 5001 verwendet.

## Routen

| Route | Methode | Beschreibung |
|-------|---------|--------------|
| `/` | GET | Startseite mit allen Blogbeiträgen |
| `/add` | GET | Formular zum Erstellen eines Beitrags |
| `/add` | POST | Neuen Beitrag speichern und zur Startseite weiterleiten |

## Datenstruktur

Beiträge werden als Liste von Dictionaries in `posts.json` gespeichert:

```json
[
    {
        "id": 1,
        "author": "John Doe",
        "title": "First Post",
        "content": "This is my first post."
    }
]
```

## Projektstruktur

| Datei / Ordner | Beschreibung |
|----------------|--------------|
| `app.py` | Flask-App mit Routen und JSON-Hilfsfunktionen |
| `posts.json` | Datenspeicher für alle Blogbeiträge |
| `templates/index.html` | Startseite mit Beitragsliste |
| `templates/add.html` | Formular zum Hinzufügen von Beiträgen |
| `static/styles.css` | Stylesheet |
