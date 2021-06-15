import os
import re
# Make sure that the configuration.py is in the same folder as this file
import configuration as config

## Get the codes for all the languages to be considered
lang_codes = ['sa','en','hi','ml','ta','kn','te','bn','gu','el','he','la','fr','de','ru','it','zh']
lang_codes.sort()

## Mapping the language codes in the obtained file to the actual language codes
def map_codes():
    code_dict = dict()

    code_dict['Chi'] = 'zh'
    code_dict['Ita'] = 'it'
    code_dict['Rus'] = 'ru'
    code_dict['Ger'] = 'de'
    code_dict['Fre'] = 'fr'
    code_dict['Lat'] = 'la'
    code_dict['Heb'] = 'he'
    code_dict['Gre'] = 'el'

    code_dict['Guj'] = 'gu'
    code_dict['Ben'] = 'bn'
    code_dict['Tel'] = 'te'
    code_dict['Kan'] = 'kn'
    code_dict['Tam'] = 'ta'
    code_dict['Mal'] = 'ml'
    code_dict['Hin'] = 'hi'
    code_dict['Eng'] = 'en'

    return code_dict

## Creating the global mapping dictionary from the above function
mapping_dict = map_codes()

## Create a dictionary corresponding to the list of lines for all the languages
def create_lang_lines():
    code_dict = dict()

    code_dict['zh'] = []
    code_dict['it'] = []
    code_dict['ru'] = []
    code_dict['de'] = []
    code_dict['fr'] = []
    code_dict['la'] = []
    code_dict['he'] = []
    code_dict['el'] = []

    code_dict['gu'] = []
    code_dict['bn'] = []
    code_dict['te'] = []
    code_dict['kn'] = []
    code_dict['ta'] = []
    code_dict['ml'] = []
    code_dict['hi'] = []
    code_dict['en'] = []
    code_dict['sa'] = []

    return code_dict

## Create a dictionary corresponding to the Temporary lines to be saved for all languages
def create_lang_strs():
    code_dict = dict()

    code_dict['zh'] = '\n'
    code_dict['it'] = '\n'
    code_dict['ru'] = '\n'
    code_dict['de'] = '\n'
    code_dict['fr'] = '\n'
    code_dict['la'] = '\n'
    code_dict['he'] = '\n'
    code_dict['el'] = '\n'

    code_dict['gu'] = '\n'
    code_dict['bn'] = '\n'
    code_dict['te'] = '\n'
    code_dict['kn'] = '\n'
    code_dict['ta'] = '\n'
    code_dict['ml'] = '\n'
    code_dict['hi'] = '\n'
    code_dict['en'] = '\n'
    code_dict['sa'] = '\n'

    return code_dict

## Parsing a code from the given tab seperated part of the input sentence
def parse_code(sent):
    
    # Check if it is corresponding to Sanskrit. Their texts do not have a language code in [] 
    if sent[0]!='[':
        return 'sa'
    
    # Remove the special characters and make use of the Mapping dictionary
    else:
        result = re.sub(r'[^a-zA-Z]', '', sent)
        return mapping_dict[result]

## Converting a given input file into the required format for the corresponding language
def parse_sent(lang_strs_dict, sent):

    # The given sentence is Tab-seperated
    tabs_seperated = sent.split('\t')

    # Getting the line to be saved
    line_output = tabs_seperated[-1]

    # Getting the language code as well from the sentence
    code = parse_code(tabs_seperated[0])

    # Replacing the sentence in the temporary language strings dictionary 
    lang_strs_dict[code] = line_output

## Parsing the obtained files to get the individual pairs
def parse_chapter(file_path, lang_lines_dict):

    # Getting the lines in the file
    with open(file_path) as f:
        file_lines = f.readlines()
    
    # Getting the dictionary corresponding to the temporary strings for all the languages
    lang_strs_dict = create_lang_strs()

    ##  Looping through the read input file
    for i in range(len(file_lines)):

        # Breaking the loop if the first character of the line is '#'
        if file_lines[i][0]=='#':

            # Adding the lines here and then getting out of the loop 
            for lang in lang_codes:
                lang_lines_dict[lang].append(lang_strs_dict[lang])

            return

        # If the given line is sanskrit then add the saved temporary sentences to the langage lines dictionary
        # And Empty the temporary lines for each language by replacing them all by empty lines
        elif file_lines[i][0]!='[':

            # Add those lines only if we are not looking at the first line of the data
            if i!=0:
                for lang in lang_codes:
                    lang_lines_dict[lang].append(lang_strs_dict[lang])
            
            # Clearing the data once added to the language lines
            lang_strs_dict = create_lang_strs()

            # Adding the line for Sanskrit here
            parse_sent(lang_strs_dict, file_lines[i])
        
        # As the given line is not in sanskrit, we simply add the lines to the Temporary strings dictionary
        else:
            parse_sent(lang_strs_dict, file_lines[i])
    
## Parsing the Entire Bible and storing it in the corresponding files
def parse_bible():

    # Creating a Dictionary for the list of all the lines present for all the languages
    lang_lines_dict = create_lang_lines()

    # Getting the list of the books present and the path of the Sanskrit-Bible directory
    bible_books = config.bible_books
    path_sanskrit_bible = config.path_sanskrit_bible

    # Going through all the Chapters of all the Books present in the Bible here
    for book in bible_books:
        path_book = os.path.join(path_sanskrit_bible, book)
        for chapter in os.listdir(path_book):
            print(book, chapter)
            file_path = os.path.join(path_book, chapter)
            parse_chapter(file_path, lang_lines_dict)
    
    # Saving the lines in the corresponding files
    for lang in lang_codes:
        lang_lines = lang_lines_dict[lang]
        save_path = os.path.join(path_sanskrit_bible, config.language_bible_name + '.' + lang)
        with open(save_path,'w') as f:
            for line in lang_lines:
                f.write(line.strip().replace('\n','') + '\n')

## The function to create the directory structure as required by the library
def create_directories():
    path_sanskrit_bible = config.path_sanskrit_bible
    for i in range(len(lang_codes)-1):
        for j in range(i+1, len(lang_codes)):
            src = lang_codes[i]
            tgt = lang_codes[j]
            print(src,tgt)

            path_pair = os.path.join(path_sanskrit_bible, src + '-' + tgt)
            os.makedirs(path_pair, exist_ok = True)

            # Copying the corresponding files
            cmd_src = 'cp ' + os.path.join(path_sanskrit_bible, config.language_bible_name + '.' + src) + ' ' + path_pair
            cmd_tgt = 'cp ' + os.path.join(path_sanskrit_bible, config.language_bible_name + '.' + tgt) + ' ' + path_pair
            os.system(cmd_src)
            os.system(cmd_tgt)

            # Renaming the copied files
            rename_src = 'mv ' + os.path.join(path_pair, config.language_bible_name + '.' + src) + ' ' + os.path.join(path_pair, config.base_train_name + '.' + src)
            rename_tgt = 'mv ' + os.path.join(path_pair, config.language_bible_name + '.' + tgt) + ' ' + os.path.join(path_pair, config.base_train_name + '.' + tgt)
            os.system(rename_src)
            os.system(rename_tgt)


## The main function that would be executed
def main():
    
    ## First of all, parse the obtained text files and get the lines for each languages in their separate files
    # parse_bible()

    ## After that, we create the directory structure are required by the Library
    create_directories()

if __name__== '__main__':
    main()
