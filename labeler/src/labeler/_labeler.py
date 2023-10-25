import pickle

import numpy as np

from labeler._preproccessor import preprocess_get_roots
import pandas as pd

MODELS_PATH = 'model/'
NON_POLITIC_MODEL_PATH = MODELS_PATH + 'non_pol.model'
NON_POLITIC_COLUMNS_PATH = MODELS_PATH + 'non_pol_columns'
POLITIC_MODEL_PATH = MODELS_PATH + 'pol.model'
POLITIC_COLUMNS_PATH = MODELS_PATH + 'pol_columns'


class Labeler:
    def __init__(self, model, columns):
        self.model = model
        self.columns = columns

    def label(self, words: list) -> int:
        words = pd.Series(words)
        words = preprocess_get_roots(words)
        words = words[0]
        words_row = np.zeros_like(self.columns)

        # this could be a bottle neck in the future
        # if speed issues happen, this may be the place to redo
        for i, column in enumerate(self.columns):
            if column in words:
                words_row[i] = 1
        return self.model.predict([words_row])[0]

    @staticmethod
    def _load_file(file_path: str):
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def _load_model(model_path: str, columns_path: str):
        model = Labeler._load_file(model_path)
        columns = Labeler._load_file(columns_path)
        return model, columns

    @staticmethod
    def get_non_politic_labeler():
        return Labeler(*Labeler._load_model(NON_POLITIC_MODEL_PATH, NON_POLITIC_COLUMNS_PATH))

    @staticmethod
    def get_politic_labeler():
        return Labeler(*Labeler._load_model(POLITIC_MODEL_PATH, POLITIC_COLUMNS_PATH))


def main():
    model_file = open('model/non_pol.model', 'rb')
    model = pickle.load(model_file)
    columns_file = open('model/non_pol_columns', 'rb')
    columns = pickle.load(columns_file)
    labeler = Labeler.get_politic_labeler()
    print(labeler.label(['umělec']))
    print(labeler.label(['zdravotník']))
    print(labeler.label(['řada', 'vzít']))
    columns_file.close()
    model_file.close()


if __name__ == '__main__':
    main()