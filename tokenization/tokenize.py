# Usage: python indic_tokenize.py <infile> <outfile> <language>

from indicnlp.tokenize import indic_tokenize  
import os,sys
import codecs

if len(sys.argv)<4:
    print("Usage: python indic_tokenize.py <infile> <outfile> <language>")
    sys.exit(1)

with open(sys.argv[1],'r', encoding='utf-8') as ifile:
    with open(sys.argv[2],'w', encoding='utf-8') as ofile:
        for line in ifile:
            tokenized_line=' '.join(indic_tokenize.trivial_tokenize(line,sys.argv[3]))
            ofile.write(tokenized_line)