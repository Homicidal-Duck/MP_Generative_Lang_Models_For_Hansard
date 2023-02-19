import xml.etree.ElementTree as ET
import re
import nltk

nltk.download('punkt')


def tokenise(string):
    extra_abbreviations = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                           's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'hon', 'gent', 'vol', 'col']
    # extra_abbreviations.append(list("abcdefghijklmnopqrstuvwxyz"))

    tokeniser = nltk.data.load('tokenizers/punkt/english.pickle')
    tokeniser._params.abbrev_types.update(extra_abbreviations)

    # tokenised = tokeniser.tokenize(string)
    tokenised = nltk.sent_tokenize(string, language='english')
    tokenised_tagged = ""
    for sent in tokenised:
        tokenised_tagged += " <s> " + sent + " <e> "
    return tokenised_tagged


def process_strings(root):
    string = ""
    hyphenated = False

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
    for n in root.iter(tag_name):
        n.text = ""  # seems to work??
        # print(n.text)
        # n.clear()

    # input() #for waiting to investigate outputs of attribute

    # for n in root.findall('{http://www.w3.org/2001/XMLSchema-instance}col'):
    #     n.remove()

    # for n in root.iter():
    #     for tag in tag_names:
    #         if (n.attrib == tag):
    #             n.remove()


def preprocess_xml(file_name):
    root = ET.parse("xml/" + file_name + ".xml").getroot()
    tags_to_delete = ["col", "title", "td"]  # all tags to be deleted
    remove_tags(tags_to_delete, root)

    for tag in tags_to_delete:
        remove_tags(tag, root)

    string = process_strings(root)
    string = tokenise(string)
    return string


def xml_to_string(file):
    xml_string = preprocess_xml(file)
    xml_string = re.sub("[^a-zA-Z<> \n-]", "", xml_string).lower()
    xml_string = " ".join(xml_string.split())  # works but seems relatively inefficient as far as options go
    return xml_string
