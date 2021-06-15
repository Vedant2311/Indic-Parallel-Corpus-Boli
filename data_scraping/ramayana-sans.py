import requests
import pickle
from bs4 import BeautifulSoup
import re
import os
# Make sure that the configuration.py is in the same folder as this file
import configuration as config

## Some global parameters that are dependant on the website
url='https://www.valmiki.iitk.ac.in/sloka'  # The URL of the ramayana website
kanda_ids = [1,2,3,4,5]                     # The IDs of the different 'Kandas' present on the website. Note that the data for the 6th Kanda was not present at the time of this compilation
sarga_ids = [77,119,75,67,68]               # The maximum number of sargas corresponding to the different Kandas present

## Gets the English Translations of the different Sanskrit words as present in the website
def get_word_translations():
    tuple_list=[]

    ## Going through all the Kandas and all the Sargas in them
    for kanda in kanda_ids:
        print('Current kanda is: ' + str(kanda))
        for sarga in range(1,sarga_ids[kanda-1]+1):
            # Getting the corresponding parameters and obtaining the corresponding HTML page
            p={'field_kanda_tid':kanda,'language':'dv','field_sarga_value':sarga}
            r=requests.get(url,params=p)
            soup=BeautifulSoup(r.text,"html5lib")

            # The first class is the Sanskrit text, the second one is the word translations, the third one is the English Translation. 
            # We need to have the text extracted from the second class. So making use of a parameter to denote so
            mod=0
            for c in soup.find_all(class_="field-content"):
                if mod%3==1:
                    s=c.text

                    # Splitting the text and seperating the Sanskrit and English texts via these character
                    for a in s.split(','):
                        x=0
                        a=a.strip()
                        for i in range(len(a)):
                            if (a[i]>='a' and a[i]<='z') or (a[i]>='A' and a[i]<='Z'):
                                x=i
                                break
                        # Appending the Sanskrit text followed by the English text
                        if x>1:
                            tuple_list.append((a[:x-1],a[x:]))
                mod+=1

    ## Done with the list creation. Now writing the values to the directory structure
    path_ramayana_sans = config.path_ramayana_sans
    path_pair = os.path.join(path_ramayana_sans, 'en-sa')
    os.makedirs(path_pair, exist_ok = True)

    ## Opening a file to be written
    f_en = open(os.path.join(path_pair,config.word_translation_name + '.en'),'w')
    f_sa = open(os.path.join(path_pair,config.word_translation_name + '.sa'),'w')

    ## Writing the pairs to these files
    for (sa,en) in tuple_list:
        if sa.strip() and en.strip():
            f_sa.write(sa.replace('\n','') + '\n')
            f_en.write(en.replace('\n','') + '\n')
    
    f_en.close()
    f_sa.close()

