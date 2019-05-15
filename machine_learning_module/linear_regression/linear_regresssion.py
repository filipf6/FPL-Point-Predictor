# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
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

columns_to_convert = ['points_per_game','form','selected_by_percent','previous_fixtures_influence_2','previous_fixtures_creativity_2','previous_fixtures_threat_2','previous_fixtures_ict_index_2']
defender_samples_dataframe[columns_to_convert] = defender_samples_dataframe[columns_to_convert].astype(float)
stats = defender_samples_dataframe.describe()

# =============================================================================
# divide data into dependent and undependent variables
# 
# =============================================================================
defender_undependent_variables = defender_samples_dataframe[all_models_variables+defender_specific_variables]
defender_dependent_variable = defender_samples_dataframe["score"]

# =============================================================================
# divide data into training and test sets
# 
# =============================================================================
X_train, X_test, y_train, y_test = train_test_split(defender_undependent_variables, defender_dependent_variable, test_size=0.2, random_state=0)

# =============================================================================
# train the algorithm
# =============================================================================
regressor = LinearRegression()  
regressor.fit(X_train, y_train) 

#check coefficients of attributes
#coeff_df = pd.DataFrame(regressor.coef_, defender_undependent_variables.columns, columns=['Coefficient'])  
#print(coeff_df) 

# =============================================================================
# test the model
# =============================================================================
y_pred = regressor.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
print('R-squared: ', metrics.r2_score(y_test, y_pred))

predictions = copy.deepcopy(X_test)
predictions['predict'] = y_pred
predictions['real score'] = y_test