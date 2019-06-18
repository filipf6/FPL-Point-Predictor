from sklearn import metrics

def train(X_train, X_test, y_train, y_test):
    return 0

def evaluate(regressor, X_test, y_train, y_test):
    y_pred = regressor.predict(X_test)
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
    print('R-squared: ', metrics.r2_score(y_test, y_pred))