#  basically this a demo deployment of our model 
#  First we load the models 
#  secound as we receive prediction requests we  preprocess the text data 
#  then we invoke predict method for every model 
#  then we return results as a list of dictionaries of model and prediction. 


import numpy as np,pandas as pd

import os,re,string,pickle,warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer , TfidfTransformer

from nltk.stem import PorterStemmer
stopWords= set(stopwords.words('english'))

# Machine Learning Models
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import PassiveAggressiveClassifier, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from tempfile import mkdtemp
from shutil import rmtree
from sklearn.model_selection import GridSearchCV
from xgboost.sklearn import XGBClassifier 

def clean_string(text):
    ''' This function cleans string texts 
    input: string; messy text
    output: string; clean text
    '''
    # strip HTML tags
    html_strip = re.compile('<.*?>')                # Html tag striper
    text = re.sub(html_strip, ' ', text)                # Html strip
    # delete URLS
    text = text.replace("^https?:\/\/.*[\r\n]*', '", " ") # url deleting
    # strip puctuations
    text = re.sub(r'[?|!|\'|"|#]',r' ',text) # exclamation , question marks etc....  
    text = re.sub(r'[.|,|)|(|\|/]',r' ',text) # punctuations
    text = re.sub(r'\d+',r' ',text) # punctuations
    my_punctuations = string.punctuation + '’' + '“' + '”' + '•'
    translator = str.maketrans(' ', ' ', my_punctuations ) # string translator 
    text = text.translate(translator)
    text = re.sub(r'[^\w\s]',' ',text)
    text = re.sub(r'\W+', ' ', text) # Remove all the special characters
    text = re.sub(r"[^a-zA-Z0-9]", r" ", text)
        
    #strip whitespaces
    text = text.lower().strip()   # lower case and strip leading and trailing lines
    text = text.replace("\n", " ") # striping new line tags
    text = text.replace("\t", " ") # striping tab tags
    
    #     text = text.replace("Image copyright Getty Images Image caption".lower(), "") # bu datasete özel
    #     text = text.replace("Image copyright Getty Images".lower(), "") # bu datasete özel
    return text

# test = "?  | $ | . | ! / ( ) { } \[ \] \| @,; \n a4\n%  MEXICO CITY\tis am•are the why 1990 1 2 3(Reuters)!! -/ \ Egypt’s Cheiron Holding <b>htmltag<b> [paranthes] {paranthes} *  ? = & % +     "
# test=clean_string(test)
# word_tokenize(test)
# test
def clean_stop_words(text):
    '''this function cleans a word list from the stop word
    input: list; list of tokenized words 
    output: list; list of tokenized words excluding the stop worlds
    '''

    text = word_tokenize(text)
    text = [word for word in text if word not in stopWords] # and w.isalpha() and len(w) > 2]
    return text

# test = "no one there here the he she is am are in on above not 4\n%  MEXICO CITY \n \t is am are the why 1990 1 2 3(Reuters)!! -/ \ Egypt’s Cheiron Holding <b>htmltag<b> [paranthes] {paranthes} *  ? = & % +     "
# test = clean_string(test)
# test = word_tokenize(test) # in order to feed t to clean stop words you need to tokenize it first. 
# test = clean_stop_words(test)
# test
def myStemmer(text):
    '''this function finds the stem words for a word list
    input: list; list of tokenized words 
    output: list; list of tokenized stemmed words
    '''
    ps = PorterStemmer()
    text1 = filter(lambda x: isinstance(x,str) , text)
    stemmed_text = [ps.stem(word) for word  in text1]
    stemmed_text = " ".join(stemmed_text)
    return stemmed_text

# test = " 4\n%  MEXICO CITY \n \t is am are the why 1990 1 2 3(Reuters)!! -/ \ Egypt’s Cheiron Holding <b>htmltag<b> [paranthes] {paranthes} *  ? = & % +     "
# test = clean_string(test)
# test = word_tokenize(test) # in order to feed t to clean stop words you need to tokenize it first. 
# test = clean_stop_words(test)
# myStemmer(test)

models = [
    "SVC",
    "MultinomialNB",
    "LogisticRegression",
    "KNeighborsClassifier",
    "DecisionTreeClassifier",
    "RandomForestClassifier",
    "AdaBoostClassifier",
    "BaggingClassifier",
    "ExtraTreesClassifier",
    "SGDClassifier",
    "LinearSVC",
    "PassiveAggressiveClassifier",
    'XGBClassifier'
]

from joblib import dump, load
clf = {}
for model_name in models:
    clf[model_name] = load('fullmodels/'+model_name+'.joblib')
    # print(model_name+' Loaded')
    
def prediction(text):
    result = {}
    text = clean_string(text)
    text = clean_stop_words(text)
    text = myStemmer(text)
    for model_name in models:
        result[model_name] = str(clf[model_name].predict([text])[0])
    return result


# news = "My name is is nader what is your name my good friend"
# news = clean_string(news)
# news = clean_stop_words(news)
# news = myStemmer(news)
# prediction = clf.predict([news])
# print(str(prediction))
