import nltk
import pandas as pd
import numpy as np
import string
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

'''
some exploration at the beginning
word_tokens = nltk.word_tokenize(comments_raw)
text1 = nltk.Text(word_tokens)

#text1[:10]
#Out[6]: ['Ok', ',', 'i', 'have', 'seen', 'everything', '.', 'I', 'take', 'out']
# Number of unique tokens (unique words and punctuation)

len(text1)
#Out[5]: 33657
len(set(text1)) # 8444
#lexical diversity: ratio of unique tokens to the total number of tokens
float(len(set(text1)))/float(len(text1))

lemmatizer = WordNetLemmatizer()
# unique tokens after lemmatizing the verbs
lemmatized = [lemmatizer.lemmatize(w,'v') for w in text1]
len(set(lemmatized)) #33657

# keep tokens before emojis are translated for the response
# sent_tokens_w_emojis verses sent_tokens
# translate the user response to handle emojis first
'''

def response(user_response, sent_tokens, lemmer):

    sent_tokens.append(user_response)
    LemTokens = lambda tokens: [lemmer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    LemNormalize = lambda text: LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)

    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    sent_tokens.pop()
    return sent_tokens[idx] if flat[-2] != 0 else ''

if __name__=='__main__':
    lemmer = nltk.stem.WordNetLemmatizer()
    #WordNet is a semantically-oriented dictionary of English included in NLTK.
    with open('dog_comments.txt', 'r') as f:
      comments_raw = f.read()
    comments_raw = comments_raw.split('\n')
    output = response(sys.argv[1], comments_raw, lemmer)
    print('A dog lover would respond with: %s' % (output))

