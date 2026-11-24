# AskWise FAQ Chatbot

AskWise is a Streamlit FAQ chatbot for common e-commerce questions about orders,
delivery, cancellations, returns, refunds, payments, accounts, and support.

## How it works

- `data/faqs.json` contains FAQ intents, example questions, and answers.
- NLTK tokenization and Porter stemming normalize text. English stop words are
  removed while negation words are retained. The stop-word list is built from
  scikit-learn, so no separate NLTK corpus download is required.
- Word TF-IDF and character n-gram TF-IDF are combined with cosine similarity.
  Character n-grams improve matching for common misspellings.
- Matches below the default `0.20` threshold, empty input, and negated
  cancellation/return requests receive the existing fallback response.

## Requirements

- Python 3.9 or newer
- pip

## Setup and run (Windows PowerShell)

From the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit opens the chatbot in your browser. To run it without activating the
environment, use `.\.venv\Scripts\python.exe -m streamlit run app.py`.

## Tests

Run the matching, preprocessing, fallback, threshold, and Streamlit interface
tests from the project directory:

```powershell
python -m unittest discover -s tests -v
```

## Project structure

```text
app.py                  Streamlit chat interface
chatbot/engine.py       FAQ loading and similarity matching
chatbot/preprocessing.py NLTK preprocessing
data/faqs.json          FAQ questions and answers
tests/                  Automated unit and interface tests
requirements.txt        Runtime dependencies
```
