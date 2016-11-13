from utils import *


def _read_data():
    """
    A generator that iterates over all the lines of the data
    """
    with open('data/im2latex_formulas.lst') as f:
        for line in f:
            # if "A=A_zdz+A_" in line:
                # print(line)
            # if "\RS" in line:
                # print(line)
            yield generate_tokens.get_tokens("\START "+line.strip()+" \END")
    return


def get_unique_tokens(tokens_list):
    """
    Returns unique tokens in a list
    """
    return list(set(tokens_list))


def create_dict():
    """
    Generates a dictionary of tokens, and considers tokens only which occur atleast 10 times
    Finally creates a list of such tokens
    """
    dict_tokens = {}
    for datum in _read_data():
        datum = get_unique_tokens(datum)
        for token in datum:
            if token not in dict_tokens:
                dict_tokens[token] = 1
            else:
                dict_tokens[token] = dict_tokens[token] + 1
    # print(len(dict_tokens))
    # print(dict_tokens)
    unique_dict_tokens = []
    for key in dict_tokens:
        if dict_tokens[key] > 10:
            unique_dict_tokens.append(key)
    print(unique_dict_tokens)
    print(len(unique_dict_tokens))

if __name__ == "__main__":
    create_dict()
