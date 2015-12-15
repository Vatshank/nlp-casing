"""
INTENTIONS AT THE TIME of WRITING: Combine smaller (pickled)dictionaries into a bigger dictionary (updating)
WHAT THIS ACTUALLY DOES: same as above
Date: 20/04/15
"""

import pickle
import os
import sys
sys.stderr = open('/z/vatshank/log_combine_pickled_dicts.txt', 'w')
# sys.stdout = open('out','w')

if __name__ == '__main__':
	f = open('out','w')
	ls = os.listdir('/z/vatshank/pickles_9/')
	total = {}
	for file in ls:
		print file
		with open('/z/vatshank/pickles_9/'+file,'r') as f_in:
			temp = pickle.load(f_in)
		total.update(temp)
	print "Pickling..."
	f.close()
	with open('/z/vatshank/pickles_9/combined_dict.pickle','w') as f_out:
		pickle.dump(total,f_out)
