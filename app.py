from flask import Flask, request, jsonify
from naive_bayes import NaiveBayes
import pickle
import numpy as np
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer

# Inisialisasi Flask
app = Flask(__name__)

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Load model dan vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

@app.route('/')
def home():
    return "Aplikasi Naive Bayes untuk Deteksi SMS Spam"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ambil data input
        data = request.json
        text = str(data.get('text', ''))
        print('Pengambilan data berhasil ' + text)

        # Cleaning
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.lower()

        # Tokenizing
        tokens = word_tokenize(text)

        # Stopword removal
        stop_words = set(stopwords.words('indonesian'))
        tokens = [word for word in tokens if word not in stop_words]

        # Stemming
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stemmed_tokens = [stemmer.stem(word) for word in tokens]

        text_cleaned = ' '.join(stemmed_tokens)
        print('Preprocess berhasil: ' + text_cleaned)

        # Transformasi text menggunakan TF-IDF
        text_tfidf = vectorizer.transform([text_cleaned])
        print('TF IDF berhasil')

        # Prediksi menggunakan model
        prediction = model.predict(text_tfidf.toarray())[0]
        print(prediction)

        # Respon hasil
        return jsonify({
            "text": text,
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def preprocess_text(text):
    # Cleaning
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    print('Cleaned text: ' + text)

    # Tokenizing
    tokens = word_tokenize(text)

    # Stopword removal
    stop_words = set(stopwords.words('indonesian'))
    tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]

    return ' '.join(stemmed_tokens)

@app.route('/preprocess', methods=['GET'])
def preprocess_text():

    text = str(request.args['Query'])

    # Cleaning
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    print('Pre processing text: ' + text)

    # Tokenizing
    tokens = word_tokenize(text)
    print('Pre processing token berhasil ')

    # Stopword removal
    stop_words = set(stopwords.words('indonesian'))
    tokens = [word for word in tokens if word not in stop_words]
    print('Stop word removal berhasil')

    # Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]

    text_cleaned = ' '.join(stemmed_tokens)
    print('Preprocess berhasil ' + text_cleaned)

    print(f"Cleaned text: {text_cleaned}, Type: {type(text_cleaned)}")
    print(f"Type of vectorizer: {type(vectorizer)}")

    text_tfidf = vectorizer.transform([text_cleaned])
    print('TF IDF berhasil')

if __name__ == '__main__':
    app.run(debug=True)
