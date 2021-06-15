import os
import configuration as config

# Getting the important parameters
langs = config.langs
path_pmi = config.path_pmi
path_indic_dev = config.path_indic_dev
path_indic_test = config.path_indic_test

# Function that reads pairwise data from the PMI dataset
def read_from_pmi(src,tgt):
    if tgt > src:
        str_pair = src + '-' + tgt
    else:
        str_pair = tgt + '-' + src
    path_pair = os.path.join(path_pmi, str_pair)

    lines_src, lines_tgt  = [], []
    if os.path.exists(os.path.join(path_pair,config.pmi_data_name + '.' + src)) and os.path.exists(os.path.join(path_pair,config.pmi_data_name + '.' + tgt)):
        with open(os.path.join(path_pair,config.pmi_data_name + '.' + src)) as f:
            lines_src = f.readlines()
        
        with open(os.path.join(path_pair,config.pmi_data_name + '.' + tgt)) as f:
            lines_tgt = f.readlines()

    if len(lines_src)==0:
        return []
    
    lines_pair = []    
    for (src,tgt) in zip(lines_src, lines_tgt):
        lines_pair.append((src, tgt))
    
    return lines_pair

# Function that scans the WAT dataset and removes the test and dev occurences from the PMI data
def remove_from_wat(lines_pmi_data, src, tgt, type_in):
    if type_in=='dev':
        dir_name = config.path_indic_dev
        f_name = config.wat_dev_name
    else:
        dir_name = config.path_indic_test
        f_name = config.wat_test_name

    src_path = os.path.join(dir_name, f_name + '.' + src)
    tgt_path = os.path.join(dir_name, f_name + '.' + tgt)

    if os.path.exists(src_path) and os.path.exists(tgt_path):
        with open(src_path) as f:
            src_lines = f.readlines()
        with open(tgt_path) as f:
            tgt_lines = f.readlines()

        lines_pmi_new = []
        for (src,tgt) in lines_pmi_data:
            if src in src_lines or tgt in tgt_lines:
                continue
            else:
                lines_pmi_new.append((src,tgt))

        return lines_pmi_new

# Function that removes test/dev occurences from the PMI data
def remove_from_pmi(src,tgt):    
    if tgt > src:
        str_pair = src + '-' + tgt
    else:
        str_pair = tgt + '-' + src
    path_pair = os.path.join(path_pmi, str_pair)

    # Return if there is no such path in the PMI dataset
    if not os.path.exists(path_pair):
        return

    # Reading the original data as present in the PMI dataset
    lines_pmi_data = read_from_pmi(src,tgt)

    # Removing overlaps with the Dev data first
    lines_pmi_data = remove_from_wat(lines_pmi_data, src, tgt, 'dev')

    # Removing overlaps with the Test data
    lines_pmi_data = remove_from_wat(lines_pmi_data, src, tgt, 'test')

    # Saving the data into the appropriate files
    f_src = open(os.path.join(path_pair, config.base_train_name + '.' + src),'w')
    f_tgt = open(os.path.join(path_pair, config.base_train_name + '.' + tgt),'w')
    for (src, tgt) in lines_pmi_data:
        f_src.write(src)
        f_tgt.write(tgt)
    f_src.close()
    f_tgt.close()

# Going through all the language pairs and removing the test-dev-train alignment
if __name__ == '__main__':
    for i in range(len(langs)-1):
        for j in range(i+1, len(langs)):
            print(langs[i],langs[j])
            remove_from_pmi(langs[i], langs[j])