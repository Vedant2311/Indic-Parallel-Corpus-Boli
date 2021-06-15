import os
import configuration as config
import json
langs = config.langs

## Gets the length of the source and target files
def get_length(path_source, path_target):
    with open(path_source,'r') as f1:
        lines_source = f1.readlines()
    with open(path_target,'r') as f2:
        lines_target = f2.readlines()
    total_source = len(lines_source)
    total_target = len(lines_target)

    # Checking if the lengths are equal or not
    if total_source == total_target:
        return total_source
    else:
        return -1

## Removes the data where any side of the parallel data is empty
def remove_empty(lines_source, lines_target):
    out_source = []
    out_target = []

    for (source, target) in zip(lines_source, lines_target):
        if (not(source.strip())) or (not(target.strip())):
            continue
        else:
            ## Stripping the sentences too in order to remove extra spaces in any case
            out_source.append(source.strip() + '\n')
            out_target.append(target.strip() + '\n')
    
    # Reverting the correction if it is buggy!
    if len(out_source)==len(out_target):
        return out_source, out_target
    else:
        return lines_source, lines_target

## Removes the data where both the source and target are either the same English sentence or some special characters
def remove_english(lines_source, lines_target):
    out_source = []
    out_target = []

    for (source, target) in zip(lines_source, lines_target):
        if source == target:
            continue
        else:
            ## Stripping the sentences too in order to remove extra spaces in any case
            out_source.append(source.strip() + '\n')
            out_target.append(target.strip() + '\n')
    
    # Reverting the correction if it is buggy!
    if len(out_source)==len(out_target):
        return out_source, out_target
    else:
        return lines_source, lines_target

## Removes repetitions within a particular source
def remove_repetitions(lines_source, lines_target):

    # Adding tuples of sentences to a set
    tup_set = set()
    for (source, target) in zip(lines_source, lines_target):
        tup_set.add((source,target))

    # Converting it to a list and dividing the sentences     
    tup_list = list(tup_set)
    out_source = []
    out_target = []

    for (source,target) in tup_list:
        ## Stripping the sentences too in order to remove extra spaces in any case
        out_source.append(source.strip() + '\n')
        out_target.append(target.strip() + '\n')
    
    # Reverting the correction if it is buggy!
    if len(out_source)==len(out_target):
        return out_source, out_target
    else:
        return lines_source, lines_target

### Cleans the base dataset at different levels
def clean_base(path_source, path_target, dest_source, dest_target):
    ## Note that here the lines that are extracted will also consist of '\n' in the end
    with open(path_source,'r') as f1:
        lines_source = f1.readlines()
    with open(path_target,'r') as f2:
        lines_target = f2.readlines()

    ## If the lengths of the two files are not equal, then just discard that entire dataset
    if len(lines_source)!=len(lines_target):
        lines_source, lines_target = [], []
    else:
        ## Removes the data where any side of the parallel data is empty
        lines_source, lines_target = remove_empty(lines_source, lines_target)

        ## Removes the data where both the source and target sentences are the same sentence (which is English). 
        ## Might be having some same special character on both the sides
        lines_source, lines_target = remove_english(lines_source, lines_target)

        ## Removes repetitions within the dataset
        lines_source, lines_target = remove_repetitions(lines_source, lines_target)

    ## Now writing the obtained lines in the destinations
    with open(dest_source, 'w') as f1:
        for source in lines_source:
            f1.write(source)
    with open(dest_target, 'w') as f2:
        for target in lines_target:
            f2.write(target)
    return

## Function to add the tuple of source-target in the set
def add_to_set(path_source, path_target, merge_set):
    # Note that here the lines that are extracted will also consist of '\n' in the end
    with open(path_source,'r') as f1:
        lines_source = f1.readlines()
    with open(path_target,'r') as f2:
        lines_target = f2.readlines()

    # Do not modify the set if the number of lines are not same for the dataset
    if len(lines_source)!=len(lines_target):
        return

    for (source,target) in zip(lines_source, lines_target):
        merge_set.add((source,target))

### Has all the required tasks for the dataset files
### path_source can either be the path of a source language file or it can be the path of the json file
def task(path_source, path_target, str_task, path_pair, merge_set):    

    ## Calculates the length of the files
    if str_task == config.get_base_stats or str_task == config.get_clean_stats:
        return get_length(path_source, path_target)
    
    ## Cleans the base dataset
    elif str_task == config.clean_base_data:

        ## Assumes that the files are properly passed
        src = path_source.split('.')[-1]
        tgt = path_target.split('.')[-1]

        ## Getting the destination files
        dest_source = os.path.join(path_pair, config.clean_train_name + '.' + src)
        dest_target = os.path.join(path_pair, config.clean_train_name + '.' + tgt)

        ## Checking if we are passing the proper name as the Input or not
        if dest_source==path_source or dest_target==path_target:
            print('Aborted: Attempted to overwrite the stored base data')
            return -1

        ## Call the functon that would clean the dataset files
        clean_base(path_source, path_target, dest_source, dest_target)
        return 0

    ## Merges the training data into one file
    elif str_task == config.merge_clean_data:
        add_to_set(path_source, path_target, merge_set)
        return 0


## Converts a list of tuples into a dictionary along with adding a total
def tuplist2json(tup_list):
    temp = dict()
    sumVal = 0
    for tup in tup_list:
        temp[tup[0]] = tup[1]
        sumVal = sumVal + int(tup[1])
    temp['total'] = sumVal
    return temp

