"""
INTENTIONS AT THE TIME OF WRITING: Returns one big (pickled) dict of {bigram:tf_idf} from the frequencies file which looks like this - [bigram] tf idf
WHAT THIS ACTUALLY DOES : Takes a list of (smaller) text files and pickles mutliple dicts
Date: 19/04/15
"""
import pickle
import numpy as np
import sys
import os
sys.stderr = open('/z/vatshank/log_make_tfidf.txt', 'w')


if __name__ == '__main__':
	ls = os.listdir('/local/vatshank/wiki_blm/splitting_9/splits/')
	os.mkdir('/z/vatshank/pickles_9')
	for file in ls:
		dict = {}
		with open('/local/vatshank/wiki_blm/splitting_9/splits/'+file,'r') as f_in:
			for line in f_in:
				##Will replace this with a regular expression when I have more caffeine in me
				entries = line.replace('[','').replace(']','').replace(',','').replace('"','').split()
				tf_ = float(entries[2])
				df_ = float(entries[3])
				tf_idf = (1.0 + np.log(tf_))*np.log(total/df_)
				dict[(entries[0], entries[1])] = tf_idf
		with open('/z/vatshank/pickles_9/'+file+'_tf_idf.pickle','w') as f_out:
			pickle.dump(dict,f_out)
