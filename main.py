import ssl
import nltk
from newspaper import Article
import string
import random
from nltk.translate.bleu_score import sentence_bleu
from requests.models import Response
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)

# article to scrape info from
article = Article('https://rotogrinders.com/articles/lakers-odds-3491059')
article.download()
article.parse()
article.nlp()

corpus = article.text

# now tokenize
text = corpus
sentence_list = nltk.sent_tokenize(text)

# fxn to respond to greeting


def greeting_response(txt):
    txt = txt.lower()
    bot_greetings = ['hello', 'hey', 'hi', 'hey there']
    user_greetings = ['hi', 'hello', 'hey there', 'whats up', 'hey']

    for word in txt.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def index_sort(lis):
    length = len(lis)
    list_index = list(range(0, length))

    x = lis
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


def bot_response(user_in):
    user_in = user_in.lower()
    sentence_list.append(user_in)
    bot_response = ''
    countMatrix = CountVectorizer().fit_transform(sentence_list)
    similarityScores = cosine_similarity(countMatrix[-1], countMatrix)
    similarityScore_list = similarityScores.flatten()
    index = index_sort(similarityScore_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarityScore_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j+1

        if j > 2:
            break

    if response_flag == 0:
        bot_response = bot_response + ' ' + 'Sorry'
    sentence_list.remove(user_in)
    return bot_response


# start chat
print('Chatter Bot Bob: Let us talk LakeShow Lakers, if you want to exit type "bye"')

exit_words = ['exit', 'bye', 'quit', 'break']

while(True):
    user_in = input()
    if user_in.lower() in exit_words:
        print('Chatter Bot Bob: See you later!! ')
        break
    else:
        if greeting_response(user_in) != None:
            print('Lakers Bias Bot: ' + greeting_response(user_in))
        else:
            print('Lakers Bias Bot: ' + bot_response(user_in))
