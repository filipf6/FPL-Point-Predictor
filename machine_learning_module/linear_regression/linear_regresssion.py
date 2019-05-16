# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from common.common import all_models_variables, defender_specific_variables
import copy

# =============================================================================
# get data from database
# 
# =============================================================================
client = MongoClient('mongodb+srv://filipf6:poiuy7u8@fpl-point-predictor-eneet.mongodb.net/test?retryWrites=true')
db = client['fpl-point-predictor']

defender_samples_collection = db['defender-samples']
defender_samples_dataset = defender_samples_collection.find({"score": { '$ne': None }}) 
defender_samples_dataframe = pd.DataFrame(list(defender_samples_dataset))


# =============================================================================
# choose variables for regression, drop rows with missing values
# 
# =============================================================================
defender_model_variables = all_models_variables + defender_specific_variables
defender_model_variables.append('score')
defender_samples_dataframe = defender_samples_dataframe[defender_model_variables].dropna()

# =============================================================================
# converts string values to floats, calculate statistical details of dataset
# 
# =============================================================================

#columns_to_convert = ['points_per_game','form','selected_by_percent','previous_fixtures_influence_2','previous_fixtures_creativity_2','previous_fixtures_threat_2','previous_fixtures_ict_index_2']
#defender_samples_dataframe[columns_to_convert] = defender_samples_dataframe[columns_to_convert].astype(float)

defender_samples_dataframe = defender_samples_dataframe.astype(float)
stats = defender_samples_dataframe.describe()

# =============================================================================
# divide data into dependent and undependent variables
# 
# =============================================================================
defender_undependent_variables = defender_samples_dataframe[all_models_variables+defender_specific_variables]

#min-max normalization
#defender_undependent_variables = (defender_undependent_variables-defender_undependent_variables.min())/(defender_undependent_variables.max()-defender_undependent_variables.min())

defender_dependent_variable = defender_samples_dataframe["score"]

# =============================================================================
# divide data into training and test sets
# 
# =============================================================================
X_train, X_test, y_train, y_test = train_test_split(defender_undependent_variables, defender_dependent_variable, test_size=0.2, random_state=0)



# =============================================================================
# Zscore normalization
# =============================================================================
sc = StandardScaler()
X_train = pd.DataFrame(sc.fit_transform(X_train), index = X_train.index, columns = X_train.columns)
X_test = pd.DataFrame(sc.transform(X_test), index = X_test.index, columns = X_test.columns)


mae=[0,1000000.0]
mse=[0,1000000.0]
r2=[0,0.0]

c=1
any_vif_exceeded = True
while any_vif_exceeded:
    vif = pd.DataFrame()
    vif['VIF Factor'] = [variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]
    vif['features'] = X_train.columns
    if vif['VIF Factor'].max() > 5.0:
        print(c, ' removing ', vif.loc[vif['VIF Factor'].idxmax(), 'features'])
        X_train.drop(vif.loc[vif['VIF Factor'].idxmax(), 'features'], axis=1, inplace=True)
        X_test.drop(vif.loc[vif['VIF Factor'].idxmax(), 'features'], axis=1, inplace=True)
        
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
        #print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
        print('R-squared: ', metrics.r2_score(y_test, y_pred))
        c+=1
    else:
        any_vif_exceeded = False

print('mae', mae)
print('mse', mse)
print('r2', r2)

reg = LassoCV()
reg.fit(X_train, y_train)
coef = pd.Series(reg.coef_, index = X_train.columns)
coef = coef[coef == 0]
to_remove = coef.index.values.tolist()
X_train.drop(to_remove, axis=1, inplace=True)
X_test.drop(to_remove, axis=1, inplace=True)
print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")

regressor = LinearRegression()  
regressor.fit(X_train, y_train) 
y_pred = regressor.predict(X_test)
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
#print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
print('R-squared: ', metrics.r2_score(y_test, y_pred))

# =============================================================================
# train the algorithm
# =============================================================================
#regressor = LinearRegression()  
#regressor.fit(X_train, y_train) 


#check coefficients of attributes
#coeff_df = pd.DataFrame(regressor.coef_, defender_undependent_variables.columns, columns=['Coefficient'])  
#print(coeff_df) 

# =============================================================================
# test the model
# =============================================================================
#y_pred = regressor.predict(X_test)

#print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
#print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
#print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
#print('R-squared: ', metrics.r2_score(y_test, y_pred))

#print('R-squared: ', regressor.score(X_train, y_train))


predictions = copy.deepcopy(X_test)
predictions['predict'] = y_pred
predictions['real score'] = y_test
# =============================================================================
# X_test['predict'] = y_pred
# X_test['real score'] = y_test
# =============================================================================
