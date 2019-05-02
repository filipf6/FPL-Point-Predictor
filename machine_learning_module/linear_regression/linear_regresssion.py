# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from common.common import all_models_variables, defender_specific_variables
from tabulate import tabulate

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
# choose only needed columns
# 
# =============================================================================
defender_model_variables = all_models_variables + defender_specific_variables
defender_model_variables.append('score')
defender_samples_dataframe = defender_samples_dataframe[defender_model_variables]

# =============================================================================
# converts string values to floats
# 
# =============================================================================

columns_to_convert = ['points_per_game','form','selected_by_percent','previous_fixtures_influence_2','previous_fixtures_creativity_2','previous_fixtures_threat_2','previous_fixtures_ict_index_2']
defender_samples_dataframe[columns_to_convert] = defender_samples_dataframe[columns_to_convert].astype(float)

# =============================================================================
# fill missing data with mean
# 
# =============================================================================
for var in defender_model_variables:
    defender_samples_dataframe[var].fillna(defender_samples_dataframe[var].mean(), inplace=True)

#print(defender_samples_dataframe.count())

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

#train the algorithm
regressor = LinearRegression()  
regressor.fit(X_train, y_train) 

#check coefficients of attributes
#coeff_df = pd.DataFrame(regressor.coef_, defender_undependent_variables.columns, columns=['Coefficient'])  
#print(coeff_df) 

#test the model
y_pred = regressor.predict(X_test)

predictions = X_test.iloc[:,:]

predictions['prediction'] = y_pred

#a = np.c_[X_test, y_pred]


#b = np.c_(X_test[:,:7], y_pred)

#print(a[:,:7]+a[:,len(a)-2:len(a)-1])

#print(tabulate(np.c_(a[:,:7]+a[len(a)-1]), headers=defender_model_variables[:7], tablefmt='orgtbl'))
#print(tabulate(np.c_(X_test[:,:7], y_pred[y_pred.size-1:]), headers=defender_model_variables[:7], tablefmt='orgtbl'))



