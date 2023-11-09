# respondent-classifier

**A REST service to classify respondents based on their labels.**

The register contains people who do not have one of the approximately 50 standardized labels assigned to them. On the basis of non-standardized labels, we want to assign one of the *standardized labels* to such persons.

## Overview

This is a monorepository which consists of these parts:

|directory|description|
|----|-------|
|model| Train machine learning model.
|server| Serve model over HTTP REST.
|vendor| The third party software HTTP REST services.

## Deployment

**Prerequisities:** For the use of of program required services are: morphodita, korektor

At first, external services in the `vendor` directory must be built before you are running them for the first time.

```shell
cd vendor/morphodita 
source build.sh
cd -
```

```shell
cd vendor/korektor 
source build.sh
cd -
```

Than all services should be started with `run.sh` script.

```shell
. vendor/korektor/run.sh 8080
. vendor/morphodita/run.sh 8080
```

### Development

See [server](server/README.md) and [training](training/README.md). 

## Poznámky (cs)

### Návrhy na změny

- [ ] Rozděl trénování a "používání" na dva balíky.

### Malá rekapitulace projektu

Jde vlastně o tři samostatné projekty/moduly:

1. Trénování a ověřování modelu strojového učení na zadaných datech.

   To je v podstatě kolona (*pipeline*), jejíž vstupem jsou trénovací data a výstupem model pro klasifikaci v podobě binárního souboru.
   Takový model bychom měli verzovat a poznamenávat na jakých datach byl trénován a jaké podává výsledky. V budoucnu se může stát, že
   budeme pracovat na vylepšení modelu a proto bychom měli ctoto mít pod kontrolou. Výsledný model se pak buď může ukládat přímo do
   kontejneru ve kterém poběží služba (*service*) paracující s tímto modelem nebo může být uložen na serveru. Toto je nutné ještě
   rozhodnout. Tato část může být realizováná v podobě notebooků bnebo jednoduché aplikace s konzolovým rozhraním (CLI) -- což by
   určitě zjednodušilo opakované použití  -- přeci jen notebooky jsou horší na zprávu -- ale i to se dá nějak nastavit a udržovat viz

   - <https://netflixtechblog.com/notebook-innovation-591ee3221233>
   - <https://netflixtechblog.com/scheduling-notebooks-348e6c14cfd6>

2. Knihovna pro klasifikaci.

   Jde v podstatě o jednu velkou funkci, která bere natrénovaný model, vstupní data a vrací odpověď v podobě klasifikační třídy.
   Prakticky jde o Python balík, který se importuje do aplikace, skrze kterou přichází vstupní data viz bod 3.

3. Služba pro klasifikaci.

   Tato služba je aplikace zajišťující požadovanou funkcionalitu pro koncovéhp uživatele. Její cílem je přijmout vstupní data, v našem případě přes HTTP REST API a
   vrátit odpověď v podobě klasifikační třídy. Důvod proč mít samostatně službu a nepoužívat knihovnu (2) přímo je, že nás odstiňuje od manipulaci s modelem
   a jinými *low-level* záležitostí. Takovou službu můžeme přes HTTP používat z jakéhokoliv jiného programu nebo nástroje.

   Tato služba může používat a volat i jiné služby např. službu pro lematizaci/stamatizaci. Je otázka, do jaké části projektu tyto služby patří.
   Mají být tato volání součástí knihovny nebo až tato služba je má jako závislost předávat knihovně? Nebo dokonce má knihovna dostat už
   lematizované/stematizované slovo (token)? Možná že ano. Pojďme se nad tím zamyslet. Jasné je, že *hard-coded* volání např. na `localhost:8080` není
   ideální řešení do budocuna.

   Všechny tyto služby můžeme uvažovat, že běží v kontejnerech nabo že je vlastní třetí strana a nemáme k nim přístup jinak než přes HTTP dotaz.
