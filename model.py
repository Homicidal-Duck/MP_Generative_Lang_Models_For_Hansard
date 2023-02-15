def count_words(string, word_counts):
    for word in string.split():
        num_occurrences = word_counts.get(word, 0)  # if the word is in the list, get its value, otherwise get 0
        word_counts.update({word: num_occurrences + 1})  #
    return word_counts
