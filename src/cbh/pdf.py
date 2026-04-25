import re

from PyPDF2 import PdfReader

class PDFData:

    def __init__(self, year):

        self.year = year
        self.pdf_path = f"src/files/{year}.pdf"
        self._text = ""

    def _load_text(self):

        if self._text == "":
            reader = PdfReader(self.pdf_path)
            for page in reader.pages:
                self._text += page.extract_text() or ""
            # print(self._text)

    def get_essential_data(self):

        self._load_text()


        grain_received_re = r"^(?:(Tonnes received|Tonnes handled))\s*(?:Mt)\s*(?P<value>[0-9][0-9 .]*)"
        aifr_re = r"^(?:All([- ]time)?[- ]injury frequency rate (\(AIFR\))?)\s*(?P<value>[0-9][0-9 .]*)"
        fertiliser_re = r"^(?:Fertiliser tonnes outturned)\s*(?:t)\s*(?P<value>[0-9][0-9 ,]*)"
        
        revenue_re = r"^(?:Revenue from continuing operations)\s*(?:\$m )\s*(?P<value>[0-9][0-9 ,]*)"
        pool_revenue_re = r"^(?:Pools revenue)\s*(?:\$m)\s*(?P<value>[0-9][0-9 ,]*)"
        othergains_and_losses_re = r"^(?:Other gains and losses)\s*(?:\$m )\s*(?P<value>[0-9() ]*)"
        total_revenue_re = r"^(?:Total revenue including other income)\s*(?:\$m )\s*(?P<value>[0-9][0-9 ,]*)"

        grain_received_list = []
        aifr_list = []
        fertiliser_list = []
        revenue_list = []
        pool_revenue_list = []
        othergains_and_losses_list = []
        total_revenue_list = []

        for line in self._text.splitlines():
            grain_received_match = re.search(grain_received_re, line, re.IGNORECASE)
            if grain_received_match:
                grain_received_list = grain_received_match.group("value").strip().split()
                print("Grain received:", grain_received_list)
            
            aifr_match = re.search(aifr_re, line, re.IGNORECASE)
            if aifr_match:
                aifr_list = aifr_match.group("value").strip().split()
                print("AIFR:", aifr_list)

            fertiliser_match = re.search(fertiliser_re, line, re.IGNORECASE)
            if fertiliser_match:
                fertiliser_list = fertiliser_match.group("value").strip().split()
                print("Fertiliser:", fertiliser_list)

            revenue_match = re.search(revenue_re, line, re.IGNORECASE)
            if revenue_match:
                revenue_list = revenue_match.group("value").strip().split()
                print("Revenue:", revenue_list)

            pool_revenue_match = re.search(pool_revenue_re, line, re.IGNORECASE)
            if pool_revenue_match:
                pool_revenue_list = pool_revenue_match.group("value").strip().split()
                print("Pools Revenue:", pool_revenue_list)

            othergains_and_losses_match = re.search(othergains_and_losses_re, line, re.IGNORECASE)
            if othergains_and_losses_match:
                othergains_and_losses_temp_list = othergains_and_losses_match.group("value").strip().split()
                othergains_and_losses_list = [value.replace("(", "-").replace(")", "") for value in othergains_and_losses_temp_list]
                print("Other Gains and Losses:", othergains_and_losses_list)

            total_revenue_match = re.search(total_revenue_re, line, re.IGNORECASE)
            if total_revenue_match:
                total_revenue_list = total_revenue_match.group("value").strip().split()
                print("Total Revenue:", total_revenue_list)


        # Tonnes sold
        # 2020 125,000 
        # 2019 103,000 
        # 2018 90,000 
        # 2017 64,000
        # 2016 55,000
        
        if not fertiliser_list:
            fertiliser_version_2_re = r"Tonnes sold\s*((?:\d{4}\s[\d,]+\s*)+)"
            fertiliser_list_match = re.search(fertiliser_version_2_re, self._text, re.IGNORECASE)
            if fertiliser_list_match:
                block = fertiliser_list_match.group(1)
                fertiliser_list = [value.replace(",", "") for value in re.findall(r"\d{4}\s([\d,]+)", block)]
                print("Fertiliser (Version 2):", fertiliser_list)


        return (grain_received_list, 
                aifr_list, 
                fertiliser_list, 
                revenue_list, 
                pool_revenue_list, 
                othergains_and_losses_list, 
                total_revenue_list)
            


 