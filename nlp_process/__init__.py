import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from nltk.corpus import stopwords
from bs4 import BeautifulSoup

def apply_regex(text):
    text = BeautifulSoup(text, "html.parser").text
    
    text = text.lower()

    #Folder path
    text = re.sub(r'[a-z]:\\\S+', r' ', text) 
    #non-ASCII
    text = re.sub(r'[^\x00-\x7F]+', r' ', text)
    #ponctuation
    text = re.sub(r',|\.|\(|\)|\:|\-|\_|\&|\?|\*|\>|\<', r' ', text)
    #Number
    text = re.sub(r'\d+', r' ', text)
    #one letter
    text = re.sub(r' [a-z] ', r' ', text)
    #ntlk stopwords
    text = re.sub(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*', r' ', text)
    
    
    return text

def apply_tokenize(text):
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if len(word) <= 2:
                continue
            tokens.append(word.lower())
    return tokens

# Lemmatize with POS Tag
from nltk.corpus import wordnet

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def apply_lemmatize(text):
    from nltk.stem import WordNetLemmatizer 
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(t,get_wordnet_pos(t)) for t in text] 
    return text

def apply_stopwordsLocal(text, stopw):
    text =  [t for t in text if t not in stopw]
    return text

stopwordsLocal = ['inc']

def cleanText(text):
    text = apply_regex(text)
    text = apply_tokenize(text)
    #text = apply_lemmatize(text)
    text = apply_stopwordsLocal(text, stopwordsLocal)
    text = ' '.join(map(str, text))
    return text