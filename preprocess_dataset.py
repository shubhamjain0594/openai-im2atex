from utils import *
import cPickle as pickle
import math


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


def create_tokens_dict(tokens):
    """
    Takes tokens list as argument and creats a dict of tokens and their indices
    """
    tokens_dict = {}
    index = 1
    for x in sorted(tokens):
        tokens_dict[x] = index
        index = index + 1
    return tokens_dict


def save_tokens_dict(tokens):
    """
    Saves tokens dictionary to a pickle file
    To load:
    with open('data.p', 'rb') as fp:
        data = pickle.load(fp)
    """
    tokens_dict = create_tokens_dict(tokens)
    with open('data/tokens_dict.p', 'wb') as fp:
        pickle.dump(tokens_dict, fp)
    print("Tokens dictionary saved")


def load_tokens_dict():
    """
    Loads tokens dict
    """
    with open('data/tokens_dict.p', 'r') as fp:
        tokens_dict = pickle.load(fp)
        # print(tokens_dict)
    print("Tokens dictionary loaded")
    return tokens_dict


def create_data_dict(data_mode):
    """
    Creates dictionary of data, formula number as key and image_id as value
    """
    data_dict = {}
    min_formula_num = 2
    with open('data/im2latex_'+data_mode+'.lst') as f:
        for line in f:
            line_comp = line.strip().split(" ")
            formula_num = int(line_comp[0])
            min_formula_num = min(min_formula_num, formula_num)
            image_id = line_comp[1]
            data_dict[formula_num] = image_id
    print("Size of " + data_mode, len(data_dict))
    print("Minimum value of formula number: ", min_formula_num)
    with open('data/im2latex_'+data_mode+'.p', 'wb') as fp:
        pickle.dump(data_dict, fp)


def create_data_sequences():
    """
    Creates a data sequence of tokens indexes for each sequence
    """
    formula_num_tokens_seq_dict = {}
    with open('data/tokens_dict.p', 'r') as fp:
        tokens_dict = pickle.load(fp)
    formula_num = 0
    for tokens_list in _read_data():
        tokens_seq_num = []
        if all(token in tokens_dict for token in tokens_list):
            for token in tokens_list:
                tokens_seq_num.append(tokens_dict[token])
        formula_num_tokens_seq_dict = tokens_seq_num
        formula_num = formula_num + 1
    with open('data/im2latex_formulas_tokens_dict.p', 'wb') as fp:
        pickle.dump(formula_num_tokens_seq_dict, fp)
    print("Created a dictionary of formula number and list of tokens id")


def main():
    # saves a list of tokens to dictionary with key as token and value as token_id
    tokens = tokens_list.get_tokens_list()
    save_tokens_dict(tokens)

    # check if tokens dictionary created
    tokens_dict = load_tokens_dict()

    # creates a data dictionary with keys as formula id and values as image ids
    create_data_dict('train')
    create_data_dict('test')
    create_data_dict('validate')

    # creates a dictionary with keys as formula id and values as list of token ids for the formula
    create_data_sequences()

if __name__ == '__main__':
    main()
