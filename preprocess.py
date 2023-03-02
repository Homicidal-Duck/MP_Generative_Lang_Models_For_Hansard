import xml.etree.ElementTree as ET
import re
import nltk
import json
import os
import time

nltk.download('punkt')


def tokenise(string):
    extra_abbreviations = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                           's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'hon', 'gent', 'vol', 'col', 'esq', 'rt']
    # Text often followed by a full stop that does not denote the end of the sentence

    tokeniser = nltk.data.load('tokenizers/punkt/english.pickle')
    tokeniser._params.abbrev_types.update(extra_abbreviations)
    # Uses prebuilt file for common abreviations, and updates with those marked in extra_abbreviations

    # tokenised = tokeniser.tokenize(string)
    tokenised = nltk.sent_tokenize(string, language='english')
    tokenised_tagged = ""
    for sent in tokenised:
        tokenised_tagged += " <s> " + sent + " <e> "
    return tokenised_tagged


def process_strings(root):
    string = ""
    hyphenated = False

    for n in root.iter("member"):
        if type(n.text) is str:
            n.text = re.sub("[^a-zA-Z</> \n-]", "", n.text)

    for n in root.itertext():
        if hyphenated:
            init = "<hyphenated>"  # set tag where word is split between lines
            hyphenated = False
        else:
            init = ""
        temp = init + n

        temp = temp.replace("—", " ")
        if "-\n" in temp:
            temp = temp.replace("-\n", "")
            hyphenated = True
        temp = temp.replace("<hyphenated>\n", "")  # remove tag
        temp = temp.replace(",", "")

        # temp = re.sub(r'(?:^|\s)(\w)\.', r'\1', temp)
        string += temp

    return string


def remove_tags(tag_name, root):
    # for n in root.iter(tag_name):
    #     n.text = ""  # seems to work??
    #     for c in n.iter():
    #         c.text = ""

    for n in root.iter():
        if n.tag != "member" and n.tag != "membercontribution":
            n.text = ""

        # print(n.text)
        # n.clear()

    # input() #for waiting to investigate outputs of attribute

    # for n in root.findall('{http://www.w3.org/2001/XMLSchema-instance}col'):
    #     n.remove()

    # for n in root.iter():
    #     for tag in tag_names:
    #         if (n.attrib == tag):
    #             n.remove()

# def get_membercontributions(root):
#     count = 0
#     for i in root.iter("member"):
#         if i.text != "":
#             count = count + 1
#     print("members = " + str(count))
#
#     cont_count = 0
#     for i in root.iter("membercontribution"):
#         cont_count = cont_count + 1
#     print("membercontributions = " + str(cont_count))
#
#     print("diff = " + str(count - cont_count))


def write_contributions_to_file(contributions):
    for name, contribution_list in contributions.items():
        if len(name.split()) < 13 and len(contribution_list) > 2:
            with open("output/MP_contributions/" + name + ".json", "w") as file:
                json.dump(contribution_list, file)
                # todo opened as append, make sure to clear on first open


def append_contribution_to_dict(mp_name, mp_contribution, contributions):
    if not mp_contribution:  # Empty list considered "False"
        return contributions

    if mp_contribution[-1] == "<s>":  # remove trailing "start of sentence" tags
        del mp_contribution[-1]

    if mp_contribution[-1] != "<e>":
        mp_contribution.append("<e>")

    mp_contribution.insert(0, "<cs>")  # start of contribution tag

    name_str = " ".join(mp_name)
    contribution_str = " ".join(mp_contribution)

    contributions.update({name_str: contributions.get(name_str, [])})
    contributions.get(name_str).append(contribution_str)
    return contributions
    # f = open("output/MP_contributions/" + mp_name_str + ".json", "w")
    #
    # print(mp_name_str + " : " + contribution_str)


def process_contributions(contribution_str, contributions):
    mp_name = []
    mp_contribution = []
    do_record_name = False
    do_record_contribution = False
    is_contribution_valid = False
    # contributions = dict()

    word_list = contribution_str.split()
    for word in word_list:

        if do_record_contribution:
            if "</mc>" not in word:
                mp_contribution.append(word)
            else:
                do_record_contribution = False
                if is_contribution_valid:
                    contributions = append_contribution_to_dict(mp_name, mp_contribution, contributions)
                    # write_to_mp_file(mp_name, mp_contribution)
                mp_name.clear()
                mp_contribution.clear()
                is_contribution_valid = False

        if do_record_name:
            if "</m>" not in word:
                mp_name.append(word)
            else:
                do_record_name = False
                if word == "</m><mc>":
                    is_contribution_valid = True
                    do_record_contribution = True
                else:
                    mp_name.clear()

        if word == "<m>":
            do_record_name = True

    return contributions
    # write_contributions_to_file(contributions)


def mark_contributions(root):
    for i in root.iter("member"):
        if type(i.text) is str:  # Ensures the node actually contains text - not always guaranteed it seems
            i.text = " <m> " + i.text + " </m>"

    for i in root.iter("membercontribution"):
        if type(i.text) is str:  # Ensures the node actually contains text
            i.text = "<mc> " + i.text + " </mc> "


def preprocess_xml(file_name):
    root = ET.parse("xml/" + file_name).getroot()

    tags_to_delete = ["col", "title", "td", "writtenanswers"]  # all tags to be deleted

    # for tag in tags_to_delete:
    #     remove_tags(tag, root)
    remove_tags("", root)

    mark_contributions(root)

    # for c in root.iter():
    #     print(c.text, end="")

    string = process_strings(root)
    string = tokenise(string)
    return string


def load_from_xml():
    all_files = []
    contributions = {}

    for xml_file in os.listdir(os.getcwd() + "/xml"):
        all_files.append(xml_file)

    # for xml_file in os.listdir(os.getcwd() + "/xml_test"):
    #     all_files.append(xml_file)
    # debug mode - fewer files to iterate through. todo add debug mode already good heavens

    for file in all_files:
        start_file = time.perf_counter()
        contributions = xml_to_string(file, contributions)
        end_file = time.perf_counter()
        print(file + f" read in {end_file - start_file:0.4f} seconds")

    write_contributions_to_file(contributions)


def xml_to_string(file, contributions):
    xml_string = preprocess_xml(file)
    xml_string = re.sub("[^a-zA-Z</> \n-]", "", xml_string).lower()
    return process_contributions(xml_string, contributions)

    # xml_string = " ".join(xml_string.split())  # works but seems relatively inefficient as far as options go
    # #todo join from splitting done earlier
    # return xml_string
