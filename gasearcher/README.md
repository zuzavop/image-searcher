# Specifikace - GASearcher

Načtení dat zpracovaných pomocí neuronové sítě CLIP probíhá po spuštění serveru ze souboru [models](gas/models.py).

Vyhledávání v datasetech je zpracováno jako dotaz na [server](gas/view.py).

Veškerá data týkající se uživatelského rozhraní jsou rozdělena na soubory [html](templates), [css](static/css) a [javascriptu](static/js).

Projekt obsahuje dva datasety obsahující podstatná jména, která jsou použita jako class ve vyhledávači:

1. [dataset](static/data/nounlist.txt) - obsahující 6800 podstatných jmen

2. [dataset](static/data/sea_nounlist.txt) - obsahující názvy podmořských živočíchů