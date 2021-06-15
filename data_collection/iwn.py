import os
# Make sure that the configuration.py is in the same folder as this file
import configuration 

## Creating a dictionary to map different langauges to their ids in the csv file
index= dict()
index['as'] = 0
index['bn'] = 1
index['gu'] = 3
index['hi'] = 4
index['kn'] = 5
index['ml'] = 8
index['mni'] = 10
index['mr'] = 9
index['or'] = 12
index['pa'] = 13
index['ta'] = 15
index['te'] = 16
index['ur'] = 17
langs = ['as', 'bn', 'gu', 'hi', 'kn', 'ml', 'mni', 'mr', 'or', 'pa', 'ta', 'te', 'ur']

## Download the IndoWordNet dataset (v0.2) and using the above indices, convert the 'example.csv' and 'gloss.csv' files into text files for the above languages
## Thus, for the language Hindi, a textfile should be created with the name: total.hi. The size is 112016 lines (after removing the head rows in both the csv files)

### The following code deals with converting the above files into many bilingual datasets. 
# Taking the path of the iwn dataset from the configuration file
path_iwn = configuration.path_iwn
os.chdir(path_iwn)
cwd = os.getcwd()

# Going through each paiir {lang1}-{lang2} and getting 'proper' sentence alignment for them
for i in range(len(langs)-1):
    for j in range(i+1, len(langs)):

        src = langs[i]
        tgt = langs[j]
        print(src,tgt)

        path_pair = os.path.join(path_iwn, src + '-' + tgt)
        os.makedirs(path_pair, exist_ok = True)

        fsrc = open('total.' + src)
        lines_src = fsrc.readlines()
        fsrc.close()

        ftgt = open('total.' + tgt)
        lines_tgt = ftgt.readlines()
        ftgt.close()

        tup_list = []
        for (source,target) in zip(lines_src, lines_tgt):
            if (not source.strip()) or (not target.strip()):
                # Has empty lines. So ignore them
                continue
            else:
                tup_list.append((source,target))
        
        os.chdir(path_pair)

        f1 = open('overall.' + src, 'w')        
        f2 = open('overall.' + tgt, 'w')

        for tup in tup_list:
            text1 = tup[0]
            text2 = tup[1]

            f1.write(text1)
            f2.write(text2)
        
        f1.close()
        f2.close()

        os.chdir(cwd)
