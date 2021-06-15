# Indic Parallel Corpus

## Data scraping
As listed in the **configuration.py** file, all the datasets that someone would want to add to the existing corpus should go in the **addition** directory, with the same directory structure being followed for the datasets used in the original Indic Parallel corpus. The directory structure is also properly described in the README section for **data_collection**. Go through that once. 

The files in this directory are corresponding to the codes written to add the corpora for Sanskrit that were scraped by us and added to the earlier version of this dataset which consisted of 14 languages, which excluded sanskrit. Note that this earlier version of the dataset was never released, the directories other than **addition** correspond to this older version of the dataset. The purpose of seperating the Sanskrit corpus from the remaining ones is to create a well-defined open source platform for the addition of any further dataset and to serve as a tutorial of how to do so. 

For the Sanskrit-Bible dataset, because of the lack of proper Html structure via which the data could be automatically extracted; we had to manually get the parallel sentence aligned texts corresponding to the different chapters of the different books from the [Sanskrit-Bible website](http://www.sanskritbible.in/readmode.html). The script **sanskrit-bible.py** would seperate them into the individual language files. We consider the Indic languages of Sanskrit(sa), English(en), Hindi(hi), Malyalam(ml), Tamil(ta), Kannada(kn), Telugu(te), Bengali(bn), Gujarati(gu). We further consider other foreign languages as well here during this extraction like Greek(el), Hebrew(he), Latin(la), French(fr), German(de), Russian(ru), Italian(it), and Chinese(zh).

### Issues encountered while scraping
During this scraping, We also witnessed some issues corresponding to the text online. Some examples in the IIT-K Ramayana website can be found as below:
1. For the shloka 2.114.15; the sanskrit text was 'वृक्णभूमितलां निम्नां वृक्णपात्रैस्समावृताम्। उपयुक्तोदकां भग्नां प्रपां निपतितामिव।।2.114.15।।', while the corresponding English text given on the website was 'a dale.'
2. For the shlokas 3.20.23, 3.39.19, 3.40.17; there are 'Missing' text on the website
3. For the shlokas 4.18.48, 4.54.19; there was 'In progress' text on the website

Some other similar issues we noticed for this dataset were:
1. For the shloka 3.5.43; Improper text was present on the web, where the English sentence contained the sanskrit punctuation of '।।'
2. For the shloka 3.11.93; No sarga completion text was there like in the other cases
3. In the fourth Kanda, for many texts there was no '।।' in the beginning (like 4.6.8।। instead of ।।4.6.8।।)

We also found some issues regarding the translation of the text present. For example, in the Ramcharitmanas dataset; for the sanskrit text of 'सचिव सभीत बिभीषन जाकें। बिजय बिभूति कहाँ जग ताकें॥सुनि खल बचन दूत रिस बाढ़ी। समय बिचारि पत्रिका काढ़ी॥4॥' has the translation of 'सुनि खल बचन दूत रिस बाढ़ी। समय बिचारि पत्रिका काढ़ी॥4॥' in Hindi; which is completely wrong. 

These issues were manually found in the dataset obtained by us and correspondingly removed/rectified. There were issues regarding inconsistent Html tags as well and those were discarded too.
