import os
# Make sure that the configuration.py is in the same folder as this file
import configuration as config

## Get the repetitions present within the dataset by making use of a set datastructure
def use_set(src, tgt, pair_path):
    lines_src = []
    with open(os.path.join(pair_path,config.base_train_name + '.' + src)) as f:
        lines_src = f.readlines()

    lines_tgt = []
    with open(os.path.join(pair_path,config.base_train_name + '.' + tgt)) as f:
        lines_tgt = f.readlines()

    print('The earlier size was: ' + str(len(lines_src)))
    set_en = set()
    for (src,tgt) in zip(lines_src, lines_tgt):
        set_en.add((src,tgt))
    
    removed_rep_en = list(set_en)
    print('The final size is: ' + str(len(removed_rep_en)))

# A helper function to check if the tuple is present in the list or not
def check_tuple(tup, l):
    flag = False
    for x in l:
        if tup[0]==x[0] and tup[1]==x[1]:
            flag = True
            break
    
    return flag

# A helper function to return the tuple found in the list
def return_tuple(tup, l):
    tupV = ('','',[])
    for x in l:
        if tup[0]==x[0] and tup[1]==x[1]:
            tupV = x
            break
    return tupV

## Get the repetitions within the dataset by making use of a list. Naive approach
## Writes the detailed information about the repetitions present in the file 'repeated_lines.txt' (see configuration file)
## Caution: This code has not been optimised yet and so it will run very slow for medium resource datasets
def use_list(src, tgt, pair_path):
    lines_src = []
    with open(os.path.join(pair_path,config.base_train_name + '.' + src)) as f:
        lines_src = f.readlines()

    lines_tgt = []
    with open(os.path.join(pair_path,config.base_train_name + '.' + tgt)) as f:
        lines_tgt = f.readlines()

    print('The earlier size was: ' + str(len(lines_src)))

    f_out = open(os.path.join(pair_path,config.repeated_lines_check),'w')

    # Storing all the index related information in a list
    final_list = []
    for i in range(len(lines_src)):
        src = lines_src[i]
        tgt = lines_tgt[i]

        if not check_tuple((src,tgt), final_list):
            final_list.append((src,tgt,[i]))
        else:
            # Remove the previous version of the element from the list
            temp = return_tuple((src,tgt), final_list)
            final_list.remove(temp)

            # Add the current list index in the tuple
            temp[2].append(i)
            final_list.append(temp)
    
    print('The final size is: ' + str(len(final_list)))

    ## Writing the above computed pair information in the file that was opened by this program
    ## Line Format: <src_line> \t <tgt_line> \t <occurence_indices> \n
    for (src,tgt,list_ind) in final_list:
        list2str = ''
        for ind in list_ind:
            list2str = list2str + str(ind) + ', '
 
        f_out.write(src.replace('\n','') + '\t' + tgt.replace('\n','') + '\t' + 'Indices: ' + list2str + '\n')

    f_out.close()

## Define the main function that governs the above function calls
def main(strin, src, tgt, dataset):

    datapath_list = config.datapath_list

    ## Check if the dataset is present and if it is then return it's exact path
    datapath = ''
    for path in datapath_list:
        if path.split('/')[-1] == dataset:
            datapath = path
            break
    
    if datapath=='':
        print('Improper dataset name given. Check if it is consistent with the configuration file')
    else:
        if src < tgt:
            pair_path = os.path.join(datapath, src + '-' + tgt)
        else:
            pair_path = os.path.join(datapath, tgt + '-' + src)

        if not os.path.exists(pair_path):
            print('The path ' + pair_path + ' does not exist. Set proper paths')
        else:
            if strin=='set':
                use_set(src, tgt, pair_path)
            elif strin=='list':
                use_list(src, tgt, pair_path)
            else:
                print('The first argument was improper. Choose either (\'set\' or \'list\')')

if __name__ == '__main__':
    ## The arguments for getting the repetitions in the GNOME corpus for Hi-En
    ## Note: The 'dataset' name much match with what's present in the configuration file
    main('list', 'en', 'hi', 'gnome')