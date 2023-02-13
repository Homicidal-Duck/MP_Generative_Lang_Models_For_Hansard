import xml.etree.ElementTree as ET
import re


def main():
    load_files()


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

        temp = re.sub("[^a-zA-Z. \n-]", "", temp).lower()
        # temp = re.sub(r'(?:^|\s)(\w)\.', r'\1', temp)
        string += temp

    return "".join(string.split())  # works but seems relatively inefficient as far as options go


def preprocess_xml(file_name):
    root = ET.parse("xml/" + file_name + ".xml").getroot()
    tags_to_delete = ["col", "title", "td"]  # all tags to be deleted
    remove_tags(tags_to_delete, root)

    for tag in tags_to_delete:
        remove_tags(tag, root)

    string = process_strings(root)
    return string


def load_files():
    all_files = ["S1V0008P0"]  # todo change back to 1
    # ,"S1V0003P0","S1V0004P0","S1V0005P0","S1V0006P0","S1V0007P0","S1V0008P0","S1V0009P0_a",
    # "S1V0009P0_b","S1V0010P0","S1V0011P0","S1V0012P0","S1V0013P0","S1V0014P0","S1V0015P0","S1V0019P0",
    # "S1V0020P0"]

    for n in all_files:
        xml_string = preprocess_xml(n)
        print(xml_string)


if __name__ == '__main__':
    main()
