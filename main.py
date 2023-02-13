import xml.etree.ElementTree as ET
import re




def main():
    load_files()


def xml_to_alphanumeric(file_name):
    root = ET.parse("xml/" + file_name + ".xml").getroot()
    str = ""
    hyphenated = ""
    for n in root.itertext():
        temp = " " + n
        temp = temp.replace("—", " ")
        temp = temp.replace("-\n", "")
        temp = re.sub("[^a-zA-Z \n-]", "", temp).lower()
        temp = temp.replace("\n", "")
        temp = re.sub("\\s+", " ", temp)

        str += temp
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