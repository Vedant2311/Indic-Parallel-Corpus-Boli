### Just a random program doing random debugging!
import os
import configuration as config

# Important paths
path_indic_test = config.path_indic_test
path_indic_dev = config.path_indic_dev
path_indic_train = config.path_indic_dataset

# The pair of English-Gujarati as considered in README
src = 'en'
tgt = 'pa'
if tgt < src:
    src, tgt = tgt, src
print('The pair is: ', src, tgt)
str_pair = src + '-' + tgt

### Getting the train data for the required comparison
# For having the train data from the overall dataset
path_train = os.path.join(path_indic_train, str_pair)
with open(os.path.join(path_train, config.merge_train_name + '.' + src)) as f:
    src_train = f.readlines()
with open(os.path.join(path_train, config.merge_train_name + '.' + tgt)) as f:
    tgt_train = f.readlines()    
print('Size of the train data is:', len(src_train))
# # For having the train data corresponding to any particular dataset
# path_train = os.path.join(config.path_pmi, str_pair)
# with open(os.path.join(path_train, config.pmi_data_name + '.' + src)) as f:
#     src_train = f.readlines()
# with open(os.path.join(path_train, config.pmi_data_name + '.' + tgt)) as f:
#     tgt_train = f.readlines()

# Getting the test and dev data
with open(os.path.join(path_indic_dev, config.wat_dev_name + '.' + src)) as f:
    src_dev = f.readlines()
with open(os.path.join(path_indic_dev, config.wat_dev_name + '.' + tgt)) as f:
    tgt_dev = f.readlines()

with open(os.path.join(path_indic_test, config.wat_test_name + '.' + src)) as f:
    src_test = f.readlines()
with open(os.path.join(path_indic_test, config.wat_test_name + '.' + tgt)) as f:
    tgt_test = f.readlines()

# Creating the pairs for the langauges
pairs_train, pairs_test, pairs_dev = [],[],[]
for (src_d, tgt_d) in zip(src_dev, tgt_dev):
    pairs_dev.append((src_d,tgt_d))

for (src_te, tgt_te) in zip(src_test, tgt_test):
    pairs_test.append((src_te, tgt_te))
pairs_dev = set(pairs_dev)
pairs_test = set(pairs_test)

# Checking for alignments
print('total dev and test is:', len(pairs_dev) + len(pairs_test))
count = 0
for (src, tgt) in zip(src_train, tgt_train):
    if (src,tgt) in pairs_test or (src,tgt) in pairs_dev:
        count+=1
print('aligned sentences:', count)