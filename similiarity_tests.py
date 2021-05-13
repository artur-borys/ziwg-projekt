from similiarities import calculate_cosine_similarity_for_pairs
from utils import convert_statements_to_base_words_and_load, export_to_excel, load_statements

# corpus = load_statements('./wypowiedzi.tsv')
corpus = convert_statements_to_base_words_and_load('./wypowiedzi.tsv')


#BoW
bow_similarities = calculate_cosine_similarity_for_pairs(corpus, method='count')
export_to_excel(corpus, bow_similarities, filename="results/bow_cosine_results")


#TF-IDF
tfidf_similarities = calculate_cosine_similarity_for_pairs(corpus, 'tfidf')
export_to_excel(corpus, tfidf_similarities, filename="results/tfidf_cosine_results")