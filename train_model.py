import json
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training Data
training_sentences = [
    "hello",
    "hi",
    "how are you",
    "bye",
    "what is your name",
    "help",
    "good morning"
]

training_labels = [
    "Hello User!",
    "Hi there!",
    "I am fine.",
    "Goodbye!",
    "I am AI ChatBot.",
    "How can I help you?",
    "Good Morning!"
]

# Vectorization
vectorizer = CountVectorizer()

X = vectorizer.fit_transform(training_sentences)

# Train Model
model = MultinomialNB()
model.fit(X, training_labels)

# Save model
pickle.dump(model, open("model/chatbot_model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("Model Trained Successfully")