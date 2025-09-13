import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

# Simple keyword-based categorization
CATEGORY_KEYWORDS = {
    'groceries': ['grocery', 'food', 'supermarket', 'market', 'store', 'milk', 'bread', 'vegetables', 'fruit'],
    'travel': ['flight', 'hotel', 'bus', 'train', 'taxi', 'uber', 'lyft', 'gas', 'fuel', 'trip', 'vacation'],
    'bills': ['electricity', 'water', 'gas bill', 'internet', 'phone', 'rent', 'insurance', 'utility'],
    'entertainment': ['movie', 'cinema', 'concert', 'game', 'party', 'restaurant', 'bar', 'club'],
    'shopping': ['clothes', 'shoes', 'electronics', 'amazon', 'ebay', 'mall'],
    'health': ['doctor', 'pharmacy', 'medicine', 'hospital', 'gym', 'fitness'],
    'other': []  # Default category
}

def categorize_expense(description):
    """Categorize an expense based on description using keyword matching."""
    description_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category
    return 'other'

# Simple ML-based categorization (train on sample data)
MODEL_FILE = 'expense_classifier.pkl'
VECTORIZER_FILE = 'tfidf_vectorizer.pkl'

def train_classifier(sample_data):
    """Train a simple ML classifier for categorization."""
    descriptions = [item['description'] for item in sample_data]
    categories = [item['category'] for item in sample_data]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(descriptions)
    clf = MultinomialNB()
    clf.fit(X, categories)

    # Save model and vectorizer
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(clf, f)
    with open(VECTORIZER_FILE, 'wb') as f:
        pickle.dump(vectorizer, f)

def load_classifier():
    """Load the trained classifier and vectorizer."""
    if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
        with open(MODEL_FILE, 'rb') as f:
            clf = pickle.load(f)
        with open(VECTORIZER_FILE, 'rb') as f:
            vectorizer = pickle.load(f)
        return clf, vectorizer
    return None, None

def ml_categorize_expense(description):
    """Categorize using ML if model exists, else fallback to keyword."""
    clf, vectorizer = load_classifier()
    if clf and vectorizer:
        X = vectorizer.transform([description])
        return clf.predict(X)[0]
    else:
        return categorize_expense(description)

# For demo, use keyword-based; can train ML later
def auto_categorize(description):
    """Auto-categorize expense description."""
    return ml_categorize_expense(description)
