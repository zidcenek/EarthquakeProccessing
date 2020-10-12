# Konverze dat zemětřesení
## Instalační příručka: 
**Nainstalovaný Python 3 (doporučená verze 3.7 nebo vyšší):** \
Nutné balíčky ke spuštění nainstalované v Python 3:
- pip install numpy
- pip install pandas

## Data (vstupní data)
Vstupní data jsou brána ze složky *data* a je pracováno se soubory typu *.bul*.
Soubory nesplňující předepsaný počet sloupců nejsou zpracovány.

## Output (výstupní data)
Výstupní data jsou ve formátu *.csv* uloženy do souboru *output*. Jednotlivé sloupce jsou odděleny pomocí tabulátoru.
Při duplicitě dat jsou vytvořeny různé výstupní soubory, pokud jsou stejné jsou smazány do jednoho.

## Src
V adresáři se nachází spustitelná verze skriptu

## Jupyter 
V adresáři se nachází verze ve formátu Jupyter notebooku.

## Comp.sh 
Shell skript pro porovnání souborů (jeho obdoba je zahrnuta i v hlavním skriptu).