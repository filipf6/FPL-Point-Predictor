from methods.linear_regression import preprocessing
from methods.linear_regression import modeling
from dataset.dataset import Dataset
from common.common import goalkeeper_specific_variables, defender_specific_variables, midfielder_specific_variables, forward_specific_variables

def main():
    X_train, X_test, y_train, y_test = preprocessing.process(Dataset().get_dataset('defender-samples'), defender_specific_variables)
    model = modeling.train(X_train, X_test, y_train, y_test)
    #modeling.evaluate(model, X_test, y_train, y_test)
    
    #X_train, X_test, y_train, y_test = preprocessing.process(Dataset().get_dataset('goalkeeper-samples'), goalkeeper_specific_variables)
    #model = modeling.train(X_train, X_test, y_train, y_test)
    
# =============================================================================
#     X_train, X_test, y_train, y_test = preprocessing.process(Dataset().get_dataset('midfielder-samples'), midfielder_specific_variables)
#     model = modeling.train(X_train, X_test, y_train, y_test)
#     
#     X_train, X_test, y_train, y_test = preprocessing.process(Dataset().get_dataset('forward-samples'), forward_specific_variables)
#     model = modeling.train(X_train, X_test, y_train, y_test)
# =============================================================================

main()
