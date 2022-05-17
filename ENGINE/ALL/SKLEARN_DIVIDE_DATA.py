from sklearn.model_selection import train_test_split

def divideDataByPercent(X,y,Percent):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1-Percent/100, random_state=1, stratify=y)
    return X_train, X_test, y_train, y_test