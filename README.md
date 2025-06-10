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


Installation der Requirements
1. Stelle sicher, dass Python 3.8 oder neuer installiert ist
Windows:
Öffne die Eingabeaufforderung (cmd) oder PowerShell.

Linux:
Öffne ein Terminal.

2. Installation der Abhängigkeiten mit pip
Windows
Standardbefehl:

sh
pip install -r requirements.txt
Fallback, wenn pip nicht gefunden wird:

sh
python -m pip install -r requirements.txt
oder

sh
py -m pip install -r requirements.txt
Linux
Standardbefehl:

sh
pip3 install -r requirements.txt
Fallback, wenn pip3 nicht gefunden wird:

sh
python3 -m pip install -r requirements.txt
3. Hinweise
Sollte keine requirements.txt vorhanden sein, kannst du die Pakete auch einzeln installieren:
sh
pip install reportlab Pillow PyQt5
Bei Problemen mit Berechtigungen unter Linux ggf. sudo verwenden:
sh
sudo pip3 install -r requirements.txt
Prüfe nach der Installation, ob die Pakete korrekt installiert wurden:
sh
pip show reportlab Pillow PyQt5
Tipp:
Verwende nach Möglichkeit eine virtuelle Umgebung (python -m venv venv), um Paketkonflikte zu vermeiden.
