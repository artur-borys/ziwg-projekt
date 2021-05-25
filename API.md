# Serwer API
Serwer API można wywołać poprzez:
``` bash
python server.py [-p | --port numer_portu, domyślnie 8080]
```

## CORS
Serwer powinien przyjmować zapytania cross-origin bez problemu

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
      "method": "POST",
      "path": "/similarity/"
    }
  ]
}
```

### ``GET /text/{id}``
Zwraca zawartość wypowiedzi o podanym ``id``, np.
``` json
// GET /text/1
{
  "author": "Mateusz Morawiecki",
  "party": "PiS",
  "summary": "Wirus jest w odwrocie 2",
  "date": "01.07.2020",
  "content": "Cieszę się, że coraz mniej obawiamy się tego wirusa, tej epidemii. To jest dobre podejście, bo on jest w odwrocie. Już teraz nie trzeba się go bać. Trzeba pójść na wybory tłumnie 12 lipca. Wszyscy, zwłaszcza seniorzy, nie obawiajmy się, idźmy na wybory. To ważne, żeby móc kontynuować tę sprawiedliwą linię rozwoju."
}
```

### ``POST /similarity/``
Zwraca posortowaną listę według wyniku podobieństwa. Przyjmuje zapytanie o treści w formacie JSON:

| Klucz  | Wartości |
| -----  | -------- |
| `method` | ``bow``, ``tfidf`` lub ``jaccard`` |
| `text`   | tekst do analizy |
| `corpus_variant` | `full` lub `base` |

Przykład zapytania:
``` json
// POST /similarity
{
  "method": "tfidf",
  "text": "Próbuje się nam proszę państwa wmówić, że to ludzie. A to jest po prostu ideologia. Jeżeli ktoś ma jakiekolwiek wątpliwości, czy to jest ideologia, czy nie, to niech sobie zajrzy w karty historii i zobaczy, jak wyglądało na świecie budowanie ruchu LGBT, niech zobaczy jak wyglądało budowanie tej ideologii, jakie poglądy głosili ci, którzy ją budowali.",
  "corpus_variant": "base"
}
```

Przykład odpowiedzi:
``` json
[
  {
    "score": 0.32829168214011767,
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