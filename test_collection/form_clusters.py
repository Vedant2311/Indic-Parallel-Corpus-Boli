import os
import operator
import configuration as config

# Creating a Global list that consists of all the dataset names
datapath_list_global = config.datapath_list
dataset_name_list = []
for path in datapath_list_global:
    dataset_name_list.append(path.split('/')[-1])

## Function that compare two datasets based on their occurences in the dataset list
## Output:
##      returns 0 if data_1 = data_2
##      returns 1 if data_1 > data_2
##      returns -1 if data_1 < data_2
def compare_datasets(data_1, data_2):
    datapath_list = dataset_name_list

    if datapath_list.index(data_1) == datapath_list.index(data_2):
        return 0
    elif datapath_list.index(data_1) > datapath_list.index(data_2):
        return 1
    else:
        return -1

## Function that reads the files from the Given source (English) and Target (Given Language) paths
## And returns the list of the tuples sorted according to the English texts
def initialise_dataset(path_source, path_target, dataset):
    with open(path_source,'r') as f1:
        lines_source = f1.readlines()
    with open(path_target,'r') as f2:
        lines_target = f2.readlines()

    dataset_list = []
    for (source, target) in zip(lines_source, lines_target):
        dataset_list.append((source,target,dataset))
    
    # Sorting the tuples according to the first element Only i.e the English texts
    # Note that the sequence with respect to the other tuple elements will not be changed
    # Thus, the English texts will be sorted here and the datasets will be in the same order as earlier
    # USING 'sorted(dataset_list)' would be modifying the sequence relative to the other keys as well
    dataset_list = sorted(dataset_list,key = lambda x: x[0])
    return dataset_list

## Function that Initialises the common cluster according to given input language
## Note that these tuples are being formed with respect to the pairs with English
def initialise_cluser(lang, print_val):
    cluster_list = []
    if lang > 'en':
        str_pair = 'en' + '-' + lang
    else:
        str_pair = lang + '-' + 'en'
    
    # Can add specific datasets to be checked here
    datapath_list = config.datapath_list
    for path in datapath_list:
        dataset = path.split('/')[-1]
        path_pair = os.path.join(path, str_pair)

        # Proceed if the Dataset directory exsists for the corresponding pair
        if os.path.exists(path_pair):
            # The source has to be English, as will be needed in 'initialise_dataset' function
            # Note that we are reading the data from the cleaned files of these datasets
            path_source = os.path.join(path_pair, config.clean_train_name + '.' + 'en')
            path_target = os.path.join(path_pair, config.clean_train_name + '.' + lang)

            # Proceed further only if all the specified files and directories exist
            if os.path.exists(path_source) and os.path.exists(path_target):
                temp_list = initialise_dataset(path_source, path_target, dataset)
                cluster_list = cluster_list + (temp_list)
            
    if print_val:
        print('Test cluster Initialised with the languages of ' + 'en ' + 'and ' + lang)
        print('The order of the Elements stored is: ' + 'en' + '->' + lang) 
        print('The size of the cluster is: ' + str(len(cluster_list)))
    return cluster_list

## Function that gives the stats corresponding to each dataset source in the cluster formed
def get_dataset_stats(test_cluster):
    dataset_tuples = []
    current_dataset = test_cluster[0][-1]
    current_count=0
    for i in range(len(test_cluster)):
        if test_cluster[i][-1] == current_dataset:
            current_count = current_count+1
        else:
            dataset_tuples.append((current_dataset, current_count))
            current_dataset = test_cluster[i][-1]
            current_count=1
    dataset_tuples.append((current_dataset, current_count))
    return dataset_tuples

## Print the stats of the dataset tuples in a tab seperated manner
def print_dataset_stats(dataset_tuples):
    for (dataset,count) in dataset_tuples:
        print(dataset + ':\t' + str(count))

## Function that saves the Language cluster in a file
def save_cluster(test_cluster):
    path_test_cluster = config.path_test_cluster
    path_test_cluster_file = os.path.join(path_test_cluster, config.saved_test_cluster)
    with open(path_test_cluster_file,'w') as f:
        for tup in test_cluster:
            str_save = tup[-1] + '\t'
            for i in range(len(tup)-1):
                str_save = str_save + tup[i].replace('\n','') + '\t'
            str_save = str_save + '\n'
            f.write(str_save)

