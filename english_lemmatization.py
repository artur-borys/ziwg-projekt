import utils
import string

from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
import nltk

import pattern
from pattern.en import lemma, lexeme

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize(sentence):
    lemmatizer = WordNetLemmatizer()
    lemmatizedText = " ".join([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(sentence) if w not in string.punctuation])
    
    return lemmatizedText
