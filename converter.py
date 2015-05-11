
# coding: utf-8

# In[1]:

#Gloabl variables and import declarations
from bs4 import BeautifulSoup
import StringIO
import argparse
import os
import glob
path = "c:\\users\\netmier\\documents\\book conversion\\"

parser = argparse.ArgumentParser()
parser.add_argument('book_name',type = str,  help ='the file name of the book to be converted') #the prepared book file
parser.add_argument('TOC_name', type = str, help = 'the file name of the TOC to be generated') #the name of the generated TOC
parser.add_argument('NCX_name', type = str, help = 'the file name of the NCX to be generated') #the name of the generated NCX
args = parser.parse_args()
userBookName = args.book_name
theBook = open(args.book_name)
soup = BeautifulSoup(theBook) #the main soup, made from the prepared book file


finalToc = open(args.TOC_name, "w")
finalNcx = open(args.NCX_name, "w")
tempToc = StringIO.StringIO()
tempNcx = StringIO.StringIO()


# In[ ]:

print(args.book_name) #I just like being reminded of what you're converting


# In[ ]:

#TOC and NCX templates
TocTemplate = BeautifulSoup("""<html>
		<head>
		<title>Table Of Contents</title>
		<link rel='stylesheet' type='text/css' href='c:\\users\\netmier\\documents\\books in progress\\python scripts\\BLStyleSheet.css'>
		</head>
		<body>
		<ul>
		</ul>
		</body>
		</html>""")
NcxTemplate = BeautifulSoup("""
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE ncx PUBLIC '-//NISO/DTD ncx 2005-1/EN' 'http://www.daisy.org/z3986/2005/ncx-2005-1.dtd'>
<ncx xmlsn='http://www.daisy.org z3986/2005/ncx/' version='2005-1' xml:lang='en-US'>
<head>
<meta content='uid' name='dtb:uid'/>
<meta content='1' name='dtb:depth'/>
<meta content='0' name='dtb:totalPageCount'/>
<meta content='0' name='dtb:maxPageNumber'/>
</head>
<docTitle><text></text></docTitle>
<docAuthor><text></text></docAuthor>
<navMap>
</navMap>
</ncx>""", "xml")


# In[ ]:

#TOC Generator
NcxTemplate.docTitle.string = soup.title.string #puts the title in
NcxTemplate.docAuthor.string = soup.h3.string #puts the author in. I don't like this method, but it works. 
for tag in reversed(soup.find_all("a", attrs={"id":True})):
    #tempId = userBookName + "#" + (tag["id"])
    TocTemplate.body.ul.insert(0,TocTemplate.new_tag("a"))
    TocTemplate.a["href"] = userBookName + '#' + (tag["id"])
    TocTemplate.a.string = tag.string
    NcxTemplate.navMap.insert(0, NcxTemplate.new_tag("navpoint", id = tag["id"], playorder = 0))
    NcxTemplate.navMap.navpoint.insert(2,NcxTemplate.new_tag("content", src = userBookName + '#' + (tag["id"])))
    NcxTemplate.navMap.navpoint.insert(0, NcxTemplate.new_tag("navLabel"))
    NcxTemplate.navLabel.string = tag.string
    NcxTemplate.navLabel.string.wrap(NcxTemplate.new_tag("text"))
    

for tag in TocTemplate.find_all("a"): #this wraps the tags with <li> tags.
        tag.wrap(TocTemplate.new_tag("li")) 


# In[ ]:

counter = 3 #counter for the play order 

for tag in NcxTemplate.find_all("navpoint"): #and this finishes off the NCX by incrementing the playorder value
    tag["playorder"] = counter
    counter = counter + 1   


# In[ ]:

print >> finalToc, TocTemplate.prettify()
print >> finalNcx, NcxTemplate.prettify()

finalToc.close()
finalNcx.close()