## Function that performs a one-step addition of a new language to the cluster
def one_step_addition(previous_cluster, lang, print_val):
    # Get the Data between the given language and English
    lang_data = initialise_cluser(lang, False)

    # Initialise the variables needed in the searching here
    new_cluster = []
    previous_counter = 0
    lang_counter = 0

    # Loop through these lists and compare the data according to the clusters
    while (previous_counter < len(previous_cluster)) and (lang_counter < len(lang_data)):
        prev_tuple = previous_cluster[previous_counter]
        lang_tuple = lang_data[lang_counter]

        # Getting the English text and the dataset for these two tuples
        prev_english, lang_english = prev_tuple[0], lang_tuple[0]
        prev_dataset, lang_dataset = prev_tuple[-1], lang_tuple[-1]

        # Comparing the two datasets and moving ahead to the English texts only if they're equal
        datasets_comparison = compare_datasets(prev_dataset, lang_dataset)
        if datasets_comparison > 0:
            lang_counter = lang_counter+1
        elif datasets_comparison < 0:
            previous_counter = previous_counter+1
        else:
            ## Add to the new cluster if the English texts of the same dataset match
            if prev_english == lang_english:
                # The previous language texts present in the previous cluster, in their order
                prev_langs = prev_tuple[1:-1]

                # Adding the new language text to the previous cluster, maintaining the data of the previous cluster
                # The new language text will be appended at the end of the previous list of language texts
                # Thus if it was (en,ta) earlier and we add 'te', then it will be (en,ta,te)
                new_tuple = (prev_english,) + prev_langs + lang_tuple[1:-1] + (prev_dataset,)
                new_cluster.append(new_tuple)

                # Increasing the counters one step further
                previous_counter = previous_counter+1
                lang_counter = lang_counter+1
            
            ## Add the language counter by one step if it is smaller than the current previous cluster English
            elif prev_english > lang_english:
                lang_counter = lang_counter+1
            
            ## Otherwise, increase the counter for the previous cluster
            else:
                previous_counter = previous_counter+1

    # Returning the previous cluster along with printing some statements
    if print_val:
        print('New test cluster formed with addition of: ' + lang)
        print('The size of the cluster is: ' + str(len(new_cluster)))
    return new_cluster

### The main function that performs the required steps
### The given situation has five languages in the cluster: En, Hi, Bn, Ta, Ml
def main():
    ## Initialising the Cluster with Hindi language
    print('##############################################################################')
    print('Initialising the Test cluster for Hi:')
    test_cluster = initialise_cluser('hi',True)
    print()

    ## Getting the dataset stats of the above formed cluster
    print('##############################################################################')
    print('Getting the Dataset stats for the above formed cluster:')
    print_dataset_stats(get_dataset_stats(test_cluster))
    print()

    ## Getting a One step addition, Adding Bangla
    print('##############################################################################')
    print('Getting a one step addition of Bn on the top of the previous cluster:')
    test_cluster = one_step_addition(test_cluster,'bn',True)
    print()

    ## Getting the dataset stats of the above formed cluster
    print('##############################################################################')
    print('Getting the Dataset stats for the above formed cluster:')
    print_dataset_stats(get_dataset_stats(test_cluster))
    print()

    ## Getting a One step addition, adding Tamil
    print('##############################################################################')
    print('Getting a one step addition of Ta on the top of the previous cluster:')
    test_cluster = one_step_addition(test_cluster,'ta',True)
    print()

    ## Getting the dataset stats of the above formed cluster
    print('##############################################################################')
    print('Getting the Dataset stats for the above formed cluster:')
    print_dataset_stats(get_dataset_stats(test_cluster))
    print()

    ## Getting a One step addition, adding Malyalam
    print('##############################################################################')
    print('Getting a one step addition of Ml on the top of the previous cluster:')
    test_cluster = one_step_addition(test_cluster,'ml',True)
    print()

    ## Getting the dataset stats of the above formed cluster
    print('##############################################################################')
    print('Getting the Dataset stats for the above formed cluster:')
    print_dataset_stats(get_dataset_stats(test_cluster))
    print()

    ## Saving the cluster in the required file as mentioned in the configuration file
    save_cluster(test_cluster)

if __name__ == '__main__':
    main()