
from itertools import combinations
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity_for_pairs(corpus: pd.DataFrame, method: str) -> tuple:
  print('Obliczanie kosinusowej odległości dla wszystkich par')
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
    rep = model.texts_to_matrix(texts, mode=method)
    similarity = cosine_similarity(rep)

    result = ((i1, i2), similarity[0, 1])

    similarities.append(result)

  similarities = sorted(similarities, key=lambda tup: tup[1], reverse=True)
  print('Gotowe')

  return similarities
