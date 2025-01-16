from textblob import TextBlob
import nltk

# Download required NLTK data if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/movie_reviews')
except LookupError:
    nltk.download('punkt')
    nltk.download('movie_reviews')

def analyze_sentiment(feedback_text):
    blob = TextBlob(feedback_text)
    return blob.sentiment.polarity
