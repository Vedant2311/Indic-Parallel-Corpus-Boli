inFile=$1
outFile=$2
language=$3

echo "Starting Normalization"
python /scratch/cse/btech/cs1170339/indic_parallel/tokenization/normalize.py $inFile $1.temp $language

INFILE_LINES="$(wc -l < ${inFile})"
TEMPFILE_LINES="$(wc -l < ${inFile}.temp)"
Tokenize_Stat=1

if (( INFILE_LINES = TEMPFILE_LINES ))
then
    echo "Normalization Done for Language ${language}"
else
    echo "Error in Normalization for language ${language}"
    echo "Skipping Normalization."
    Tokenize_Stat=0
fi


if (( Tokenize_Stat == 1 ))
then
    echo "Starting Tokenization"
    python /scratch/cse/btech/cs1170339/indic_parallel/tokenization/tokenize.py ${inFile}.temp ${outFile} ${language}
else
    echo "Starting Tokenization from source"
    python /scratch/cse/btech/cs1170339/indic_parallel/tokenization/tokenize.py ${inFile} ${outFile} ${language}
fi

echo "Deleting Temp Files."
rm ${inFile}.temp

OUTFILE_LINES="$(wc -l < ${outFile})"
if (( INFILE_LINES == OUTFILE_LINES ))
then
    echo "Done."
else
    echo "Number of Lines don't match for Tokensiation output and Input File"
    echo "Deleting ${outFile}"
    rm ${outFile}
fi