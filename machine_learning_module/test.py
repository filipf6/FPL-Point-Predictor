from preprocessing.preprocessing import process_data
from dataset.dataset import Dataset
from common.common import goalkeeper_specific_variables, defender_specific_variables, midfielder_specific_variables, forward_specific_variables

import pandas as pd
import numpy as np
from sklearn.feature_selection import RFECV
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from pyswarm import pso
from sklearn.svm import SVC, LinearSVC, SVR
from sklearn.linear_model import LinearRegression

from sklearn.decomposition import PCA
from statsmodels.stats.outliers_influence import variance_inflation_factor

#X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('defender-samples'), defender_specific_variables)
#X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('goalkeeper-samples'), goalkeeper_specific_variables)
#X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables)
#X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('forward-samples'), forward_specific_variables)




# =============================================================================
# OPTIMIZING RFC
# =============================================================================

# =============================================================================
# X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('forward-samples'), forward_specific_variables, 0.1212)
# 
# 
# def optimise_rfc(x):
#     print('rfc')
#     pca = PCA(x[4])
#     train = pca.fit_transform(X_train)
#     test = pca.transform(X_test)
#     criterion = 'entropy' if x[1] > 0.5 else 'gini'
#     rfc = RandomForestClassifier(n_estimators = int(x[0]), criterion = criterion, min_samples_split=int(x[2]), min_samples_leaf=int(x[3]), random_state = 3)
#     rfc.fit(train, y_train)
#     y_pred = rfc.predict(test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro'))
# 
# lb = [1,0,5,1,0.5]
# ub = [5,1,19,6,0.9]
# rfc_xopt, rfc_fopt = pso(optimise_rfc, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# 
# print('The optimum for RFC is at:')
# print('    {}'.format(rfc_xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(rfc_fopt))
# =============================================================================

# =============================================================================
# RFC
# =============================================================================
# =============================================================================
# X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('forward-samples'), forward_specific_variables, 0.74938823)
# 
# rfc = RandomForestClassifier(n_estimators = 3, criterion = 'gini', min_samples_split=8, min_samples_leaf=2, random_state = 3).fit(X_train, y_train)
# y_pred = rfc.predict(X_test)
# 
# print('F1 score micro: ', metrics.f1_score(y_test, y_pred, average='micro')) 
# print('F1 score macro: ', metrics.f1_score(y_test, y_pred, average='macro')) 
# comparison = np.vstack((y_test, y_pred)).T
# =============================================================================


# =============================================================================
# OPTIMIZING KNN
# =============================================================================
# =============================================================================
# X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables, 0.5500293818)
# 
# def optimise_knn(x):
#     print('knn')
#     pca = PCA(x[4])
#     train = pca.fit_transform(X_train)
#     test = pca.transform(X_test)
#     weights = 'uniform' if x[1] > 0.5 else 'distance'
#     p = 1 if x[3] < 0.5 else 2 
#     knn = KNeighborsClassifier(n_neighbors=int(x[0]), weights = weights, leaf_size = int(x[2]), p = p, n_jobs = -1)
#     knn.fit(train, y_train)
#     y_pred = knn.predict(test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro'))
# 
# lb = [3,0,8,0,0.5]
# ub = [6,1,14,1,0.7]
# knn_xopt, knn_fopt = pso(optimise_knn, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# 
# print('The optimum for KNN is at:')
# print('    {}'.format(knn_xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(knn_fopt))
# =============================================================================

# =============================================================================
# KNN
# =============================================================================
# =============================================================================
# X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables, 0.62)
# 
# knn = KNeighborsClassifier(n_neighbors=4, weights = 'distance', leaf_size = 10, p = 1, n_jobs = -1)
# knn.fit(X_train, y_train)
# y_pred = knn.predict(X_test)
# 
# print('F1 score micro: ', metrics.f1_score(y_test, y_pred, average='micro')) 
# print('F1 score macro: ', metrics.f1_score(y_test, y_pred, average='macro')) 
# comparison = np.vstack((y_test, y_pred)).T
# =============================================================================


# =============================================================================
# OPTIMIZING SVC
# =============================================================================
# =============================================================================
# X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables, 0.8825448)
# 
# def optimise_svc(x):
#     print('opt svc')
#     pca = PCA(n_components=x[4])
#     train = pca.fit_transform(X_train)
#     test = pca.transform(X_test)
#     kernel_list = ['rbf', 'linear']#, 'sigmoid', 'linear', 
#     svm = SVC(C = x[0], kernel = kernel_list[int(x[1])], degree = int(x[2]), gamma = x[3])
#     svm.fit(train, y_train)
#     y_pred = svm.predict(test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro'))
# 
# lb = [6, 0, 1, 0.1, 0.5]
# ub = [15, 1.99, 3, 2, 0.8]
# svc_xopt, svc_fopt = pso(optimise_svc, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=70, swarmsize=70)
# 
# print('The optimum for SVC is at:')
# print('    {}'.format(svc_xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(svc_fopt))
# =============================================================================

# =============================================================================
# SVC
# 
# =============================================================================
X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables, 0.56387)

svm = SVC(C = 8.0, kernel = 'rbf', gamma = 0.318881)
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)

