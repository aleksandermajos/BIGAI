#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd

pd_fr = pd.read_excel("FREQ_WORDS_GER.xlsx")


# In[37]:


pd_fr.head


# In[38]:


cutted_pd_fr = pd_fr[0:6000]


# In[39]:


cutted_pd_fr


# In[40]:


rem_digits_pd = cutted_pd_fr['ich 702146'].str.replace('\d+', '')


# In[41]:


rem_digits_pd


# In[42]:


rem_digits_pd.to_csv('GER.csv', index=False) 


# In[ ]:




