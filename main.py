import os
import random
import time
import json

import preprocess
import trigram
import model
import bigram


def clear_directory_files(path):
    for file in os.listdir(path):
        os.remove(path + "/" + file)


# def weighted_random(max_val):
#     randomised = random.random()
#     for i in range(0, max_val):
#         if randomised < 1 / (2 ** (i + 1)):
#             return i


def retrieve_prompt(model_type):  # TODO add suggestion generation?
    invalid_input = True
    while invalid_input:
        prompt = input("Please enter a start prompt or enter \'q\' to quit (Note: \"<cs>\" denotes \"start of contribution\")\n> ")
        if prompt:
            if model_type == "bigram":
                prompt = prompt.split()[-1]
                invalid_input = False
            if model_type == "trigram":
                if len(prompt.split()) > 1:
                    prompt = ' '.join(prompt.split()[-2:])
                    invalid_input = False
                else:
                    print("\nINVALID INPUT: \"" + prompt + "\". Please enter at least two words.\n")

    return prompt


def generate_text(generate_funct, prompt, model_dict_nd):
    num_sentences = random.randint(1, 4)  # randomises the number of sentences to print
    sentences_printed = 0
    prev_token = prompt

    to_print = ""
    while sentences_printed != num_sentences:
        next_token = generate_funct(model_dict_nd, prev_token)

        print_next_word = next_token.split()[-1]  # To ensure the last word is printed and not full trigrams each time

        if print_next_word != "<e>" and print_next_word != "<s>":  # special cases - tags should not be printed
            to_print += " " + print_next_word
        elif next_token.split()[0] == "<e>":
            to_print += "."
            sentences_printed += 1
        prev_token = next_token
    print("\n" + prompt + to_print + "\n")


def init_model(model_dict_str, model_type):
    model_dict = model.strings_to_tuples(model_dict_str)
    match model_type:
        case "bigram":
            model_dict_nd = bigram.dict2d_from_dict(model_dict)
            model_dict_nd = bigram.normalise_counts_2d(model_dict_nd)
            generate_funct = bigram.generate_text_2d  # function to be used set based on
        case "trigram":
            model_dict_nd = trigram.dict3d_from_dict(model_dict)
            model_dict_nd = trigram.normalise_counts_3d(model_dict_nd)
            generate_funct = trigram.generate_text_3d

    prompt = ""
    while prompt != "q":
        prompt = retrieve_prompt(model_type)
        if prompt != "q":
            try:
                generate_text(generate_funct, prompt, model_dict_nd)
            except KeyError:
                print("\n" + prompt + " is not a valid prompt")
    run_menu()


def run_model(model_type):  # TODO investigate double full stop ..
    invalid_choice = True
    while invalid_choice:
        mp = (input("Enter an MP to generate text\n> ") + ".json").lower()

        match model_type:
            case 'bigram':
                model_path = os.getcwd() + "/output/bigram_counts/" + mp
            case 'trigram':
                model_path = os.getcwd() + "/output/trigram_counts/" + mp
            # each normalised at runtime
        if os.path.exists(model_path):
            invalid_choice = False
            f = open(model_path)
            model_dict_str = json.load(f)
            init_model(model_dict_str, model_type)


def run_menu():
    reprint_menu = True
    model_type = "bigram"
    model_index = 0
    models = ["bigram", "trigram", "neural_network"]
    while reprint_menu:
        choice = input("-------------------------\n"
                       f"Current model: {model_type}\n"
                       "-------------------------\n"
                       "Please select an option:\n"  # TODO rework for trigram model
                       "0) Change model type in use\n"
                       "1) Load MP contributions from XML\n"
                       "2) Get " + model_type + " counts\n"  # TODO change menu when providing options for NN
                       "3) Normalise bigram_counts\n"
                       "4) Run model\n"
                       "q) Quit\n\n"
                       "> ")
        reprint_menu = False
        start = time.perf_counter()
        match choice.lower():
            case '0':
                model_index = (model_index + 1) % 2
                model_type = models[model_index]
                reprint_menu = True
            case '1':
                preprocess.load_from_xml()
            case '2':
                if model_type == "neural network":
                    print("\nCannot run this for a neural network model")
                else:
                    model.build_count_files(model_type)
            case '3':
                model.build_normalised_files()
            case '4':
                run_model(model_type)
            case 'q':
                print("quitting...")
                # not an invalid choice
            case _:
                reprint_menu = True

    end = time.perf_counter()
    print(f"{end - start:0.4f} seconds")


def main():
    time.sleep(1)
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

    # Build 2D dictionary
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