print('F1 score micro: ', metrics.f1_score(y_test, y_pred, average='micro')) 
print('F1 score macro: ', metrics.f1_score(y_test, y_pred, average='macro')) 
comparison = np.vstack((y_test, y_pred)).T

# =============================================================================
# SVR OPTIMIZATION
# 
# =============================================================================
# =============================================================================
# X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('goalkeeper-samples'), goalkeeper_specific_variables, 0.8825448)
# 
# def optimise_svr(x):
#     print('svr goal')
#     pca = PCA(n_components=x[4])
#     train = pca.fit_transform(X_train)
#     test = pca.transform(X_test)
#     kernel_list = ['rbf', 'linear'] #, 'sigmoid' 'linear', 'poly', 
#     svm = SVR(C = x[0], kernel = kernel_list[int(x[1])], gamma = x[2], epsilon = x[3])
#     svm.fit(train, y_train)
#     y_pred = svm.predict(test)
#     r_squared = metrics.r2_score(y_test, y_pred)
#     adj_r_squared = 1 - (1-r_squared)*(len(y_test)-1)/(len(y_test)-test.shape[1]-1)
#     return -(adj_r_squared)
# 
# lb = [0.005, 0, 0.9, 0.1, 0.1]
# ub = [0.09, 1.99, 2, 0.3, 0.6]
# 
# goa_svr_xopt, goa_svr_fopt = pso(optimise_svr, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=50, swarmsize=50)
# 
# print('The optimum for SVR is at:')
# print('    {}'.format(goa_svr_xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(goa_svr_fopt))
#     
# 
# X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('defender-samples'), defender_specific_variables, 0.8825448)
# 
# def optimise_svr(x):
#     print('svr def')
#     pca = PCA(n_components=x[4])
#     train = pca.fit_transform(X_train)
#     test = pca.transform(X_test)
#     kernel_list = ['rbf', 'linear'] #, 'sigmoid' 'linear', 'poly', 
#     svm = SVR(C = x[0], kernel = kernel_list[int(x[1])], gamma = x[2], epsilon = x[3])
#     svm.fit(train, y_train)
#     y_pred = svm.predict(test)
#     r_squared = metrics.r2_score(y_test, y_pred)
#     adj_r_squared = 1 - (1-r_squared)*(len(y_test)-1)/(len(y_test)-test.shape[1]-1)
#     return -(adj_r_squared)
# 
# lb = [5, 0, 0.5, 0.1, 0.6]
# ub = [8, 1.99, 2, 0.4, 0.75]
# 
# def_svr_xopt, def_svr_fopt = pso(optimise_svr, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=50, swarmsize=50)
# 
# print('The optimum for SVR is at:')
# print('    {}'.format(def_svr_xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(def_svr_fopt))
# =============================================================================

# =============================================================================
# X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables, 0.8825448)
# 
# def optimise_svr(x):
#     print('svr mid')
#     pca = PCA(n_components=x[2])
#     train = pca.fit_transform(X_train)
#     test = pca.transform(X_test)
#     #kernel_list = ['rbf', 'linear'] #, 'sigmoid' 'linear', 'poly', 
#     svm = SVR(C = x[0], kernel = 'rbf', gamma = x[1], epsilon = 0.24475588)
#     svm.fit(train, y_train)
#     y_pred = svm.predict(test)
#     r_squared = metrics.r2_score(y_test, y_pred)
#     adj_r_squared = 1 - (1-r_squared)*(len(y_test)-1)/(len(y_test)-test.shape[1]-1)
#     return -(adj_r_squared)
# 
# lb = [0.05, 0.1, 0.005]
# ub = [1, 1.5, 0.1]
# 
# mid_svr_xopt, mid_svr_fopt = pso(optimise_svr, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# 
# print('The optimum for SVR is at:')
# print('    {}'.format(mid_svr_xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(mid_svr_fopt))
# =============================================================================

# =============================================================================
# SVR
# 
# =============================================================================
X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables, 0.0500029)

svm = SVR(C = 0.170544, kernel = 'rbf', gamma = 0.895228, epsilon = 0.24475588)
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))   
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
r_squared = metrics.r2_score(y_test, y_pred)
print('R-squared: ', r_squared)
adj_r_squared = 1 - (1-r_squared)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)
print('adjusted R-squared: ', adj_r_squared)
comparison = np.vstack((y_test, y_pred)).T



X_train, X_test, y_train, y_test = process_data(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables, 0.8825448)

# =============================================================================
# def optimise_svc(x):
#     print('opt svc')
#     pca = PCA(n_components=x[3])
#     train = pca.fit_transform(X_train)
#     test = pca.transform(X_test)
#     #kernel_list = ['rbf', 'linear']#, 'sigmoid', 'linear', 
#     svm = SVC(C = x[0], kernel = 'rbf', degree = int(x[1]), gamma = x[2])
#     svm.fit(train, y_train)
#     y_pred = svm.predict(test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro'))
# 
# lb = [6, 1, 0.05, 0.5]
# ub = [15, 3, 1, 0.8]
# svc_xopt, svc_fopt = pso(optimise_svc, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=70, swarmsize=70)
# 
# print('The optimum for SVC is at:')
# print('    {}'.format(svc_xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(svc_fopt))
# =============================================================================
