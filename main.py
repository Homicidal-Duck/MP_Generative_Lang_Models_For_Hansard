import time

import preprocess
import model
import torch


def main():
    start = time.perf_counter()

    all_files = ["S1V0001P0", "S1V0003P0", "S1V0004P0", "S1V0005P0", "S1V0006P0", "S1V0007P0", "S1V0008P0",
                 "S1V0009P0_a", "S1V0009P0_b", "S1V0010P0", "S1V0011P0", "S1V0012P0", "S1V0013P0", "S1V0014P0",
                 "S1V0015P0", "S1V0019P0", "S1V0020P0"]

    word_counts = {}
    bigram_counts = {}

    for file in all_files:
        preprocessed = preprocess.xml_to_string(file)
        # word_counts = model.count_words(preprocessed, word_counts)
        bigram_counts = model.count_bigrams(preprocessed, bigram_counts)

    # Build 2D dictionary
    bigram_2D_dict = model.dict2D_from_dict(bigram_counts)

    # Build 2D array TAKES A LONG TIME - make dense
    print(model.array_from_dict(bigram_counts))

    # Print word counts to file
    # word_count_file = open("output/word_counts.txt", "w")
    # for w in sorted(word_counts, key=word_counts.get, reverse=True):
    #     word_count_file.write(w + ' : ' + str(word_counts[w]))

    # Print bigram counts to file
    # bigram_count_file = open("output/bigram_counts.txt", "w")
    # for w in sorted(bigram_counts, key=bigram_counts.get, reverse=True):
    #     if(bigram_counts[w] > 3):
    #         bigram_count_file.write(str(w) + ' : ' + str(bigram_counts[w]) + '\n')

    end = time.perf_counter()
    print(f"{end - start:0.4f} seconds")


if __name__ == '__main__':
    main()
