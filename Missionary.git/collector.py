#I added some shit!
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup


# In[2]:

import StringIO


# In[21]:

import argparse


# In[ ]:

import shutil


# In[4]:

parser = argparse.ArgumentParser()


# In[11]:

parser.add_argument('books',nargs='+',  help='List the files to collect')


# In[16]:

parser.add_argument( 'output',type=str,  help='name the collected book')


# In[18]:

args = parser.parse_args()


# In[19]:




# In[20]:

with open(args.output, "w+") as outfile:
    for bname in args.books:
        with open(bname, "r") as readfile:
            outfile.write(readfile.read() + "\n\n")
            



# In[ ]:



