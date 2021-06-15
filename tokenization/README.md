# Indic Parallel Corpus

## Tokenization
This directory includes all the scripts that were used by us to perform **Normalisation** and **Tokenization** of the raw data that was collected by us. This step will be needed before making use of the data to train any model. For all the languages other than English(en), Manipuri(mni), and Urdu(ur): We make use of the **Indic NLP library** to perform the tokenisation and Normalization steps. These steps are performed for English using **Moses** tokeniser. 


<!-- instructions to run moses at https://stackoverflow.com/a/63388920/10055814 -->
## Moses Tokenizer
In Boli Corpus Moses is used for English tokenization. The moses [repo](https://github.com/moses-smt/mosesdecoder.git) is cloned at */home/cse/btech/cs1170339/mosesdecoder*

```
tokenizer=/scratch/cse/btech/cs1170339/indic_parallel/tokenization/mosesdecoder/scripts/tokenizer/tokenizer.perl
$tokenizer -l <lang> < <input_file> > <output_file>
```

A summary of the different scripts used is as follows:
- process_all.sh : Runs tokenization/normalisation for all files. Note specific to file structure used
- norm_tok.sh : Script running Normalisation and tokenization using IndicNLP 

Note that for Manipuri(mni), we couldn't get any resources for Normalisation and tokenisation over the raw text. In the case of Urdu(ur), we made use of the IndicNLP library that performs tokenisation of the urdu texts, but not normalisation.