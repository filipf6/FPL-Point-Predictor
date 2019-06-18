from dataset.dataset import Dataset
from common.common import all_models_variables
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.decomposition import PCA

def process_data_for_classification(samples_dataframe, position_specific_variables):    
    # =============================================================================
    # choose variables for exploration, drop rows with missing values
    # 
    # =============================================================================
    model_variables = all_models_variables + position_specific_variables
    model_variables.append('score')
    samples_dataframe = samples_dataframe[model_variables].dropna()
    
    
    # =============================================================================
    # discretizate dependent variable
    # =============================================================================
    discretizate(samples_dataframe)
    
    # =============================================================================
    # converts dataframe values to floats, calculate statistical details of dataset
    # 
    # =============================================================================
    samples_dataframe = samples_dataframe.astype(float)
    #stats = samples_dataframe.describe()
    
    # =============================================================================
    # divide data into dependent and undependent variables
    # 
    # =============================================================================
    undependent_variables = samples_dataframe[all_models_variables+position_specific_variables]
    dependent_variable = samples_dataframe["score"]
    
    # =============================================================================
    # display data distribution
    # =============================================================================
    #distribution(dependent_variable)
    
    # =============================================================================
    # divide data into training and test sets
    # 
    # =============================================================================
    X_train, X_test, y_train, y_test = train_test_split(undependent_variables, dependent_variable, test_size=0.2, random_state=0)
    
    # =============================================================================
    # Zscore normalization
    # =============================================================================
    X_train, X_test = normalize(X_train, X_test)
    
    # =============================================================================
    # remove highly correlated variables with variance inflation factor collinearity detection
    # 
    # =============================================================================
    vif_feature_selection(X_train, X_test)
    
    
    # =============================================================================
    # reduce dimentions to 80% of variance with principal component analysis
    # =============================================================================
    pca = PCA(n_components=0.80)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)
    
    return X_train, X_test, y_train, y_test


def discretizate(samples_dataframe):
    samples_dataframe['score'] = np.where(samples_dataframe['score'] < 0, 0, samples_dataframe['score'])
    samples_dataframe['score'] = np.where(samples_dataframe['score'] == 4, 3, samples_dataframe['score'])
    samples_dataframe['score'] = np.where(samples_dataframe['score'] == 5, 3, samples_dataframe['score'])
    samples_dataframe['score'] = np.where(samples_dataframe['score'] == 6, 3, samples_dataframe['score'])
    samples_dataframe['score'] = np.where(samples_dataframe['score'] > 6, 4, samples_dataframe['score'])
    
def distribution(dependent_variable):
    plt.xticks(np.arange(5), ('<1', '1', '2', '3-6', '>6'))

    plt.hist(dependent_variable, bins = int(np.max(dependent_variable) - np.min(dependent_variable)) + 1,  color = 'blue', edgecolor = 'black')
    plt.title('Obrońcy')
    plt.xlabel('Wynik')
    plt.ylabel('Ilość obserwacji')

    
def normalize(X_train, X_test):
    sc = StandardScaler()
    X_train = pd.DataFrame(sc.fit_transform(X_train), index = X_train.index, columns = X_train.columns)
    X_test = pd.DataFrame(sc.transform(X_test), index = X_test.index, columns = X_test.columns)
    return X_train, X_test

def vif_feature_selection(X_train, X_test):
    #c = 1
    any_vif_exceeded = True
    while any_vif_exceeded:
        vif = pd.DataFrame()
        vif['VIF Factor'] = [variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]
        vif['features'] = X_train.columns
        if vif['VIF Factor'].max() > 5.0:
            #print(c, ' removing ', vif.loc[vif['VIF Factor'].idxmax(), 'features'])
            X_train.drop(vif.loc[vif['VIF Factor'].idxmax(), 'features'], axis=1, inplace=True)
            X_test.drop(vif.loc[vif['VIF Factor'].idxmax(), 'features'], axis=1, inplace=True)
            #c += 1
        else:
            any_vif_exceeded = False