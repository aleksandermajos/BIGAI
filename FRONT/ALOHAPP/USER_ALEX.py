from USER import USER
from SOURCE import SOURCE_CREATE, SOURCE

Alex_user = USER(native='pl',langs=['fr'])
Assimil_FR = SOURCE(source_type='AUDIO',user_type='BOOK',path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/FR/SELF_LEARNING/ASSIMIL')
Alex_user.sources.append(Assimil_FR)
oko = 4