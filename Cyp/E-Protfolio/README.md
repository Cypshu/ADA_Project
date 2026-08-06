# E-Portfolio – Santander

Die Hauptdatei ist `ADA_138_Sawarzynski_Portfolio.tex`.

## PDF erzeugen

Im Ordner `E-Protfolio` ausführen:

```powershell
xelatex -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
xelatex -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
```

Der zweite Lauf aktualisiert Inhaltsverzeichnis und Querverweise. Für Abbildungen können
Dateien im Ordner `assets` abgelegt und anschließend mit `\includegraphics` eingebunden werden.

## Struktur

- `ADA_138_Sawarzynski_Portfolio.tex`: editierbare Portfolio-Hauptdatei
- `assets/`: Abbildungen und sonstige Portfolio-Assets
