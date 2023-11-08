import pandas as pd

import json
import requests
from typing import Protocol
from pandarallel import pandarallel

__all__ = ["RootsPreprocessor", "Preprocessor"]

pandarallel.initialize()

zkratky = {'zast': 'zastupitel', 'kand': 'kandidát', 'posl': 'poslanec'}
MAIN_SEPARATOR = ';'
INTERPUNCTION_MARKS = '",.;:_!?(){}-'
STOPWORDS_FILE = 'data/stopwords-cs.json'
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


def remove_stop_words(column: pd.Series, filename: str = STOPWORDS_FILE) -> pd.Series:
    with open(filename, 'r') as fd:
        stop_words = json.load(fd)
        return column.apply(lambda words: [word for word in words if word not in stop_words])


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


def correct_word(word: str, host: str, port: str | int) -> str:
    url = f'http://{host}:{port}/correct?data={word}'
    response = requests.get(url)
    return response.json()['result']


def correct_grammar(column: pd.Series, host: str, port: str | int) -> pd.Series:
    return column.parallel_apply(lambda row: [correct_word(word, host, port) for word in row])


class Preprocessor(Protocol):
    def transform(self, column: pd.Series) -> pd.Series:
        pass


class BasePreprocessor:
    def __init__(self, korektor_host, korektor_port) -> None:
        self.korektor_host = korektor_host
        self.korektor_port = korektor_port

    def fit(self, column: pd.Series):
        # Just to fill the interface.
        return

    def transform(self, column: pd.Series) -> pd.Series:
        column = remove_interpunctions(column)
        column = split_into_words(column)
        column = remove_empty(column)
        column = lower_l(column)
        column = unify_parties(column)
        column = remove_shortened_words(column)
        column = remove_numbers(column)
        column = correct_grammar(column, self.korektor_host, self.korektor_port)
        column = lower_l(column)
        column = remove_stop_words(column)
        return column

    def fit_transform(self, column: pd.Series):
        self.fit()
        return self.transform(column)


class MorphoditaPreprocessor(BasePreprocessor):
    """Base class for morphodita based prepreprocesing, for example Roots or Lemmas"""
    def __init__(self, korektor_host: str,  korektor_port: str | int, morphodita_host: str, morphodita_port: str | int):
        super().__init__(korektor_host, korektor_port)
        self.morphodita_host = morphodita_host
        self.morphodita_port = morphodita_port

    def transform(self, column: pd.Series) -> pd.Series:
        column = super().transform(column)
        return column


class RootsPreprocessor(MorphoditaPreprocessor):
    def __init__(self, *args):
        super().__init__(*args)

    def transform(self, column: pd.Series) -> pd.Series:
        column = super().transform(column)
        return get_roots(column, self.morphodita_host, self.morphodita_port)


class LemmaPreprocessor(MorphoditaPreprocessor):

    def transform(self, column: pd.Series) -> pd.Series:
        column = super().transform(column)
        return get_lemmas(column, self.morphodita_host, self.morphodita_port)


"""
Commented out, until Preprocessor classes are fully tested


def preprocess_base(column: pd.Series) -> pd.Series:
    column = remove_interpunctions(column)
    column = split_into_words(column)
    column = remove_empty(column)
    column = lower_l(column)
    column = unify_parties(column)
    column = remove_shortened_words(column)
    column = remove_numbers(column)
    column = correct_grammar(column)
    column = lower_l(column)
    column = remove_stop_words(column)
    return column
"""


def get_lemma(row: list, host: str, port: str | int) -> list:
    if len(row) == 0:
        return row
    words = " ".join(row)
    url = f'http://{host}:{port}/analyze?data={words}&output=vertical&convert_tagset=strip_lemma_id'
    response = requests.get(url)
    return [x.split('\t')[1] for x in response.json()['result'].split('\n') if len(x) != 0]


def get_row_roots(row: list, host: str, port: str | int) -> list:
    if len(row) == 0:
        return row
    words = " ".join(row)
    url = f'http://{host}:{port}/analyze?data={words}&derivation=root&output=vertical&convert_tagset=strip_lemma_id'
    response = requests.get(url)
    return [x.split('\t')[1] for x in response.json()['result'].split('\n') if len(x) != 0]


def get_roots(column: pd.Series, roots_host, roots_port) -> pd.Series:
    return column.parallel_apply(lambda row : get_row_roots(row, roots_host, roots_port))


def get_lemmas(column: pd.Series, host: str, port: str | int) -> pd.Series:
    return column.parallel_apply(get_lemma, args=(host, port))
