from USER import USER
from SOURCE import SOURCE_CREATE, SOURCE

Alex_user = USER(native='pl',langs=['fr'])
Assimil_FR = SOURCE(source_type='AUDIO',user_type='BOOK',path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/FR/SELF_LEARNING/ASSIMIL')
LittlePrince_FR = SOURCE(source_type='AUDIO',user_type='BOOK',path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/FR/LITTLE_PRINCE')
BlondynkaNew_FR = SOURCE(source_type='AUDIO',user_type='BOOK',path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/FR/SELF_LEARNING/BLONDYNA_NEW')
BlondynkaOld_FR = SOURCE(source_type='AUDIO',user_type='BOOK',path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/FR/SELF_LEARNING/BLONDYNA_OLD')
MowimyPoFrancusku_FR = SOURCE(source_type='AUDIO',user_type='BOOK',path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/FR/SELF_LEARNING/MOWIMY_PO_FRANCUSKU')
Alex_sources = [Assimil_FR,LittlePrince_FR,BlondynkaNew_FR,BlondynkaOld_FR,MowimyPoFrancusku_FR]

all_words_in_sources = []
for source in Alex_sources:
    all_words_in_sources.append(source.all_words)
all_words_in_sources = set().union(*all_words_in_sources)

Alex_user.sources.extend(Alex_sources)





oko = 4