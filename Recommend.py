import pickle
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
from sklearn.metrics.pairwise import linear_kernel

stop = stopwords.words('english')

data= pd.read_csv("recommend.csv")


def recommend(title):
    # Convert the index into series(easier to search)
    indices = pd.Series(data.index, index = data['book_title'])
    
    #Converting the book title into vectors and used bigram
    # tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df = 1, stop_words='english')
    # tf.fit(data['clean_summary'])
    # tfidf_matrix = tf.transform(data['clean_summary'])
    
    
    tf1 = pickle.load(open("model/feature.pkl", 'rb'))
    # tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df = 1, stop_words='english',vocabulary=tf1)
    tfidf_matrix = tf1.transform(data['clean_summary'])
    
    #Save vectorizer.vocabulary_
    # pickle.dump(tf,open("model/feature.pkl","wb"))
        
    # Calculating the similarity measures based on Cosine Similarity
    sg = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # Get index correspond to the title
    idx = indices[title]
    
    # Get the pairwsie similarity scores
    sig = list(enumerate(sg[idx]))
    # Sort
    sig = sorted(sig, key=lambda x:x[1],reverse=True)
    # sig = sorted(sig,reverse=True)
    # Scores of the 5 most similar books
    sig = sig[1:6]
    book_indices= [i[0] for i in sig]
    rec = data[['book_title']].iloc[book_indices]
    print(data[data.book_title.isin(rec['book_title'])])
    print(rec)
 
print(recommend('Victory'))   