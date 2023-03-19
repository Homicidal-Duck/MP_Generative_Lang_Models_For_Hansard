import nltk
# import torch
import random
import json
import os

import main


def count_words(string, word_counts):
    for word in string.split():
        num_occurrences = word_counts.get(word, 0)  # if the word is in the list, get its value, otherwise get 0
        word_counts.update({word: num_occurrences + 1})  #
    return word_counts


def count_ngrams(string, ngram_counts, model_type):
    match model_type:
        case "bigram":
            ngrams = list(nltk.bigrams(string.split()))
        case "trigram":
            ngrams = list(nltk.trigrams(string.split()))

    for ngram in ngrams:
        num_occurrences = ngram_counts.get(ngram, 0)  # if the word is in the list, get its value, otherwise get 0
        ngram_counts.update({ngram: num_occurrences + 1})
    # print(*map(' '.join, bigrams), sep=', ')
    return ngram_counts


def weighted_random(word_list):
    randomised = random.random()

    # randomised = 0.5 #TODO REMOVE!!!

    val_sum = 0.0
    num_checks = 0
    for word, val in word_list.items():
        val_sum += val
        if word != "<cs>":  # doesn't allow "start contribution" tags to be used when building sentences
            if val_sum >= randomised:
                return word
            if num_checks > 10:
                return list(word_list.keys())[random.randint(9, len(word_list) - 1)]
        else:
            while word == "<cs>":
                word = list(word_list.keys())[random.randint(0, len(word_list) - 1)]
            return word



# def array_from_dict(bigram_2D_dict, bigram_counts):
#     # bigram_2D_arr = torch.zeros(len(bigram_2D_dict), len(bigram_2D_dict), dtype=torch.int32)
#     # bigrams_sorted = sorted(bigram_counts, key=bigram_counts.get, reverse=True)
#     print(bigram_2D_dict)
#
#     tensor_bigrams = []
#     for row in bigram_2D_dict:
#         tensor_row = torch.tensor(list(row[1].values()))
#         tensor_bigrams.append(tensor_row)
#
#     padded_tensor_bigrams = torch.pad_sequence(tensor_bigrams, batch_first=True)
#     print(padded_tensor_bigrams)


# def clear_model_files():
#     for file in os.listdir(os.getcwd() + "/output/bigram_counts"):
#         os.remove(os.getcwd() + "/output/bigram_counts/" + file)


def strings_to_tuples(str_keys):
    tuple_keys = {}
    for string in str_keys:
        tuple_keys[tuple(string.split(","))] = str_keys[string]
    return tuple_keys


def normalise_counts(ngram_counts):
    sum = 0
    for count in ngram_counts.values():
        sum += count  # get sum of all values

    normalised_counts = {}
    for ngram, count in ngram_counts.items():
        normalised_counts[ngram] = count / sum  # get proportion of each value

    return normalised_counts


def build_normalised_files():  # Unnecessary? Don't think I'll use this
    main.clear_directory_files(os.getcwd() + "/output/normalised_counts")

    bigrams_path = os.getcwd() + "/output/bigram_counts/"
    for bigram_file in os.listdir(bigrams_path):
        f = open(bigrams_path + bigram_file)
        bigram_counts_str = json.load(f)
        bigram_counts = strings_to_tuples(bigram_counts_str)
        normalised_counts = normalise_counts(bigram_counts)

        normalised_counts_str = tuples_to_strings(normalised_counts)
        with open("output/normalised_counts/" + bigram_file, "w") as file:
            json.dump(normalised_counts_str, file)


def tuples_to_strings(tuple_keys):  # Necessary as nltk's "bigrams" function outputs a list of tuples
    str_keys = {}
    for tuple in tuple_keys:
        str_keys[",".join(tuple)] = tuple_keys[tuple]
    return str_keys


def write_counts_to_json(ngram_counts, filename, model_type):
    ngrams_to_write = {}
    for ngram in ngram_counts:
        # if bigram_counts[bigram] > 4: TODO do this more intelligently to avoid filename repeats
        ngrams_to_write[ngram] = ngram_counts[ngram]
    # bigrams_sorted = tuples_to_strings(bigrams_sorted)
    ngrams_to_write_str = tuples_to_strings(ngrams_to_write)
    # bigrams_sorted = sorted(bigrams_to_write_str, key=bigrams_to_write_str.get, reverse=True)
    if len(ngrams_to_write_str) > 30:  # ensures only MPs with sufficient data have their counts recorded TODO tweak
        with open(filename[1:], "w") as file:  # "filename" uses directory with opening '/' so removed here
            json.dump(ngrams_to_write_str, file)


# def build_count_files(path):
#     main.clear_directory_files(path)
#
#     cont_path = os.getcwd() + "output/MP_contributions"


def build_count_files(model_type):
    directory = ""
    match model_type:
        case "bigram":
            directory = "/output/bigram_counts"
            main.clear_directory_files(os.getcwd() + directory)
        case "trigram":
            directory = "/output/trigram_counts"
            main.clear_directory_files(os.getcwd() + directory)

    cont_path = os.getcwd() + "/output/MP_contributions/"
    for cont_file in os.listdir(cont_path):
        print(cont_file)  # todo remove
        f = open(cont_path + cont_file)
        contributions = json.load(f)
        ngram_counts = {}
        for c in contributions:
            ngram_counts = count_ngrams(c, ngram_counts, model_type)

        write_counts_to_json(ngram_counts, directory + '/' + cont_file, model_type)


# TODO only store bigrams that appear more than n times


#     # word_counts = model.count_words(preprocessed, word_counts)
#     # bigram_counts = model.count_bigrams(preprocessed, bigram_counts)


# def array_from_dict(bigram_counts):
#     # Get indices from keys
#     row_indices = list(set([k[0] for k in bigram_counts.keys()]))
#     col_indices = list(set([k[1] for k in bigram_counts.keys()]))
#
#     # Create a 2D PyTorch tensor
#     tensor_bigrams = torch.zeros(len(row_indices), len(col_indices))
#
#     # Fill in tensor with vals from bigram_counts
#     for key, val in bigram_counts.items():
#         row_index = row_indices.index(key[0])
#         col_index = col_indices.index(key[1])
#         tensor_bigrams[row_index, col_index] = val
#
#     return tensor_bigrams
