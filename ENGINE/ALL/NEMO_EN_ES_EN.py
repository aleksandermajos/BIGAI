#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import NeMo and it's ASR, NLP and TTS collections
import nemo
# Import Speech Recognition collection
import nemo.collections.asr as nemo_asr
# Import Natural Language Processing colleciton
import nemo.collections.nlp as nemo_nlp
# Import Speech Synthesis collection
import nemo.collections.tts as nemo_tts
# We'll use this to listen to audio
import IPython


# In[2]:


# Neural Machine Translation model
#nmt_model = nemo_nlp.models.machine_translation.MTEncDecModel.from_pretrained(model_name="nmt_en_es_transformer12x2").cuda()
nmt_model2 = nemo_nlp.models.machine_translation.MTEncDecModel.from_pretrained(model_name="nmt_es_en_transformer12x2").cuda()


# In[13]:


english_text = ['Information can be thought of as the resolution of uncertainty']
print(english_text)


# In[14]:


spanish_text = nmt_model.translate(english_text)
print(spanish_text)


# In[3]:


spanish_text = ['mil ciento veintiséis noticias en españolevenido a laovodst para aprender español cada día dialosaves publicamos nuestro podcas de lunes a viernes si quies ver la transqición completa y un hoja trabajo con ejercicios y con explicaciones misitanosta web hoyblamos com azte suscritor premio para acceder a todo ese contenido hola oiente como stas ya estamos a diez de junio y el verano está muy cerca sabers un secreto de junio que los primeros días de junio son los mejores pareda playa tranquilo antes de que los niños extende vacaciones es el momento de disfrutar de la tranquilidad de la playa porque a partir de finales de junio todo empieza a llenarse de gente pero mientras no vasa la playa y con mos jueves vamos a ver las noticias de hoy empezaremos hablando de un hombre que ha desarrollado una habilidad muy especial siguremos con la historia de un perro que tiene un trabajo muy interesante y terminaremos com una mujer que decidió pasar a la acción para conseguir seguidores en redes sociales hoy hablamos de noticias en española na expresión que dice que cada vida es un mundo y no puedo estar más de acuerdo porque aunque parezca una ovidad todo si cada uno de nosotros tenemos nuestros problemas nuestras historias nuestros triunfos nuestras derrotas nuestros momentos de felicidad y nuestras penas todos no hay nadie que se escape de eso pero tamienes cierto que teniendo muy en cuenta lo que acabó decir y sin despreciar los problemas de nadie algunas personas tienen una vida más difícil que otras personas eso es así y amí siempre me a parecido que tienen un gran mélito todas aquellas personas que luchan contra trastornos de aprendizaje comopudeser la dislecia o contratrastornos']


# In[4]:


english_text = nmt_model2.translate(spanish_text)
print(english_text)


# In[ ]:




