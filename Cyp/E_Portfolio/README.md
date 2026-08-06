# E-Portfolio – Santander

Die Hauptdatei ist `ADA_138_Sawarzynski_Portfolio.tex`.

Das laufende individuelle Arbeitsprotokoll befindet sich in `Logbuch_Santander_Cyp.tex`.
Es wird nach jedem relevanten Arbeitsschritt ergänzt und später als Grundlage für die
Zusammenfassung des E-Portfolios verwendet. Das Hauptportfolio bindet diese Datei im
Anhang automatisch per `\input{Logbuch_Santander_Cyp.tex}` ein. Die Quelle bleibt damit
separat und wird trotzdem in der finalen Portfolio-PDF berücksichtigt.

## PDF erzeugen

Im Ordner `E_Portfolio` ausführen:

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
```

Das Logbuch kann separat kompiliert werden:

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error Logbuch_Santander_Cyp.tex
```

Die Hauptdatei bindet `Logbuch_Santander_Cyp.tex` im Anhang per `\input{...}` ein. Der
einzige notwendige Befehl für die finale Portfolio-PDF ist daher der erste Befehl oben.
Für Abbildungen können Dateien im Ordner `assets` abgelegt und anschließend mit
`\includegraphics` eingebunden werden.

## Struktur

- `ADA_138_Sawarzynski_Portfolio.tex`: editierbare Portfolio-Hauptdatei
- `Logbuch_Santander_Cyp.tex`: separat gepflegte Logbuch-Quelle und eingebundener Portfolio-Anhang
- `ADA_138_Sawarzynski_Portfolio.pdf`: finale zusammengeführte Portfolio-PDF
- `assets/`: Abbildungen und sonstige Portfolio-Assets
