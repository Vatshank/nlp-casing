from mrjob.job import MRJob
import pickle
import numpy as np
from nltk import word_tokenize, sent_tokenize
import nltk.data
from nltk.util import ngrams
from nltk.corpus import stopwords
from collections import Counter
import sys

sys.stderr = open('log.txt', 'w')
doc = ''
count = 0

def counter_bigrams(article):
	tokens = [word for sent in sent_tokenize(article) for word in word_tokenize(sent)]
	tokens_filtered = [token for token in tokens if token.isalpha()]
	bigrams = ngrams(tokens_filtered,2)
	freq_bigrams = Counter(bigrams)
	return freq_bigrams

class wiki_bigram_LM(MRJob):

  def mapper(self, _, line):
  	global doc
  	global count
  	line= unicode(line, 'utf-8')
  	if line.startswith('NewArticleBegins'):
		if doc:
			count+=1
			counter = counter_bigrams(doc)
			for item in counter.iteritems():
				yield item[0], item[1]
		doc = ''
	else:
		doc = doc + line

  def reducer(self, bigram, counts):
  	tf_list = list(counts)
  	tf = sum(tf_list)
  	df = len(tf_list)
  	yield bigram , (tf, df)

if __name__ == '__main__':
	wiki_bigram_LM.run()
	with open('no_articles.txt','w') as f:
		f.write(str(count))
