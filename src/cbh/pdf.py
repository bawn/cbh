from csv import reader
from email.mime import text
import re

from PyPDF2 import PdfReader

class PDFData:

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path

        self._text = ""

    def _load_text(self):

        if self._text == "":
            reader = PdfReader(self.pdf_path)
            for page in reader.pages:
                self._text += page.extract_text() or ""
            print(self._text)
        # print(self._text)

    def get_essential_data(self):

        self._load_text()


 
        grain_received_re = r"(?<=^(Grain received Mt|Tonnes received))([0-9 .]+)"

        re_rules = r"(?<=^Tonnes received Mt)([0-9 .]+)"

        mathch_tonnes_received = re.findall(re_rules, self._text, re.MULTILINE | re.IGNORECASE)
        if not mathch_tonnes_received:
            print("No match found for '" + re_rules + "'")
            return
        tonnes_received_string = mathch_tonnes_received[0] if mathch_tonnes_received else ""
        tonnes_received_list = tonnes_received_string.split()

        print(tonnes_received_list)


    # def get_AIFR(self):

    #     self._load_text()

    #     target_string = "All-injury frequency rate (AIFR)".lower()

    #     mathch_tonnes_received = [x for x in self._text.splitlines() if x.lower().startswith(target_string) and len(x) > len(target_string)]
    #     if not mathch_tonnes_received:
    #         print("No match found for '" + target_string + "'")
    #         return
    #     tonnes_received_string = mathch_tonnes_received[0] if mathch_tonnes_received else ""
    #     tonnes_received_list = [float(x) for x in tonnes_received_string.lower().removeprefix(target_string).split()]

    #     print(tonnes_received_list)



    def get_other_data(self):

        self._load_text()

        return ""
