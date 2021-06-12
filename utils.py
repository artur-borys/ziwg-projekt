import glob
from itertools import combinations
from os import stat, path
import pandas as pd
from requests.api import head
import clarin
import re

def export_to_excel(corpus, similarities, filename='results'):
  print(f'Eksportowanie do arkusza Excel ({filename}.xlsx)...')
  author1_col = []
  author2_col = []
  party1_col = []
  party2_col = []
  text1_col = []
  text2_col = []
  topic1_col = []
  topic2_col = []
  score_col = []

  for data in similarities:
    id1 = data[0][0]
    id2 = data[0][1]
    score = data[1]

    text1 = corpus.loc[[id1], ['Treść']].squeeze()
    text2 = corpus.loc[[id2], ['Treść']].squeeze()
    topic1 = corpus.loc[[id1], ['Temat (krótki opis)']].squeeze()
    topic2 = corpus.loc[[id2], ['Temat (krótki opis)']].squeeze()
    author1 = corpus.loc[[id1], ['Autor']].squeeze()
    author2 = corpus.loc[[id2], ['Autor']].squeeze()
    party1 = corpus.loc[[id1], ['Partia']].squeeze()
    party2 = corpus.loc[[id2], ['Partia']].squeeze()

    text1_col.append(text1)
    text2_col.append(text2)
    topic1_col.append(topic1)
    topic2_col.append(topic2)
    author1_col.append(author1)
    author2_col.append(author2)
    party1_col.append(party1)
    party2_col.append(party2)
    score_col.append(score)

  data = {
    'topic1': topic1_col,
    'topic2': topic2_col,
    'score': score_col,
    'author1': author1_col,
    'author2': author2_col,
    'party1': party1_col,
    'party2': party2_col,
    'text1': text1_col,
    'text2': text2_col
  }

  df = pd.DataFrame(data=data)

  df.to_excel(f'./{filename}.xlsx', index=False, header=True)
  print('Gotowe')


def load_statements(filepath: str) -> pd.DataFrame:
  print(f'Wczytywanie korpusu z pliku {filepath}')
  statements = pd.read_csv(filepath, sep="\t")
  
  # pandas błędnie odczytuje dodatkową kolumnę i trzeba ją usunąć
  statements = statements.iloc[:, 0:5]

  # wyczyszczenie rekordów z pustą "Treścią"
  statements.dropna(subset=["Treść"], inplace=True)
  print('Gotowe')

  return statements

def get_pairs(corpus: pd.DataFrame):
  """ Zwraca wszystkie pary wyrażeń w podanym korpusie"""
  return combinations(corpus.iterrows(), 2)
  
def convert_statements_to_base_words_and_load(filepath: str) -> pd.DataFrame:
  statements = load_statements(filepath)
  
  user = '235730@student.pwr.edu.pl'
  clarin.set_user(user)

  print('Konwertowanie wyrazów do ich podstawowej formy.')
  statements['Treść'] = statements['Treść'].apply(lambda text: clarin.get_base_words(text))
  statements.to_csv(filepath.replace('.tsv', '_base.tsv'), sep="\t",index= False ,header=True)

  return statements

def translate_statement_dict(statement):
  return {
    'author': statement['Autor'],
    'party': statement['Partia'],
    'summary': statement['Temat (krótki opis)'],
    'date': statement['Data'],
    'content': statement['Treść']
  }

def get_available_corpuses():
  # UGH, Łanadołs kurła!
  separator = path.sep
  # Find only primary corpuses, discard *_base variants
  corpuses = glob.glob(f".{separator}corpuses{separator}*[!_base].tsv")
  corpuses = [c.split(separator)[2].split('.tsv')[0] for c in corpuses]
  return corpuses

def remove_linking_words(text: str) -> str:
  linking_words_regex = r'\s+(i|ale|jednak|lecz|albo|bądź|oraz|a|także|lub|też|no)\s+'
  while re.search(linking_words_regex, text):
    text = re.sub(linking_words_regex, " ", text)
  return text