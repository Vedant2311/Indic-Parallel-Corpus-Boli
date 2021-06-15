import os
import configuration as config

# Languages that are not present/present in the test/dev set
langs_nt = ['as','mni','sa','ur']
langs_t = ['bn', 'en', 'gu', 'hi', 'kn', 'ml', 'mr', 'or', 'pa', 'ta', 'te']

# Getting the important paths 
path_pmi = config.path_pmi
path_indic_dev = config.path_indic_dev
path_indic_test = config.path_indic_test

# Creating a function to read from the English aligned pairs from the PMI dataset
# UPDATE: This function can now take any pivot language 'src', and not just English
def read_from_src(src,lang):
    if lang > src:
        str_pair = src + '-' + lang
    else:
        str_pair = lang + '-' + src
    path_pair = os.path.join(path_pmi, str_pair)

    lines_lang, lines_en  = [], []
    if os.path.exists(os.path.join(path_pair,config.pmi_data_name + '.' + src)) and os.path.exists(os.path.join(path_pair,config.pmi_data_name + '.' + lang)):
        with open(os.path.join(path_pair,config.pmi_data_name + '.' + src)) as f:
            lines_en = f.readlines()
        
        with open(os.path.join(path_pair,config.pmi_data_name + '.' + lang)) as f:
            lines_lang = f.readlines()

    if len(lines_en)==0:
        return []
    
    lines_pair = []    
    for (en,lang) in zip(lines_en, lines_lang):
        lines_pair.append((en, lang))
    
    return lines_pair

# Creating a function that returns the index of an element occurence
# The value of -1 will be returned in case of any error
def findIndex(line, lines_pair):
    ind = -1
    for i in range(len(lines_pair)):
        if lines_pair[i][0]==line:
            ind = i
            break
    return ind

## Getting the stats of the languages that would be needed to be manually annotated
def get_stats():
    for src in langs_nt:
        print(src)

        # Since Sanskrit is not there in PMI, we need all the translations
        if src=='sa' or src=='mni':
            print('Left over for Dev data',1000)
            print('Left over for Test data', 2390)
            continue

        # Getting the stats for the Dev data
        if os.path.exists(os.path.join(path_indic_dev, config.wat_dev_name + '.' + src)):
            with open(os.path.join(path_indic_dev, config.wat_dev_name + '.' + src)) as f:
                lines_lang = f.readlines()

            count = 0
            for line in lines_lang:
                if not(line.strip()):
                    count+=1
            print('Left over for Dev data',count)

        # Getting the stats for the Test data                
        if os.path.exists(os.path.join(path_indic_test, config.wat_test_name + '.' + src)):
            with open(os.path.join(path_indic_test, config.wat_test_name + '.' + src)) as f:
                lines_lang = f.readlines()

            count = 0
            for line in lines_lang:
                if not(line.strip()):
                    count+=1
            print('Left over for Test data', count)

## Scanning the test and train dataset to get the alignments for either Test or Dev
def scan_alignments(dir_name, f_name):

    # Gettings the pairs for these left-over languages via any pivot language
    for src in langs_nt:

        # Creating a dictionary that will consist of all the sentences of the new languages
        # According to the index as in the Test/Dev dataset of WAT2021
        lines_lang = dict()
        total_len = 0

        for pivot in langs_t:
            print(src, pivot)
            with open(os.path.join(dir_name, f_name + '.' + pivot)) as f:
                lines_en = f.readlines()

            # Gets the size of the Dev/Test data
            if total_len==0:
                total_len = len(lines_en)

            lines_pair = read_from_src(pivot, src)
            if len(lines_pair)==0:
                continue 
            
            # Storing the lines corresponding to the indices for the new language
            for j in range(len(lines_en)):
                line = lines_en[j]
                i = findIndex(line, lines_pair)
                if i!=-1 and j not in lines_lang.keys():
                    lines_lang[j] = (lines_pair[i][1])
        
        with open(os.path.join(dir_name, f_name + '.' + src),'w') as f:
            for i in range(total_len):
                if i not in lines_lang.keys():
                    f.write('\n')                
                else:
                    f.write(lines_lang[i])


## Getting the translations of the left-over languages that are already present in PMI
def get_translations():
    # Getting for the Dev data first
    print('Getting the alignments for Dev data')
    dev_folder = path_indic_dev
    dev_name = config.wat_dev_name
    scan_alignments(dev_folder, dev_name)

    # Getting for the test data
    print('Getting the alignments for Test data')
    test_folder = path_indic_test
    test_name = config.wat_test_name
    scan_alignments(test_folder, test_name)

## The main function that will get the alignments between test and train for the new languages
## And print the stats that would be obtained correspondingly
def main():
    # Getting the alignments
    print('Getting the alignments')
    get_translations()
    print()

    # Getting the stats for the manual annotations
    print('Getting the annotation stats')
    get_stats()

if __name__ == '__main__':
    main()