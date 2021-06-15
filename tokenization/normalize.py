# USAGE
# python normalize.py <infile> <outfile> <language> [<replace_nukta(True,False)>] [<normalize_nasals(do_nothing|to_anusvaara_strict|to_anusvaara_relaxed|to_nasal_consonants)>]

from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
import os
import sys
import codecs

if len(sys.argv)<4:
    print("Usage: python normalize.py <infile> <outfile> <language> [<replace_nukta(True,False)>] [<normalize_nasals(do_nothing|to_anusvaara_strict|to_anusvaara_relaxed|to_nasal_consonants)>]") 
    sys.exit(1)

ifile = sys.argv[1]
ofile = sys.argv[2]
language=sys.argv[3]

remove_nuktas=False
normalize_nasals='do_nothing'

if len(sys.argv)>=5:
    remove_nuktas=bool(sys.argv[4])
if len(sys.argv)>=6:
    normalize_nasals=sys.argv[5]

# create normalizer
factory=IndicNormalizerFactory()
normalizer=factory.get_normalizer(language,remove_nuktas=remove_nuktas,nasals_mode=normalize_nasals)

# DO normalization 
with codecs.open(sys.argv[1],'r','utf-8') as ifile:
    with codecs.open(sys.argv[2],'w','utf-8') as ofile:
        for line in ifile.readlines():
            normalized_line=normalizer.normalize(line)
            ofile.write(normalized_line)