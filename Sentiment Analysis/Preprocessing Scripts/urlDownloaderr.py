import bs4 as bs
import urllib.request
import re, pprint,os

indir = "C:/Users/USER/Desktop/webtxt"
i = 0
for subdir, dirs, files in os.walk(indir): #loop sub directory in a folder
	for file in files: #loop files in a folder 	
		filepath = subdir + "/" + file       #get the file path
		
		folderpath = os.path.splitext(filepath)[0];
		if not os.path.exists(folderpath):
			os.mkdir(folderpath)
		
		content = open(filepath,'r',encoding="utf-8")           #open a file read, Universal 
		#print(filepath)                         #display the full path of the file
		for line in content:                     # loop throught the content of the file
			text1 = line.strip() 
			i += 1
			try:
				sauce = urllib.request.urlopen(text1).read()
				soup = bs.BeautifulSoup(sauce,'lxml')
				for mul_tags in soup.find_all(['p','h1','h3']):
					print("Downloading webpage " + line)	
					print(folderpath)
					if not mul_tags.string == None : 
						text_file = open(folderpath + "/" + "webapge{}.txt".format(i), "a",encoding="utf-8")
						text_file.write(mul_tags.string)
						text_file.close()
						print("Done downloading " + line)
			except Exception as e:
				print ("Error occured downloading webpage " + line)
				
			
			