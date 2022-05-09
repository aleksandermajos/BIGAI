#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import nemo
import nemo.collections.nlp as nemo_nlp


# In[2]:


nmt_model = nemo_nlp.models.machine_translation.MTEncDecModel.from_pretrained(model_name="nmt_fr_en_transformer12x2")


# In[3]:


all_words_es = pd.read_csv('FR.csv')


# In[4]:


all_words_es


# In[8]:


for ind in all_words_es.index:
    if all_words_es['WORD_TRAN_A'][ind] == 'NaN':
        continue
    translate = nmt_model.translate([all_words_es['WORD'][ind]])
    all_words_es['WORD_TRAN_A'][ind] = translate[0]
    print(ind)


# In[6]:


all_words_es[887:1000]


# In[ ]:


all_words_es.to_csv('FR.csv')


# In[ ]:




