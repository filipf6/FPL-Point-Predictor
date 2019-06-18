from pymongo import MongoClient
import pandas as pd

class Dataset:
    def __init__(self):
        client = MongoClient('mongodb+srv://filipf6:poiuy7u8@fpl-point-predictor-eneet.mongodb.net/test?retryWrites=true')
        self.db = client['fpl-point-predictor']
        
    def get_dataset(self, collection_name):
        defender_samples_collection = self.db[collection_name]
        defender_samples_dataset = defender_samples_collection.find({"score": { '$ne': None }}) 
        return pd.DataFrame(list(defender_samples_dataset))
