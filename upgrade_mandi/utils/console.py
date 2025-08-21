import os
from os.path import join
from typing import List

import inquirer
from utils import config, utils


def selectBox(prompt: str, listOptions: List[str]):
    return inquirer.list_input(prompt, choices=listOptions)


def __question(prompt: str):
    return inquirer.text(prompt)


def prompt(prompt: str):
    return __question(prompt)


def selectRawExcelFile():
    fileNameList = utils.fileInRawSheet()
    if len(fileNameList) == 0:
        print("❌ No raw excel file found in 'raw-sheets-dump' folder.")
        exit(0)
    rootFolder = fileNameList[0].rsplit("\\", 1)[0]
    return join(
        rootFolder,
        selectBox(
            prompt="Select an excel file from 'raw-sheets-dump'",
            listOptions=[fileName.rsplit("\\", 1)[1] for fileName in fileNameList],
        ),
    )


def selectDomain():
    return selectBox(
        prompt="Select domain", listOptions=list(config.domainConfigClass.keys())
    )


def readInvoiceVersion():
    return __question("Enter invoice version")


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    print(selectBox("Select a sheet", ["Sheet 1", "Sheet 2", "Sheet 3"]))
