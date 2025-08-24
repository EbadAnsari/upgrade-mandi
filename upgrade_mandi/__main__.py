from os import makedirs
from typing import List, Union

import pandas as pd
from pydantic import BaseModel
from um import main
from utils import config, console, types


class ReturnType:
    fileName: str
    sheetName: str
    domain: str
    date: types.Date
    locationPo: Union[dict[str, str]]
    invoiceVersion: int


class Input(BaseModel):

    def __selectFile(self):
        return console.selectRawExcelFile()

    def __selectSheet(self):
        sheetNames: List[str] = pd.ExcelFile(file).sheet_names
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


if __name__ == "__main__":

    makedirs("./raw-sheets-dump", exist_ok=True)

    console.clear()

    file = console.selectRawExcelFile()

    sheetNames = pd.ExcelFile(file).sheet_names
    if len(sheetNames) > 1:
        sheetName = console.selectBox("Select a sheet", sheetNames)
    else:
        sheetName = sheetNames[0]
    domain = console.selectDomain()

    date = None
    locationPo: dict[str, str] = {}
    if domain == "Zepto":
        date = types.Date(
            console.prompt("Enter the date in DD-MM-YYYY format: ").strip()
        )
        haveInvoice = console.yeNo("Have PO no")
        if haveInvoice:
            locationPo = {
                location.name: input(f"{location.name}: ")
                for location in config.domainConfigClass["Zepto"].locations
            }

    invoiceVersion = int(console.readInvoiceVersion())
    main(file, domain, invoiceVersion, sheetName, date, locationPo)
