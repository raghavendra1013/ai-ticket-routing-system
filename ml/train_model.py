import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv("ticket_dataset.csv")

X = data["text"]
y_category = data["category"]
y_priority = data["priority"]

# SPLIT (ADDED)
X_train, X_test, y_train, y_test = train_test_split(X, y_category, test_size=0.2)

category_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

priority_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

category_model.fit(X_train, y_train)
priority_model.fit(X, y_priority)

# EVALUATION (ADDED)
pred = category_model.predict(X_test)
print("Category Accuracy:", accuracy_score(y_test, pred))

joblib.dump(category_model, "../models/classifier.pkl")
joblib.dump(priority_model, "../models/priority_model.pkl")

print("Models trained successfully")