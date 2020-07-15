#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import math
import urls
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

class Scrapping:
    driver = ""

    def __init__(self):
        self.driver = webdriver.Chrome()

    def createConnection(self):
        # os.environ["webdriver.chrome.driver"] = self.chromedriver
        # driver = webdriver.Chrome(self.chromedriver)
        self.driver.implicitly_wait(50)
        self.driver.get(urls.MAIN_URL)
        self.driver.implicitly_wait(50)
        print(":::::: CONNECTED ::::::")

    def addFilter(self, filters):
        # submenu = self.driver.find_element_by_class_name("dijitButtonNode") 
        submenu = self.driver.find_element_by_class_name("dijitInputField")
        ActionChains(self.driver).move_to_element(submenu).click().perform()
        self.driver.implicitly_wait(20)
        submenu1 = self.driver.find_element_by_id("filterPickerSelect_popup1")
        ActionChains(self.driver).move_to_element(submenu1).click().perform()
        self.driver.find_element_by_id("projectInfo_FILTER").send_keys(filters)
        self.driver.implicitly_wait(20)
        javascript = "document.getElementById('filterSearchButton_ANCHOR').onclick();"
        self.driver.execute_script(javascript)
        #self.driver.implicitly_wait(10)
        #dijitReset dijitRight dijitButtonNode dijitArrowButton dijitDownArrowButton dijitArrowButtonContainer

    def addFilterDate(self, _date):
        submenu2 = self.driver.find_element_by_class_name("dijitDownArrowButton")
        ActionChains(self.driver).move_to_element(submenu2).click().perform()
        self.driver.implicitly_wait(10)
        submenu3 = self.driver.find_element_by_id("filterPickerSelect_popup3")
        ActionChains(self.driver).move_to_element(submenu3).click().perform()
        self.driver.find_element_by_id("firstPublishingDate_FILTER_fromDate").send_keys(_date)
        self.driver.implicitly_wait(10)
        #firstPublishingDate_FILTER_OPERATOR_ID
        submenu4 = self.driver.find_element_by_id("firstPublishingDate_FILTER_OPERATOR_ID")
        ActionChains(self.driver).move_to_element(submenu4).click().perform()
        self.driver.implicitly_wait(10)

    
    def clickInSearchButton(self):
        javascript = "document.getElementById('filterSearchButton_ANCHOR').onclick();"
        self.driver.execute_script(javascript)
        self.driver.implicitly_wait(20)

    def getNumPages(self):
        total = self.driver.find_element_by_xpath("//div[@class='columnLeft']//span//strong").text
        rows = self.driver.find_elements_by_xpath("//table[@class='list-table']//tr")
        print("::::::  TOTAL ITEMS => " + str(total))
        num_pages = int(math.ceil(float(total) / float(len(rows)-1)))  # Numero de paginas
        num_pages = num_pages
        print(":::::: NUM PAGES => "+ str(num_pages))
        return num_pages

    def getData(self, num_pages):
        data = []
        for page in range(num_pages):
            num_rows = 0;
            rows = self.driver.find_elements_by_xpath("//table[@class='list-table']//tr")
            self.driver.implicitly_wait(10)
            for row in rows:
                print(row)
                units = row.find_elements_by_xpath("//td[3]")
                refs = row.find_elements_by_xpath("//td[4]")
                desc = row.find_elements_by_xpath("//td[5]")
                types = row.find_elements_by_xpath("//td[6]")
                terms = row.find_elements_by_xpath("//td[7]")
                num_rows += 1
            for r in range(num_rows - 1):
                #print("R >> ")
                #print(r)
            #for r in range(0, 20):
                detail = rows[r + 1].find_element_by_tag_name("a").get_attribute("onclick")
                detail = detail[detail.find("'") + 1:]
                detail = detail[:detail.find("'")]
                d = {
                    "unit": units[r].text,
                    "reference": refs[r].text,
                    "description": desc[r].text,
                    "type": types[r].text,
                    "term": terms[r].text,
                    "uuid_detail": detail,
                    "products": [],
                    "documents": []}
                print(d["unit"] + " ==> " + d["reference"])
                data.append(d)

            if page < num_pages:
                #print("PAGE")
                #print(page)
                #print("NEXT PAGE >>")
                if(page + 1) == num_pages:
                    print('')
                else:
                    if(self.driver.find_element_by_xpath("//div[@class='columnRight']//span[@class='NavBtn']//a[@class='NavBtnForward']")):
                        next_page = self.driver.find_element_by_xpath("//div[@class='columnRight']//span[@class='NavBtn']//a[@class='NavBtnForward']")
                        ActionChains(self.driver).move_to_element(next_page).click().perform()
            else:
                break

        return data

    def getDetails(self, data):
        for index in range(len(data)):
            url_detail = urls.DETAIL_URL_01 + data[index]["uuid_detail"] + urls.DETAIL_URL_02
            print(url_detail)
            self.driver.get(url_detail)
            # file_code = self.driver.find_elements_by_xpath("//div[@class='containerDetail']//div[1]//ul//li[1]//div[2]")
            # print(file_code)
            # print(file_code[0].text)
            # data[index]['file_code'] = file_code[0].text
            
            publication_date = self.driver.find_elements_by_xpath("//div[@class='containerDetail']//div[2]//ul//li[5]//div[2]")
            
            if publication_date:
                data[index]['publication_date'] = publication_date[0].text
            else:
                data[index]['publication_date'] = ""
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_xpath("//a[@class='openNewPage']")
            self.driver.implicitly_wait(10)
            if len(elements) == 0:
                status = 0
                uuid = 'none'
            else:
                status = 1
                element = elements[0].get_attribute("onclick")
                uuid = element[element.find("=") + 1:]
                uuid = uuid[:uuid.find("'")]
            print(data[index]["unit"] + " -- " + data[index]["reference"] + "  DETAILS >> " + uuid)
            data[index]["procedure_status"] = status
            data[index]["uuid_procedure"] = uuid
            documents = self.driver.find_elements_by_xpath("//a")
            for document in documents:
                str = "DownloadProxy"
                if document.get_attribute("href").find(str) > -1:
                    d = {
                        "document": document.text,
                        "url": document.get_attribute("href")
                    }
                    data[index]["documents"].append(d)
        return data

    def searchProduct(self, data):
        for index in range(len(data)):
            print(data[index]["unit"] + " ::: " + data[index]["reference"] + "  DETAILS ::: " + str(data[index]["procedure_status"]) + " - " + str(data[index]["uuid_procedure"]))
            # print("FC => " + str(data[index]["file_code"]) + " ::  PD =>" + str(data[index]["publication_date"]))
            if data[index]["procedure_status"] == 1:
                url_product = urls.PRODUCT_URL
                url_product = url_product + data[index]["uuid_procedure"]
                self.driver.get(url_product)
                self.driver.implicitly_wait(30)
                if len(self.driver.find_elements_by_xpath("//table[11]/tbody/tr")) > 0:
                    print(" IN TABLE  NUMBER 11")
                    _rows = self.driver.find_elements_by_xpath("//table[11]/tbody/tr")  # - 1
                    num_rows = len(_rows)
                    self.driver.implicitly_wait(10)
                    num_columns = len(self.driver.find_elements_by_xpath("//table[11]/tbody/tr[1]/th"))
                    print(" THE TABLE 11 HAVE >>> " + str(num_columns) + " COLUMNS")
                    self.driver.implicitly_wait(10)
                    for index_ in range(1, num_rows):
                        print("THE ROW HAVE >> " + str(
                            len(_rows[index_].find_elements_by_tag_name("td"))) + " COLUMNS")
                        if len(_rows[index_].find_elements_by_tag_name("td")) == 6:
                            p = {
                                "no_control": _rows[index_].find_elements_by_tag_name("td")[0].text.replace(" ", "").replace(".", ""),
                                "description": _rows[index_].find_elements_by_tag_name("td")[1].text,
                                "code": _rows[index_].find_elements_by_tag_name("td")[2].text,
                                "note": _rows[index_].find_elements_by_tag_name("td")[3].text,
                                "unit": _rows[index_].find_elements_by_tag_name("td")[4].text,
                                "quantity": _rows[index_].find_elements_by_tag_name("td")[5].text
                            }
                            print(p)
                            data[index]["products"].append(p)
                        if len(_rows[index_].find_elements_by_tag_name("td")) == 2:
                            p = {
                                "no_control": _rows[index_].find_elements_by_tag_name("td")[0].text.replace(" ", "").replace(".", ""),
                                "description": _rows[index_].find_elements_by_tag_name("td")[1].text,
                                "code": "",
                                "note": "",
                                "unit": "",
                                "quantity": ""
                            }
                            print(p)
                            data[index]["products"].append(p)
                #Table 10
                elif len(self.driver.find_elements_by_xpath("//table[10]/tbody/tr")) > 0:
                    print(" IN TABLE  NUMBER 10")
                    _rows = self.driver.find_elements_by_xpath("//table[10]/tbody/tr")  # - 1
                    num_rows = len(_rows)
                    self.driver.implicitly_wait(10)
                    num_columns = len(self.driver.find_elements_by_xpath("//table[10]/tbody/tr[1]/th"))
                    print(" THE TABLE 10 HAVE >>> " + str(num_columns) + "  COLUMNS")
                    self.driver.implicitly_wait(10)
                    for index_ in range(1, num_rows):
                        print("THIS ROW HAVE >> " + str(
                            len(_rows[index_].find_elements_by_tag_name("td"))) + " COLUMNS")
                        if len(_rows[index_].find_elements_by_tag_name("td")) == 6:
                            p = {
                                "no_control": _rows[index_].find_elements_by_tag_name("td")[0].text.replace(" ", "").replace(".", ""),
                                "description": _rows[index_].find_elements_by_tag_name("td")[1].text,
                                "code": _rows[index_].find_elements_by_tag_name("td")[2].text,
                                "note": _rows[index_].find_elements_by_tag_name("td")[3].text,
                                "unit": _rows[index_].find_elements_by_tag_name("td")[4].text,
                                "quantity": _rows[index_].find_elements_by_tag_name("td")[5].text
                            }
                            print(p)
                            data[index]["products"].append(p)
                        if len(_rows[index_].find_elements_by_tag_name("td")) == 5:
                            p = {
                                "no_control": _rows[index_].find_elements_by_tag_name("td")[0].text.replace(" ", "").replace(".", ""),
                                "description": _rows[index_].find_elements_by_tag_name("td")[1].text,
                                "code": "",
                                "note": _rows[index_].find_elements_by_tag_name("td")[2].text,
                                "unit": _rows[index_].find_elements_by_tag_name("td")[3].text,
                                "quantity": _rows[index_].find_elements_by_tag_name("td")[4].text
                            }
                            print(p)
                            data[index]["products"].append(p)
                        if len(_rows[index_].find_elements_by_tag_name("td")) == 2:
                            p = {
                                "no_control": _rows[index_].find_elements_by_tag_name("td")[0].text.replace(" ", "").replace(".", ""),
                                "description": _rows[index_].find_elements_by_tag_name("td")[1].text,
                                "code": "",
                                "note": "",
                                "unit": "",
                                "quantity": ""
                            }
                            print(p)
                            data[index]["products"].append(p)
                #Table 09
                elif len(self.driver.find_elements_by_xpath("//table[9]/tbody/tr")) > 0:
                    print(" IN TABLE  NUMBER 09")
                    _rows = self.driver.find_elements_by_xpath("//table[9]/tbody/tr")  # - 1
                    num_rows = len(_rows)
                    self.driver.implicitly_wait(10)
                    num_columns = len(self.driver.find_elements_by_xpath("//table[9]/tbody/tr[1]/th"))
                    print(" THE TABLE 09 HAVE >>> " + str(num_columns) + " COLUMNS")
                    self.driver.implicitly_wait(10)
                    for index_ in range(1, num_rows):
                        print("THIS ROW HAVE >> " + str(
                            len(_rows[index_].find_elements_by_tag_name("td"))) + " COLUMNS")
                        if len(_rows[index_].find_elements_by_tag_name("td")) == 6: #6 COLUMNS
                            p = {
                                "no_control": _rows[index_].find_elements_by_tag_name("td")[0].text.replace(" ", "").replace(".", ""),
                                "description": _rows[index_].find_elements_by_tag_name("td")[1].text,
                                "code": _rows[index_].find_elements_by_tag_name("td")[2].text,
                                "note": _rows[index_].find_elements_by_tag_name("td")[3].text,
                                "unit": _rows[index_].find_elements_by_tag_name("td")[4].text,
                                "quantity": _rows[index_].find_elements_by_tag_name("td")[5].text
                            }
                            print(p)
                            data[index]["products"].append(p)

        return data