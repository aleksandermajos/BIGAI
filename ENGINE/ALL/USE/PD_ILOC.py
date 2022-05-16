import pandas as pd

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html
# Get the row of dataframe from...to....

mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},
          {'a': 100, 'b': 200, 'c': 300, 'd': 400},
          {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000 }]

df = pd.DataFrame(mydict)

First_row = df.iloc[0]
First_and_second_row = df.iloc[[0, 1]]
oko=5