#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[2]:


req = requests.get("https://context.reverso.net/translation/spanish-english/tímido", headers={'User-Agent': 'Mozilla/5.0'})


# In[3]:


soup = BeautifulSoup(req.text, 'html.parser')


# In[4]:


sentences = [x.text.strip() for x in soup.find_all('span', {'class':'text'}) if '\n' in x.text]


# In[7]:


type(sentences)


# In[ ]:





# In[ ]:




