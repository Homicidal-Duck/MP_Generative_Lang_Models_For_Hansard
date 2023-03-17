import model


def normalise_counts_3d(counts_3d):
    normalised_counts_3d = {}
    for first_word, first_word_dict in counts_3d.items():
        normalised_counts_3d[first_word] = first_word_dict
        for second_word, second_word_dict in first_word_dict.items():
            normalised_counts_3d[first_word][second_word] = model.normalise_counts(second_word_dict)

    return normalised_counts_3d


def dict3d_from_dict(trigram_counts):
    trigram_3d_dict = {}
    trigrams_sorted = sorted(trigram_counts, key=trigram_counts.get, reverse=True)
    for trigram in trigrams_sorted:
        trigram_3d_dict.update({trigram[0]: dict()})

    for trigram in trigrams_sorted:
        trigram_3d_dict.get(trigram[0]).update({trigram[1]: dict()})

    for trigram in trigrams_sorted:
        count = trigram_counts.get(trigram)
        # first_dict = trigram_3D_dict.get(trigram[0])
        # second_dict = first_dict.get(trigram[1])
        # second_dict.update({trigram[2]: count})
        trigram_3d_dict.get(trigram[0]).get(trigram[1]).update({trigram[2]: count})

    return trigram_3d_dict


def generate_text_3d(model_dict_nd, prev_word):
    prev_token_pair = prev_word.split()
    # navigates 3D dictionary based on past two words
    next_word_list = model_dict_nd[prev_token_pair[0]][prev_token_pair[1]]
    next_word = model.weighted_random(next_word_list)
    # next_bigram = list(prev_token_pair[1]).append(list(next_word_list.keys())[next_word_index])
    next_bigram = prev_token_pair[1] + " " + next_word
    return next_bigram
