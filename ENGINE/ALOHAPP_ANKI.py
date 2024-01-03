import pandas as pd
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'

path = path_beginning+"DATA/ALOHAPP/DECKS/JA/JP_FULL"

from ankipandas import Collection

col = Collection(path)
oko=5