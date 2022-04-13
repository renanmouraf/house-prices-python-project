import pickle
import pandas as pd


class HousePriceService():

    def __init__(self, model_file):
        self.model = self.load_model(model_file)
        self.preds = None

    def load_model(self, model):
        pkl_filename = model

        try:
            with open(pkl_filename, 'rb') as file:
                pickle_model = pickle.load(file)
        except:
            print(f'Error loading the model at {pkl_filename}')
            return None

        return pickle_model

    def predict(self, data):

        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data, index=[0])

        self.preds = self.model.predict(data)
        return self.preds
