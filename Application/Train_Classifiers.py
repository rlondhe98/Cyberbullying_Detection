from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import LinearSVC
from sklearn import svm

documents_f = "pickle_data/preprocessedText.pickle"
documents = joblib.load(documents_f)

labels_f = "pickle_data/labels.pickle"
y = joblib.load(labels_f)

tfidfconverter = TfidfVectorizer(max_features=7000, min_df=5, max_df=0.7, stop_words=stopwords.words('english'), encoding = 'unicode_escape')
X = tfidfconverter.fit_transform(documents).toarray()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

print("Linear SVC")
LinearSVCClassifier = LinearSVC(random_state=0, tol=1e-5)
LinearSVCClassifier.fit(X_train, y_train)

save_LinearSVCClassifier = "pickle_data/LinearSVCClassifier.pickle"
joblib.dump(LinearSVCClassifier, save_LinearSVCClassifier)

print("BernoulliNB")
BernoulliNBClassifier = BernoulliNB()
BernoulliNBClassifier.fit(X_train, y_train)

save_BernoulliNB = "pickle_data/BernoulliNBClassifier.pickle"
joblib.dump(BernoulliNBClassifier, save_BernoulliNB)

print("MultinomialNB")
MNVnaiveBayesClassifier = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
MNVnaiveBayesClassifier.fit(X_train, y_train)

save_MNVnaiveBayesClassifier = "pickle_data/MNVnaiveBayesClassifier.pickle"
joblib.dump(MNVnaiveBayesClassifier, save_MNVnaiveBayesClassifier)

print("GaussianNB")
GaussianNBClassifier = GaussianNB()
GaussianNBClassifier.fit(X_train, y_train)

save_GaussianNBClassifier = "pickle_data/GaussianNBClassifier.pickle"
joblib.dump(GaussianNBClassifier, save_GaussianNBClassifier)

print("classification complete!")
