# Wörterbuch Deutsch–Persisch — Android-Version

Installierbare Web-App (PWA) für Android mit statischem Manifest und App-Icons.

## Einrichtung (einmalig, ~3 Minuten)

1. **Repo anlegen**: Auf github.com → „New repository" → Name: `Dictionary-Android` → **Public** → „Create repository"
2. **Dateien hochladen**: Auf der neuen Repo-Seite → „uploading an existing file" → alle Dateien aus diesem Ordner hineinziehen → „Commit changes"
3. **GitHub Pages aktivieren**: Settings → Pages → Source: „Deploy from a branch" → Branch: `main` / `/ (root)` → Save
4. Nach 1–2 Minuten ist die App erreichbar unter:
   `https://noahhwagnerr-wq.github.io/Dictionary-Android/`

## Installation auf dem Android-Gerät

1. Die URL in **Chrome** öffnen
2. Menü (⋮) → **„App installieren"**
3. Die App erscheint mit Buch-Icon im App-Drawer und läuft im Vollbild

## Wörter vom iPhone übernehmen

1. iPhone-App → Export → `.lvtdeck`-Datei speichern und aufs Android-Gerät schicken
2. Android-App → Import → Datei auswählen
3. API-Keys (Claude usw.) einmal neu in den Einstellungen eintragen

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Die komplette App (Single-File) |
| `manifest.json` | Android-Installierbarkeit (Name, Icons, Vollbild) |
| `icon-192.png`, `icon-512.png`, `icon-512-maskable.png` | App-Icons |
| `sw.js` | Service Worker (Pflicht für PWA-Installation) |
| `reset.html` | Notfall-Reset der lokalen Daten |
