import pandas as pd
from lpmn_client.src.requester import Requester

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

print_stats(statements)
stmnt = statements.loc[0]

ner(stmnt['Treść'])