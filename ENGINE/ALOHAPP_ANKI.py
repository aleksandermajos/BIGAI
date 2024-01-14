import pandas as pd
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'

path = path_beginning+"DATA/ALOHAPP/DECKS/JA/JP_FULL"

from ankipandas import Collection

col = Collection(path)
cards = col.cards.merge_notes()
counts = cards[cards.has_tag("leech")]["cdeck"].value_counts()
counts.plot.pie(title="Leeches per deck")
grouped = col.cards.groupby("cdeck")
data = grouped.mean()["civl"].sort_values().tail()
ax = data.plot.barh()
ax.set_ylabel("Deck name")
ax.set_xlabel("Average expected retention length/review interval [days]")
ax.set_title("Average retention length per deck")
oko=4