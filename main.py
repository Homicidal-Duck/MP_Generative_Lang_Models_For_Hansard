import xml.etree.ElementTree as ET
import re

def main():
    load_files()


def remove_tags(tag_name, root):
    for n in root.iter(tag_name):
        n.text = "" #seems to work??
        # print(n.text)
        # n.clear()

    # input() #for waiting to investigate outputs of attribute

    # for n in root.findall('{http://www.w3.org/2001/XMLSchema-instance}col'):
    #     n.remove()

    # for n in root.iter():
    #     for tag in tag_names:
    #         if (n.attrib == tag):
    #             n.remove()

def xml_to_alphanumeric(file_name):
    root = ET.parse("xml/" + file_name + ".xml").getroot()
    tags_to_delete = ["col"]
    # remove_tags(tags_to_delete, root)

    for tag in tags_to_delete:
        remove_tags(tag, root)

    str = ""
    hyphenated = False # search "proposed plan per cents at d shews" in 08 output to check

    for n in root.itertext():

        if (hyphenated):
            init = "" #work this out
            hyphenated = False
        else:
            init = " "
        temp = init + n

        temp = temp.replace("—", " ")
        if ("-\n" in temp):
            temp = temp.replace("-\n", "")
            hyphenated = True
        temp = re.sub("[^a-zA-Z \n-]", "", temp).lower()
        # temp = temp.replace("\n", "")
        # temp = re.sub('s+', ' ', temp)
        str += temp

    str = " ".join(str.split()) #works but seems relatively inefficient as far as options go
    return str

def load_files():
    all_files = ["S1V0008P0"] #todo change back to 1
        # ,"S1V0003P0","S1V0004P0","S1V0005P0","S1V0006P0","S1V0007P0","S1V0008P0","S1V0009P0_a",
        #          "S1V0009P0_b","S1V0010P0","S1V0011P0","S1V0012P0","S1V0013P0","S1V0014P0","S1V0015P0","S1V0019P0",
        #          "S1V0020P0"]

    for n in all_files:
        xml_string = xml_to_alphanumeric(n)
        print(xml_string)

if __name__ == '__main__':
    main()