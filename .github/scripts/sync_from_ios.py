#!/usr/bin/env python3
"""Synchronisiert die App-Dateien aus dem iOS-Repo (noahhwagnerr-wq/Dictionary-)
in dieses Android-Repo und wendet dabei die Android-spezifischen Anpassungen an:

1. <head>: statischer Manifest-Link + Icon-Links (Android/Chrome braucht ein
   statisches Manifest fuer die App-Installation).
2. Der iOS-Blob-Manifest-Block ("// ── PWA ──"-IIFE) wird entfernt, da
   Android/Chrome Blob-URLs nicht fuer die App-Installation akzeptiert.
3. Die Versionskennung erhaelt das Praefix "android-", bleibt aber an die
   iOS-Version gekoppelt (z. B. "v2026-05-23i" -> "android-v2026-05-23i").

sw.js und reset.html werden unveraendert uebernommen. manifest.json, die Icons
und die README existieren nur im Android-Repo und werden nicht angefasst.

Das Skript bricht mit Fehler ab, wenn eine der erwarteten Stellen in der
iOS-Datei nicht (oder mehrfach) gefunden wird, damit eine strukturelle
Aenderung im iOS-Repo nicht unbemerkt eine kaputte Android-Version erzeugt.

Aufruf: sync_from_ios.py <pfad-zum-ios-repo> <pfad-zum-android-repo>
"""
import re
import shutil
import sys
from pathlib import Path

HEAD_ANCHOR = '<meta name="referrer" content="no-referrer">\n'
HEAD_LINKS = (
    '<link rel="manifest" href="./manifest.json">\n'
    '<link rel="icon" type="image/png" sizes="192x192" href="./icon-192.png">\n'
    '<link rel="apple-touch-icon" href="./icon-192.png">\n'
)

PWA_BLOCK = re.compile(r"// ── PWA ──\n\(\(\)=>\{.*?\}\)\(\);\n", re.DOTALL)
PWA_REPLACEMENT = (
    "// ── PWA ── (Manifest ist jetzt statisch im <head> verlinkt --\n"
    "// Blob-URLs akzeptiert Android/Chrome nicht für die App-Installation)\n"
)

VERSION_DIV = re.compile(
    r'(<div style="font-size:9px;color:rgba\(255,255,255,0\.18\);[^"]*">)(v[^<]+)(</div>)'
)

COPY_AS_IS = ["sw.js", "reset.html"]


def fail(msg: str) -> None:
    sys.exit(f"FEHLER: {msg}")


def transform_index(html: str) -> str:
    if '<link rel="manifest"' in html:
        fail(
            "Die iOS-index.html enthaelt bereits einen statischen Manifest-Link. "
            "Die Android-Anpassungen in .github/scripts/sync_from_ios.py muessen "
            "ueberprueft werden."
        )

    if html.count(HEAD_ANCHOR) != 1:
        fail(
            "Anker fuer die <head>-Links ('meta referrer') nicht eindeutig in der "
            "iOS-index.html gefunden."
        )
    html = html.replace(HEAD_ANCHOR, HEAD_ANCHOR + HEAD_LINKS, 1)

    html, n = PWA_BLOCK.subn(PWA_REPLACEMENT, html, count=1)
    if n != 1:
        fail("PWA-Blob-Manifest-Block nicht in der iOS-index.html gefunden.")

    html, n = VERSION_DIV.subn(
        lambda m: f"{m.group(1)}android-{m.group(2)}{m.group(3)}", html, count=1
    )
    if n != 1:
        fail("Versionskennung nicht in der iOS-index.html gefunden.")

    return html


def main() -> None:
    if len(sys.argv) != 3:
        fail(f"Aufruf: {sys.argv[0]} <pfad-zum-ios-repo> <pfad-zum-android-repo>")
    ios_dir = Path(sys.argv[1])
    android_dir = Path(sys.argv[2])

    ios_index = ios_dir / "index.html"
    if not ios_index.is_file():
        fail(f"{ios_index} existiert nicht.")

    html = transform_index(ios_index.read_text(encoding="utf-8"))
    (android_dir / "index.html").write_text(html, encoding="utf-8")
    print("index.html synchronisiert (mit Android-Anpassungen).")

    for name in COPY_AS_IS:
        src = ios_dir / name
        if not src.is_file():
            fail(f"{src} existiert nicht.")
        shutil.copyfile(src, android_dir / name)
        print(f"{name} unveraendert uebernommen.")


if __name__ == "__main__":
    main()
