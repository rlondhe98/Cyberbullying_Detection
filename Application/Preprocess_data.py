import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.externals import joblib
from nltk.stem.porter import *
stemmer = PorterStemmer()

'''
df_pos = pd.read_csv('datasets/KerasPos.csv')
df_neg = pd.read_csv('datasets/KerasNeg.csv')
neg = open('datasets/negative.txt', 'r', encoding = 'iso-8859-1').read().split('\n')
#words = open('datasets/words.txt', 'r').read().split('\n')
pos = open('datasets/positive.txt', 'r', encoding = 'iso-8859-1').read().split('\n')

documents = []
label = []

def stemsent(i):
	temp = word_tokenize(i)
	tempstr = ''
	for i in temp:
		i = stemmer.stem(i)
		tempstr += i + " "
	return tempstr

def keras_pos():
	for i in df_pos.Sentences:
		temp = i
		i = i.replace("<START>","")
		i = i.replace("<PAD>","")
		i = i.replace("<UNK>","")
		i = i.replace("<UNUSED>","")
		i = stemsent(i)
		documents.append(i)
		label.append("Not Cyberbullying")
keras_pos()

def keras_neg():
	for i in df_neg.Sentences:
		temp = i
		i = i.replace("<START>","")
		i = i.replace("<PAD>","")
		i = i.replace("<UNK>","")
		i = i.replace("<UNUSED>","")
		i = stemsent(i)
		documents.append(i)
		label.append("Cyberbullying")
keras_neg()

def words_cyb():
	del words[0]
	del words[-1]
	for i in words:
		temp = i.split('\t')
		if temp[1] == 0:
			ttt = stemsent(temp[0])
			documents.append(ttt)
			label.append('Cyberbullying')
		elif temp[1] == 1:
			tty = stemsent(temp[0])
			documents.append(tty)
			label.append('Not Cyberbullying')
#words_cyb()

def neg_sent():
	for i in neg:
		i = stemsent(i)
		documents.append(i)
		label.append('Cyberbullying')

neg_sent()

def pos_sent():
	for i in pos:
		i = stemsent(i)
		documents.append(i)
		label.append('Not Cyberbullying')

pos_sent()

print(len(documents),len(label))

save_documents = "pickle_data/documents.pickle"
joblib.dump(documents, save_documents)

save_labels = "pickle_data/labels.pickle"
joblib.dump(label, save_labels)

'''
documents_f = "pickle_data/documents.pickle"
documents = joblib.load(documents_f)
preprocessedText = []

count = 0
def cleanmess(text):
	t = ''
	global count
	temp = word_tokenize(text)
	for i in temp:
		if not i in stopwords.words('english'):
			t += i + ' '
	count += 1
	#print(count)
	return t


for i in documents:
	
	temp = cleanmess(i)
	#print(temp)
	
	preprocessedText.append(temp)

print(len(documents), len(preprocessedText))

save_preprocessedText = "pickle_data/preprocessedText.pickle"
joblib.dump(preprocessedText, save_preprocessedText)
