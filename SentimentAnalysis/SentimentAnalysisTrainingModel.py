import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.tokenize import word_tokenize

short_pos = open("data/positive.txt", 'r').read()
short_neg = open("data/negative.txt", 'r').read()

all_words = []
documents = []

allowed_word_types = ["J", "R", "V"]
allowed_word_types = ["J"]

for p in short_pos.split('\n'):
    documents.append((p, "pos"))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

for n in short_neg.split('\n'):
    documents.append((n, "neg"))
    words = word_tokenize(n)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

save_documents = open('algos/documents.pickle', "wb")
pickle.dump(documents, save_documents)
save_documents.close()

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:5000]

save_word_features = open('algos/word_features5k.pickle', 'wb')
pickle.dump(word_features, save_word_features)
save_word_features.close()


def find_features(document):
    tokenized_words = word_tokenize(document)
    features = {}
    for word in word_features:
        features[word] = (word in tokenized_words)

    return features


feature_sets = [(find_features(rev),category) for (rev, category) in documents]

random.shuffle(feature_sets)
print("Length of Feature Set:", len(feature_sets))

testing_set = feature_sets[10000:]
training_set = feature_sets[:10000]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(15)
# ====================== Save Models =============
save_classifier = open("algos/originalnaivebayes5k.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB classifier accuracy percent:",(nltk.classify.accuracy(MNB_classifier,training_set))*100)

save_classifier = open("algos/MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier,save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB classifier accuracy percent:",(nltk.classify.accuracy(BernoulliNB_classifier,training_set))*100)

save_classifier = open("algos/BernoulliNB_classifier5k.pickle","wb")
pickle.dump(BernoulliNB_classifier,save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

save_classifier = open("algos/LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

save_classifier = open("algos/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)

save_classifier = open("algos/SGDC_classifier5k.pickle","wb")
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()