# Labeler

- labeler: The library to train machine learning model for classification.
- server: The web application to serve trained model over HTTP REST API.

## Problems

- Hard coded services e.g. `localhost:8000` for lematization etc.
- Separate domain logic and services.

---

## Poznámky

### Návrhy na změny

- Adresář `server` bych přejmenoval na `service`.

### Malá rekapitulace projektu

Jde vlastně o tři samostatné projekty/moduly:

1. Trénování a ověřování modelu strojového učení na zadaných datech.

   To je v podstatě kolona (*pipeline*), jejíž vstupem jsou trénovací data a výstupem model pro klasifikaci v podobě binárního souboru.
   Takový model bychom měli verzovat a poznamenávat na jakých datach byl trénován a jaké podává výsledky. V budoucnu se může stát, že
   budeme pracovat na vylepšení modelu a proto bychom měli ctoto mít pod kontrolou. Výsledný model se pak buď může ukládat přímo do
   kontejneru ve kterém poběží služba (*service*) paracující s tímto modelem nebo může být uložen na serveru. Toto je nutné ještě
   rozhodnout. Tato část může být realizováná v podobě notebooků bnebo jednoduché aplikace s konzolovým rozhraním (CLI) -- což by
   určitě zjednodušilo opakované použití  -- přeci jen notebooky jsou horší na zprávu -- ale i to se dá nějak nastavit a udržovat viz
   
   - https://netflixtechblog.com/notebook-innovation-591ee3221233
   - https://netflixtechblog.com/scheduling-notebooks-348e6c14cfd6
    
2. Knihovna pro klasifikace.

   Jde v podstatě o jednu velkou funkci, která bere natrénovaný model, vstupní data a vrací odpověď v podobě klasifikační třídy.
   Prakticky jde o Python balík, který se importuje do aplikace, skrze kterou přichází vstupní data viz bod 3.

3. Služba pro klasifikaci.

   Tato služba je aplikace zajišťující požadovanou funkcionalitu pro uživatele. Její cílem je přijmout vstupní data, v našem případě přes HTTP REST API a
   vrátit odpověď v podobě klasifikační třídy. Důvod proč mít samostatně službu a nepoužívat knihovnu (2) přímo je, že nás odstiňuje od manipulaci s modelem
   a jinými low-level záležitostmi. Takovou službu můžeme přes HTTP používat z jakéhokoliv jiného programu nebo nástroje.

   Tato služba může používat a volat i jiné služby např. službu pro lematizaci/stamatizaci. je otázka, kam tyto služby "dát" v kódu.
   Mají být tato volání osučástí knihovny nebo až tato služba je má jako závislost předávat knihovně. Nebo dokonce má knihovna dostat už
   lematizované/stematizované slovo (token)? Možná že ano. Pojďme se nad tím zamyslet. Jasné je, že *hard-coded* volání např. na `localhost:8080` není
   ideální řešení do budocuna.

   Všechny tyto služby můžeme uvažovat, že běží b kontejnerech nabo že je vlastní třetí strana a nemáme k nim přístup jinak než přes HTTP dotaz.
