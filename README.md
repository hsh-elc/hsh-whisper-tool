# Whisper GUI

KI-gestütztes, lokal laufendes Tool zur automatischen Untertitel-Generierung für Audio- und Videodateien – basierend auf OpenAI Whisper.

---

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Features](#features)
- [Projektstruktur](#projektstruktur)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Starten der Anwendung](#starten-der-anwendung)
- [Verwendung](#verwendung)
- [Konfiguration](#konfiguration)
- [Getestete Systeme](#getestete-systeme)

---

## Übersicht

Whisper GUI ist eine Desktop-Anwendung mit grafischer Benutzeroberfläche (tkinter + ttkbootstrap), die mithilfe des Whisper-Modells von OpenAI Sprache aus Audio- und Videodateien transkribiert und als Untertiteldatei speichert. Die gesamte Verarbeitung läuft **lokal** – es werden keine Daten an externe Server gesendet.

---

## Features

- Transkription von **MP4- und MP3-Dateien** zu Untertiteln
- Ausgabe als **.srt** (SubRip) und/oder **.vtt** (WebVTT)
- **Batch-/Bulk-Modus**: Alle Dateien mit der gleichen Dateiendung im selben Ordner werden automatisch verarbeitet
- **GPU-Beschleunigung** via CUDA (PyTorch) – fällt automatisch auf CPU zurück
- Konfigurierbare Modellgröße (Standard: `medium`)
- Tooltip-Hilfen in der GUI
- Fehlermeldungen direkt in der Oberfläche

---

## Projektstruktur

```
hsh-whisper-tool1/
│
├── Main.py             # Einstiegspunkt – startet die Anwendung
├── app.py              # Haupt-App-Klasse (tkinter-Root-Window, Frame-Verwaltung)
├── startPage.py        # Haupt-GUI-Seite (Dateiauswahl, Formatwahl, Start-Button)
├── page.py             # Basisklasse für alle Seiten/Frames
├── SubtitleService.py  # Service-Schicht: Einzel- und Batch-Verarbeitung
├── whisperBackend.py   # Kernlogik: Transkription mit stable-whisper / faster-whisper
├── Constants.py        # Konfiguration: Untertitelformate, Sprachen, Modellgröße
├── ToolTip.py          # Hilfsklasse für Tooltips in der GUI
└── README.md
```

---

## Dependencies

### Paketliste

| Paket | Zweck | Installation |
|---|---|---|
| `ttkbootstrap` | Moderne Themes/Styles für tkinter-Widgets | `pip install ttkbootstrap` |
| `stable-whisper` | Whisper mit verbesserter Zeitstempel-Genauigkeit | `pip install stable-whisper` |
| `faster-whisper` | Optimierte Whisper-Implementierung via CTranslate2 | `pip install faster-whisper` |
| `torch` (PyTorch) | CUDA-GPU-Unterstützung für beschleunigte Verarbeitung | siehe unten |
| `numpy` | Numerische Operationen (interne Abhängigkeit) | `pip install numpy` |
| `tkinter` | GUI-Framework (in Python-Standardbibliothek enthalten) | – |

### Schnellinstallation (alle Pakete auf einmal)

```bash
pip install ttkbootstrap stable-whisper faster-whisper numpy
```

### PyTorch (GPU-Unterstützung)

Für **CUDA-GPU-Beschleunigung** (NVIDIA) PyTorch mit dem passenden CUDA-Build installieren:

```bash
# Aktuelle Installationsbefehle unter https://pytorch.org/get-started/locally/
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

Ohne dedizierte GPU läuft das Tool automatisch auf der **CPU**.

> **Hinweis:** Auf Apple Silicon (M1/M2/M3) wird Metal Performance Shaders (MPS) von PyTorch unterstützt, aber `faster-whisper` läuft dort auf der CPU.

---

## Installation

1. **Python 3.10+** sicherstellen
2. Repository klonen oder herunterladen
3. Dependencies installieren:

```bash
pip install ttkbootstrap stable-whisper faster-whisper numpy
```

4. PyTorch installieren (siehe oben, je nach System)

5. Auf einigen **Linux**-Systemen muss `tkinter` separat installiert werden:

```bash
sudo apt install python3-tk   # Debian/Ubuntu
```

---

## Starten der Anwendung

```bash
python Main.py
```

---

## Verwendung

1. **Datei auswählen**: Button „Select a file" klicken → Dateiauswahl-Dialog öffnet sich (MP4 oder MP3)
2. **(Optional) Batch-Modus aktivieren**: Checkbox „Batch-/Bulk-Mode" ankreuzen – dann werden alle Dateien mit der gleichen Endung im selben Ordner wie die gewählte Datei verarbeitet
3. **Ausgabeformat wählen**: Eine oder beide Checkboxen ankreuzen (`.srt` und/oder `.vtt`)
4. **Transkription starten**: Button „Start" klicken
5. Die Ausgabedatei(en) werden **im selben Ordner wie die Eingabedatei** gespeichert

---

## Konfiguration

In `Constants.py` können folgende Einstellungen angepasst werden:

```python
# Verfügbare Ausgabeformate
subtitle_types = ["srt", "vtt"]

# Unterstützte Sprachen (derzeit nur in der Logik vorhanden, nicht aktiv in der GUI)
languages = ["german", "english"]
language_abbreviations = ["de", "en"]

# Whisper-Modellgröße: tiny | base | small | medium | large
# Größere Modelle = höhere Genauigkeit, aber mehr RAM/VRAM und längere Ladezeit
model_size = "medium"
```

### Modellgrößen-Übersicht

| Modell | VRAM | Geschwindigkeit | Genauigkeit |
|--------|------|-----------------|-------------|
| `tiny` | ~1 GB | sehr schnell | niedrig |
| `base` | ~1 GB | schnell | niedrig |
| `small` | ~2 GB | mittel | mittel |
| `medium` | ~5 GB | langsam | hoch |
| `large` | ~10 GB | sehr langsam | sehr hoch |

---

## Getestete Systeme

- Apple MacBook Air M1 – macOS Sonoma 14.1.2
- Windows 10 – NVIDIA GeForce GTX 1080 Ti, AMD Ryzen 5 1600
