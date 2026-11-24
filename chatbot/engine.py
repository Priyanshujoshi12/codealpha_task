
import json
import math
import re
from numbers import Real
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from chatbot.preprocessing import preprocess_text


NEGATED_ACTION_PATTERN = re.compile(
    r"\b(?:do not|don't|does not|doesn't|did not|didn't|never)"
    r"\s+(?:want|need|plan|intend)\s+to\s+(?:cancel|return)\b"
)


# Locate FAQ dataset relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
FAQ_FILE = BASE_DIR / "data" / "faqs.json"


def load_faqs():
    """Load FAQ records from the JSON dataset."""

    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Load FAQ records
faqs = load_faqs()

# Store every question variation with its associated FAQ
faq_questions = []
faq_records = []

for faq in faqs:
    for question in faq["questions"]:
        faq_questions.append(question)
        faq_records.append(faq)


# Use our NLP preprocessing before TF-IDF vectorization
def nlp_analyzer(text):
    return preprocess_text(text).split()


# Convert all stored questions into numerical vectors
vectorizer = TfidfVectorizer(analyzer=nlp_analyzer)
faq_vectors = vectorizer.fit_transform(faq_questions)

char_vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(2, 5),
    preprocessor=preprocess_text,
    lowercase=False,
)
char_faq_vectors = char_vectorizer.fit_transform(faq_questions)


def find_best_match(user_question, threshold=0.20):
    """
    Find the most similar FAQ using word and character TF-IDF similarity.

    Returns the matching FAQ and similarity score,
    or None if no sufficiently good match exists.
    """

    if isinstance(threshold, bool) or not isinstance(threshold, Real):
        raise TypeError("threshold must be a number between 0 and 1.")
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1.")

    # Handle empty input
    if not isinstance(user_question, str) or not user_question.strip():
        return None

    if not preprocess_text(user_question):
        return None

    normalized_question = user_question.replace("’", "'").lower()
    if NEGATED_ACTION_PATTERN.search(normalized_question):
        return None

    # Convert user question into a TF-IDF vector
    user_vector = vectorizer.transform([user_question])
    char_user_vector = char_vectorizer.transform([user_question])

    # Character n-grams improve typo matching while word matches remain primary.
    word_similarities = cosine_similarity(user_vector, faq_vectors)[0]
    char_similarities = cosine_similarity(char_user_vector, char_faq_vectors)[0]
    similarities = 0.55 * word_similarities + 0.45 * char_similarities

    # Find the index of the highest similarity score
    best_index = similarities.argmax()
    best_score = float(similarities[best_index])

    # Reject weak matches
    if best_score < threshold:
        return None

    # Get the corresponding FAQ
    best_faq = faq_records[best_index]

    return {
        "intent": best_faq["intent"],
        "answer": best_faq["answer"],
        "matched_question": faq_questions[best_index],
        "similarity": round(best_score, 4)
    }
