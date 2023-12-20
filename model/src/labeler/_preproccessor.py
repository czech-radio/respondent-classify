import pandas as pd

import json
import requests
from typing import Protocol
from pandarallel import pandarallel
from importlib.resources import files

__all__ = ["RootsPreprocessor", "LemmaPreprocessor", "Preprocessor"]

pandarallel.initialize()

zkratky = {'zast': 'zastupitel', 'kand': 'kandidát', 'posl': 'poslanec'}
MAIN_SEPARATOR = ';'
INTERPUNCTION_MARKS = '",.;:_!?(){}-'
STOPWORDS_FILE = files('labeler.data').joinpath('stopwords-cs.json').read_text()
STOPWORDS_FILE = json.loads(STOPWORDS_FILE)

POLITICAL_PARTIES = ['ods', 'kdu', 'čsl', 'čssd', 'ano', 'piráti', 'stan', 'ksčm', 'spd', 'top 09', 'ano 2011']


def has_numbers(input_string: str):
    return any(char.isdigit() for char in input_string)


def replace_party(word: str) -> str:
    result = word
    if word in POLITICAL_PARTIES:
        result = "strana"
    return result


def unify_parties(column: pd.Series) -> pd.Series:
    return column.apply(lambda row: [replace_party(x) for x in row])


def remove_shortened(word: str) -> str:
    if word in zkratky.keys():
        return zkratky[word]
    return word


def remove_shortened_words(column: pd.Series, translations: dict = zkratky) -> pd.Series:
    return column.apply(lambda row: [remove_shortened(x) for x in row])


def remove_interpunctions(column: pd.Series, interpunkcni_z: str = INTERPUNCTION_MARKS, sep: str = ' ') -> pd.Series:
    without_interpunction = column
    for letter in interpunkcni_z:
        without_interpunction = without_interpunction.str.replace(letter, sep)
    return without_interpunction


def split_into_words(column: pd.Series, sep=' ') -> pd.Series:
    return column.str.split(sep)


def remove_stop_words(column: pd.Series, stopwords: list[str] = STOPWORDS_FILE) -> pd.Series:
    return column.apply(lambda words: [word for word in words if word not in stopwords])


def remove_empty(column: pd.Series) -> pd.Series:
    return column.apply(lambda words: [word for word in words if word != ''])


def remove_numbers(column: pd.Series) -> pd.Series:
    return column.apply(lambda words: [word for word in words if not has_numbers(word)])


def apply_pipeline(column: pd.Series, pipeline: list) -> pd.Series:
    processed = column.copy()
    for func in pipeline:
        processed = func(processed)
    return processed


def lower(column: pd.Series) -> pd.Series:
    return column.str.lower()


def lower_l(column: pd.Series) -> pd.Series:
    return column.apply(lambda x: [a.lower() for a in x])

# Morphodita helper functions


def get_lemma(row: list, service_url: str) -> list:
    if len(row) == 0:
        return row
    words = " ".join(row)
    url = f'{service_url}/analyze?data={words}&output=vertical&convert_tagset=strip_lemma_id'
    response = requests.get(url)
    return [x.split('\t')[1] for x in response.json()['result'].split('\n') if len(x) != 0]


def get_row_roots(row: list, service_url: str) -> list:
    if len(row) == 0:
        return row
    words = " ".join(row)
    url = f'{service_url}/analyze?data={words}&derivation=root&output=vertical&convert_tagset=strip_lemma_id'
    response = requests.get(url)
    return [x.split('\t')[1] for x in response.json()['result'].split('\n') if len(x) != 0]


def get_roots(column: pd.Series, service_url: str) -> pd.Series:
    return column.parallel_apply(lambda row: get_row_roots(row, service_url))


def get_lemmas(column: pd.Series, service_url: str) -> pd.Series:
    return column.parallel_apply(lambda row: get_lemma(row, service_url))


class Preprocessor(Protocol):
    def transform(self, column: pd.Series) -> pd.Series:
        pass


class _BasePreprocessor:
    def __init__(self, korektor_url) -> None:
        self.korektor_url = korektor_url

    def fit(self, column: pd.Series):
        # Just to fill the interface.
        return

    @staticmethod
    def _correct_grammar(column: pd.Series, service_url: str) -> pd.Series:
        
        def _correct_word(word: str, service_url: str) -> str:
            return requests.get(f'{service_url}/correct?data={word}').json()['result']
        
        return column.parallel_apply(lambda row: [_correct_word(word, service_url) for word in row])

    def transform(self, column: pd.Series) -> pd.Series:
        column = remove_interpunctions(column)
        column = split_into_words(column)
        column = remove_empty(column)
        column = lower_l(column)
        column = unify_parties(column)
        column = remove_shortened_words(column)
        column = remove_numbers(column)
        column = self._correct_grammar(column, self.korektor_url)
        column = lower_l(column)
        column = remove_stop_words(column)
        return column

    def fit_transform(self, column: pd.Series):
        self.fit(column)
        return self.transform(column)

    def predict(self, column: pd.Series) -> pd.Series:
        return self.transform(column)

class RootsPreprocessor(_BasePreprocessor):
    """Base class for morphodita based prepreprocesing, for example Roots or Lemmas"""
    def __init__(self, korektor_url: str, morphodita_url: str):
        super().__init__(korektor_url=korektor_url)
        self.morphodita_url = morphodita_url

    def transform(self, column: pd.Series) -> pd.Series:
        column = super().transform(column)
        return get_roots(column, service_url=self.morphodita_url)

    @staticmethod
    def _get_roots(column: pd.Series, service_url) -> pd.Series:
        def _get_row_roots(row: list, service_url: str) -> list:
            if len(row) == 0:
                return row
            words = " ".join(row)
            url = f'{service_url}/analyze?data={words}&derivation=root&output=vertical&convert_tagset=strip_lemma_id'
            response = requests.get(url)
            return [x.split('\t')[1] for x in response.json()['result'].split('\n') if len(x) != 0]

        return column.parallel_apply(lambda row: _get_row_roots(row, service_url))


class LemmaPreprocessor(_BasePreprocessor):

    def __init__(self, korektor_url: str, morphodita_url: str):
        super().__init__(korektor_url=korektor_url)
        self.morphodita_url = morphodita_url

    def transform(self, column: pd.Series) -> pd.Series:
        column = super().transform(column)
        return get_lemmas(column, service_url=self.morphodita_url)
