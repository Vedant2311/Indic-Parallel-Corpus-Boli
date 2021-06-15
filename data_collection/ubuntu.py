### A file to directly get parallely-aligned sentences files from the OPUS websites
### This has a limitation as compared with the **opus_tools** pipeline which can make use of the sentence alignment score to get a quantatively shorter but qualitiatively better dataset
### This is compulsorily used for the OPUS datasets like Ubuntu, GNOME, WikiMatrix etc, because the xml files obtained using the OPUS tools are corrupt
### This file corresponds to Ubuntu. Would require minor changes for other datasets. 

import os
# Make sure that the configuration.py is in the same folder as this file
import configuration 

path_scratch = configuration.path_scratch

### The paths for the major datasources obtained from OPUS
path_opus = configuration.path_opus
path_ubuntu = configuration.path_ubuntu

langs = ['as', 'bn', 'en', 'gu', 'hi', 'kn', 'ml', 'mni', 'mr', 'or', 'pa', 'ta', 'te', 'ur']
cwd = os.getcwd()

for i in range(len(langs)-1):
    for j in range(i+1,len(langs)):

        src = langs[i]
        tgt = langs[j]
        print(src,tgt)

        link = 'http://opus.nlpl.eu/download.php?f=Ubuntu/v14.10/moses/' + src + '-' + tgt + '.txt.zip'

        path_pair = os.path.join(path_ubuntu, src + '-' + tgt)
        os.makedirs(path_pair, exist_ok = True)
        os.chdir(path_pair)

        os.system('wget ' + link + ' --no-check-certificate')

        file_name = 'download.php?f=Ubuntu%2Fv14.10%2Fmoses%2F' + src + '-' + tgt + '.txt.zip'
        os.system('unzip ' + file_name)

        extracted_base = 'Ubuntu.' + src + '-' + tgt + '.'
        os.system('mv ' + extracted_base + src + ' ' + 'overall.' + src)
        os.system('mv ' + extracted_base + tgt + ' ' + 'overall.' + tgt)

        os.chdir(cwd)