#### This file makes use of the English centric Bible-uedin dataset obtained by us and gets other alignments too
import os
import configuration as config

# Langs present in the bibe-uedin dataset
langs = ['en','gu','hi','kn','ml','mr','te']
langs_ne = ['gu','hi','kn','ml','mr','te']

# Getting the important paths
path_bible_uedin = config.path_bible_uedin

# Creating a function to read from the English aligned pairs
def read_from_en(lang):
    str_pair = 'en' + '-' + lang
    path_pair = os.path.join(path_bible_uedin, str_pair)

    lines_lang, lines_en  = [], []
    with open(os.path.join(path_pair,config.base_train_name + '.en')) as f:
        lines_en = f.readlines()
    
    with open(os.path.join(path_pair,config.base_train_name + '.' + lang)) as f:
        lines_lang = f.readlines()

    lines_pair = []    
    for (en,lang) in zip(lines_en, lines_lang):
        lines_pair.append((en, lang))
    
    # Sorting the lines with respect to English
    lines_pair = sorted(lines_pair, key = lambda x: x[0])
    return lines_pair

for i in range(len(langs_ne)-1):
    for j in range(i+1,len(langs_ne)):
        src = langs_ne[i]
        tgt = langs_ne[j]
        print(src,tgt)

        # Getting the source and target pairs with English
        src_en_tuple = read_from_en(src)
        tgt_en_tuple = read_from_en(tgt)

        # Creating the pair directory in the folder
        path_pair = os.path.join(path_bible_uedin, src + '-' + tgt)
        os.makedirs(path_pair, exist_ok = True)

        # Adding the common lines between the two of them
        src_tgt_tuple = []
        count_src = 0
        count_tgt = 0
        while (count_src < len(src_en_tuple)) and (count_tgt < len(tgt_en_tuple)):
            if src_en_tuple[count_src][0] == tgt_en_tuple[count_tgt][0]:
                src_tgt_tuple.append((src_en_tuple[count_src][1], tgt_en_tuple[count_tgt][1]))
                count_src+=1
                count_tgt+=1
            elif src_en_tuple[count_src][0] < tgt_en_tuple[count_tgt][0]:
                count_src+=1
            else:
                count_tgt+=1
        
        # Writing them back to some files
        f_src = open(os.path.join(path_pair, config.base_train_name + '.' + src),'w')
        f_tgt = open(os.path.join(path_pair, config.base_train_name + '.' + tgt),'w')
        for (src,tgt) in src_tgt_tuple:
            f_src.write(src)
            f_tgt.write(tgt)
        f_src.close()
        f_tgt.close()
