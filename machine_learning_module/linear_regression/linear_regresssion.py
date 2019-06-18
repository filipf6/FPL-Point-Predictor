# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from common.common import all_models_variables, goalkeeper_specific_variables, defender_specific_variables, midfielder_specific_variables, forward_specific_variables
import copy
from dataset.dataset import Dataset
from pymongo import MongoClient
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFECV

# =============================================================================
# get data from database
# 
# =============================================================================
# =============================================================================
# ds = Dataset()
#client = MongoClient('mongodb+srv://filipf6:poiuy7u8@fpl-point-predictor-eneet.mongodb.net/test?retryWrites=true')
#db = client['fpl-point-predictor']
# 
#defender_samples_collection = db['defender-samples']
#defender_samples_dataset = defender_samples_collection.find({"score": { '$ne': None }}) 
# =============================================================================

dataset = Dataset()
defender_samples_dataframe = dataset.get_dataset('goalkeeper-samples') #pd.DataFrame(list(defender_samples_dataset))
#defender_samples_dataframe = dataset.get_dataset('defender-samples')
#defender_samples_dataframe = dataset.get_dataset('midfielder-samples')
#defender_samples_dataframe = dataset.get_dataset('forward-samples')

# =============================================================================
# choose variables for regression, drop rows with missing values
# 
# =============================================================================
defender_model_variables = all_models_variables + goalkeeper_specific_variables
#defender_model_variables = all_models_variables + defender_specific_variables
#defender_model_variables = all_models_variables + midfielder_specific_variables
#defender_model_variables = all_models_variables + forward_specific_variables
defender_model_variables.append('score')
defender_samples_dataframe = defender_samples_dataframe[defender_model_variables].dropna()
#defender_samples_dataframe.loc[defender_samples_dataframe['score'] < 0, 'score'] = 0
defender_samples_dataframe['score'] = np.where(defender_samples_dataframe['score'] < 0, 0, defender_samples_dataframe['score'])
defender_samples_dataframe['score'] = np.where(defender_samples_dataframe['score'] == 4, 3, defender_samples_dataframe['score'])
defender_samples_dataframe['score'] = np.where(defender_samples_dataframe['score'] == 5, 3, defender_samples_dataframe['score'])
defender_samples_dataframe['score'] = np.where(defender_samples_dataframe['score'] == 6, 3, defender_samples_dataframe['score'])
defender_samples_dataframe['score'] = np.where(defender_samples_dataframe['score'] > 6, 4, defender_samples_dataframe['score'])
#defender_samples_dataframe.loc[defender_samples_dataframe['score'] > 2 and defender_samples_dataframe['score'] < 7, 'score'] = 3

#defender_samples_dataframe = defender_samples_dataframe[defender_samples_dataframe.score >= 0]

# =============================================================================
# converts dataframe values to floats, calculate statistical details of dataset
# 
# =============================================================================

#columns_to_convert = ['points_per_game','form','selected_by_percent','previous_fixtures_influence_2','previous_fixtures_creativity_2','previous_fixtures_threat_2','previous_fixtures_ict_index_2']
#defender_samples_dataframe[columns_to_convert] = defender_samples_dataframe[columns_to_convert].astype(float)

defender_samples_dataframe = defender_samples_dataframe.astype(float)
#stats = defender_samples_dataframe.describe()

# =============================================================================
# divide data into dependent and undependent variables
# 
# =============================================================================
#defender_undependent_variables = defender_samples_dataframe[all_models_variables+defender_specific_variables]
defender_undependent_variables = defender_samples_dataframe[all_models_variables+goalkeeper_specific_variables]
defender_dependent_variable = defender_samples_dataframe["score"]



#sc = StandardScaler()
#defender_undependent_variables = pd.DataFrame(sc.fit_transform(defender_undependent_variables), index = defender_undependent_variables.index, columns = defender_undependent_variables.columns)


#pca = PCA(n_components=0.95)
#defender_undependent_variables = pca.fit_transform(defender_undependent_variables)


plt.xticks([-4,-2,0,2,4,6,8,10,12,14,16])

plt.xticks([-1,0,1,2,3,4,5])
plt.hist(defender_dependent_variable, bins = int(np.max(defender_dependent_variable - np.min(defender_dependent_variable))) + 1,  color = 'blue', edgecolor = 'black')
plt.title('Rozkład wyników')
plt.xlabel('Wynik')
plt.ylabel('Ilość próbek')


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



# =============================================================================
# collinearity detection with variance inflation factor
# 
# =============================================================================
mae=[0,1000000.0]
mse=[0,1000000.0]
r2=[0,0.0]

c=1
any_vif_exceeded = True
while any_vif_exceeded:
    vif = pd.DataFrame()
    x = X_train.values
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

pca = PCA(n_components=0.80)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

# =============================================================================
# feature selection with lasso method
# 
# =============================================================================

# =============================================================================
# reg = LassoCV()
# reg.fit(X_train, y_train)
# =============================================================================

# =============================================================================
# coef = pd.Series(reg.coef_, index = X_train.columns)
# coef = coef[coef == 0]
# to_remove = coef.index.values.tolist()
# X_train = X_train.drop(to_remove, axis=1)
# X_test = X_test.drop(to_remove, axis=1) #X_test.drop(to_remove, axis=1, inplace=True)
# print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")
# =============================================================================



# =============================================================================
# coef = reg.coef_
# to_remove = np.where(coef == 0)
# X_train = np.delete(X_train, to_remove, 1)
# X_test = np.delete(X_test, to_remove, 1)
# =============================================================================

# =============================================================================
# training the alghoritm - linear regression
# =============================================================================
regressor = LinearRegression() 

rfe = RFECV(regressor)
fit = rfe.fit(X_train, y_train)
a1 = fit.n_features_
a2 = fit.support_
a3 = fit.ranking_
 
indexes = np.where(fit.support_ != True)

# removing columns in numpy array
train = np.delete(X_train, indexes, 1)
test = np.delete(X_test, indexes, 1)

# removing columns in dataframe
#train = X_train.drop(X_train.columns[indexes], axis=1)
#test = X_test.drop(X_test.columns[indexes], axis=1)

regressor.fit(train, y_train)

y_pred = regressor.predict(test)
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
#print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
print('R-squared: ', metrics.r2_score(y_test, y_pred))

comparison = np.vstack((y_test, y_pred)).T

#regressor.fit(X_train, y_train) 

# =============================================================================
# training the alghoritm - lassoCV
# =============================================================================
#reg.fit(X_train, y_train) 

# =============================================================================
# testing model
# =============================================================================


# =============================================================================
# y_pred = regressor.predict(X_test)
# print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
# print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
# #print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
# print('R-squared: ', metrics.r2_score(y_test, y_pred))
# =============================================================================

# =============================================================================
# y_pred = reg.predict(X_test)
# print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
# print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
# #print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
# print('R-squared: ', metrics.r2_score(y_test, y_pred))
# =============================================================================





#predictions = copy.deepcopy(X_test)
#predictions['predict'] = y_pred
#predictions['real score'] = y_test



#check coefficients of attributes
#coeff_df = pd.DataFrame(regressor.coef_, defender_undependent_variables.columns, columns=['Coefficient'])  
#print(coeff_df) 





