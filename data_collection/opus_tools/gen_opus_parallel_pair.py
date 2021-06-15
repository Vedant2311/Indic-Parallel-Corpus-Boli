#### Usage: $ python3 gen_opus_parallel_pair.py hi gu jw300 overall.txt
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

### We look locally in the sub-directories for the cwd
path_opus = os.getcwd()
base_path = os.path.join(os.path.join(path_opus,base),src + "-" + tgt)
file_path = os.path.join(base_path,file_name)

### Now perform the operations on this file to divide this into parts
src_file = file_name.replace('.txt','') + '.' + src
tgt_file = file_name.replace('.txt','') + '.' + tgt

src_path = os.path.join(base_path,src_file)
tgt_path = os.path.join(base_path, tgt_file)

file_obj = open(file_path,'r') 
file_src = open(src_path,'w')
file_tgt = open(tgt_path,'w')

## Reading all the lines of input file
lines = file_obj.readlines()
lines_output = []
line_temp = []

### Removing all the improper lines from the file
for i in range(len(lines)):	

	# Check if it is an empty line	
	if lines[i]=='\n':
		continue		
	
	# Check if the first character is a '#'
	elif lines[i][0]=='#':
		continue
		
	# Add elements between line breaks in a block
	elif lines[i][0]=='=':
		if len(line_temp)==0:
			continue
		else:
			lines_output.append(line_temp)
			line_temp=[]

	# Else just add the line to the block
	else:
		line_temp.append(lines[i])

### Dividing the lines into different files
for i in range(len(lines_output)):
	if len(lines_output[i])==2:
		if '(src)' in lines_output[i][0] and '(trg)' in lines_output[i][1]:
			src_line_all = lines_output[i][0]
			tgt_line_all = lines_output[i][1]
			
			src_line = src_line_all[src_line_all.find('>')+1:]
			tgt_line = tgt_line_all[tgt_line_all.find('>')+1:]
			
			if src_line=='' or tgt_line=='':
				continue
			else:
				file_src.write(src_line)
				file_tgt.write(tgt_line)
			
			
## Closing the open files
file_obj.close()
file_src.close()
file_tgt.close()
