from __future__ import division
from collections import Counter
import re, pprint,os
import re
indir = '//ds.strath.ac.uk/hdrive/21/kqb16121/cis/windows/Desktop/ICCRC'
outdir = '//ds.strath.ac.uk/hdrive/21/kqb16121/cis/windows/Desktop/output/'
#usedWords = ['dead','war','prison','violence','terrorist','security','enemies','jihad','islamic','sahaba','territory','saint','civilian','counterterrorism','kingdom','taxes','science','president','weapon','cnn','isis','police','fighters','soldiers','politics','militants','twitter','memorandum','narcostic']
usedWords = ['islam','allah','muslim','jihad','news','islamic','war','prophet','rights','government','law','programs','activism','trade','policy','security','education','affairs','counterterrorism','trial','obama','reports','politics','facebook','twitter','victims','bombing','media','iraq','office','terroritory','safequards','officer','council','ridiculist','syria','death','police','battle','CNN']
wordfound = []
output = ""
print('===============================================================================================')
print("Program Starting...............................................................................")
for words in usedWords:
    regex = r'(?i)((?:\S+\s+){0,5})\b'+words+r'\b((?:\S+\s+){0,5})'
 
    for subdir, dirs, files in os.walk(indir): #loop sub directory in a folder
        for file in files: #loop files in a folder
        #print os.path.join(subdir, file)
             filepath = subdir + os.sep + file       #get the file path
             
             content = open(filepath,'rU',encoding="utf-8")           #open a file read, Universal 
             print('Searching for word {}'.format(words))
             print(filepath) 
             print('===============================================================================================')
             for line in content:                    # loop through the content of the file
                 text1 = line.strip()  
                 text1 = re.sub(r'[^\w]', ' ', text1)
                 text1 = text1.replace(" ", ", ") 
                   
                 #print(text1+"\n")
                 
                 #print(text1)     
                 matches = re.finditer(regex, text1.lower())
                 for matchNum, match in enumerate(matches):
                     matchNum = matchNum + 1
                     word = match.group().replace("," , " ").replace("  " , " ").replace("   " , " ")
                     #wordfound.append(word)
                     #print('{} {}'.format(filename,word))
                     text_file = open(outdir+words+".txt", "a",encoding="utf-8")
                     text_file.write(file +"-"+word+"\n")
    
    #             for wrd in wordfound:
    #                output += file + " " +wrd+"\n"   
    #text_file = open(outdir+words+".txt", "a",encoding="utf-8")
    #text_file.write(output)
    #         #text_file.close()
    #wordfound = []
    #output = ""
        
 
