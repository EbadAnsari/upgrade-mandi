from os import makedirs
from os.path import join

from report import rawToReport
from upgrade_mandi.rawToZeptoSticker import rawToZeptoSticker
from upgrade_mandi.rawToBlinkitSticker import rawToBlinkitSticker
from um import main
from utils import config, console
from utils.read import getSheetNames
from utils.types import date


if __name__ == "__main__":

    makedirs(join(console.root(), "raw-sheets-dump"), exist_ok=True)

    console.clear()

    domain = console.selectDomain(
        list(config.domainConfigClass.keys()) + ["Report", "Zepto Sticker", "Blinkit Sticker"]
    )
    _date = None
    locationPo: dict[str, str] = {}
    if domain == "Zepto":
        _date = date.Date(
            console.prompt("Enter the date in DD-MM-YYYY format: ").strip()
        )
        haveInvoice = console.yesNo("Have PO no")
        if haveInvoice:
            locationPo = {
                location.name: input(f"{location.name}: ")
                for location in config.domainConfigClass["Zepto"].locations
            }
    if domain == "Zepto Sticker":
        shelfLifeFileName = console.select_file_from(console.root(), "shelf-life", "*.xlsx")
        _shelfLifeSheetNames = getSheetNames(shelfLifeFileName)
        if len(_shelfLifeSheetNames) > 1:
            shelfLifeSheetName = console.selectBox("Select a sheet", _shelfLifeSheetNames)
        else:
            shelfLifeSheetName = _shelfLifeSheetNames[0]

        nxFileName = console.select_file_from(console.root(), "nx", "*.xlsx")
        _nxSheetNames = getSheetNames(nxFileName)
        if len(_nxSheetNames) > 1:
            nxSheetName = console.selectBox("Select a sheet", _nxSheetNames)
        else:
            nxSheetName = _nxSheetNames[0]

    if domain == "Blinkit Sticker":
        print(console.root())
        itemIdFileName = console.select_file_from(console.root(), "item-id", "*.xlsx")
        _itemIdSheetNames = getSheetNames(itemIdFileName)
        if len(_itemIdSheetNames) > 1:
            itemIdSheetName = console.selectBox("Select a sheet", _itemIdSheetNames)
        else:
            itemIdSheetName = _itemIdSheetNames[0]

    file = console.selectRawExcelFile()
    sheetNames = getSheetNames(file)
    if len(sheetNames) > 1:
        sheetName = console.selectBox("Select a sheet", sheetNames)
    else:
        sheetName = sheetNames[0]

    if domain == "Report":
        # Handle the "Raw to Report" domain
        rawToReport(file)
    elif domain == "Zepto Sticker":
        # Sticker data
        rawToZeptoSticker(
            file,
            sheetName,
            shelfLifeFileName,
            shelfLifeSheetName,
            nxFileName,
            nxSheetName,
        )
    elif domain == "Blinkit Sticker":
        # Sticker data
        rawToBlinkitSticker(
            file,
            sheetName,
            itemIdFileName,
            itemIdSheetName,
        )
    else:
        invoiceVersion = int(console.readInvoiceVersion())
        main(file, domain, invoiceVersion, sheetName, _date, locationPo)
