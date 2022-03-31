#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import nemo
import nemo.collections.nlp as nemo_nlp


# In[2]:


nmt_model = nemo_nlp.models.machine_translation.MTEncDecModel.from_pretrained(model_name="nmt_de_en_transformer12x2")


# In[3]:


all_words_es = pd.read_csv('GER.csv')


# In[4]:


all_words_es


# In[ ]:


for ind in all_words_es.index:
    translate = nmt_model.translate([all_words_es['WORD'][ind]])
    all_words_es['WORD_TRAN_A'][ind] = translate[0]


# In[21]:


all_words_es


# In[22]:


all_words_es.to_csv('ALL_WORDS_ES.csv')


# In[ ]:




