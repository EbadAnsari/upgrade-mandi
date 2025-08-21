import pandas as pd
from um import main
from utils import console, types

if __name__ == "__main__":

    console.clear()

    file = console.selectRawExcelFile()

    sheetNames = pd.ExcelFile(file).sheet_names
    if len(sheetNames) > 1:
        sheetName = console.selectBox("Select a sheet", sheetNames)
    else:
        sheetName = sheetNames[0]
    domain = console.selectDomain()

    date = None
    if domain == "Zepto":
        date = types.Date(
            console.prompt("Enter the date in DD-MM-YYYY format: ").strip()
        )

    invoiceVersion = int(console.readInvoiceVersion())

    main(file, domain, invoiceVersion, sheetName, date)
