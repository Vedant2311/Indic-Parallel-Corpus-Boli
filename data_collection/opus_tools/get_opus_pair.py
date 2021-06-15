#### Usage: $ python3 get_opus_parallel_pair.py hi gu jw300
import os
import sys
import time
# Make sure that the configuration.py is in the same folder as this file
import configuration as config

## Taking inputs from command line
### src -> Source language Id (eg hi)
### tgt -> Target language Id (eg gu)
### base -> Name of the OPUS corpus directory (eg jw300)
src = sys.argv[1]
tgt = sys.argv[2]
base = sys.argv[3]

### Saving the current directory of execution somewhere
cwd = os.getcwd()

### We look locally in the sub-directories for the OPUS cwd
path_opus = config.path_opus
dir_path = (os.path.join(path_opus,base))
creation_path = os.path.join(dir_path, src+'-'+tgt) 

### Creating the corresponding Directory and changing cwd
os.makedirs(creation_path, exist_ok = True) 
os.chdir(creation_path)

### Run the opus_get command and download the files
## Checking for src-tgt file
if base=='jw300' or base=='gnome':
	cmd = 'wget https://object.pouta.csc.fi/OPUS-'+base.upper()+'/v1/xml/'+src+'-'+tgt+'.xml.gz' + ' --no-check-certificate'	
	os.system(cmd)

	## Checking for tgt-src file
	cmd = 'wget https://object.pouta.csc.fi/OPUS-'+base.upper()+'/v1/xml/'+tgt+'-'+src+'.xml.gz' + ' --no-check-certificate'
	os.system(cmd)

	cmd = 'wget https://object.pouta.csc.fi/OPUS-'+base.upper()+'/v1/xml/'+src+'.zip' + ' --no-check-certificate'
	os.system(cmd)

	cmd = 'wget https://object.pouta.csc.fi/OPUS-'+base.upper()+'/v1/xml/'+tgt+'.zip' + ' --no-check-certificate'
	os.system(cmd)

elif base=='subtitles':
        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'OpenSubtitles'+'/v2018/xml/'+src+'-'+tgt+'.xml.gz' + ' --no-check-certificate'
        os.system(cmd)

        ## Checking for tgt-src file
        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'OpenSubtitles'+'/v2018/xml/'+tgt+'-'+src+'.xml.gz' + ' --no-check-certificate'
        os.system(cmd)

	#### Getting the alt files too
        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'OpenSubtitles'+'/v2018/xml/'+src+'-'+tgt+'.alt.xml.gz' + ' --no-check-certificate'
        os.system(cmd)

        ## Checking for tgt-src file
        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'OpenSubtitles'+'/v2018/xml/'+tgt+'-'+src+'.alt.xml.gz' + ' --no-check-certificate'
        os.system(cmd)

	### Getting the Source and Target files
        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'OpenSubtitles'+'/v2018/xml/'+src+'.zip' + ' --no-check-certificate'
        os.system(cmd)

        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'OpenSubtitles'+'/v2018/xml/'+tgt+'.zip' + ' --no-check-certificate'
        os.system(cmd)

elif base=='ubuntu':
        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'Ubuntu'+'/v14.10/xml/'+src+'-'+tgt+'.xml.gz' + ' --no-check-certificate'
        os.system(cmd)

        ## Checking for tgt-src file
        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'Ubuntu'+'/v14.10/xml/'+tgt+'-'+src+'.xml.gz' + ' --no-check-certificate'
        os.system(cmd)

        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'Ubuntu'+'/v14.10/xml/'+src+'.zip' + ' --no-check-certificate'
        os.system(cmd)

        cmd = 'wget https://object.pouta.csc.fi/OPUS-'+'Ubuntu'+'/v14.10/xml/'+tgt+'.zip' + ' --no-check-certificate'
        os.system(cmd)

### Renaming the downloaded files in the right format
if base=='jw300' or base=='gnome':
	cmd = 'mv ' + src+'-'+tgt+'.xml.gz ' + base.upper()+'_latest_xml_'+src+'-'+tgt+'.xml.gz'
	os.system(cmd)

	cmd = 'mv '+src+'.zip ' + base.upper()+'_latest_xml_'+src+'.zip'
	os.system(cmd)

	cmd = 'mv '+tgt+'.zip ' + base.upper()+'_latest_xml_'+tgt+'.zip'
	os.system(cmd)

elif base=='subtitles':
        cmd = 'mv ' + src+'-'+tgt+'.xml.gz ' + 'OpenSubtitles'+'_latest_xml_'+src+'-'+tgt+'.xml.gz'
        os.system(cmd)

	cmd = 'mv ' + src+'-'+tgt+'.alt.xml.gz ' + 'OpenSubtitles'+'_latest_xml_'+src+'-'+tgt+'.alt.xml.gz'
        os.system(cmd)

        cmd = 'mv '+src+'.zip ' + 'OpenSubtitles'+'_latest_xml_'+src+'.zip'
        os.system(cmd)

        cmd = 'mv '+tgt+'.zip ' + 'OpenSubtitles'+'_latest_xml_'+tgt+'.zip'
        os.system(cmd)

elif base=='ubuntu':
        cmd = 'mv ' + src+'-'+tgt+'.xml.gz ' + 'Ubuntu'+'_latest_xml_'+src+'-'+tgt+'.xml.gz'
        os.system(cmd)

        cmd = 'mv '+src+'.zip ' + 'Ubuntu'+'_latest_xml_'+src+'.zip'
        os.system(cmd)

        cmd = 'mv '+tgt+'.zip ' + 'Ubuntu'+'_latest_xml_'+tgt+'.zip'
        os.system(cmd)

### Coming back to the original directory
os.chdir(cwd)
