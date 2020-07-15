#from sendEmail import SendEmail
#from jsonToExcel import JSonToExcel

#send = SendEmail("hgraymundo@gmail.com","outfile.json")
#JSonToExcel("data2020-06-29 10:44","data").convert()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unicodedata
import json
import re
import datetime

from scrapping import Scrapping

_d = Scrapping()
_d.createConnection()
_d.addFilter("MEDICAMENTO")
num_pages = _d.getNumPages()
data = _d.getData(num_pages)
details = _d.getDetails(data)
#GENERAR JSON 
print(json.dumps(details, indent=4, sort_keys=True))

