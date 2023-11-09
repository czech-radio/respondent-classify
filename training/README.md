# machine learning model

## Motivace a cíl

V registru se nachází osoby, které nemají přiřazený jeden z cca 50 standardizovaných popisků. Na základě nestandardizovaných popisků chceme takovým osobám přiřazovat jeden ze *standardizovaných popisků*.

Soupis standardizovaných popisků:

```text
advokát', 'akademik', 'aktivista', 'blogger', 'byznys', 
'celebrita', 'církev', 'europol', 'komentátor', 'kontrolor', 
'kultura', 'léčitel', 'lobby', 'zdravotník', 'mluvčí', 'ngo', 
'novinář', 'odborník', 'odbory', 'ostatní', 'ombudsman', 
'ozbrojenec', 'politik', 'social', 'soudce', 'soudce_us', 
'spolek', 'sport', 'starosta', 'stát_byznys', 'ttank', 
'umělec', 'úředník', 'vyslanec', 'zaměstnavatel', 'zástupce', 
'záchranář', 'média', 'mezinárodní'
```

## Instalace

```shell
pip install -r requirements.txt
```

## Postup

- Vstupní data se nacházejí v `data/input`.
- První krok je (před)připravit data pomocí notebooku `processing.ipynb`.
- Druhý krok je tvorba a analýza modelu pro klasifikaci pomocí notebooku `analysing.ipynb`.
- Třetí krok uložit model (matice) pomocí modulu `pickle`.

Poté co máme model, můžeme vytvořit jednoduchou REST mikroslužbu.

## Poznámky/Roadmap

1. Problém: Sjednoť popisky v ženském a mužském tvaru např. `politik` a `politička`.
   Řešení: Zřejmě podle slovníku, seznamu. Zkusíme se doptat na ÚJČ.

3. Problém: Potřebujeme ideálně získat kořen slova/popisku abychom seskupili ty popisky (např. `politik` a `politické hnutí`), které odkazují na stejný základ.
   Řešení: Použít nějaký stemmer nebo slovník.

4. Problém: Potřebujeme lematizovat. Prozatím používáme MorphoDiTa.
   Řešení: Lepší využít službu Geneea. Musíme napsat funkci pro zaslání popisků na tuto službu.

5. Problém: Missclick/Grammar error detection.
   Řešení: Nějaká služba/knihovna na autokorekci? Vlastní řešení?

- [ ] Kolik máme unikátních popisků? cca 28 000
- [ ] Kolik je z nich je překlep (missclick)?
  