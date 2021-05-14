import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.metrics.pairwise import cosine_similarity
import utils

def calculate_cosine_similarity_for_pairs(corpus: pd.DataFrame, method: str) -> list:
  print('Obliczanie kosinusowej odległości dla wszystkich par')
  pairs = utils.get_pairs(corpus)

  similarities = []

  for pair in pairs:
    i1, row1 = pair[0]
    i2, row2 = pair[1]

    t1 = row1['Treść']
    t2 = row2['Treść']

    texts = [t1, t2]

    model = Tokenizer()
    model.fit_on_texts(texts)
    rep = model.texts_to_matrix(texts, mode=method)
    similarity = cosine_similarity(rep)

    result = ((i1, i2), similarity[0, 1])

    similarities.append(result)

  similarities = sorted(similarities, key=lambda tup: tup[1], reverse=True)
  print('Gotowe')

  return similarities

def jaccard_similarity(text1: str, text2: str) -> float:
  # Tokenizacja poprzez lowercase i split (domyślnie podzieli na ' ')
  set1 = set(text1.lower().split())
  set2 = set(text2.lower().split())

  # Część wspólna
  intersection = set1.intersection(set2)

  # Suma
  union = set1.union(set2)

  # Podobieństwo Jaccarda
  similarity = len(intersection)/len(union)

  return similarity

def jaccard_similarity_pairwise(corpus: pd.DataFrame) -> list:
  """ Zwraca listę z wynikami dla podobieństwa Jaccarda
  
  Wartość zwrócona:
  * lista wyników w postaci:
    [((i1, i2), wynik)]
  
  """

  print('Obliczanie Jaccard Similarity dla wszystkich par')
  pairs = utils.get_pairs(corpus)

  similarities = []

  for pair in pairs:
    i1, row1 = pair[0]
    i2, row2 = pair[1]

    t1 = row1['Treść']
    t2 = row2['Treść']

    score = jaccard_similarity(t1, t2)

    similarities.append(((i1, i2), score))

  similarities = sorted(similarities, key=lambda tup: tup[1], reverse=True)
  print('Gotowe')
  
  return similarities