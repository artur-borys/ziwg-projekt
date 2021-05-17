from similarities import calculate_cosine_similarity_for_pairs, jaccard_similarity_pairwise
from utils import convert_statements_to_base_words_and_load, export_to_excel, load_statements
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--all', '-a', action="store_true", help='Przeprowadź testy dla wszystkich metod')
parser.add_argument('--bow', action="store_true")
parser.add_argument('--tfidf', action="store_true")
parser.add_argument('--jaccard', action="store_true")
parser.add_argument('--full-words', action="store_true", help="Przeprowadź testy na pełnych, a nie na podstawowych formach wyrazów")

args = parser.parse_args()

words_filename = 'full' if args.full_words else 'base'

if args.full_words:
  print('Używanie korpusu z pełnymi wyrazami')
  corpus = load_statements('./wypowiedzi.tsv')
else:
  print('Używanie korpusu z podstawowywmi formami wyrazów')
  corpus = load_statements('./wypowiedzi_base.tsv')


#BoW
if args.all or args.bow:
  bow_similarities = calculate_cosine_similarity_for_pairs(corpus, method='count')
  export_to_excel(corpus, bow_similarities, filename=f"results/bow_cosine_{words_filename}_results")


#TF-IDF
if args.all or args.tfidf:
  tfidf_similarities = calculate_cosine_similarity_for_pairs(corpus, 'tfidf')
  export_to_excel(corpus, tfidf_similarities, filename=f"results/tfidf_cosine_{words_filename}_results")

#Jaccard
if args.all or args.jaccard:
  jaccard_similarities = jaccard_similarity_pairwise(corpus)
  export_to_excel(corpus, jaccard_similarities, filename=f"results/jaccard_{words_filename}_results")