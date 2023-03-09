import os
import random
import time

import preprocess
import model
import json


def clear_directory_files(path):
    for file in os.listdir(path):
        os.remove(path + "/" + file)


def generate_text(model_dict_str):
    start = time.perf_counter()
    model_dict = model.strings_to_tuples(model_dict_str)
    model_dict_2d = model.dict2D_from_dict(model_dict)
    model_dict_2d = model.normalise_counts_2d(model_dict_2d)  # TODO MAKE WORK LOL
    # print(model_dict_2d)

    num_sentences = random.randint(1, 1)  # randomises the number of sentences to print
    sentences_printed = 0
    prev_word = "<cs>"
    to_print = ""
    while sentences_printed != num_sentences:
        next_word_list = model_dict_2d[prev_word]
        next_word_index = random.randint(0, min(4, len(next_word_list) - 1))
        next_word = list(next_word_list.keys())[next_word_index]

        if next_word != "<e>" and next_word != "<s>":
            to_print += " " + next_word
        elif next_word == "<e>":
            to_print += "."
            sentences_printed += 1
        prev_word = next_word
    print(to_print)
    end = time.perf_counter()
    print(f"generated in {end - start:0.4f} seconds")

def run_model():

    invalid_choice = True
    while invalid_choice:
        mp = (input("Enter an MP to generate text\n> ") + ".json").lower()
        # model_path = os.getcwd() + "/output/normalised_counts/" + mp pre-normalised
        model_path = os.getcwd() + "/output/bigram_counts/" + mp  # normalised at runtime
        if os.path.exists(model_path):
            invalid_choice = False
            f = open(model_path)
            model_dict_str = json.load(f)
            generate_text(model_dict_str)


def run_menu():
    invalid_choice = True
    while invalid_choice:
        choice = input("\nPlease select an option:\n"
                       "1) Load MP contributions from XML\n"
                       "2) Get bigram counts\n"
                       "3) Normalise bigram_counts\n"
                       "4) Run model\n"
                       "q) Quit\n\n"
                       "> ")
        invalid_choice = False
        start = time.perf_counter()
        match choice.lower():
            case '1':
                preprocess.load_from_xml()
            case '2':
                model.build_bigram_count_files()
            case '3':
                model.build_normalised_files()
            case '4':
                run_model()
            case 'q':
                print("quitting...")
                # not an invalid choice
            case _:
                invalid_choice = True

    end = time.perf_counter()
    print(f"{end - start:0.4f} seconds")


# def write_contributions_to_file(contributions):
#     for name, contribution_list in contributions.items():
#         if len(name.split()) < 13 and len(contribution_list) > 2:
#             with open("output/MP_contributions/" + name + ".json", "w") as file:
#                 json.dump(contribution_list, file)


def main():
    run_menu()

    # all_files = []
    #
    # # ["S1V0001P0", "S1V0003P0", "S1V0004P0", "S1V0005P0", "S1V0006P0", "S1V0007P0", "S1V0008P0",
    # #          "S1V0009P0_a", "S1V0009P0_b", "S1V0010P0", "S1V0011P0", "S1V0012P0", "S1V0013P0", "S1V0014P0",
    # #          "S1V0015P0", "S1V0019P0", "S1V0020P0"]
    #
    # for i in range(400, 523):
    #     all_files.append("S5LV0" + str(i) + "P0")
    #
    # # all_files.append("S5LV0406P0")
    #
    # word_counts = {}
    # bigram_counts = {}
    # contributions = {}
    #
    # for file in all_files:
    #     start_file = time.perf_counter()
    #     contributions = preprocess.xml_to_string(file, contributions)
    #     end_file = time.perf_counter()
    #     print(file + f" read in {end_file - start_file:0.4f} seconds")
    #     # print(preprocessed)
    #     # word_counts = model.count_words(preprocessed, word_counts)
    #     # bigram_counts = model.count_bigrams(preprocessed, bigram_counts)
    #
    # write_contributions_to_file(contributions)

    # Build 2D dictionary TODO THIS ONE
    # bigram_2D_dict = model.dict2D_from_dict(bigram_counts)
    # print(bigram_2D_dict)

    # Build 2D array TAKES A LONG TIME - make dense
    # print(model.array_from_dict(bigram_counts))

    # Print word counts to file
    # word_count_file = open("output/word_counts.txt", "w")
    # for w in sorted(word_counts, key=word_counts.get, reverse=True):
    #     word_count_file.write(w + ' : ' + str(word_counts[w]))

    # Print bigram counts to file
    # bigram_count_file = open("output/bigram_counts.txt", "w")
    # for w in sorted(bigram_counts, key=bigram_counts.get, reverse=True):
    #     if(bigram_counts[w] > 3):
    #     #         bigram_count_file.write(str(w) + ' : ' + str(bigram_counts[w]) + '\n')




if __name__ == '__main__':
    main()
