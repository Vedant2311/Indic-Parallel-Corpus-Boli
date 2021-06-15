# Indic Parallel Corpus

## Introduction
This directory consists the stats about all the datasets that have been compiled by us. Moreover, this also contains the different scripts that have been used by us. The different datasets that have been used by as are mentioned in the **configuration.py** file. The scripts for downloading these individual datasets and the information about the format in which we organize the data can be found in the directory **data_collection**. Kindly refer to that before proceeding ahead. The further content assumes that the dataset is downloaded and organized in the required format. For adding some new dataset to this repository, check the directory **data_scraping** where we provide the scripts that were used to curate the parallel data for Sanskrit, which was later added to the earlier indic_parallel dataset consisting of 14 languages. In the **tokenization** section, the scripts corresponding to performing tokenization and normalization of the data can be found.

## Data cleaning
We analysed more than 20 major public dataset sources available for the Indic languages in a thorough detail and came across different short-comings that these resources possessed that would account to misrepresentation of the actual dataset size along with containing a lot of noisy text that might detoriorate the performance of the model that would be trained using the data.

In order to get rid of such issues, we perform cleaning of the dataset at multiple levels in order to combat the issues currently present in some of the most popular training data resources for Indic languages. For all the examples discussed ahead, the index of the first parallel pair is taken as 0. Note that the stats for the different cases that are explained ahead were obtained in an independent and isolated manner with respect to other levels of cleaning. While in the final setup, we perform all the levels of cleaning on the data along with some trivial preprocessing which leads to even further reduction of the total data. These steps would be performed in the script **perform_task.py**.

### Remove the pairs where atleast one side is Empty
If we consider the IITB En-Hi parallel corpus version 3.0 (total size: 1,609,682 parallel sentences), then upon inspection it was found that the dataset contained 6102 pairs where atleast one side of Hi or En was empty. Some examples where this error has occured in the dataset are given below:

1. For example, in the pairs occuring at indices 1070551, 1070577, 1070597 -> Both the source and target side sentences were actually empty!
2. If we look at the index 1080963, the source sentence (En) is "my tasks have become cluttered. This tab bar..." while the target sentence (Hi) is Empty. The same thing occurs for the index of 1080967 as well.
3. For the index 10809196, the source side (En) is Empty, while the target sentence (Hi) is "अब हम सवाल #48 का हल निकालेंगे". Similar thing is also present at the index of 1130790.

Errors like this could be hard to identify, especially if the the data is passed to some preprocessing step which requires the data to be non-empty (for eg. Stanza pipeline, version 1.1.1). Thus, we perform a simple RegEx based cleaning to remove such empty pairs from each individual data file present.

### Remove the pairs where the both the source and target are exactly the same
If there is a parallel corpus where a sentence at any side of the data is written in a different language then those such sentences would be detoriorating the quality of the corpus. That same issue would also arise if the texts at both the source and target side of the data are just some special characters without consisting of any words.

Upon careful inspection; it was observed that in the case of many parallel pairs in such corpora, the same text written in English was present in both the sides of the data. Similary, we found that there were sentences where the same special character sequence would be present on both the sides. And removal of such pairs would be extremely trivial and it would not require being dependant on some language identification model(s). Thus this was the other cleaning that we perform on the data. 

In the case of IITB parallel corpus (version 3.0), it was found that 3474 pairs were having the same sentence present on both the sides of the data. Some examples for the same can be found as follows:
1. The text "% d:% 02d" was found on both the Hi and En side of the data at the index of 1916. This corresponds to the case of *Special character removal*
2. The text "Cachegrind" was found on both the Hi and En side of the data at the index of 7417. This corresponds to the case of *Foriegn Lanuage removal*

If we have a look at the JW300 parallel corpus for Mr-Pa (total sentences: 2,86,868), it was found that 1086 pairs among those were such that both the sides of the data were the same text written in English. Some examples of those are as follows:

1. The text "© 2014 Watch Tower Bible and Tract Society of Pennsylvania ." was found on the Mr as well as the Pa side of the data for the pair occurring at the index of 234021. The same text is also found at the indices of 234910, 235801 etc. 
2. Similarly, the text "© 2015 Watch Tower Bible and Tract Society of Pennsylvania" was found on both the sides for the pairs occurring at indices of 245173, 245364, 246148 etc.

### Removing repetitions within and across the datasets
Since we are compiling data from different data sources with a few sources being related to each other, it is very necessary to ensure that we check for the pairs to be distinct before merging them into our final dataset. We also checked for repetitions present within the dataset itself and upon some experimentations, we came across unexpected results. 

On checking for sentence pair repetitions and discarding repeated pairs, the IITB corpus (version 3.0) got reduced from a size of 1,609,682 parallel sentences to 1,392,168 parallel sentences; a loss of more than 0.2 million sentence pairs. When we further checked for this repetition within the constituent datasources present in this corpus, we observed that on removing such repeated cases; the sentences obtained from the GNOME (opus) corpus were reduced from an initial size of 1,45,706 segments to a size of 29,147 sentences, accounting for a loss of 0.1 million pairs itself. The examples of such errors present in the GNOME En-Hi corpus are as follows:

1. The pair "Event monitor" & "घटना मानिटर" was repeated 8 times at the indices: 19, 212, 412, 613, 819, 1021, 1221, 1423.
2. The pair "Relative position" & "सापेक्ष स्थिति" was repeated 8 times at the indices: 43, 236, 439, 637, 847, 1048, 1248, 1450.

Thus, we consider such repetitions and handle them while cleaning the data as well as while combining the data into the final Indic Parallel dataset. 

### Creating the Train-Test-Dev split
As described in the section **Test Collection**, we make use of the WAT2021 task splits for Dev and Test data for performing the required evaluations necessary for benchmarking our data. So while merging all the cleaned data sources into the final train dataset; we also remove the sentence pair those were either present in the Test or the Dev data, along with removing repeated sentences across the datasets as discussed in the previous subsection.
