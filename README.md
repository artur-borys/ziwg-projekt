# Instalacja
Myślałem, że pipenv fajnie zadziała albo będzie się dało jakoś to zrobić na requirements.txt, ale nie, bo klarin sobie zrobiło własny indeks z modułem.

Potrzebny Python 3.6+ i Linux, a potem zależności :
``` bash
python3 -m pip install pandas
python3 -m pip install -i https://pypi.clarin-pl.eu lpmn_client
```

Jak się wszystko zainstaluje, to w metodzie ner() w pliku ``main.py`` wpisz swój adres e-mail, zapisz, a potem ``python3 main.py``, wypowiedzi zostaną wczytane z ``wypowiedzi.tsv``, zostanie wyświetlone podsumowanie
zbioru i zostanie wywołane zapytanie do Clarinu do [NER](https://ws.clarin-pl.eu/ner.shtml). Odpowiedź zostanie zapisana do pliku ``test.zip`` gdzie będzie plik z jakimś uuid w nazwie i w nim będzie XML.

Chyba i tak będzie trzeba ogarnąć to Clarin API na piechotę żeby potem ładnie połączyć wyniki z metadanymi (autor, partia, data, opis)