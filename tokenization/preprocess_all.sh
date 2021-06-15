#!/bin/bash
# declare an array called array and define 3 values
# Note: Manipuri (ISO - mni) is not included in the IndicNLP normalization and tokenization
lang_dirs=( as bn en gu hi kn ml mni mr or pa sa ta te ur )
lang_codes=( as bn en gu hi kn ml mP mr or pa sa ta te ur )

main_directory=/scratch/cse/btech/cs1170339/indic_parallel/train_data

tokenizer=/scratch/cse/btech/cs1170339/indic_parallel/tokenization/mosesdecoder/scripts/tokenizer/tokenizer.perl
tokenizer_urdu=/scratch/cse/btech/cs1170339/indic_parallel/tokenization/tokenize_urdu.py

prefix=train

cd $main_directory

len=${#lang_dirs[@]}

for (( i=0; i<$len; i++ ))
do 
    for (( j=i+1; j<$len; j++ ))
    do 
        dir="${lang_dirs[$i]}-${lang_dirs[$j]}"
        echo ${dir}
        cd $main_directory/$dir

        if [ ${lang_codes[$i]} = "en" ] 
        then
            echo "Running Moses for English"
            ${tokenizer} -l en < ${prefix}.${lang_dirs[$i]} > ${prefix}.tok.${lang_dirs[$i]}
        else
            echo "Starting for $main_directory/$dir/${prefix}.${lang_dirs[$i]}"
            $indicNLP ${prefix}.${lang_dirs[$i]} ${prefix}.tok.${lang_dirs[$i]} ${lang_codes[$i]}
        fi

        if [ ${lang_codes[$j]} = "en" ] 
        then
            echo "Running Moses for English"
            ${tokenizer} -l en < ${prefix}.${lang_dirs[$j]} > ${prefix}.tok.${lang_dirs[$j]}
        else
            echo "Starting for $main_directory/$dir/${prefix}.${lang_dirs[$j]}"
            $indicNLP ${prefix}.${lang_dirs[$j]} ${prefix}.tok.${lang_dirs[$j]} ${lang_codes[$j]}
        fi
        
    done
    cd $main_directory
done

# Run the script to get Urdu Tokenization (Note that IndicNLP does not include normalisation for Urdu yet)
python ${tokenize_urdu}