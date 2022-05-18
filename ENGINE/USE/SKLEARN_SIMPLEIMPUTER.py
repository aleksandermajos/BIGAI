import pandas as pd
from io import StringIO
from sklearn.impute import SimpleImputer
import numpy as np

#https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html
#

csv_data = \
'''A,B,C,D
1.0,2.0,3.0,4.0
5.0,6.0,,8.0
10.0,11.0,12.0,'''

df = pd.read_csv(StringIO(csv_data))
imr = SimpleImputer(missing_values=np.nan, strategy='mean')
imr = imr.fit(df.values)
imputed_data = imr.transform(df.values)
oko=5

