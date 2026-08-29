# E-Portfolio – Santander

Die Hauptdatei ist `ADA_138_Sawarzynski_Portfolio.tex`.

Das laufende individuelle Arbeitsprotokoll befindet sich in `Logbuch_Santander_Cyp.tex`.
Es wird nach jedem relevanten Arbeitsschritt ergänzt und später als Grundlage für die
Zusammenfassung des E-Portfolios verwendet. Das Hauptportfolio bindet diese Datei im
Anhang automatisch per `\input{Logbuch_Santander_Cyp.tex}` ein. Die Quelle bleibt damit
separat und wird trotzdem in der finalen Portfolio-PDF berücksichtigt.

## PDF erzeugen

Die auf diesem Rechner zuerst gefundene TinyTeX-Installation enthält nicht alle benötigten
Pakete. Im Ordner `E_Portfolio` deshalb die vorhandene MiKTeX-Installation explizit zweimal
aufrufen (zweiter Lauf für Inhaltsverzeichnis und Querverweise):

```powershell
$adaXeLaTeX = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"
& $adaXeLaTeX -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
& $adaXeLaTeX -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
```

`Logbuch_Santander_Cyp.tex` ist bewusst keine eigenständige LaTeX-Datei und wird nicht
separat kompiliert. Die Hauptdatei bindet das Logbuch im Anhang per `\input{...}` ein.
Für Abbildungen können Dateien im Ordner `assets` abgelegt und anschließend mit
`\includegraphics` eingebunden werden.

## Struktur

- `ADA_138_Sawarzynski_Portfolio.tex`: editierbare Portfolio-Hauptdatei
- `Logbuch_Santander_Cyp.tex`: separat gepflegte Logbuch-Quelle und eingebundener Portfolio-Anhang
- `ADA_138_Sawarzynski_Portfolio.pdf`: finale zusammengeführte Portfolio-PDF
- `assets/`: Abbildungen und sonstige Portfolio-Assets
