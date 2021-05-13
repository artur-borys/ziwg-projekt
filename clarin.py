import requests
import json
import time
from urllib import parse
from bs4 import BeautifulSoup

BASE_URL = 'https://ws.clarin-pl.eu/nlprest2/base/'
START_TASK = 'startTask'
GET_STATUS = 'getStatus/'
DOWNLOAD_RESULT = 'download'

IGNORED_CHARS = ['.', ',', '!', '?', ';', ':', '-', '(', ')', '[', ']', '{', '}']

USER = ''

def set_user(user: str):
  """ Ustawia użytkownika jaki wykonuje zapytania do clarinu. Powinien to być adres e-mail"""
  global USER
  USER = user


def request(lpmn: str, text: str):
  """Wywołuje zapytanie do API Clarinu i zwraca odpowiedź w formie tekstu.
  
  Argumenty:
  lpmn -- zapytanie lpmn https://wiki.clarin-pl.eu/pl/nlpws/query
  text -- tekst na jakim mają zostać wykonane operacje z lpmn

  Wyjątek:
  ValueError -- wymaga określenia użytkownika za pomocą set_user()
  """

  if len(USER.strip()) == 0:
    raise ValueError('Musisz określić użytkownika (set_user())')
  requestUrl = parse.urljoin(BASE_URL, START_TASK)
  print(requestUrl)
  requestData = {
    'application': 'ws.clarin-pl.eu',
    'lpmn': lpmn,
    'text': text,
    'user': USER
  }

  r = requests.post(requestUrl, json.dumps(requestData))

  taskId = r.text

  statusUrlBase = parse.urljoin(BASE_URL, GET_STATUS)
  statusUrl = parse.urljoin(statusUrlBase, taskId)

  downloadPath = ''

  while True:
    r = requests.get(statusUrl)

    resp = r.json()

    if resp['status'] == 'DONE':
      downloadPath = resp['value'][0]['fileID']
      break
    time.sleep(0.25)
  
  downloadUrlBase = parse.urljoin(BASE_URL, DOWNLOAD_RESULT)
  downloadUrl = downloadUrlBase + downloadPath

  r = requests.get(downloadUrl)
  return r.text

def get_base_words(text: str, as_str=True):
  """ Zwraca tekst albo tablicę złożoną z podstawowych form wyrazów w podanym tekście.
  Usuwa znaki interpunkcyjne (ale to jest do dopracowania)
  
  Argumenty:
  text: str -- tekst do przetworzenia
  as_str: bool -- jeśli prawda to zwraca tekst, a jeśli fałsz to zwraca tablicę ze słowami
  """

  lpmn = 'any2txt|wcrft2|liner2({"model":"top9"})'

  response = request(lpmn, text)
  bs = BeautifulSoup(response, 'lxml')
  base_tags = bs.select('tok lex:first-of-type base')
  base_words = []
  for base_tag in base_tags:
    value = base_tag.next_sibling
    if value.strip() not in IGNORED_CHARS:
      base_words.append(value)
  
  if as_str:
    return ' '.join(base_words)
  return base_words

if __name__ == '__main__':
  text = 'Woda jest jedną z najpospolitszych substancji we Wszechświecie.Cząsteczka wody jest trzecią najbardziej rozpowszechnioną molekułą w ośrodku międzygwiazdowym, po cząsteczkowym wodorze i tlenku węgla. Jest również szeroko rozpowszechniona w Układzie Słonecznym: stanowi istotny element budowy Ceres i księżyców lodowych krążących wokół planet-olbrzymów, jako domieszka występuje w ich atmosferach, a przypuszcza się, że duże jej ilości znajdują się we wnętrzach tych planet. Jako lód występuje także na części planetoid, a zapewne również na obiektach transneptunowych. Woda jest bardzo rozpowszechniona także na powierzchni Ziemi. Występuje głównie w oceanach, które pokrywają 70,8% powierzchni globu, ale także w rzekach, jeziorach i w postaci stałej w lodowcach. Część wody znajduje się w atmosferze (chmury, para wodna). Niektóre związki chemiczne zawierają cząsteczki wody w swojej budowie (hydraty – określa się ją wówczas mianem wody krystalizacyjnej). Zawartość wody włączonej w strukturę minerałów w płaszczu Ziemi może przekraczać łączną zawartość wody w oceanach i innych zbiornikach powierzchniowych nawet dziesięciokrotnie.'
  set_user('235730@student.pwr.edu.pl')

  print(get_base_words(text))