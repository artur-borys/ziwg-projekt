import pandas as pd
from lpmn_client.src.requester import Requester

import clarin

def load_statements(filepath: str) -> pd.DataFrame:
  statements = pd.read_csv(filepath, sep="\t")
  
  # pandas błędnie odczytuje dodatkową kolumnę i trzeba ją usunąć
  statements = statements.iloc[:, 0:5]

  # wyczyszczenie rekordów z pustą "Treścią"
  statements.dropna(subset=["Treść"], inplace=True)

  return statements


def print_stats(statements: pd.DataFrame):
  authors = statements['Autor']
  parties = statements['Partia']

  print("======== Autorzy: ==========")
  print(authors.value_counts())
  print("======== Partie:  ==========")
  print(parties.value_counts())

def ner(statement_content: str):
  requester = Requester('[adres e-mail]')
  lpmn_query = "any2txt|wcrft2|liner2({\"model\":\"top9\"})"
  
  strings = requester.upload_strings([statement_content])
  response = requester.process_query(lpmn_query, [s.text for s in strings])
  requester.download_response(response[0], './test.zip')

statements = load_statements('./wypowiedzi.tsv')

# print_stats(statements)
stmnt = statements.loc[0]

lpmn = 'any2txt|wcrft2|liner2({"model":"top9"})'
text = 'Woda jest jedną z najpospolitszych substancji we Wszechświecie.Cząsteczka wody jest trzecią najbardziej rozpowszechnioną molekułą w ośrodku międzygwiazdowym, po cząsteczkowym wodorze i tlenku węgla. Jest również szeroko rozpowszechniona w Układzie Słonecznym: stanowi istotny element budowy Ceres i księżyców lodowych krążących wokół planet-olbrzymów, jako domieszka występuje w ich atmosferach, a przypuszcza się, że duże jej ilości znajdują się we wnętrzach tych planet. Jako lód występuje także na części planetoid, a zapewne również na obiektach transneptunowych. Woda jest bardzo rozpowszechniona także na powierzchni Ziemi. Występuje głównie w oceanach, które pokrywają 70,8% powierzchni globu, ale także w rzekach, jeziorach i w postaci stałej w lodowcach. Część wody znajduje się w atmosferze (chmury, para wodna). Niektóre związki chemiczne zawierają cząsteczki wody w swojej budowie (hydraty – określa się ją wówczas mianem wody krystalizacyjnej). Zawartość wody włączonej w strukturę minerałów w płaszczu Ziemi może przekraczać łączną zawartość wody w oceanach i innych zbiornikach powierzchniowych nawet dziesięciokrotnie.'
user = '241323@student.pwr.edu.pl'

response = clarin.request(lpmn, text, user)

print(clarin.get_base_words(response))