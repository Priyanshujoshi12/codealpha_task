
import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer


STOP_WORDS = set(ENGLISH_STOP_WORDS) | {"need", "want"}

# Preserve negation words because they can change meaning
STOP_WORDS -= {"not", "no", "nor"}

# Initialize stemmer
stemmer = PorterStemmer()


def preprocess_text(text):
    """
    Clean and normalize text using NLP techniques.

    Steps:
    1. Lowercase
    2. Remove special characters and numbers
    3. Tokenize
    4. Remove stopwords
    5. Apply stemming
    """

    # Handle empty input
    if not isinstance(text, str) or not text.strip():
        return ""

    # Step 1: Convert to lowercase
    text = text.lower()

    # Step 2: Remove numbers and special characters
    text = re.sub(r"[^a-z\s]", " ", text)

    # Step 3: Tokenization
    tokens = wordpunct_tokenize(text)

    # Step 4: Stopword removal and Step 5: Stemming
    cleaned_tokens = []

    for word in tokens:
        if word not in STOP_WORDS:
            stemmed_word = stemmer.stem(word)
            cleaned_tokens.append(stemmed_word)

    # Return cleaned text
    return " ".join(cleaned_tokens)
