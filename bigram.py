import model


def normalise_counts_2d(counts_2d):
    # sum = 0
    # for word_dict in counts_2d.values():
    #
    #     for count in list.values():
    #         sum += count  # get sum of all values
    #
    #         normalised_counts = {}
    #     for bigram, count in list.items():
    #         normalised_counts[bigram] = count / sum  # get proportion of each value

    normalised_counts_2d = {}
    for first_word, word_dict in counts_2d.items():
        normalised_counts_2d[first_word] = model.normalise_counts(word_dict)

    return normalised_counts_2d


def dict2d_from_dict(bigram_counts):
    # for bigram in bigram_counts.items():
    #     print(bigram[0][0])
    #       bigram[0][0]

    bigram_2d_dict = {}
    bigrams_sorted = sorted(bigram_counts, key=bigram_counts.get, reverse=True)
    for bigram in bigrams_sorted:
        bigram_2d_dict.update({bigram[0]: dict()})  # initialise dictionaries

    for bigram in bigrams_sorted:
        count = bigram_counts.get(bigram)
        bigram_2d_dict.get(bigram[0]).update({bigram[1]: count})  # set value

    return bigram_2d_dict


def generate_text_2d(model_dict_nd, prev_word):
    next_word_list = model_dict_nd[prev_word]
    # get an index for the next word to print at random from most likely candidates
    return model.weighted_random(next_word_list)