from io import StringIO
import pandas as pd
#https://docs.python.org/3/library/io.html
#

csv_data = \
'''A,B,C,D
1.0,2.0,3.0,4.0
5.0,6.0,,8.0
10.0,11.0,12.0,'''
df = pd.read_csv(StringIO(csv_data))
oko=5


