from PyPDF2 import PdfReader

class PDFData:

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path

        self._textData = []

    def _load_text(self):

        if not self._textData:

            reader = PdfReader(self.pdf_path)

            self._textData = list(page.extract_text() or "" for page in reader.pages)

    def get_grain_received(self):

        self._load_text()

        mathch_tonnes_received = [x for x in self._textData if "Tonnes received Mt" in x]
        if not mathch_tonnes_received:
            print("No match found for 'Tonnes received Mt'")
            return
        tonnes_received_string = mathch_tonnes_received[0] if mathch_tonnes_received else ""
        tonnes_received = [float(x) for x in tonnes_received_string.removeprefix("Tonnes received Mt").split()][0]

        print(tonnes_received)

    def get_other_data(self):

        self._load_text()

        return ""



