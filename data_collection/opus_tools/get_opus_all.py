### Function to obtain all the pairs of a particular OPUS corpus
### Uses the function get_opus_pair.py 
import os
import sys
# Make sure that the configuration.py is in the same folder as this file
import configuration as config

## langs is the sorted set of all languages. 'base' is the corpus name
langs = ['as', 'bn', 'en', 'gu', 'hi', 'kn', 'ml', 'mni', 'mr', 'or', 'pa', 'ta', 'te', 'ur']

## langs present in the opensubtitles dataset
langs_subt = ['bn','en','hi','ml','ta','te','ur']

## Input directory base
base = sys.argv[1]

## Saving the current working directory
cwd = os.getcwd()

### Having a 2D for loop for all the 14C2 combinations
for i in range(len(langs)-1):
	for j in range(i+1,len(langs)):
		print('================================================')
		print('The current pair is ' + langs[i] + ' ' + langs[j])
		
		if (base=='jw300' or base=='gnome' or base=='ubuntu') or (base=='subtitles' and langs[i] in langs_subt and langs[j] in langs_subt):

			### Calling the pair download function
			cmd = 'python3 get_opus_pair.py ' + langs[i] + ' ' + langs[j] + ' ' + base
			os.system(cmd)
		
			# Coming back to the original cwd
			os.chdir(cwd)
		else:
			print('The current pair is not present')
