import preprocess
import model


def main():
    all_files = ["S1V0001P0", "S1V0003P0", "S1V0004P0", "S1V0005P0", "S1V0006P0", "S1V0007P0", "S1V0008P0",
                 "S1V0009P0_a", "S1V0009P0_b", "S1V0010P0", "S1V0011P0", "S1V0012P0", "S1V0013P0", "S1V0014P0",
                 "S1V0015P0", "S1V0019P0", "S1V0020P0"]

    word_counts = {}

    for file in all_files:
        preprocessed = preprocess.xml_to_string(file)
        word_counts = model.count_words(preprocessed, word_counts)

    for w in sorted(word_counts, key=word_counts.get, reverse=True):
        print(w + ' : ' + str(word_counts[w]))

    # for word, count in word_counts.items():
    #     print(word + ":" + str(count))


if __name__ == '__main__':
    main()
