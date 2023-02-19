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


def init_2D_dict(bigram_counts):
    # for bigram in bigram_counts.items():
    #     print(bigram[0][0])
    #       bigram[0][0]

    # bigram_2D = torch.zeros(len(bigram_counts), len(bigram_counts), dtype=torch.int32)
    bigram_2D_dict = {}
    bigrams_sorted = sorted(bigram_counts, key=bigram_counts.get, reverse=True)
    for bigram in bigrams_sorted:
        bigram_2D_dict.update({bigram[0]: dict()}) #initialise dictionaries

    for bigram in bigrams_sorted:
        count = bigram_counts.get(bigram)
        bigram_2D_dict.get(bigram[0]).update({bigram[1]: count}) #set value

    input()