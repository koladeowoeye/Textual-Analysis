from __future__ import division
import  os
import re

class Sentistrenght:
    @staticmethod
    def run_analysis(indir, outdir):

        usedWords = ['programs','party','security','officer','investor','education','crime','teritory','news','defuse','counterterrorism','safeguard','nacotics','ridiculist','news','twitter','death','jobs','victims','police','war','email','isis','sport','death','war','security','attacks','enemy','terrorism','violence','jihad','islamic','abortion']

        print('===============================================================================================')
        print("Program Starting...............................................................................")
        for words in usedWords:
            regex = r'(?i)((?:\S+\s+){0,5})\b'+words+r'\b((?:\S+\s+){0,5})'

            for subdir, dirs, files in os.walk(indir): #loop sub directory in a folder
                for file in files: #loop files in a folder
                #print os.path.join(subdir, file)
                     filepath = subdir + os.sep + file       #get the file path

                     # encoding giving error so i removed it and run with the default encoding
                     # content = open(filepath,'ru', encoding="utf-8")  #open a file read, universal,
                     content = open(filepath,'ru')           #open a file read, universal

                     print('Searching for word {}'.format(words))
                     print(filepath)
                     print('===============================================================================================')
                     for line in content:                    # loop through the content of the file
                         text1 = line.strip()
                         text1 = re.sub(r'[^\w]', ' ', text1)
                         text1 = text1.replace(" ", ", ")


                         matches = re.finditer(regex, text1.lower())
                         for matchNum, match in enumerate(matches):
                             matchNum = matchNum + 1
                             word = match.group().replace("," , " ").replace("  " , " ").replace("   " , " ")
                             # encoding giving error on, so i removed it
                             # text_file = open(outdir+words+".txt", "a",encoding="utf-8")
                             text_file = open(outdir+words+".txt", "a")
                             text_file.write(file +"-"+word+"\n\n")