## Parses all the available directories for a particular pair of langids
## Assumes the directory structure that we proposed earlier
def parsePair(src, tgt, str_task):
    datapath_list = config.datapath_list
    str_pair = src + '-' + tgt
    tup_list = []       # To be used to get the stats of the dataset
    merge_set = set()   # To be used to merge the training data

    for path in datapath_list:
        dataset = path.split('/')[-1]
        path_pair = os.path.join(path, str_pair)

        if os.path.exists(path_pair):

            # Getting the absolute paths of the input files to be read
            if str_task == config.get_base_stats or str_task == config.clean_base_data:
                path_source = os.path.join(path_pair, config.base_train_name + '.' + src)
                path_target = os.path.join(path_pair, config.base_train_name + '.' + tgt)

            elif str_task == config.get_clean_stats or str_task == config.merge_clean_data:
                path_source = os.path.join(path_pair, config.clean_train_name + '.' + src)
                path_target = os.path.join(path_pair, config.clean_train_name + '.' + tgt)

            # Proceed further only if all the specified files and directories exist
            if os.path.exists(path_source) and os.path.exists(path_target):
                val = task(path_source, path_target, str_task, path_pair, merge_set)

                if val!=-1 and (str_task == config.get_base_stats or str_task == config.get_clean_stats):
                    tup_list.append((dataset, val))
            
    # Writing the data tuples stored in the set to the final file
    if str_task == config.merge_clean_data:

        path_base = config.path_indic_dataset
        path_pair = os.path.join(path_base,str_pair)

        # Creating the particular folder in the Indic Parallel folder
        os.makedirs(path_pair,exist_ok = True)

        # Getting the destination of the files
        dest_source = os.path.join(path_pair, config.merge_train_name + '.' + src)
        dest_target = os.path.join(path_pair, config.merge_train_name + '.' + tgt)

        # Opening the files to be written
        f_source = open(dest_source, 'w')
        f_target = open(dest_target, 'w')

        # Converting the set into a list
        merge_set = list(merge_set)

        # Loading the test and dev data for removal from train
        path_indic_test = config.path_indic_test
        path_indic_dev = config.path_indic_dev

        with open(os.path.join(path_indic_dev, config.wat_dev_name + '.' + src)) as f:
            src_dev = f.readlines()
        with open(os.path.join(path_indic_dev, config.wat_dev_name + '.' + tgt)) as f:
            tgt_dev = f.readlines()

        with open(os.path.join(path_indic_test, config.wat_test_name + '.' + src)) as f:
            src_test = f.readlines()
        with open(os.path.join(path_indic_test, config.wat_test_name + '.' + tgt)) as f:
            tgt_test = f.readlines()

        # Creating set of tuples for the test and dev data
        pairs_test, pairs_dev = [],[]
        for (src_d, tgt_d) in zip(src_dev, tgt_dev):
            pairs_dev.append((src_d,tgt_d))
        for (src_t, tgt_t) in zip(src_test, tgt_test):
            pairs_test.append((src_t, tgt_t))
        pairs_dev = set(pairs_dev)
        pairs_test = set(pairs_test)

        # Removing test + dev from the merged data
        count = 0
        for (source, target) in merge_set:
            if (source,target) in pairs_dev or (source,target) in pairs_test:
                continue
            else:
                f_source.write(source)
                f_target.write(target)
                count+=1

        # Appending the total train (after the dev-test split) stats in the Json file        
        tup_list.append(('total',count))

        # Closing the open files
        f_source.close()
        f_target.close()

    return tup_list

## Defining the main function to do the task across all the pairs
def main(str_task):
    
    stat_dict = dict()
    for i in range(len(langs)-1):
        for j in range(i+1, len(langs)):

            # Print the on-going language
            print(langs[i], langs[j])

            # The task corresponding to getting the file stats
            if str_task==config.get_base_stats or str_task == config.get_clean_stats:
                stat_dict[langs[i] + '-' + langs[j]] = tuplist2json(parsePair(langs[i], langs[j], str_task))
            
            # The task corresponding to cleaning the training data
            elif str_task==config.clean_base_data:
                unusedTemp = parsePair(langs[i], langs[j], str_task)

            # The task corresponding to merge the cleaned training data. Also has the overall stats for the data
            elif str_task == config.merge_clean_data:
                stat_dict[langs[i] + '-' + langs[j]] = tuplist2json(parsePair(langs[i], langs[j], str_task))
            
    # Writing the computed stats in the corresponding files
    if str_task == config.get_base_stats:
        with open(config.saved_base_stats, 'w') as fp:
            json.dump(stat_dict, fp, indent=4)
    elif str_task == config.get_clean_stats:
        with open(config.saved_clean_stats, 'w') as fp:
            json.dump(stat_dict, fp, indent=4)
    elif str_task == config.merge_clean_data:
        with open(config.saved_merge_stats, 'w') as fp:
            json.dump(stat_dict, fp, indent=4)

    return 

if __name__ == '__main__':

    ## 0 -> Call this function to get the stats of the base dataset
    # print('Getting the stats of the base data')
    # main(config.get_base_stats)

    ## 1 -> Call this function to get the cleaned data
    # print('Cleanining the base data obtained by us')
    # main(config.clean_base_data)

    ## 2 -> Call this function to get the stats of the cleaned data (to be called only after the above step)
    # print('Getting the stats of the cleaned data')
    # main(config.get_clean_stats)

    ## 3 -> Call this function to merge all the dataset files along with taking the repetitions into account. Also reports the overall stats, and removes WAT test+dev
    print('Merging the overall data and getting the stats for that')
    main(config.merge_clean_data)