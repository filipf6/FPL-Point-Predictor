import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn import metrics
import copy
from sklearn.decomposition import PCA

def train(X_train, X_test, y_train, y_test):
    # =============================================================================
    # collinearity detection with variance inflation factor
    # 
    # =============================================================================
    mae=[0,1000000.0]
    mse=[0,1000000.0]
    r2=[0,0.0]
    #features_to_remove = []
    #prev_r2 = 0.0
    #new_X_train = copy.deepcopy(X_train)
    #new_X_test = copy.deepcopy(X_test)
    
    c=1
    any_vif_exceeded = True
    while any_vif_exceeded:
        vif = pd.DataFrame()
        vif['VIF Factor'] = [variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]
        vif['features'] = X_train.columns
        #vif['VIF Factor'] = [variance_inflation_factor(new_X_train.values, i) for i in range(new_X_train.shape[1])]
        #vif['features'] = new_X_train.columns
        if vif['VIF Factor'].max() > 5.0:
            print(c, ' removing ', vif.loc[vif['VIF Factor'].idxmax(), 'features'])
            
            X_train.drop(vif.loc[vif['VIF Factor'].idxmax(), 'features'], axis=1, inplace=True)
            X_test.drop(vif.loc[vif['VIF Factor'].idxmax(), 'features'], axis=1, inplace=True)
            
            #new_X_train.drop(vif.loc[vif['VIF Factor'].idxmax(), 'features'], axis=1, inplace=True)
            #new_X_test.drop(vif.loc[vif['VIF Factor'].idxmax(), 'features'], axis=1, inplace=True)
            
            regressor = LinearRegression()  
            regressor.fit(X_train, y_train) 
            y_pred = regressor.predict(X_test)
    
            
            if  metrics.mean_absolute_error(y_test, y_pred)<mae[1]:
                mae[0] = c
                mae[1] = metrics.mean_absolute_error(y_test, y_pred)
            if  metrics.mean_squared_error(y_test, y_pred)<mse[1]:
                mse[0] = c
                mse[1] = metrics.mean_squared_error(y_test, y_pred)
            if  metrics.r2_score(y_test, y_pred)>r2[1]:
                r2[0] = c
                r2[1] = metrics.r2_score(y_test, y_pred)
            
            print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
            print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
            print('R-squared: ', metrics.r2_score(y_test, y_pred))

            c+=1
            
            #if metrics.r2_score(y_test, y_pred) > prev_r2:
            #    features_to_remove.append(vif.loc[vif['VIF Factor'].idxmax(), 'features'])
            #prev_r2 = metrics.r2_score(y_test, y_pred)
        else:
            any_vif_exceeded = False
    
    print('mae', mae)
    print('mse', mse)
    print('r2', r2)
    #print('to_remove', features_to_remove)
    #X_train.drop(features_to_remove, axis=1, inplace=True)
    #X_test.drop(features_to_remove, axis=1, inplace=True)
    #regressor = LinearRegression()  
    #regressor.fit(X_train, y_train) 
    #y_pred = regressor.predict(X_test)
    #print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
    #print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
    #print('R-squared: ', metrics.r2_score(y_test, y_pred))
    
    # =============================================================================
    # feature selection with lasso method
    # 
    # =============================================================================
    reg = LassoCV(cv=3)
    reg.fit(X_train, y_train)
    coef = pd.Series(reg.coef_, index = X_train.columns)
    zero_coef = coef[coef == 0]
    to_remove = zero_coef.index.values.tolist()
    X_train.drop(to_remove, axis=1, inplace=True)
    X_test.drop(to_remove, axis=1, inplace=True)
    print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")
    print(X_train.columns)
    
    # =============================================================================
    #     dimension reduction with principal component analisys
    #     
    # =============================================================================
    pca = PCA(n_components=12)
    X_train = pca.fit_transform(X_train)
    X_test = pca.fit_transform(X_test)
    
    #reg.fit(X_train, y_train)
    #evaluate(regressor, X_test, y_train, y_test)
    #return reg
    # =============================================================================
    # training the alghoritm
    # =============================================================================
    regressor = LinearRegression()  
    regressor.fit(X_train, y_train) 
    evaluate(regressor, X_test, y_train, y_test)
    return regressor

# =============================================================================
# testing model
# =============================================================================
def evaluate(regressor, X_test, y_train, y_test):
    y_pred = regressor.predict(X_test)
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
    print('R-squared: ', metrics.r2_score(y_test, y_pred))
    
    #predictions = copy.deepcopy(X_test)
    #predictions['predict'] = y_pred
    #predictions['real score'] = y_test


