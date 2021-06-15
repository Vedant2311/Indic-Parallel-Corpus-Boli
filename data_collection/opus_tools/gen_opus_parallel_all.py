### Function to obtain all the pairs of a particular OPUS corpus
### Uses the function gen_opus_parallel_pair.py 
import os
import sys
# Make sure that the configuration.py is in the same folder as this file
import configuration as config

## langs is the sorted set of all languages. 'base' is the corpus name. 'thr' is the required threshold. Ideally to be set as 1.1
langs = ['as', 'bn', 'en', 'gu', 'hi', 'kn', 'ml', 'mni', 'mr', 'or', 'pa', 'ta', 'te', 'ur']
base = sys.argv[1]
thr = sys.argv[2]

## Saving the current working directory
cwd = os.getcwd()

## Saving the directory for the OPUS files
cwd_opus = config.path_opus

### Having a 2D for loop for all the 14C2 combinations
for i in range(len(langs)-1):
	for j in range(i+1,len(langs)):
		print('================================================')
		print('The current pair is ' + langs[i] + ' ' + langs[j])
		
		base_path = os.path.join(os.path.join(cwd_opus,base),langs[i] + "-" + langs[j])
		dirs = os.listdir(base_path) 
		
		# If the folder is empty, i.e no file downloaded from OPUS
		if len(dirs)==0:
			continue 
		
		### Calling the pair creation function for all the sentences
		cmd = 'python3 gen_opus_parallel_pair.py ' + langs[i] + ' ' + langs[j] + ' ' + base + ' overall.txt'
		os.system(cmd)
		
		# Coming back to the original cwd
		os.chdir(cwd)

		### Calling the pair creation function for all the sentences above the threshold 
		cmd = 'python3 gen_opus_parallel_pair.py ' + langs[i] + ' ' + langs[j] + ' ' + base + ' t_' + thr + '.txt'  
		os.system(cmd)
		
		# Coming back to the original cwd
		os.chdir(cwd)		