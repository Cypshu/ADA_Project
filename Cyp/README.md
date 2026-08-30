# ADA-Projekt Santander – Arbeitsleitfaden

Dieses Dokument ist der zentrale Einstiegspunkt für die Arbeit im persönlichen
Projektbereich \`Cyp\`. Es beschreibt die aktuelle Architektur, den Entstehungsweg der
EDA, den Aufbau des E-Portfolios und die Aufgaben, die bei jeder weiteren Bearbeitung
mitgeführt werden müssen.

Die README ist eine dokumentierte Momentaufnahme. Wenn sich die maßgebliche Notebook-
oder Portfolio-Struktur ändert, muss dieser Leitfaden anschließend ebenfalls aktualisiert
werden.

## 1. Verbindliche Arbeitsregeln

- Es wird ausschließlich innerhalb von \`Cyp\` gearbeitet.
- Die Ordner anderer Gruppenmitglieder (\`Tim\`, \`Ang\` und \`Tro\`) werden niemals bearbeitet.
- Vor jeder Änderung wird der Arbeitsstand mit \`git status --short --branch\` geprüft.
- Vorhandene Änderungen gehören zunächst zum aktuellen Arbeitsstand und werden nicht
  überschrieben, zurückgesetzt oder automatisch bereinigt.
- Destruktive Befehle wie \`git reset --hard\` oder \`git checkout -- ...\` werden nicht verwendet.
- Änderungen werden nur gezielt und nachvollziehbar vorgenommen.
- Der Arbeitsbranch ist \`dev-cyp\`.
- Commit und Push erfolgen erst nach Prüfung von Diff, Tests und Dateiumfang.

## 2. Projektarchitektur

~~~
Cyp/
├── data/
│   ├── README.md
│   └── santander_customer_transaction_prediction.csv
├── EDA/
│   ├── 01_Datensatz_Einfuehrung_final.ipynb
│   ├── 01_Datensatz_Einfuehrung_alt.ipynb
│   └── assets/
├── ML/
│   ├── 02_Machine_Learning_NaiveBayes_ANN.ipynb
│   ├── 03_Verification_and_Diagnostics.py
│   ├── runs/
│   └── verification/
├── E_Portfolio/
│   ├── ADA_138_Sawarzynski_Portfolio.tex
│   ├── Logbuch_Santander_Cyp.tex
│   ├── ADA_138_Sawarzynski_Portfolio.pdf
│   ├── README.md
│   └── assets/
├── Bewertungshinweise_ADA.pdf
├── Projekt_Kaggle_Santander.pdf
├── Projekt_Kaggle_PortoSeguro.pdf
├── responses.json
├── .gitignore
└── README.md
~~~

### Verzeichnisse und Dateien

| Bereich | Zweck |
|---|---|
| \`data/\` | Lokale Rohdaten und Hinweise zur Datenbeschaffung. Die große CSV-Datei wird nicht in der Versionskontrolle geführt. |
| \`EDA/\` | Aktuelle explorative Datenanalyse, Notebooks und erzeugte Grafiken. |
| \`EDA/01_Datensatz_Einfuehrung_final.ipynb\` | Aktuelle maßgebliche EDA-Arbeitsdatei. Neue Analysen werden grundsätzlich hier eingeordnet. |
| \`EDA/01_Datensatz_Einfuehrung_alt.ipynb\` | Archivierte frühere Notebook-Version; nur als Referenz verwenden. |
| \`EDA/assets/\` | Grafiken und weitere EDA-Ergebnisse mit beschreibenden Dateinamen. |
| \`ML/02_Machine_Learning_NaiveBayes_ANN.ipynb\` | Reproduzierbare Train-/Validation-/Hold-out-Pipeline für GaussianNB und ANN. |
| \`ML/03_Verification_and_Diagnostics.py\` | Unabhängige Kontrolle der gespeicherten Metriken und Schwellen sowie Learning-Curve- und train-only PCA-Diagnostik. |
| \`ML/runs/20260815_030409_NB_ANN/\` | Maßgeblicher gespeicherter ML-Run mit Predictions, Modellen, Checkpoints, Tabellen und Plots. |
| \`ML/verification/\` | Korrigierte EDA-Prüftabelle, Metrik-/Threshold-Kontrollen und zusätzliche Kriterienplots. |
| \`E_Portfolio/\` | LaTeX-Quellen, Logbuch, Portfolio-PDF und Portfolio-Abbildungen. |
| \`Bewertungshinweise_ADA.pdf\` | Bewertungsgrundlage für das Projekt und das E-Portfolio. |
| \`Projekt_Kaggle_Santander.pdf\` | Fachlicher Projekt- und Datensatzkontext. |
| \`Projekt_Kaggle_PortoSeguro.pdf\` | Vergleichs- bzw. Referenzmaterial. |
| \`responses.json\` | Projektbezogene Notizen bzw. gespeicherte Antworten. |
| \`.gitignore\` | Regeln für Rohdaten, EDA-Quellen und LaTeX-Buildartefakte. |

Die Dateien direkt unter \`Cyp\` werden durch die aktuelle Ignore-Konfiguration teilweise
ausgeschlossen. Diese neue README wird deshalb später gezielt mit \`git add -f Cyp/README.md\`
versioniert; die bestehende \`.gitignore\` wird dafür nicht verändert.

## 3. Datenbasis und Entstehung der EDA

Verwendet wird der Santander-Datensatz *Customer Transaction Prediction* aus OpenML,
Datensatz-ID \`45566\`. Die lokale Datenbeschreibung befindet sich in \`data/README.md\`.
Die EDA entstand als schrittweise Untersuchung des Datensatzes:

1. Laden des Datensatzes und technische Prüfung von Form, Speichergröße, Spaltennamen und
   Datentypen.
2. Prüfung von fehlenden, nicht-finiten und doppelten Werten.
3. Trennung der booleschen Zielvariable \`target\` von den 200 anonymisierten Features.
4. Untersuchung von Wertebereichen, Kardinalitäten, Varianzen, Schiefe, Kurtosis und
   Ausreißerindikatoren.
5. Analyse der Klassenverteilung und der starken Klassenimbalance.
6. Vergleich der Featureverteilungen für \`target=False\` und \`target=True\`.
7. Berechnung von Mittelwertdifferenzen, Cohen’s d, Welch-Tests und Benjamini-Hochberg-
   FDR-korrigierten p-Werten.
8. Stabilitäts- und Bootstrap-Analysen der wichtigsten Effekte.
9. Untersuchung nichtlinearer Einzelassoziationen mit Mutual Information.
10. Berechnung von Feature-Feature-Korrelationen und Analyse möglicher Redundanz.
11. Vergleich unausgeglichener Labelgruppen mit einer 1:1-Undersampling-
    Sensitivitätsanalyse.
12. Vergleich von Rohwerten, Min-Max-normalisierten Werten und robuster Skalierung.
13. Dimensionsreduktion mit PCA und t-SNE.
14. Unüberwachte Zusatzdiagnostik mit K-Means und DBSCAN.
15. Logistic Regression als überwachte, interpretierbare Baseline mit geeigneten
    Imbalance-Metriken.
16. Zusammenführung der Befunde in einer Gesamtauswertung und Schlussfolgerung.

### Methodische Leitplanken

- \`target\` wird ausschließlich als Label verwendet und darf nicht in Featurematrizen,
  PCA/t-SNE-Eingaben oder Feature-Feature-Korrelationen gelangen.
- Min-Max-normalisierte Features liegen im Intervall \`[0,1]\`.
- Die 1:1-Analyse gleicht die Klassen durch zufälliges Undersampling der False-Gruppe an.
  Sie ist daher eine Sensitivitätsanalyse und ersetzt nicht automatisch die Hauptanalyse.
- PCA ist eine lineare Projektion, die globale Varianz durch Linearkombinationen der
  Eingangsfeatures zusammenfasst.
- t-SNE ist eine nichtlineare, nachbarschaftsbasierte Projektion. Achsen und globale
  Abstände sind nicht direkt inhaltlich interpretierbar.
- K-Means und DBSCAN sind unüberwachte Zusatzdiagnostik. Cluster oder deren Überlappung
  sind weder ein Beweis für noch gegen eine gute überwachte Modellierbarkeit.

## 4. Aktueller analytischer Stand

Der derzeit dokumentierte Stand umfasst:

- 200.000 Beobachtungen und 200 numerische Features
- eine boolesche Zielvariable \`target\`
- starke Klassenimbalance mit ungefähr 10 % positiven Fällen
- keine fehlenden Werte im untersuchten Datensatz
- labelbedingte Mittelwert- und Verteilungsvergleiche
- Welch-Tests mit Benjamini-Hochberg-FDR-Korrektur
- Cohen’s-d-Stabilität über mehrere 1:1-Stichproben
- Bootstrap-Intervalle für ausgewählte Effekte und Korrelationsbefunde
- Mutual-Information-Ranking
- Redundanz- und Korrelationsanalyse
- Vergleich unausgeglichener und balancierter Korrelationsschätzungen
- verschiedene Skalierungen, PCA, t-SNE, K-Means und DBSCAN
- eine balancierte Logistic-Regression-Baseline mit ROC-AUC, PR-AUC, Balanced Accuracy,
  Recall, Precision und F1
- vier ML-Varianten (GaussianNB und ANN, jeweils Standard/EDA-adaptiert) mit strikt
  train-only gefittetem Preprocessing und Validation-basierter Auswahl
- Standard-GaussianNB als ausgewähltes Modell (Validation-AP 0,5805; interner Test AP 0,5755)
- unabhängig aus den gespeicherten Predictions reproduzierte Metriken und F1-Schwellen
- Learning Curve und train-only PCA-Vergleich; PCA 10--100 bleibt unter der AP ohne PCA

Die 2D-Projektionen liefern keine vollständige Labeltrennung. Das ist eine Aussage über
die jeweilige Projektion und deren Informationskompression, nicht über die grundsätzliche
Unmöglichkeit einer Klassifikation. Die anonymisierten Features erlauben außerdem keine
fachliche Interpretation einzelner Variablennamen.

### Status des Arbeitsstands

Die aktuelle finale EDA-Datei ist \`EDA/01_Datensatz_Einfuehrung_final.ipynb\`; die Datei
mit dem Suffix \`_alt\` bleibt eine Archivversion. Am 29.08.2026 wurden EDA (25 Codezellen)
und ML (26 Codezellen) vollständig sequenziell und ohne Fehler ausgeführt. Die zuvor
positionsbasiert falsch zugeordneten Welch-/FDR-p-Werte werden nun über Feature-Namen
ausgerichtet; die Gesamtzahl 181/200 bleibt unverändert. Portfolio, Logbuch und
Prüfartefakte verwenden denselben kontrollierten Ergebnisstand.

Als nächste fachliche Schritte sind wiederholte bzw. verschachtelte Cross-Validation,
mehrere ANN-Seeds, eine neu reservierte Schlussbewertung und eine kostenbasierte
Threshold-Wahl vorgesehen. Der bisherige Hold-out war bereits Teil der EDA-Logistic-
Referenz und ist deshalb projektweit nicht vollständig blind.

## 5. Aufbau des E-Portfolios

~~~
ADA_138_Sawarzynski_Portfolio.tex
└── \input{Logbuch_Santander_Cyp.tex}
~~~

Die Hauptdatei \`ADA_138_Sawarzynski_Portfolio.tex\` erzeugt das vollständige Portfolio.
Das separat gepflegte \`Logbuch_Santander_Cyp.tex\` wird per \`\\input\` in das Portfolio
integriert. Dadurch bleibt das Logbuch als Arbeitsdatei übersichtlich, erscheint aber
auch im finalen Portfolio.

Die Portfolio-Zusammenfassung und das Logbuch dürfen nicht unabhängig voneinander veralten:
Neue belastbare Ergebnisse werden zunächst im Notebook erzeugt, anschließend im Logbuch
dokumentiert und danach verdichtet im Portfolio zusammengefasst. Abbildungen des Portfolios
liegen in \`E_Portfolio/assets/\`.

### Portfolio kompilieren

Auf diesem Rechner fehlen der zuerst gefundenen TinyTeX-Installation einzelne Pakete.
Deshalb im Ordner \`Cyp/E_Portfolio\` die vorhandene MiKTeX-Installation zweimal aufrufen:

~~~
$adaXeLaTeX = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"
& $adaXeLaTeX -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
& $adaXeLaTeX -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
~~~

Die finale Datei ist \`ADA_138_Sawarzynski_Portfolio.pdf\`. LaTeX-Zwischendateien wie
\`.aux\`, \`.log\`, \`.out\`, \`.toc\`, \`.fls\` und \`.fdb_latexmk\` bleiben lokale
Buildartefakte. Eine separate Logbuch-PDF wird nicht versioniert.

## 6. Verbindliche passive Pflegeaufgaben

Diese Aufgaben laufen bei jeder weiteren Projektarbeit mit:

- Nach jedem relevanten Arbeitsschritt das Logbuch aktualisieren.
- Im Logbuch Datum, Ziel, Methode, Begründung, Ergebnis, Grenzen, Zeitaufwand und nächsten
  Schritt festhalten.
- Neue EDA-Analysen im aktuellen finalen Notebook ergänzen.
- Neue Grafiken in \`EDA/assets/\` speichern und nicht unabsichtlich bestehende Baselines
  überschreiben.
- Plot-Titel, Achsen, Labelgruppen, Skalierung, Stichprobengröße und verwendete Statistik
  eindeutig beschriften.
- \`target\` in jeder neuen Featurematrix konsequent ausschließen.
- Das Notebook nach Änderungen vollständig ausführen und Fehler sowie Warnungen prüfen.
- Ergebnisse erst nach erfolgreicher Prüfung in Logbuch und Portfolio übernehmen.
- Das Portfolio nach Änderungen an Logbuch oder Portfolio-TeX neu kompilieren.
- Platzhalter im Portfolio schrittweise durch reale Angaben, Zeitaufwände und Reflexionen
  ersetzen.
- Quellen, Softwareversionen, verwendete Bibliotheken und KI-Unterstützung transparent
  dokumentieren.
- Vor Commit und Push \`git diff\` und \`git status\` prüfen.
- Nur absichtlich geänderte Dateien auf \`dev-cyp\` committen.
- Niemals Rohdaten oder Dateien der anderen Gruppenmitglieder verändern.

## 7. Sicherer Standardablauf

### Arbeitsbeginn

~~~
git status --short --branch
~~~

Danach ausschließlich relevante Dateien innerhalb von \`Cyp\` bearbeiten.

### EDA prüfen

~~~
jupyter nbconvert --to notebook --execute --inplace Cyp/EDA/01_Datensatz_Einfuehrung_final.ipynb
~~~

Dieser Befehl verändert das Notebook durch die gespeicherten Outputs und darf deshalb
nur ausgeführt werden, wenn diese Änderung ausdrücklich Teil des aktuellen Arbeitsschritts
ist. Vorher und nachher sind Diff und Ausführungsergebnis zu prüfen.

### Portfolio prüfen

~~~
Set-Location Cyp/E_Portfolio
$adaXeLaTeX = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"
& $adaXeLaTeX -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
& $adaXeLaTeX -interaction=nonstopmode -halt-on-error ADA_138_Sawarzynski_Portfolio.tex
Set-Location ../..
~~~

### Abschlusskontrolle

~~~
git diff -- Cyp
git status --short --branch
~~~

Die neue README wird wegen der aktuellen Ignore-Regel gezielt aufgenommen:

~~~
git add -f Cyp/README.md
~~~

Die bestehende \`.gitignore\` wird dafür nicht verändert.

## 8. Definition eines sauberen nächsten Arbeitsschritts

Ein Arbeitsschritt ist erst abgeschlossen, wenn:

1. die Analyse oder Änderung im vorgesehenen Bereich umgesetzt wurde;
2. die Ergebnisse reproduzierbar geprüft wurden;
3. die relevanten Grafiken oder Tabellen gespeichert sind;
4. das Logbuch den Arbeitsschritt vollständig dokumentiert;
5. die Portfolio-Zusammenfassung bei relevanten Befunden aktualisiert wurde;
6. Notebook und Portfolio ohne Fehler erzeugt werden können;
7. der Diff nur beabsichtigte Änderungen enthält.

Damit bleibt nachvollziehbar, was analysiert wurde, warum eine Methode gewählt wurde,
welche Unsicherheiten bestehen und welcher nächste Schritt fachlich sinnvoll ist.
