# E-Portfolio – Santander

Die Hauptdatei ist `ADA_138_Sawarzynski_Portfolio.tex`.

Das laufende individuelle Arbeitsprotokoll befindet sich in `Logbuch_Santander_Cyp.tex`.
Es wird nach jedem relevanten Arbeitsschritt ergänzt und später als Grundlage für die
Zusammenfassung des E-Portfolios verwendet.

## PDF erzeugen

Im Ordner `E-Protfolio` ausführen:

```powershell
xelatex -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
xelatex -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
```

Das Logbuch wird analog kompiliert:

```powershell
xelatex -interaction=nonstopmode -halt-on-error Logbuch_Santander_Cyp.tex
xelatex -interaction=nonstopmode -halt-on-error Logbuch_Santander_Cyp.tex
```

Der zweite Lauf aktualisiert Inhaltsverzeichnis und Querverweise. Für Abbildungen können
Dateien im Ordner `assets` abgelegt und anschließend mit `\includegraphics` eingebunden werden.

## Struktur

- `ADA_138_Sawarzynski_Portfolio.tex`: editierbare Portfolio-Hauptdatei
- `assets/`: Abbildungen und sonstige Portfolio-Assets
