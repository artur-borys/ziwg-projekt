# Instalacja
Najprościej zainstalować przez [pipenv](https://github.com/pypa/pipenv):
``` bash

# Najpierw stworzyć environment, sam korzystam z 3.8, jak chcecie inne to trzeba zmienić wersję w Pipfile, bo będzie krzyczał
pipenv --python 3.8

# Następnie instalacja zależności
# --skip-lock, bo biblioteka Clarinu nie przechodzi locka
pipenv install --skip-lock

# Potem aktywacja środowiska
pipenv shell

# A potem np. przeprowadzenie wszystkich testów
python similarity_tests.py --all
```

**UWAGA** użyjcie swojego adresu e-mail w ``clarin.set_user(adres_email)``
# Struktura
* ~~``main.py``~~ - w sumie sobie tak o jest, można zmienić, tam tylko próbowałem wczytać wypowiedzi z tsv
* ``clarin.py`` - kod komunikacji z API Clarinu
* ``utils.py`` - zawiera przydatne funkcje pomocnicze, jak np. export do xlsx czy wczytanie wypowiedzi, czy wygenerowanie par dla danego zbioru
* ``similarities.py`` - zawiera funkcje, które wykonują dane metody
* ``similarity_tests.py`` - służy do przeprowadzania testów na metodach z ``similarities.py``. Można wywołać ``python similarity_tests.py --help`` żeby zobaczyć listę dostępnych argumentów: np. ``--all`` do przeprowadzenia wszystkich testów, albo ``--jaccard`` do przeprowadzenia tylko Jaccard Similarity
* ``wypowiedzi.tsv`` - zawiera wypowiedzi wyeksportowane bezpośrednio z arkusza
* ``wypowiedzi_base.tsv`` - zawiera wypowiedzi po sprowadzeniu wyrazów do formy podstawowej
* ``results/*`` - tutaj należy zapisywać wyniki testów, patrz na plik ``similarity_tests.py``
* ``server.py`` - serwer API projektu
* ``front/`` - kod źródłowy front-endu
* ``corpuses/`` - zawiera korpusy dla serwera API. Każdy korpus powinien być w dwóch wariantach:
  * ``nazwa_korpusu.tsv`` - na wzór ``corpuses/wypowiedzi_polityków.tsv``
  * ``nazwa_korpusu_base.tsv`` - na wzór ``corpuses/wypowiedzi_politykow_base.tsv``, czyli po lematyzacji

# Dokumentowanie
Można skorzystać z [docstringów](https://www.python.org/dev/peps/pep-0257/). Wtedy po najechaniu myszą na daną metodę, powinien być widoczny opis i argumenty.

# Serwer API
Dokumentacja serwera API znajduje się [tutaj](./API.md)

# API Clarin
Czasem może się przydać wywołanie zapytania do [Clarinu](https://wiki.clarin-pl.eu/pl/nlpws/query).
W pliku ``clarin.py`` będą znajdować się wszystkie służące temu metody.

Podstawową metodą jest tam ``request(lpmn, text)``, która wysyła zapytanie do API Clarinu i zwraca odpowiedź w formie tekstu, a nie pliku zip jak robi to oficjalny moduł.

Trzeba określić użytkownika za pomocą ``set_user(user)``. Powinien to być adres e-mail, ale pewnie może to być cokolwiek - nie trzeba się nigdzie rejestrować.

Oprócz tego jest tam metoda ``get_base_words(text)``, która przekształca zadany tekst w taki, który zawiera podstawowe formy wyrazów, co może być przydatne w niektórych metodach. Ogółem tzw. **lematyzacja**

# Instalacja nowych modułów
Najlepiej zrobić to za pomocą pipenva:
``` bash
pipenv install nazwa_modułu --skip-lock
```
**Ważny jest tutaj ``--skip-lock``, bo jeszcze zostawiłem w zależnościach oficjalną bibliotekę Clarinu, która jest spoza oficjalnego repo Pythona i nie można na niej zrobić locka**

Po dodaniu zależności, każdy po zrobienia pulla powinien wywołać ``pipenv install --skip-lock``
# Stary opis
## Odnośnie ``main.py``
Jak się wszystko zainstaluje, to w metodzie ner() w pliku ``main.py`` wpisz swój adres e-mail, zapisz, a potem ``python3 main.py``, wypowiedzi zostaną wczytane z ``wypowiedzi.tsv``, zostanie wyświetlone podsumowanie
zbioru i zostanie wywołane zapytanie do Clarinu do [NER](https://ws.clarin-pl.eu/ner.shtml). Odpowiedź zostanie zapisana do pliku ``test.zip`` gdzie będzie plik z jakimś uuid w nazwie i w nim będzie XML.

Chyba i tak będzie trzeba ogarnąć to Clarin API na piechotę żeby potem ładnie połączyć wyniki z metadanymi (autor, partia, data, opis)