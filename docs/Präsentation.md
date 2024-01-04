# Präsentationsablauf

## 1 Was war unser Projekt?

### Aufgabenstellung
- GUI für einen Wochenbehandlungsplan für Zahnärtze und deren Patienten
- Zusammenstellung der Behandlungszeiten und Kosten
- Patienten wählen Termine selbst
- Ärzte und Patienten haben übersicht über gebuchte Termine
- Einlesen, der zur Verfügung gestellten Excel-Datei

## 2 Umsetztung

### Programmierbasis
- Programmiersprache: Python 3.11
- Framework **Tkinter**
    - **Customtkinter** als mordernisiertes Tkinter benutzt
- **Diverse Packages**
    - Pandas
        - parsen der Excel-Datei
        - handhaben der Daten (Dataframes)
    - bcrypt
        - Passwortverschlüsselung
        - Hashing/Salting
    - Pillow
        - Anzeigen von Icons und Logos
    - Interne Libraries

### Programmaufbau
- Login/Registration
- Einstellungen
- Terminübersicht
- Terminbuchung

## 3 Features

### Login/Registration
- Login mit **eindeutigem** Benutzernamen und Passwort
- Loginvalidierung und Fehlermeldungen
---
- Registrierung als Patient
    - Benutzername, Name und Namenspräfix
    - Passwort und Passwortbestätigung
    - Krankenkassenart und Dentale Problematik
    - Anzahl der zu behandelnden Zähne
- Registrierung als Zahnarzt
    - Eingeben der generellen Daten (siehe Patient)
    - Freischalt-Code von Admin
    - Behandlungszeiten Wählen

### Einstellungen
- Farbdesign
    - System, Hell, Dunkel
- Passwort ändern
    - Eingabe von altem Passwort benötigt
    - Validierung vie bei Anmeldung

### Terminübersicht
- Direkt nach der Anmeldung mit generellen Daten
- Eigener Tab in Seitenleiste
- Alle relevanten Informationen zu gebuchten Terminen (ausgenommen vergangene)
- Zeitlich angeordnet
- Für Zahnärzte sowie Patienten

### Terminbuchung
- Eigener Tab in Seitenleiste
- interaktive Progressbar
- Auswahl der Termindetails
    - Zahnanzahl und Füllmaterial
    - dynamische Kostenberechnung
- Auswahl des Arztes
    - nur Ärzte mit passender Krankenkassenart
- Auswahl der Behandlungszeit
    - detaillierte Wochenübersicht
        - Zeitraum der nächsten 3 Monate
        - Anzeigen des Verfügbaren Zeitraums des Arztes 
        - Anzeigen bereits verbuchter Termine
    - Terminauswahl
        - Aktuell gewählte Woche
        - verfügbarer Tag in der Woche
        - verfügbarer Zeitraum des bestimmten Tages
        - visuelles Anzeigen des gewählten Termins
        - möglichkeit Termin wieder zu ändern

