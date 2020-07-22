from __future__ import division
from collections import Counter
import nltk, re, pprint,os
import re

#regex = r"(?i)((?:\S+\s+){0,3})\bSmartphone\b((?:\S+\s+){0,3})"

#test_str = "Nokia Lumia 930 Smartphone, Display 5 pollici, Fotocamera 20 MP, 2GB RAM, Processore Quad-Core 2,2GHz, Memoria 32GB, Windows Phone 8.1, Bianco [Germania]"

#matches = re.finditer(regex, test_str)

#for matchNum, match in enumerate(matches):
#    matchNum = matchNum + 1
    
#    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
#    for groupNum in range(0, len(match.groups())):
#        groupNum = groupNum + 1
        
#        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

indir = '//ds.strath.ac.uk/hdrive/21/kqb16121/cis/windows/Desktop/ICCRC'
#usedWords = ['war','terrorist','weapon','bomb','jihad','attacker','violence','gun','News','ridiculist','program','party','Officer','security','police','nato','safeguard','council','support','cnn','celebrity','photo','peace','islam','america']
#wordfound = []
#word_frequencies = []
#print('===============================================================================================')
i = 0
for subdir, dirs, files in os.walk(indir): #loop sub directory in a folder
    for file in files: #loop files in a folder
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file       #get the file path
        #content = open(filepath,'rU',encoding="utf-8")           #open a file read, Universal 
        #print(filepath)                         #display the full path of the file
        i += 1
        os.rename(filepath,subdir + os.sep+"webapge{}.txt".format(i))
#        print('===============================================================================================')
#        for line in content:                    # loop throught the content of the file
#            text1 = line.strip()                # get the string content of the file
#            noofwords = nltk.word_tokenize(text1.lower())       #conver content to list of words
#             #print(nltk.pos_tag(noofwords))
#            print('words found')         
#            print(noofwords)                            #Display the list of words
#            cnt = 0
#            for word in noofwords:                      #loop through the list of words to get frequently used words
#               if word  in usedWords:                   #if a word match frequently used word
#                   wordfound += [word]                  # create a list containing the frequencies from each files
            
#            for occ in wordfound:                       # loop through the frequency list 
#                print('{} position at {}'.format(occ,noofwords.index(occ))) #position of keyword in the content of the file
#                #noofwords[noofwords.index(occ)] = "###" + occ + "###"       #mark the keyword in the content
#                print('{} five words after at {}'.format(occ,noofwords[21:5]))
#            #    if occ not in word_frequencies:         #get distinct word from the frequency list
#            #       word_frequencies +=[occ]             #create another list containing distinct word from the frequency list
#            #for Z in word_frequencies:                  #loop through the distinct frequency list to get the no of occurence from the frequency list
#            #    print('{} occurs {}'.format(Z,wordfound.count(Z)))   #print the word and the frequency
#            #    print('Words after {}'.format(noofwords[noofwords.index(occ):6]))
#        print("New Words")
#        print( " ".join(str(x) for x in noofwords))
#        #text_file = open(indir+"output/"+file, "w")
#        #text_file.write(" ".join(str(x) for x in noofwords))
#        #text_file.close()
#        wordfound = []
#        word_frequencies = []
#        content.close()
       
