# Klasifikace popisků

V registru se nachází osoby, které nemají přiřazený jeden z cca 50 standardizovaných popisků. 
Na základě nestandardizovaných popisků chceme takovým osobám přiřazovat jeden ze standardizovaných popisků.

`pre-classification.R` - skript pro úpravu existujících popisků, doplňuje popisek
`mluvčí` u osob, které mají popisek `mluvčí ___`, a opravuje překlepové popisky
(tj. ty s Damerau-Levenshteinovou vzdáleností == 1).

## Postup

1. na osobách se standardizovanými popisky natrénovat naïve Bayes model (využívající DFM)
2. ?
3. Profit