import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations

def load_statements(filepath: str) -> pd.DataFrame:
  print('Wczytywanie korpusu z pliku CSV')
  statements = pd.read_csv(filepath, sep="\t")
  
  # pandas błędnie odczytuje dodatkową kolumnę i trzeba ją usunąć
  statements = statements.iloc[:, 0:5]

  # wyczyszczenie rekordów z pustą "Treścią"
  statements.dropna(subset=["Treść"], inplace=True)
  print('Gotowe')

  return statements

def calculate_similarities(corpus: pd.DataFrame) -> tuple:
  print('Obliczanie podobieństw dla wszystkich par')
  pairs = combinations(corpus.iterrows(), 2)

  similarities = []

  for pair in pairs:
    i1, row1 = pair[0]
    i2, row2 = pair[1]

    t1 = row1['Treść']
    t2 = row2['Treść']

    texts = [t1, t2]

    model = Tokenizer()
    model.fit_on_texts(texts)
    rep = model.texts_to_matrix(texts, mode='count')
    similarity = cosine_similarity(rep)

    result = ((i1, i2), similarity[0, 1])

    similarities.append(result)

  similarities = sorted(similarities, key=lambda tup: tup[1], reverse=True)
  print('Gotowe')

  return similarities

def export_to_excel(similarities):
  print('Eksportowanie do arkusza Excel...')
  author1_col = []
  author2_col = []
  party1_col = []
  party2_col = []
  text1_col = []
  text2_col = []
  score_col = []

  for data in similarities:
    id1 = data[0][0]
    id2 = data[0][1]
    score = data[1]

    text1 = corpus.loc[[id1], ['Treść']].squeeze()
    text2 = corpus.loc[[id2], ['Treść']].squeeze()
    author1 = corpus.loc[[id1], ['Autor']].squeeze()
    author2 = corpus.loc[[id2], ['Autor']].squeeze()
    party1 = corpus.loc[[id1], ['Partia']].squeeze()
    party2 = corpus.loc[[id2], ['Partia']].squeeze()

    text1_col.append(text1)
    text2_col.append(text2)
    author1_col.append(author1)
    author2_col.append(author2)
    party1_col.append(party1)
    party2_col.append(party2)
    score_col.append(score)

  data = {
    'text1': text1_col,
    'text2': text2_col,
    'score': score_col,
    'author1': author1_col,
    'author2': author2_col,
    'party1': party1_col,
    'party2': party2_col
  }

  df = pd.DataFrame(data=data)

  df.to_excel('./bow_results.xlsx', index=False, header=True)
  print('Gotowe')

corpus = load_statements('./wypowiedzi.tsv')

similarities = calculate_similarities(corpus)

export_to_excel(similarities)