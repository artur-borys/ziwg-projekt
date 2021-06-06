# Serwer API
Serwer API można wywołać poprzez:
``` bash
python server.py [-p | --port numer_portu, domyślnie 8080]
```

## CORS
Serwer powinien przyjmować zapytania cross-origin bez problemu

## Postman
Kolekcja zapytań w Postmanie jest dostępna [tutaj](./ziwg.postman_collection.json)

## Endpointy

### ``GET /``
Zwraca status i spis wszystkich endpointów, np.
``` json
{
  "status": "ok",
  "endpoints": [
    {
      "method": "GET",
      "path": "/"
    },
    {
      "method": "GET",
      "path": "/text/{id}"
    },
    {
      "method": "GET",
      "path": "/corpuses"
    },
    {
      "method": "POST",
      "path": "/similarity"
    }
  ]
}
```

### ``GET /corpuses``
Zwraca listę dostępnych korpusów. Korpusy powinny być dodawane w dwóch
wariantach do katalogu `corpuses`:
* `nazwa_korpusu.tsv` - na wzór `wypowiedzi_politykow.tsv` - pełne formy tekstów
* `nazwa_korpusu_base.tsv` - na wzór `wypowiedzi_politykow_base.tsv` - zlematyzowane teksty

Endpoint zwraca tylko rdzeń nazwy korpusu (a więc nie wyświetla wariantu `*_base.tsv`)

Przykład:
``` json
// GET /corpuses
{
  "data": [
    "wypowiedzi_politykow"
  ]
}
```

### ``GET /text/{id}?corpus_name=nazwa_korpusu``
Zwraca zawartość tekstu o podanym ``id`` w podanym ``corpus_name``

W przypadku nie znalezienia korpusu lub wypowiedzi, zwraca status 404.
W przypadku nie podania `corpus_name` zwraca status 400
``` json
// GET /text/1?corpus_name=wypowiedzi_politykow
{
  "author": "Mateusz Morawiecki",
  "party": "PiS",
  "summary": "Wirus jest w odwrocie 2",
  "date": "01.07.2020",
  "content": "Cieszę się, że coraz mniej obawiamy się tego wirusa, tej epidemii. To jest dobre podejście, bo on jest w odwrocie. Już teraz nie trzeba się go bać. Trzeba pójść na wybory tłumnie 12 lipca. Wszyscy, zwłaszcza seniorzy, nie obawiajmy się, idźmy na wybory. To ważne, żeby móc kontynuować tę sprawiedliwą linię rozwoju."
}
```

### ``POST /similarity``
Zwraca posortowaną listę według wyniku podobieństwa. Przyjmuje zapytanie o treści w formacie JSON:

W przypadku błędu w zapytaniu, zwróci odpowiedź o kodzie 400 (Bad Request), a w kluczu `errors` będą opisane błędy.

| Klucz  | Wartości |
| -----  | -------- |
| `method` | ``bow``, ``tfidf`` lub ``jaccard`` |
| `text`   | tekst do analizy |
| `corpus_variant` | `full` lub `base` |
| `corpus_name` | jedna z wartości zwracanej przez ``GET /corpuses`` |

Jeśli `corpus_variant` jest `base` to `text` jest również lematyzowany i porównywany ze zlematyzowanym korpusem.

Przykład zapytania:
``` json
// POST /similarity
{
  "method": "tfidf",
  "text": "Próbuje się nam proszę państwa wmówić, że to ludzie. A to jest po prostu ideologia. Jeżeli ktoś ma jakiekolwiek wątpliwości, czy to jest ideologia, czy nie, to niech sobie zajrzy w karty historii i zobaczy, jak wyglądało na świecie budowanie ruchu LGBT, niech zobaczy jak wyglądało budowanie tej ideologii, jakie poglądy głosili ci, którzy ją budowali.",
  "corpus_variant": "full",
  "corpus_name": "wypowiedzi_politykow"
}
```

Przykład odpowiedzi:
``` json
[
  {
    "score": 0.999999999999999,
    "author": "Andrzej Duda",
    "party": "PiS",
    "summary": "LGBT",
    "date": "13.06.2020",
    "content": "Próbuje się nam proszę państwa wmówić, że to ludzie. A to jest po prostu ideologia. Jeżeli ktoś ma jakiekolwiek wątpliwości, czy to jest ideologia, czy nie, to niech sobie zajrzy w karty historii i zobaczy, jak wyglądało na świecie budowanie ruchu LGBT, niech zobaczy jak wyglądało budowanie tej ideologii, jakie poglądy głosili ci, którzy ją budowali."
    },
  ...
]
```

Struktura odpowiedzi:

| Klucz | Typ |
| --- | --- |
| score | zawsze `float` w przedziale [0, 1] |
| author | zawsze `string` |
| party | zawsze `string`, `'-'` w przypadku braku partii |
| summary | zawsze `string` |
| date | **Uwaga!!!** zawsze `string` |
| content | Treść wypowiedzi, zawsze w pełnej postaci i zawsze `string` |