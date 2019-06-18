from pymongo import MongoClient
import pandas as pd
from dataset.dataset import Dataset
from common.common import all_models_variables, goalkeeper_specific_variables, defender_specific_variables, midfielder_specific_variables, forward_specific_variables


position = 'goalkeeper'
position_specific_variables = goalkeeper_specific_variables


dataset = Dataset()
samples_dataframe = dataset.get_dataset(position+'-samples')


model_variables = all_models_variables + position_specific_variables
model_variables.append('score')
samples_dataframe = samples_dataframe[model_variables].dropna()

samples_dataframe = samples_dataframe.astype(float)


undependent_variables = samples_dataframe[all_models_variables + position_specific_variables]
dependent_variable = samples_dataframe["score"]


X_train, X_test, y_train, y_test = train_test_split(defender_undependent_variables, defender_dependent_variable, test_size=0.2, random_state=0)
sc = StandardScaler()
X_train = pd.DataFrame(sc.fit_transform(X_train), index = X_train.index, columns = X_train.columns)
X_test = pd.DataFrame(sc.transform(X_test), index = X_test.index, columns = X_test.columns)