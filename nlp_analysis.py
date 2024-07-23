!pip install streamlit wordcloud matplotlib nltk spacy seaborn textblob

import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import seaborn as sns
from collections import Counter
from textblob import TextBlob
import spacy
import nltk
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import seaborn as sns
from collections import Counter
from textblob import TextBlob
import spacy
import nltk

# Download NLTK resources (only need to run once)
nltk.download('punkt')
nltk.download('stopwords')

# Load the Spanish NLP model
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    from spacy.cli import download
    download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

# Text preprocessing function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('spanish'))  # Change language if needed
    tokens = [word for word in tokens if word not in stop_words]
    
    return ' '.join(tokens)

# Perform NER
def perform_ner(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Streamlit app
st.title("Text Analysis Dashboard")

uploaded_file = st.file_uploader("Choose a text file", type="txt")
if uploaded_file is not None:
    # Read the file
    text_data = uploaded_file.read().decode('utf-8')
    
    # Preprocess the text data
    cleaned_text = preprocess_text(text_data)
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_text)
    
    st.subheader("Word Cloud")
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
    
    # Frequency Analysis
    tokens = word_tokenize(cleaned_text)
    word_freq = Counter(tokens)
    
    st.subheader("Top 20 Words by Frequency")
    common_words = dict(word_freq.most_common(20))
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(common_words.keys()), y=list(common_words.values()))
    plt.xticks(rotation=45)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 20 Words by Frequency')
    st.pyplot(plt)
    
    # Sentiment Analysis
    sentiment = TextBlob(cleaned_text).sentiment
    st.subheader("Sentiment Analysis")
    st.write("Polarity: ", sentiment.polarity)
    st.write("Subjectivity: ", sentiment.subjectivity)
    
    # Named Entity Recognition (NER)
    entities = perform_ner(cleaned_text)
    st.subheader("Named Entities")
    st.write(entities)
