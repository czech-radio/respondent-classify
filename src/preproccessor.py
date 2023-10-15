import pandas as pd

import json
import subprocess
import requests
from pandarallel import pandarallel

pandarallel.initialize()

zkratky = {'zast': 'zastupitel', 'kand': 'kandidát', 'posl': 'poslanec'}
main_separator = ';'
interpunkcni_z = '",.;:_!?(){}-'
stopword_file = 'data/stopwords-cs.json'
political_parties = ['ods', 'kdu', 'čsl', 'čssd', 'ano', 'piráti', 'stan', 'ksčm', 'spd', 'top 09', 'ano 2011']


def has_numbers(input_string: str):
    return any(char.isdigit() for char in input_string)


def replace_party(word: str) -> str:
    if word in political_parties:
        return "strana"
    return word


def unify_parties(column: pd.Series) -> pd.Series:
    return column.apply(lambda row: [replace_party(x) for x in row])


def remove_shortened(word: str) -> str:
    if word in zkratky.keys():
        return zkratky[word]
    return word


def remove_shortened_words(column: pd.Series, translations: dict = zkratky) -> pd.Series:
    return column.apply(lambda row: [remove_shortened(x) for x in row])


def remove_interpunctions(column: pd.Series, interpunkcni_z: str = interpunkcni_z, sep: str = ' ') -> pd.Series:
    without_interpunction = column
    for letter in interpunkcni_z:
        without_interpunction = without_interpunction.str.replace(letter, sep)
    return without_interpunction


def split_into_words(column: pd.Series, sep=' ') -> pd.Series:
    return column.str.split(sep)


def remove_stop_words(column: pd.Series, filename: str = stopword_file) -> pd.Series:
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


def correct_word(word: str) -> str:
    url = 'http://localhost/correct?data=' + word
    response = requests.get(url)
    return response.json()['result']


def correct_grammar(column: pd.Series) -> pd.Series:
    return column.parallel_apply(lambda row: [correct_word(word) for word in row])


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

def get_lemma(row: list) -> list:
    if len(row) == 0:
        return row
    words = " ".join(row)
    # print(words)
    url = f'http://localhost:3000/analyze?data={words}&output=vertical&convert_tagset=strip_lemma_id'
    response = requests.get(url)
    return [x.split('\t')[1] for x in response.json()['result'].split('\n') if len(x) != 0]

def get_row_roots(row: list) -> list:
    if len(row) == 0:
        return row
    words = " ".join(row)
    # print(words)
    url = f'http://localhost:3000/analyze?data={words}&derivation=root&output=vertical&convert_tagset=strip_lemma_id'
    response = requests.get(url)
    return [x.split('\t')[1] for x in response.json()['result'].split('\n') if len(x) != 0]


def get_roots(column: pd.Series) -> pd.Series:
    return column.parallel_apply(get_row_roots)


def preprocess_get_roots(column: pd.Series) -> pd.Series:
    column = preprocess_base(column)
    return get_roots(column)

def get_lemmas(column: pd.Series) -> pd.Series:
    return column.parallel_apply(get_lemma)

def preprocess_lemmatize(column: pd.Series) -> pd.Series:
    column = preprocess_base(column)
    return get_lemmas(column)
