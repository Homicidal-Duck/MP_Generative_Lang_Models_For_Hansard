import nltk
import torch


def count_words(string, word_counts):
    for word in string.split():
        num_occurrences = word_counts.get(word, 0)  # if the word is in the list, get its value, otherwise get 0
        word_counts.update({word: num_occurrences + 1})  #
    return word_counts


def count_bigrams(string, bigram_counts):
    bigrams = list(nltk.bigrams(string.split()))
    for bigram in bigrams:
        num_occurrences = bigram_counts.get(bigram, 0)  # if the word is in the list, get its value, otherwise get 0
        bigram_counts.update({bigram: num_occurrences + 1})
    # print(*map(' '.join, bigrams), sep=', ')
    return bigram_counts


def dict2D_from_dict(bigram_counts):
    # for bigram in bigram_counts.items():
    #     print(bigram[0][0])
    #       bigram[0][0]

    bigram_2D_dict = {}
    bigrams_sorted = sorted(bigram_counts, key=bigram_counts.get, reverse=True)
    for bigram in bigrams_sorted:
        bigram_2D_dict.update({bigram[0]: dict()})  # initialise dictionaries

    for bigram in bigrams_sorted:
        count = bigram_counts.get(bigram)
        bigram_2D_dict.get(bigram[0]).update({bigram[1]: count})  # set value

    return bigram_2D_dict
    # input()


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


def array_from_dict(bigram_counts):
    # Get indices from keys
    row_indices = list(set([k[0] for k in bigram_counts.keys()]))
    col_indices = list(set([k[1] for k in bigram_counts.keys()]))

    # Create a 2D PyTorch tensor
    tensor_bigrams = torch.zeros(len(row_indices), len(col_indices))

    # Fill in tensor with vals from bigram_counts
    for key, val in bigram_counts.items():
        row_index = row_indices.index(key[0])
        col_index = col_indices.index(key[1])
        tensor_bigrams[row_index, col_index] = val

    return tensor_bigrams
