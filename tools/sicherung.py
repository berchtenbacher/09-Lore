"""Legt Sicherungskopien der Lore-Tabellen im Ordner „00 Lore Sicherungskopien“ an.

    python3 tools/sicherung.py              # alle „Lore Tags, Kategorien und Einträge *.xlsx“
    python3 tools/sicherung.py "vor Runde 3" # mit kurzem Anlass im Dateinamen

Dateiname: „<Tabelle> (Sicherung 2026-10-31 12-30 vor Runde 3).xlsx“. Es wird nur kopiert, nie gelöscht.
"""
import datetime, pathlib, shutil, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKUP = ROOT / "00 Lore Sicherungskopien"
PATTERN = "Lore Tags, Kategorien und Einträge *.xlsx"


def tables():
    """Alle Lore-Tabellen im Projektordner. macOS speichert Umlaute zerlegt, deshalb wird normalisiert verglichen."""
    return sorted(f for f in ROOT.glob("*.xlsx")
                  if unicodedata.normalize("NFC", f.name).startswith(PATTERN.split("*")[0]) and not f.name.startswith("~$"))


def main():
    reason = " ".join(sys.argv[1:]).strip()
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")
    BACKUP.mkdir(exist_ok=True)
    files = tables()
    for f in files:
        if (ROOT / f"~${f.name}").exists():
            print(f"Hinweis: {f.name} ist gerade in Excel geöffnet, gesichert wird der zuletzt gespeicherte Stand.")
        target = BACKUP / f"{f.stem} (Sicherung {stamp}{' ' + reason if reason else ''}){f.suffix}"
        shutil.copy2(f, target)
        print(target.relative_to(ROOT))
    if not files:
        print(f"Keine Datei gefunden ({PATTERN}).")


if __name__ == "__main__":
    main()
