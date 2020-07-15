import pandas

class JSonToExcel:
    def __init__(self,jsonFile, excelFile):
        super().__init__()
        self.jsonFile = jsonFile
        self.excelFile = excelFile

    def convert(self):
        pandas.read_json(self.jsonFile + ".json").to_excel(self.excelFile + ".xlsx")
