# Indic Parallel Corpus

## Test collection
This directory deals with getting the test set for the Multilingual dataset obtained by us. 

### Getting clusters for the same shared test data
The initial plans were to create a new test dataset by making use of the pairs from the train set only such that the different data sources present in it get a fair share in the test data obtained, as per their numbers in the overall train set. But rather than getting that done for all the <sup>n</sup>C<sub>2</sub> pairs of languages, we planned to form different clusters of languages such that they share a common multilingual test dataset. The reason being that once we would obtain test data from the training data, we should also get some manual annotations and corrections done on those translations and getting that done for all the <sup>n</sup>C<sub>2</sub> pairs was not feasible. 

This above functionality of getting clusters of languages and obtained their shared translations can be found in the script of **form_clusters.py**. The process is explained in a very lucid manner in the program itself. Here, we perform pivoting w.r.t the English sentences in order to get the shared sentences across all the different languages. An example cluster corresponding to the languages of English (en), Hindi (hi), Bangla (bn), Tamil (ta), and Malyalam (ml); along with the stats of this cluster; can be found in the **test_data/test_cluster** directory. 

But upon thoroughly examining these sentences, it was found that the sentences that would be obtained from the majority of the sources are not that good enough to get their way into a sophisticated multilingual test dataset. A couple of example sentences in all the languages of the cluster discussed above, and for all the data sources present in the cluster; can be found in the file **test_sample.txt** in the **test_data/test_cluster** directory. This sample was manually selected from the cluster generated from the dataset and it is clearly visible that most of these sources would not make a good test/dev dataset. 

### Getting the dev and test data of Indic WAT 2021 task
The constraints we faced in the above situation led us to consider these three paths, from which one can be selected to move ahead.
1. Making use of the test/dev splits present in the IITB En-Hi dataset. This would require us to get manual annotations for all the sentences there into all the different languages that are considered by us, amounting to a parallel multilingual test/dev dataset.  
2. Making use of the test data obtained from the (Mann Ki Baat dataset)[http://preon.iiit.ac.in/~jerin/bhasha/]. This contains seperate test data for all the <sup>n</sup>C<sub>2</sub> pairs.
3. Making use of the multilingual test/dev splits provided in the [MultiIndicMT: An Indic Language Multilingual Task](http://lotus.kuee.kyoto-u.ac.jp/WAT/indic-multilingual/index.html) of WAT2021. This would have n test data files (for n languages) that would be used for all the <sup>n</sup>C<sub>2</sub> pairs.

So, here we decided to move ahead with the third step above i.e making use of the same test/dev as provided in the WAT2021 task. Their test/dev data is obtained from the PMI dataset, so we would need to remove those sentences from the train first before proceeding ahead. Also, the languages considered by them are lesser than the languages that are present in this dataset. And so for that, we would parse through the PMI dataset and get as many translated texts for the additional languages (having the previously present 11 languages as the pivot) as possible. And for the remaining sentences, we would have them manually annotated. 

The above steps can be found in the script **wat_test.py**. We also make sure that whatever data is present in the test and dev data is not repeated in the pair-wise train data for the PMI source. For that, we will run the script of **remove_test_pmi.py**. But simply doing this wasn't enough as we found discrpancies between the expected size of the train split obtained v/s the actual size obtained. On further debugging and exploration of the datasets, it was obtained that some of these pairs of WAT-Dev and WAT-Test split are also present in the PIB and MKB dataset. The script used for that was **check_overlaps.py**

By running the above mentioed script, we obtain the following overlap stats in the case of English(En)-Gujarati(gu). Here, *Overlap* signifies the sum total of dev + test data sentences for En-Gu pair that would be overlapping with the source mentioned in the column. Note that, in the table below; the *PMI dataset* refers to the PMI train split after the removal of WAT test and dev data (total size: 3390 pairs):
| With considered overall train | With PMI dataset | With MKB dataset | With PIB dataset| 
| ------------- | ------------- | ------------- | ------------- |
| 1128 pairs  | 0 pairs  | 321 pairs  | 806 pairs  |

Thus owing to the issue discussed above, we removed the WAT dev and test data seperately from the overall train that was obtained by us, during the merging step of the dataset curation (More details in the **Introduction** section)