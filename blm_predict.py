#!/usr/bin/env python
from nltk import word_tokenize
from nltk.util import ngrams
from numpy import mean
import nltk.data
from nltk.corpus import stopwords
import numpy as np
import pickle
import os

ls = os.listdir('/z/vatshank/pickles_9/')
dict = {}
for file in ls:
	print file
	with open('/z/vatshank/pickles_9/'+file,'r') as f_in:
		temp = pickle.load(f_in)
	dict.update(temp)

##Load the pickle dictionary of tf_idf
with open('/z/vatshank/pickles_9/wiki_frequencies_9.txt_tf_idf.pickle') as f_in:
 	dict = pickle.load(f_in)

stop = set(stopwords.words('english'))

with open('/local/vatshank/gold.txt','r') as f:
	text = f.read()

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sent_tokens = sent_tokenizer.tokenize(unicode(text,'utf-8').strip())

total = 0
acc_score = 0
exceptions_raised = 0
for sentence in sent_tokens:
	tokens = word_tokenize(sentence)
	bigrams = ngrams(tokens, 2)
	##Remove bigrams with punctuations
	bigrams = [bigram for bigram in bigrams if bigram[0].isalpha() & bigram[1].isalpha()]
	total =  total + len(bigrams)
	for count,gram in enumerate(bigrams):
		comb_list = []
		gram_lower = [entry.lower() for entry in gram]		
		try:
			dict[gram_lower[0], gram_lower[1]]
			dict[gram_lower[0].title(), gram_lower[1]]
			dict[gram_lower[0], gram_lower[1].title()]
			dict[gram_lower[0].title(), gram_lower[1].title()]
		except KeyError:
			exceptions_raised +=1
		else:
			if count==0:
				comb_list.append(tuple([gram_lower[0].title(), gram_lower[1], dict[gram_lower[0].title(), gram_lower[1]]]))
				comb_list.append(tuple([gram_lower[0].title(), gram_lower[1].title(), dict[gram_lower[0].title(), gram_lower[1].title()]]))
				comb_list = sorted(comb_list, key = lambda x: x[2], reverse = True)
				best_bigram = comb_list[0]
				##Evaluation/match with the original bigram
				if (gram == tuple([comb_list[0][0], comb_list[0][1]])):
					print gram
					acc_score +=1
				else:
					pass
			else:
				comb_list.append(tuple([gram_lower[0], gram_lower[1], dict[gram_lower[0], gram_lower[1]]]))
				comb_list.append(tuple([gram_lower[0].title(), gram_lower[1], dict[gram_lower[0].title(), gram_lower[1]]]))
				comb_list.append(tuple([gram_lower[0], gram_lower[1].title(), dict[gram_lower[0], gram_lower[1].title()]]))
				comb_list.append(tuple([gram_lower[0].title(), gram_lower[1].title(), dict[gram_lower[0].title(), gram_lower[1].title()]]))
				##Sort bigrams using similarity score
				comb_list = sorted(comb_list, key = lambda x: x[2], reverse = True)
				best_bigram = comb_list[0]
				##Evaluation/match with the original bigram
				if (gram == tuple([comb_list[0][0], comb_list[0][1]])):
					print gram
					acc_score +=1
				else:
					pass

accuracy = acc_score/float(total - exceptions_raised) * 100.0
print accuracy
print total - exceptions_raised
print acc_score

###################
###################
###################

ls = os.listdir('/local/vatshank/articles/articles/')
offset = 5

for thresh in np.arange(0,20,1):
	acc_score = 0
	acc_upper = 0
	acc_lower = 0
	exceptions_raised = 0
	count_lower = 0
	count_upper = 0
	total = 0
	raised_tokens = []
	for file in ls:
		with open('/local/vatshank/articles/articles/'+file,'r') as f_in:
			text = f_in.read()
		sent_tokens = sent_tokenizer.tokenize(text.strip())
		##Create tokens from the whole text
		temp = map(word_tokenize, sent_tokens)

		# tokens = [item for sublist in temp for item in sublist]
		##making tuples of (token, position of token in the sentence)
		tokens = [(item,i) for sublist in temp for (i,item) in enumerate(sublist)] 
		##Remove punctuations
		tokens_filtered = [token for token in tokens if token[0].isalpha()]
		total = total + len(tokens_filtered)
		for i, token in enumerate(tokens_filtered):
			# print i, token
			left_con = tokens_filtered[max(i-offset,0):i]
			left_con = [token[0] for token in left_con] ##take the first value in the tuple, ignore the position

			right_con = tokens_filtered[i+1:i+1+offset]
			right_con = [token[0] for token in right_con] ##take the first value in the tuple, ignore the position

			left_con.extend(right_con)
			context = left_con
			token_lower = token[0].lower()
			token_upper = token_lower.title()
			score_lower = []
			score_upper = []
			FLAG = 0

			##handling stop words when exception is raised
			if (token_lower in stop):
				if((token[1] == 0) | (token_lower == 'i')):
					result = token_upper
				else:
					result = token_lower
			else:
				for word in context:
					word_lower = word.lower()
					word_upper = word_lower.title()
					try:
						score_l = dict[(token_lower, word_lower)]
						score_u = dict[(token_lower, word_upper)]
					except KeyError:
						pass
					else:
						score_lower.append(score_l +  score_u)			
					try:
						score_l = dict[(token_upper, word_lower)]
						score_u = dict[(token_upper, word_upper)]
					except KeyError:
						pass
					else:
						score_upper.append(score_l +  score_u)	
				#print len(score_upper), len(score_lower)
				if (len(score_lower)==0) | (len(score_upper)==0):
					result = token_lower
				else:
					if (abs(mean(score_lower) - mean(score_upper)) < thresh):
						result = token_lower
					elif mean(score_upper) > mean(score_lower):
						result = token_upper
					else:
						result = token_lower
				# print result, token	
			if (token[1] != 0) & (token[0] not in stop) & (token_lower!='i'):
				if token[0] == token_upper:
					if result == token[0]:
						acc_upper +=1
					count_upper +=1
				if token[0] == token_lower:
					if result == token[0]:
						acc_lower +=1
					count_lower +=1
			if (result == token[0]):
				acc_score +=1
			else:
				pass
				f_fail.write(token[0] +'\t'+result +'\t'+str(mean(score_lower)) +'\t'+ str(mean(score_upper))+'\n')
	accuracy = acc_score/float(total) * 100
	accuracy_lower = acc_lower/float(count_lower) * 100
	accuracy_upper = acc_upper/float(count_upper) * 100
	print thresh, accuracy, accuracy_lower, accuracy_upper
