# respondent-classifier

V registru se nachází osoby, které nemají přiřazený jeden z cca 50 standardizovaných popisků. 
Na základě nestandardizovaných popisků chceme takovým osobám přiřazovat jeden ze standardizovaných popisků.

## TODO

1. Add stemmer
2. Implement Male/Female job name unification
3. Better lemmanizator
4. Missclick detection

## Postup

1. Na osobách se standardizovanými popisky natrénovat naïve Bayes model (využívající DFM)
2. ?
3. Profit

## OLD

`pre-classification.R` - skript pro úpravu existujících popisků, doplňuje popisek
`mluvčí` u osob, které mají popisek `mluvčí ___`, a opravuje překlepové popisky
(tj. ty s Damerau-Levenshteinovou vzdáleností == 1).
