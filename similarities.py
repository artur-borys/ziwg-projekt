import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.metrics.pairwise import cosine_similarity
import utils

def calculate_cos(text1: str, text2: str, method: str) -> float:
  texts = [text1, text2]

  model = Tokenizer()
  model.fit_on_texts(texts)
  rep = model.texts_to_matrix(texts, mode=method)
  similarity = cosine_similarity(rep)

  score = similarity[0, 1]

  return score

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

def compare_text_with_corpus_jaccard(text: str, corpus: pd.DataFrame, display_corpus: pd.DataFrame):
  results = []
  for id, entry in corpus.iterrows():
    entry_text = entry['Treść']
    score = jaccard_similarity(text, entry_text)
    result = {
      'score': score,
      **utils.translate_statement_dict(entry),
      'text': display_corpus.iloc[id]['Treść']
    }

    results.append(result)
  
  results = sorted(results, key=lambda r: r['score'], reverse=True)

  return results

def compare_text_with_corpus_cosine(text: str, corpus: pd.DataFrame, method: str, display_corpus: pd.DataFrame):
  results = []

  for id, entry in corpus.iterrows():
    entry_text = entry['Treść']
    score = calculate_cos(text, entry_text, method)

    result = {
      'score': score,
      **utils.translate_statement_dict(entry),
      'content': display_corpus.iloc[id]['Treść']
    }

    results.append(result)
  
  results = sorted(results, key=lambda r: r['score'], reverse=True)

  return results


def get_cosine_similarity(feature_vec_1, feature_vec_2):
  return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]


def compare_text_with_corpus_fasttext(text: str, corpus:pd.DataFrame, fasttextModel, display_corpus: pd.DataFrame):
  results = []

  model = fasttextModel
  predicted = model.get_sentence_vector(text)

  for id, entry in corpus.iterrows():
    entry_text = entry['Treść']
    entryPredicted = model.get_sentence_vector(entry_text)
    similarity = get_cosine_similarity(predicted, entryPredicted)

    result = {
      'score': similarity.item(),
      **utils.translate_statement_dict(entry),
      'content': entry_text
    }
    results.append((result))

  results = sorted(results, key=lambda r: r['score'], reverse=True)

  return results
