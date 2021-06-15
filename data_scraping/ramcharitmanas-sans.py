import requests
import pickle
from bs4 import BeautifulSoup
import re
import os
# Make sure that the configuration.py is in the same folder as this file
import configuration as config

## Some global parameters that are dependant on the website
url='https://hindi.webdunia.com/religion/religion/hindu/ramcharitmanas/'    # The URL of the ramcharitmanas website
kandas = ['BalKand','AyodyaKand','AranyaKand','KishkindhaKand','SunderKand','LankaKand','UttarKand']
max_dict = dict()
max_dict['BalKand']=57
max_dict['AyodyaKand']=49
max_dict['AranyaKand']=16
max_dict['KishkindhaKand']=12
max_dict['SunderKand']=19
max_dict['LankaKand']=36
max_dict['UttarKand']=21

## Going through all these links in the required format and getting the outputs in a tuple
tuple_list = []
for kanda in kandas:
    for htm in range(1,max_dict[kanda]+1):

        print(kanda, htm)
        website = url + kanda + '/' + str(htm) + '.htm'
        r = requests.get(website)
        soup = BeautifulSoup(r.text,"html5lib")

        # Getting all the classes for Sanskrit and Hindi
        wrapper = soup.find_all(class_='slok_wrapper')
        for i in range(len(wrapper)):
            c_sans = wrapper[i].find_all(class_='slok')
            c_hi = wrapper[i].find_all(class_='bhawarth')
            c_hi_temp = wrapper[i].find_all(class_='arth_pad kreative')

            # Only takings those ones where the classes match
            if len(c_sans)==len(c_hi) and len(c_hi)==1:
                sans = c_sans[0].text
                sans = sans.replace('\n','')
                sans = sans.replace('* ', '')
                sans = re.sub(' +',' ',sans)
                sans = re.sub('\t+', ' ', sans)

                hi = c_hi[0].text
                hi = hi.replace('\n','')
                hi = hi.replace('* ', '')
                hi = re.sub(' +',' ',hi)
                hi = re.sub('\t+', ' ', hi)
                hi = hi.replace('भावार्थ:-','')
                hi = hi.replace('भावार्थ : ','')

                tuple_list.append((sans,hi))

            elif len(c_sans)==len(c_hi_temp) and len(c_hi_temp)==1:
                sans = c_sans[0].text
                sans = sans.replace('\n','')
                sans = sans.replace('* ', '')
                sans = re.sub(' +',' ',sans)
                sans = re.sub('\t+', ' ', sans)

                hi = c_hi_temp[0].text
                hi = hi.replace('\n','')
                hi = hi.replace('* ', '')
                hi = re.sub(' +',' ',hi)
                hi = re.sub('\t+', ' ', hi)
                hi = hi.replace('भावार्थ:-','')

                tuple_list.append((sans,hi))

            else:
                continue

## Writing the files 
path_ramcharitmanas_sans = config.path_ramcharitmanas_sans
path_pair = os.path.join(path_ramcharitmanas_sans, 'hi-sa')
os.makedirs(path_pair, exist_ok = True)

f_sa = open(os.path.join(path_pair,config.base_train_name + '.sa'),'w')
f_hi = open(os.path.join(path_pair,config.base_train_name + '.hi'),'w')

for (sa,hi) in tuple_list:
    if sa.strip() and hi.strip():
        f_sa.write(sa.strip().replace('\n','') + '\n')
        f_hi.write(hi.strip().replace('\n','') + '\n')

f_sa.close()
f_hi.close()