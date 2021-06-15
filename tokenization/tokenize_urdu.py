## This file is meant to specifically tokenize urdu files because of the errors in the previous pipeline
import os
lang_dirs=( 'as','bn', 'en', 'gu', 'hi', 'kn', 'ml', 'mni', 'mr', 'or', 'pa', 'sa', 'ta', 'te', 'ur' )
main_directory = '/scratch/cse/btech/cs1170339/indic_parallel/train_data'

for i in range(len(lang_dirs)-1):
    for j in range(i+1,len(lang_dirs)):
        src = lang_dirs[i]
        tgt = lang_dirs[j]

        if src=='ur' or tgt=='ur':
            print(src + '-' + tgt)
            base_path = os.path.join(main_directory, src + '-' + tgt)
            urdu_file_raw = os.path.join(base_path, 'train.ur')
            urdu_file_tok = os.path.join(base_path, 'train.tok.ur')
            os.system('python /scratch/cse/btech/cs1170339/indic_parallel/tokenization/tokenize.py ' + urdu_file_raw + ' ' +  urdu_file_tok + ' ur')

            # Read the two files and see if they have the same size
            with open(urdu_file_raw) as f:
                lines_raw = f.readlines()
            with open(urdu_file_tok) as f:
                lines_tok = f.readlines()
            
            if not len(lines_raw) == len(lines_tok):
                print('Improper sizes of the two files created: ' + str(len(lines_raw)) + '(raw)' + ' ' + str(len(lines_tok)) + '(tok')
                os.system('rm ' + urdu_file_tok)