## Gets the English Translations of the different Sanskrit Shlokas present on the website
def get_shloka_translations():
    tuple_list=[]

    ## Going through all the Kandas and all the Sargas in them
    for kanda in kanda_ids:
        print('Current kanda is: ' + str(kanda))
        for sarga in range(1,sarga_ids[kanda-1]+1):
            # Getting the corresponding parameters and obtaining the corresponding HTML page
            p={'field_kanda_tid':kanda,'language':'dv','field_sarga_value':sarga}
            r=requests.get(url,params=p)
            soup=BeautifulSoup(r.text,"html5lib")

            # The first class is the Sanskrit text, the second one is the word translations, the third one is the English Translation. 
            # We need to have the text extracted from the First and Third class and have them clubbed together 
            content_list = soup.find_all(class_="field-content")

            for i in range(len(content_list)):
                # Getting the Sanskrit text first
                if i%3==0:
                    sa = content_list[i].text.replace('\n','').strip().split(']')[-1]
                # Getting the English text after that and clubbing them
                elif i%3==2:
                    # Checking if it is the last line or not
                    if i!=len(content_list)-1:
                        en = content_list[i].text.replace('\n','').strip()
                        tuple_list.append((sa,en))

                        # Reinitialize both of them to Empty strings
                        en,sa = '',''
                    else:
                        # In the last line there is another text present which is a translation for En-Sa
                        # We would try to extract that as well
                        total_text = content_list[i].text.replace('\n','').strip()

                        # Getting the English text that would map with the Sanskrit text extracted earlier
                        x = 0
                        punc_list = [' ', '.', ',', '\'', '"',';', ':', '?', '!', '(', ')']
                        for i1 in range(len(total_text)):
                            if not ((total_text[i1]>='a' and total_text[i1]<='z') or (total_text[i1]>='A' and total_text[i1]<='Z') or \
                                    total_text[i1] in punc_list):
                                x = i1
                                break
                        en = total_text[0:x-1]
                        tuple_list.append((sa,en))

                        # Getting the next Sanskrit and English pair that marks the end of the Sarga
                        y = x
                        for i1 in range(x, len(total_text)):
                            if ((total_text[i1]>='a' and total_text[i1]<='z') or (total_text[i1]>='A' and total_text[i1]<='Z')):
                                y = i1
                                break

                        sa = total_text[x:y-1]
                        en = total_text[y:]
                        tuple_list.append((sa,en))

                        # Reinitialize both of them to Empty strings
                        en,sa = '',''

    ## Done with the list creation. Now writing the values to the directory structure
    path_ramayana_sans = config.path_ramayana_sans
    path_pair = os.path.join(path_ramayana_sans, 'en-sa')
    os.makedirs(path_pair, exist_ok = True)

    ## Opening a file to be written
    f_en = open(os.path.join(path_pair,config.shloka_translation_name + '.en'),'w')
    f_sa = open(os.path.join(path_pair,config.shloka_translation_name + '.sa'),'w')

    ## Writing the pairs to these files
    for (sa,en) in tuple_list:
        if sa.strip() and en.strip():
            sa = re.sub(' +', ' ', sa)
            sa = re.sub('\t+', ' ', sa)
            f_sa.write(sa.replace('\n','') + '\n')
            f_en.write(en.replace('\n','') + '\n')
    
    f_en.close()
    f_sa.close()

## Merging the word and shloka files together
def create_overall():
    # Opening the extracted word and Shloka translation files
    path_ramayana_sans = config.path_ramayana_sans
    path_pair = os.path.join(path_ramayana_sans, 'en-sa')
    os.makedirs(path_pair, exist_ok = True)

    with open(os.path.join(path_pair,config.shloka_translation_name + '.en')) as f:
        shloka_en = f.readlines()
    with open(os.path.join(path_pair,config.shloka_translation_name + '.sa')) as f:
        shloka_sa = f.readlines()

    with open(os.path.join(path_pair,config.word_translation_name + '.en')) as f:
        word_en = f.readlines()
    with open(os.path.join(path_pair,config.word_translation_name + '.sa')) as f:
        word_sa = f.readlines()
    
    # Adding them to the final common file
    overall_en = open(os.path.join(path_pair, config.base_train_name + '.en'),'w')
    overall_sa = open(os.path.join(path_pair, config.base_train_name + '.sa'),'w')

    for (en,sa) in zip(shloka_en, shloka_sa):
        overall_en.write(en)
        overall_sa.write(sa)
    for (en,sa) in zip(word_en, word_sa):
        overall_en.write(en)
        overall_sa.write(sa)
    
    overall_en.close()
    overall_sa.close()
    

def main(strin):
    if strin=='word':
        get_word_translations()
    elif strin=='shloka':
        get_shloka_translations()
    elif strin=='overall':
        create_overall()

if __name__ == '__main__':
    ## To get the word-word mappings
    # print('Generating the word-word translations from Ramayana')
    # main('word')

    ## To get the Shloka translations
    ## Note that some manual cleaning was done on top of this as described in the README
    # print('Generating the Shloka translations from Ramayana')
    # main('shloka')

    ## To get all the parallel corpus into one file
    print('Combining the texts into one file')
    main('overall')