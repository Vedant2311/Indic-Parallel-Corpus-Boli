#### Usage: $ python3 create_opus_parallel_pair.py hi gu jw300 overall.txt
import os
import sys
import time
# Make sure that the configuration.py is in the same folder as this file
import configuration as config

## Taking inputs from command line
### src -> Source language Id (eg hi)
### tgt -> Target language Id (eg gu)
### base -> Name of the OPUS corpus directory (eg jw300)
### file_name -> Name of the file to be divided
src = sys.argv[1]
tgt = sys.argv[2]
base = sys.argv[3]
file_name = sys.argv[4]

### Saving the current directory of execution somewhere
cwd = os.getcwd()

### We look locally in the sub-directories for the OPUS cwd
path_opus = config.path_opus
dir_path = (os.path.join(path_opus,base))
creation_path = os.path.join(dir_path, src+'-'+tgt) 

### Creating the corresponding Directory and changing cwd
os.makedirs(creation_path, exist_ok = True) 
os.chdir(creation_path)

### Name of the directory
if base=='jw300' or base=='gnome':
	dir_name = base.upper()
elif base=='subtitles':
	dir_name = 'OpenSubtitles'
elif base=='ubuntu':
	dir_name = 'Ubuntu'

### Run the opus_read command and creates the one-one correponding sentence pairs
# Obtain the entire data
if 'overall' in file_name:
	cmd = 'opus_read --directory ' + dir_name + ' --source ' + src + ' --target ' + tgt + ' --leave_non_alignments_out ' + '--src_range 1 --tgt_range 1 ' + '--write ' + file_name + ' --write_mode normal'
	os.system(cmd)
# Obtain data corresponding to the threshold
else:
	## Convert a file name as t_0.9.txt into 0.9
	threshold = (file_name.split('_')[1]).replace('.txt','')
	cmd = 'opus_read --directory ' + dir_name + ' --source ' + src + ' --target ' + tgt + ' --leave_non_alignments_out ' + '--src_range 1 --tgt_range 1 ' + '--attribute certainty ' + '--threshold ' + threshold + ' --write ' + file_name + ' --write_mode normal'
	os.system(cmd)	

### Coming back to the initial directory
os.chdir(cwd)
