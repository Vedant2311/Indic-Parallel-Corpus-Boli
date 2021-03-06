import os

### A function that adds a new language code to the existing language code list. Keeps the alphabetical order maintained
def add_new_lang(lang_list, new_lang):
    new_list = []
    new_lang_added = False
    for lang in lang_list:
        if lang < new_lang:
            new_list.append(lang)
        elif (lang > new_lang) and (not new_lang_added):
            new_list.append(new_lang)
            new_list.append(lang)
            new_lang_added = True
        elif (lang > new_lang) and (new_lang_added):
            new_list.append(lang)
    return new_list

### The paths of the scatch directory. All the other paths relative to this
path_scratch = '/scratch/cse/btech/cs1170339'

### All the 14 languages initially considered by us
langs = ['as', 'bn', 'en', 'gu', 'hi', 'kn', 'ml', 'mni', 'mr', 'or', 'pa', 'ta', 'te', 'ur']

### The paths for the major datasources obtained from OPUS
path_opus = os.path.join(path_scratch, 'opus')
path_jw300 = os.path.join(path_opus, 'jw300')
path_subtitles = os.path.join(path_opus, 'subtitles')
path_opus100 = os.path.join(path_opus, 'opus100')
path_gnome = os.path.join(path_opus, 'gnome')
path_ubuntu = os.path.join(path_opus, 'ubuntu')
path_wikimatrix = os.path.join(path_opus, 'wikimatrix')
path_kde4 = os.path.join(path_opus, 'kde4')
path_tanzil = os.path.join(path_opus, 'tanzil')
path_ted2020 = os.path.join(path_opus, 'ted2020')

### The paths for the Modi and related datasources
path_pib = os.path.join(path_scratch, 'pib-v1.3')
path_pmi = os.path.join(path_scratch, 'pmi-v1')
path_mkb = os.path.join(path_scratch, 'mkb-v0')

### Path for the Indo WordNet corpus
path_iwn = os.path.join(path_scratch, 'indo-wordnet-v0.2')

### The paths for the Miscellaneour resources
path_misc = os.path.join(path_scratch, 'misc')
path_wikititles_misc = os.path.join(path_misc, 'wikititles-temp')
path_alt = os.path.join(path_misc, 'alt-corpus')
path_ufal = os.path.join(path_misc, 'ufal-en-ta')
path_odi_en = os.path.join(path_misc, 'odi-en-v2.0')
path_en_urdu = os.path.join(path_misc, 'en-ur-charles')
path_wiki_turk = os.path.join(path_misc, 'wiki-turk')
path_iitb = os.path.join(path_misc, 'iitb')
path_bible_uedin = os.path.join(path_misc, 'bible-uedin')

### A list of all the dataset paths
datapath_list = [path_jw300, path_subtitles, path_opus100, path_gnome, path_ubuntu, path_wikimatrix, path_kde4, path_tanzil, path_ted2020, path_pib, path_pmi, path_mkb, path_iwn, \
                path_wikititles_misc, path_alt, path_ufal, path_odi_en, path_en_urdu, path_wiki_turk, path_iitb, path_bible_uedin]

### Path of the final dataset
path_indic_parallel = os.path.join(path_scratch, 'indic_parallel')
path_indic_dataset = os.path.join(path_indic_parallel, 'train_data')
path_indic_test = os.path.join(path_indic_parallel, 'test_data')
path_indic_dev = os.path.join(path_indic_parallel, 'dev_data')

### Different tasks to be carried out
### Note: Base dataset means that the files in the dataset are taken as they are i.e without any cleaning
get_base_stats = 'get_base_stats'           # Get the stats of all the base datasets present
clean_base_data = 'clean_base_data'         # Clean the training data present in the base datasets
get_clean_stats = 'get_clean_stats'         # Get the stats of the files after having the dataset cleaned
merge_clean_data = 'merge_cleaned_data'     # Merge the cleaned data for the different pairs as the actual data

### The different file names to be considered
base_train_name = 'overall'                 # The name of the training data of the base datasets (eg overall.hi in en-hi corpus)
clean_train_name = 'overall_clean'          # The name of the cleaned training data corresponding to the datasets
merge_train_name = 'train'                  # The name of the training data of the overall dataset
saved_base_stats = 'base_stats.json'        # The name of the file where the stats for the base datasets will be stored
saved_clean_stats = 'clean_stats.json'      # The name of the file where the stats for the cleaned datasets will be stored
saved_merge_stats = 'merge_stats.json'      # The name of the file where the stats for the overall merged data will be stored
repeated_lines_check = 'repeated_lines.txt' # The name of the file that contains the indices of occurence for every pair in the requested dataset (see check_rep.py)

########################################################################################################################################################################################################################################################
### This does not consist of the details for the addition of dataset for Sanskrit.