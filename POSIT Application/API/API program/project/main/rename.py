from __future__ import division
import  os

class Renamefiles:
    @staticmethod
    def run(indir):
        i = 0
        for subdir, dirs, files in os.walk(indir): #loop sub directory in a folder
            for file in files: #loop files in a folder
                filepath = subdir + os.sep + file       #get the file path
                i += 1
                os.rename(filepath, subdir + os.sep+"webapge{}.txt".format(i))



