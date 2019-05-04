from sklearn.externals import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from nltk.stem.porter import *
from textblob import TextBlob
stemmer = PorterStemmer()

start = time.time()

def stemsent(i):
	temp = word_tokenize(i)
	tempstr = ''
	for i in temp:
		i = stemmer.stem(i)
		tempstr += i + " "
	return tempstr


classifier_f = "pickle_data/MNVnaiveBayesClassifier.pickle"
c2 = joblib.load(classifier_f)

classifier_f = "pickle_data/LinearSVCClassifier.pickle"
c3 = joblib.load(classifier_f)

classifier_f = "pickle_data/GaussianNBClassifier.pickle"
c4 = joblib.load(classifier_f)

classifier_f = "pickle_data/BernoulliNBClassifier.pickle"
c5 = joblib.load(classifier_f)


word_features = []
all_words = []
documents_f = "pickle_data/preprocessedText.pickle"
Documents = joblib.load(documents_f)

def cleanMess(text):
    temp1 = word_tokenize(text)
    temp2 = ''
    for i in temp1:

        if not i in stopwords.words('english'):
        	i = stemmer.stem(i)
        	temp2 += i.lower() + ' '
    return temp2

def createWordFeatures():
	'''
	for i in Documents:
		for j in word_tokenize(i):
			all_words.append(stemmer.stem(j))
	
	save_all_words = "pickle_data/all_words.pickle"
	joblib.dump(all_words, save_all_words)
	'''
	all_words_f = "pickle_data/all_words.pickle"
	all_words = joblib.load(all_words_f)
	
	all_words = nltk.FreqDist(all_words)
	
	for i in all_words.most_common(7000):
		word_features.append(i[0])
	return word_features
	
#word_features = createWordFeatures()
#save_word_features = "pickle_data/word_features.pickle"
#joblib.dump(word_features, save_word_features)

word_features_f = "pickle_data/word_features.pickle"
word_features = joblib.load(word_features_f)



def find_features(text):
	features = []
	for i in word_features:
		features.append(text.count(i))
	return features


def analyser(text):
	blob = TextBlob(text)
	if sent.sentiment.polarity <= -0.1:
		return "Cyberbullying"
	elif sent.sentiment.polarity >= 0.1:
		return "Not Cyberbullying"
	elif sent.sentiment.polarity > -0.1 and sent.sentiment.polarity < 0.1:
		return "Neutral"
	'''
	#text = stemsent(text)
	feats = find_features(text)
	#res1 = c1.predict([feats])
	res2 = c2.predict([feats])
	res3 = c3.predict([feats])
	res4 = c4.predict([feats])
	res5 = c5.predict([feats])
	res = [res2[0], res3[0], res4[0], res5[0]]
	#print(res5)
	return res4[0]
	'''


end = time.time()
#print(end-start)