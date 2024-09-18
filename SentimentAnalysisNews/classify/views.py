import pickle
import re
import string
import sklearn
import nltk
nltk.download('punkt_tab')

from nltk.corpus import stopwords

from django.shortcuts import render
from nltk.stem import LancasterStemmer

stopwords = set(stopwords.words('english'))


# Create your views here.
#A function to clean the data
def processCleanData(text):
    # Initializing the stemmer
    stemmer = LancasterStemmer()
    # getting the stopwords
    # changing to lower case
    text = text.lower()
    # removing symbols
    text = re.sub(r'@\S+', '', text)
    # removing links
    text = re.sub(r'http\S+', '', text)
    # removing pictures
    text = re.sub(r'.pic\S+', '', text)
    # removing other characters excpet text
    text = re.sub(r'[^a-zA-Z+]', ' ', text)
    # removing punctuation
    # getting punctuation list of string.punctation
    text = "".join([char for char in text if char not in string.punctuation])
    # tokenizing the workds
    words = nltk.word_tokenize(text)
    # using Lancaster stemmer to step the words
    # example eating eater becones eat
    words = list(map(lambda x: stemmer.stem(x), words))
    # removing and joining the stop words
    text = " ".join([char for char in words if char not in stopwords and len(char) > 2])
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predictData(query):
    dataToPredict = [query]
    dataToPredictCleaned = list(map(processCleanData,dataToPredict))
    model = pickle.load(open('classify/trainingModels/lrmodel', "rb"))
    predicted = model.predict(dataToPredictCleaned)
    return predicted

def getNewPage(request):
    return render(request,'newsEnter.html')


def resultView(request):
    query = request.GET.get('query')
    predictionDictionary = {
        0:'Bad',
        1:'Good'
    }
    predictionResult = predictData(query)[0]
    contextValues = {
        'query':query,
        'result':predictionDictionary.get(predictionResult)

    }
    return render(request,'results.html',contextValues)
