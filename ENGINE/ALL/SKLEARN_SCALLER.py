from sklearn.preprocessing import StandardScaler

def scaleData(data):
    sc = StandardScaler()
    sc.fit(data)
    return sc.transform(data)
