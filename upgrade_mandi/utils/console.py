import os
from os.path import join
from typing import List

import inquirer

from . import config, utils


def selectBox(prompt: str, listOptions: List[str]) -> str:
    return inquirer.list_input(prompt, choices=listOptions)


def prompt(prompt: str):
    return inquirer.text(prompt)


def selectRawExcelFile() -> str:
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


def yeNo(prompt: str):
    response = selectBox(prompt, listOptions=["Yes", "No"])
    if response == "Yes":
        return True
    else:
        return False


def readInvoiceVersion():
    return prompt("Enter invoice version")


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    print(selectBox("Select a sheet", ["Sheet 1", "Sheet 2", "Sheet 3"]))
