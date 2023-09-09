import ast
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def string_to_list(string: str) -> list:
    """ Converts string of list into an actual list

    :param string:
    :return:
    """
    return ast.literal_eval(string)


def to_bag_of_words(data: pd.Series, is_string: bool = True) -> pd.DataFrame:
    """ Creates bag of words dataframe from the inputted column of word lists

    :param
        data: pd.Series of list of words in str format
        is_string: Are the rows in string format instead of list
    :return: bag_of_words dataframe created from the list
    """
    # converts the column into form of a list
    data_as_lists = data
    if is_string:
        data_as_lists = data.apply(string_to_list)

    vec = CountVectorizer()
    bag = vec.fit_transform(data_as_lists.apply(lambda x: ' '.join(x)))

    bag_of_words = pd.DataFrame.sparse.from_spmatrix(bag, columns=vec.get_feature_names_out())
    return bag_of_words
