# Indic Parallel Corpus
## Data Collection: OPUS tools
This directory consists of the same configuration file as present in the parent directoy. The files here can be used to get the parallely aligned sentences by making use of the OPUS API giving more flexibility than simply downloading parallel files from the website (as done in **ubuntu.py** in the parent directory). This has a benefit that it can make use of the sentence alignment score, available from the Xml files obtained, to get a quantatively shorter but qualitiatively better dataset. And this *sentence alignment score* would be directly related to the relative quality of the parallel pairs. Thus, a higher value of sentence alignment would indicate that those sentences are closely related to each other and thus can be termed as 'good' translations.

But this has a limitation that for many OPUS datasets like Ubuntu, GNOME, WikiMatrix etc, the xml files obtained using the OPUS tools are corrupt. And hence it was not used while curating the Parallel corpus here. But it can be used in case of the OPUS datasets like **JW300**.

### Making use of the system to get the Jw300 corpus for all 14 languages
First of all, we need to get the jw300 zip files from the OPUS servers. This can be done by running the following command:
```sh
$ python3 get_opus_all.py jw300
```

Now, after this we would be needed to get the files containing all the correspondences between sentences of any two languages. We can either get the sentence alignments for all the parallel text present in the corpus, or we can directly make use of a threshold based on the *sentence alignment score* to get parallel pairs having their *sentence alignment score* above that threshold. Say, we want to have a threshold of 0.6, then we can run the following command:
```sh
# Generates overall.txt (contains all the alignments) and t_0.6.txt (contains alignments above the alignment value of 0.6)
$ python3 create_opus_all.py jw300 0.6
```

Now, we would needed to parse the 'overall.txt' and 't_0.6.txt' files created from step-1 and divides them into individual files for both the involved langauges in those files. We also need to ensure that a one-one mapping is present between the sentences of the two languages, ignoring any many-one, one-many, many-many etc. mappings that might be present earlier. So for that, the following command could be applied:
```sh
$ python3 gen_opus_parallel_all.py jw300 0.6
```

### Making use of the system to get the Jw300 corpus for a language pair
Suppose you wish to get the Jw300 corpus for Gujarati(gu) and Hindi(hi). Then the entire pipeline can be followed as below
```sh
# Gets the zip files from the OPUS servers
$ python3 get_opus_pair.py gu hi jw300

# Creates the parallel alignment for all the sentences 
# The output file is overall.txt
$ python3 create_opus_pair.py gu hi jw300 overall.txt

# Creates the parallel alignment above the alignment threshold of 0.6
# The output file is t_0.6.txt
$ python3 create_opus_pair.py gu hi jw300 t_0.6.txt

# Divides the 'overall.txt' file into individual langauge files
$ python3 gen_opus_parallel_pair.py gu hi jw300 overall.txt 

# Divides the 't_0.6.txt' file into individual langauge files
$ python3 gen_opus_parallel_pair.py gu hi jw300 t_0.6.txt 
```