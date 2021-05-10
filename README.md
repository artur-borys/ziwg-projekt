# Instalacja
Myślałem, że pipenv fajnie zadziała albo będzie się dało jakoś to zrobić na requirements.txt, ale nie, bo klarin sobie zrobiło własny indeks z modułem.

Najprościej zainstalować przez [pipenv](https://github.com/pypa/pipenv):
``` bash

# Najpierw stworzyć environment, sam korzystam z 3.8, jak chcecie inne to trzeba zmienić wersję w Pipfile, bo będzie krzyczał
pipenv --python 3.8

# Następnie instalacja zależności
# --skip-lock, bo biblioteka Clarinu nie przechodzi locka
pipenv install --skip-lock

# Potem aktywacja środowiska
pipenv shell

# A potem wywołanie, np. bow.py
python bow.py
```


## Odnośnie ``main.py``
Jak się wszystko zainstaluje, to w metodzie ner() w pliku ``main.py`` wpisz swój adres e-mail, zapisz, a potem ``python3 main.py``, wypowiedzi zostaną wczytane z ``wypowiedzi.tsv``, zostanie wyświetlone podsumowanie
zbioru i zostanie wywołane zapytanie do Clarinu do [NER](https://ws.clarin-pl.eu/ner.shtml). Odpowiedź zostanie zapisana do pliku ``test.zip`` gdzie będzie plik z jakimś uuid w nazwie i w nim będzie XML.

Chyba i tak będzie trzeba ogarnąć to Clarin API na piechotę żeby potem ładnie połączyć wyniki z metadanymi (autor, partia, data, opis)