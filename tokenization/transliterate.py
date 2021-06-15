from indicnlp.transliterate import unicode_transliterate  
import sys

if len(sys.argv)<4:
    print("Usage: python transliterate.py <command> <infile> <outfile> <src_language> <tgt_language>")
    sys.exit(1)

if sys.argv[1]=='transliterate':

    src_language=sys.argv[4]
    tgt_language=sys.argv[5]

    with open(sys.argv[2],'r', encoding='utf-8') as ifile:
        with open(sys.argv[3],'w', encoding='utf-8') as ofile:
            for line in ifile.readlines():
                transliterated_line=unicode_transliterate.UnicodeIndicTransliterator.transliterate(line,src_language,tgt_language)
                ofile.write(transliterated_line)

elif sys.argv[1]=='romanize':

    language=sys.argv[4]

    ### temp fix to replace anusvara with corresponding nasal
    #r1_nasal=re.compile(ur'\u0902([\u0915-\u0918])')
    #r2_nasal=re.compile(ur'\u0902([\u091a-\u091d])')
    #r3_nasal=re.compile(ur'\u0902([\u091f-\u0922])')
    #r4_nasal=re.compile(ur'\u0902([\u0924-\u0927])')
    #r5_nasal=re.compile(ur'\u0902([\u092a-\u092d])')

    with open(sys.argv[2],'r', encoding='utf-8') as ifile:
        with open(sys.argv[3],'w', encoding='utf-8') as ofile:
            for line in ifile.readlines():
                ### temp fix to replace anusvara with corresponding nasal
                #line=r1_nasal.sub(u'\u0919\u094D\\1',line)
                #line=r2_nasal.sub(u'\u091e\u094D\\1',line)
                #line=r3_nasal.sub(u'\u0923\u094D\\1',line)
                #line=r4_nasal.sub(u'\u0928\u094D\\1',line)
                #line=r5_nasal.sub(u'\u092e\u094D\\1',line)

                transliterated_line=ItransTransliterator.to_itrans(line,language)

                ## temp fix to replace 'ph' to 'F' to match with Urdu transliteration scheme
                transliterated_line=transliterated_line.replace('ph','f')

                ofile.write(transliterated_line)

elif sys.argv[1]=='indicize':

    language=sys.argv[4]

    with open(sys.argv[2],'r', encoding='utf-8') as ifile:
        with open(sys.argv[3],'w', encoding='utf-8') as ofile:
            for line in ifile.readlines():
                transliterated_line=ItransTransliterator.from_itrans(line,language)
                ofile.write(transliterated_line)