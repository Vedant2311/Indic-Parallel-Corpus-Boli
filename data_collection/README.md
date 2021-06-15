# Indic Parallel corpus

## Data collection
As listed in the **configuration.py** file (this **configuration** only includes details for the 14 Indian languages, other than Sanskrit), we incorporate different seperate datasets in our work and create a large parallel corpus across many Indian languages. In this directory, you can find some sample codes used for the collection and basic initial cleaning of many datasets. The filename corresponds to the corresponding dataset itself. 

Note that only non-trivial data-collection files are included. For eg, the dataset of PMI (version-1) can simply be downloaded from [here](data.statmt.org/pmindia/). For getting the parallel sentences from the OPUS corpus using the OPUS-API, the scripts present in the **opus_tools** can be used. But because of the limitations of these tools for many OPUS datasets (explainations in the **opus_tools** directory), we simply download the parallely-aligned sentences available from the OPUS websites using a script like **ubuntu.py**.

Note that once you download any individual dataset then you'll be needed to have the files organized in the below format in order for the further codes of dataset combination and cleaning to be able to run. Assume that there is a dataset named dataOne which has sentences in languages English(en), Gujarati(gu), and Hindi(hi). Then the directory structure should be:
```
dataOne
├── en-gu
│   ├── overall.en
│   └── overall.gu
├── en-hi
│   ├── overall.en
│   └── overall.hi
└── gu-hi
    ├── overall.gu
    └── overall.hi
```
(Notice how the folders {lang1}-{lang2} are named such that {lang1} and {lang2} are in a lexicographic order. All the parallel training data will be present in the overall.{lang} file for the langauge {lang} in any directory involving {lang}. These files within a folder need to be sentence aligned, having one sentence in each line)

## Data Analysis
As stated in the **Data cleaning** section, we perform different levels of cleaning of the dataset based on the observations that were made by us regarding the dataset available. The script for checking repetitions within a dataset can be found as **check_rep.py**. Note that we have not included the programs for the other analysis that were carried out by us. 