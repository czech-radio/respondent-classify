# README

Klasifikace popisků - přiřazení obecného popisku osobě podle specifických popisků

`create_model.ipynb` - vytvoření modelu pro klasifikace
`classify_new.ipynb` - zkouška klasifikace pro nové osoby

`*.pickle` - uložené modely a soubory nutné pro predikci


## OLD R

`pre-classification.R` - skript pro úpravu existujících popisků, doplňuje popisek `mluvčí` u osob, které mají popisek `mluvčí ___`, a opravuje překlepové popisky (tj. ty s Damerau-Levenshteinovou vzdáleností == 1).