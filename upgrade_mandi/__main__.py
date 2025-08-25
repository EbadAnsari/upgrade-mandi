from os import makedirs

import pandas as pd
from um import main
from utils import config, console, types

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
