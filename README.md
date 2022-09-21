# Ročníkový projekt

## Specifikace - GASearcher
Projekt se zabývá vyhledáváním a textovou klasifikací snímků, pomocí které uživatel může reformulovat textový dotaz do multimediální databáze. Tato strategie je vhodná hlavně díky tomu, že uživatele nemusí vždy napadnout nejpřesnější slova ze slovníku popisující vyhledávané video, tzv. „semantic gap problem”. A právě díky textové klasifikace mezivýsledku může uživatel efektivně reformulovat textový dotaz.
Popisovaný projekt bude realizován jako webová aplikace, ve které bude možné vyhledávání v multimediální databázi s využitím výše popsaného postupu. Textové dotazy do databáze a práce s neuronovou sítí [CLIP](https://beta.openai.com/) budou implementovány v Pythonu a webové rozhraní zobrazující výsledky hledání bude vyvinuto v PHP a JavaScriptu.

Podrobnější specifikace je v [pdf](Project_specification.pdf) a aktuální verzi lze zobrazit také jako [projekt](https://www.overleaf.com/read/fgthfnksmwkn) v overleaf.

Samotný projekt webové aplikace GASearcher je v [této složce](gasearcher) i s popisem funkčnosti.

Pomocný kód na zpracování snímků a jejich klasifikaci je přiložený v [složce src](src). Složka obsahuje [kód](src/parse_video.py) na zpracování videí na jednotlivé snímky, [klasifikaci](src/top_classes.py) snímků do classes a [kód](src/images_to_clip.py) na získání feature snímků ze sítě CLIP.