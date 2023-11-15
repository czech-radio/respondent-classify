import pickle

import numpy as np
import pandas as pd

from labeler._preproccessor import RootsPreprocessor, Preprocessor


class Labeler:
    
    def __init__(self, model, columns, preprocessor: Preprocessor):
        self.model = model
        self.columns = columns
        self.preprocessor = preprocessor

    def label(self, words: list) -> int:
        words = pd.Series(words)
        words = self.preprocessor.transform(words)
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
    def get_non_politic_labeler(korektor_url, morphodita_url, model_paths: tuple[str, str]):
        return Labeler(
            *Labeler._load_model(model_paths[0], model_paths[1]),
                       RootsPreprocessor(korektor_url, morphodita_url))

    @staticmethod
    def get_politic_labeler(korektor_url, morphodita_url, model_paths: tuple[str, str]):
        return Labeler(*Labeler._load_model(model_paths[0], model_paths[1]),
                       RootsPreprocessor(korektor_url, morphodita_url))
