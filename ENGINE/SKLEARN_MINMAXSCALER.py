from sklearn.preprocessing import MinMaxScaler

def scaleMinMaxData(data):
    mms = MinMaxScaler()
    return mms.fit_transform(data)