from preprocessing.preprocessing import process_data_for_classification
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

#X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('defender-samples'), defender_specific_variables)
X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('goalkeeper-samples'), goalkeeper_specific_variables)
#X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables)
#X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('forward-samples'), forward_specific_variables)
 



# =============================================================================
# def optimise_knn(x):
#     weights = 'uniform' if x[1] > 0.5 else 'distance'
#     p = 1 if x[3] > 0.5 else 2
#     knn = KNeighborsClassifier(n_neighbors=int(x[0]), weights = weights, leaf_size = int(x[2]), p = p, n_jobs = -1)
#     knn.fit(X_train, y_train)
#     y_pred = knn.predict(X_test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro', labels=np.unique(y_pred)))
# 
# lb = [7,0,8,0]
# ub = [9,1,10,1]
# xopt, fopt = pso(optimise_knn, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# 
# print('The optimum for KNN is at:')
# print('    {}'.format(xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(fopt))
# 
# X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('goalkeeper-samples'), goalkeeper_specific_variables)
# 
# 
# def optimise_rfc(x):
#     criterion = 'entropy' if x[1] > 0.5 else 'gini'
#     rfc = RandomForestClassifier(n_estimators = int(x[0]), criterion = criterion, min_samples_split=x[2], min_samples_leaf=x[3])
#     rfc.fit(X_train, y_train)
#     y_pred = rfc.predict(X_test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro', labels=np.unique(y_pred)))
# 
# lb = [7,0,6,3]
# ub = [9,1,9,6]
# xopt, fopt = pso(optimise_knn, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# 
# print('The optimum for RFC is at:')
# print('    {}'.format(xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(fopt))
# =============================================================================


# =============================================================================
# def optimise_svc(x):
#     kernel_list = ['linear', 'poly', 'rbf', 'sigmoid']
#     shrinking = True if x[5] > 0.5 else False
#     svm = SVC(C = x[0], kernel = kernel_list[int(x[1])], degree = int(x[2]), gamma = x[3], coef0 = x[4], shrinking = shrinking)
#     svm.fit(X_train, y_train)
#     y_pred = svm.predict(X_test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro', labels=np.unique(y_pred)))
# =============================================================================

# =============================================================================
# lb = [0.1, 0, 1, 0.01, 0, 0]
# ub = [10, 3.99, 10, 2, 2, 1]
# =============================================================================

# =============================================================================
# def optimise_svc(x):
#     kernel_list = ['linear', 'poly', 'rbf', 'sigmoid']
#     svm = SVC(C = x[0], kernel = kernel_list[int(x[1])], degree = int(x[2]), gamma = x[3])
#     svm.fit(X_train, y_train)
#     y_pred = svm.predict(X_test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro'))
# 
# lb = [2, 0, 1, 0.1]
# ub = [10, 3.99, 5, 2]
# xopt, fopt = pso(optimise_svc, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# =============================================================================
# =============================================================================
# def optimise_svc(x):
#     svm = SVC(C = x[0], kernel = 'poly', degree = 2, gamma = x[1])
#     svm.fit(X_train, y_train)
#     y_pred = svm.predict(X_test)
#     return -(metrics.f1_score(y_test, y_pred, average='macro'))
# 
# lb = [2, 1]
# ub = [10, 4]
# xopt, fopt = pso(optimise_svc, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# 
# print('The optimum for SVC is at:')
# print('    {}'.format(xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(fopt))
# 
# X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('goalkeeper-samples'), goalkeeper_specific_variables)
# =============================================================================

# =============================================================================
# def optimise_svr(x):
#     kernel_list = ['linear', 'poly', 'rbf', 'sigmoid']
#     shrinking = True if x[5] > 0.5 else False
#     svm = SVR(kernel = kernel_list[int(x[0])], degree=int(x[1]), gamma = x[2], C = x[3], epsilon = x[4], shrinking = shrinking)
#     svm.fit(X_train, y_train)
#     y_pred = svm.predict(X_test)
#     return -(metrics.r2_score(y_test, y_pred))
# 
# lb = [0, 1, 0.5, 0.5, 0.1]
# ub = [3.99, 4, 3, 3, 1]
# xopt, fopt = pso(optimise_svr, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# =============================================================================
# =============================================================================
# def optimise_svr(x):
#     kernel_list = ['linear', 'poly', 'rbf', 'sigmoid']
#     #shrinking = True if x[5] > 0.5 else False
#     svm = SVR(kernel = kernel_list[int(x[0])], degree=2, gamma = x[1], C = x[2], epsilon = x[3])
#     svm.fit(X_train, y_train)
#     y_pred = svm.predict(X_test)
#     return -(metrics.r2_score(y_test, y_pred))
# 
# lb = [0, 0.01, 0.01, 0.01]
# ub = [3.99, 0.5, 0.5, 0.2]
# xopt, fopt = pso(optimise_svr, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# =============================================================================
# =============================================================================
# def optimise_svr(x):
#     #kernel_list = ['linear', 'poly', 'rbf', 'sigmoid']
#     shrinking = True if x[1] > 0.5 else False
#     svm = SVR(kernel = 'rbf', degree=2, gamma = x[0], C = 0.3608172, epsilon = 0.02098194, shrinking = shrinking)
#     svm.fit(X_train, y_train)
#     y_pred = svm.predict(X_test)
#     return -(metrics.r2_score(y_test, y_pred))
# 
# lb = [0.4, 0]
# ub = [0.6, 1]
# xopt, fopt = pso(optimise_svr, lb, ub, omega=0.6, phip=0.6, phig=0.6, maxiter=100, swarmsize=100)
# 
# print('The optimum for SVR is at:')
# print('    {}'.format(xopt))
# print('Optimal function value:')
# print('    myfunc: {}'.format(fopt))
# =============================================================================


# =============================================================================
# knn = KNeighborsClassifier(n_neighbors=8, weights = 'distance', leaf_size = 9, p = 1, n_jobs = -1)
# knn.fit(X_train, y_train)
# y_pred = knn.predict(X_test)
# =============================================================================

# =============================================================================
# rfc = RandomForestClassifier(n_estimators = 8, criterion = 'gini', min_samples_split=8, min_samples_leaf=4).fit(X_train, y_train)
# y_pred = rfc.predict(X_test)
# =============================================================================


#svm = SVC(C = 4.54221665, kernel = 'poly', degree = 2, gamma = 1.30613962)
svm = SVR(kernel = 'rbf', degree=2, gamma = 0.50025385, C = 0.3608172, epsilon = 0.02098194)
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
#print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
print('R-squared: ', metrics.r2_score(y_test, y_pred))
#print('Accuracy: ', metrics.accuracy_score(y_test, y_pred))
#print('F1 score: ', metrics.f1_score(y_test, y_pred, average='macro')) #, labels=np.unique(y_pred)
#print('MCC: ', metrics.matthews_corrcoef(y_test, y_pred))

comparison = np.vstack((y_test, y_pred)).T



#X_train, X_test, y_train, y_test = process_data_for_classification(Dataset().get_dataset('goalkeeper-samples'), goalkeeper_specific_variables)


# =============================================================================
# regressor = LinearRegression(normalize = False, n_jobs = -1) 
# regressor.fit(X_train, y_train)
# 
# y_pred = regressor.predict(X_test)
# print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
# print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
# #print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 
# print('R-squared: ', metrics.r2_score(y_test, y_pred))
# =============================================================================

