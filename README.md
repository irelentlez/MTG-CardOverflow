# MTG-CardOverflow

Mit  **MTG-CardOverflow** kannst du Magic: The Gathering Kartenbilder (PNG/JPG) automatisch zu druckfertigen PDF-Seiten im A4-Format zusammenstellen.  
Das Programm platziert bis zu 9 Karten pro Seite, fügt Schneidelinien für einfaches Ausschneiden hinzu und verwaltet bereits verarbeitete Karten.

## Features

- Einlesen von Kartenbildern aus einem wählbaren Input-Ordner (`.png`, `.jpg`, `.jpeg`)
- Ausgabe als PDF in einen wählbaren Output-Ordner
- Automatische Platzierung und Skalierung der Karten auf A4
- Schneidelinien an allen Kartenrändern
- Einfache Konfiguration über `config.json` und die grafische Oberfläche

## Voraussetzungen

- Python 3.8+
- Abhängigkeiten: `reportlab`, `Pillow`, `PyQt5`
- 

## Schnellstart

1. Lege deine Kartenbilder im Input-Ordner ab (siehe `config.json`).
2. Starte das Programm mit  
   pyn main.py
3. Passe Input- und Output-Ordner bei Bedarf in der GUI an.
4. Klicke auf PNG zu PDF, um die PDFs zu erstellen.
