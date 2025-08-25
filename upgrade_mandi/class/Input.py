from typing import List, Union

import pandas as pd
from pydantic import BaseModel
from utils import config, console, types


class ReturnType:
    fileName: str
    sheetName: str
    domain: str
    date: types.Date
    locationPo: Union[dict[str, str]]
    invoiceVersion: int


class Input(BaseModel, ReturnType):

    def __selectFile(self):
        return console.selectRawExcelFile()

    def __selectSheet(self):
        sheetNames: List[str] = pd.ExcelFile(self.fileName).sheet_names
        if len(sheetNames) > 1:
            return console.selectBox("Select a sheet", sheetNames)
        return sheetNames[0]

    def __selectDomain(self):
        return console.selectDomain()

    def __selectDate(self):
        return console.prompt("Enter the date in DD-MM-YYYY format: ").strip()

    def __enterPO(self):
        print("Enter PO no for the locations: ")
        return {
            location.name: console.prompt(location.name)
            for location in config.domainConfigClass["Zepto"].locations
        }

    def input(self):
        file = self.__selectFile()
        sheetName = self.__selectSheet()
        domain = self.__selectDomain()

        date = None
        locationPo: dict[str, str] = {}
        if domain == "Zepto":
            date = self.__selectDate()
            haveInvoice = console.yeNo("Have PO no")
            if haveInvoice:
                locationPo = self.__enterPO()

        invoiceVersion = int(console.readInvoiceVersion())

        return (file, sheetName, domain, date, locationPo, invoiceVersion)
