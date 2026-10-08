import os
from os.path import join
from pathlib import Path
from typing import List, Tuple

import inquirer

from . import config, utils

class ConsolePath:
    @staticmethod
    def root():
        return join(Path.cwd())

    @staticmethod
    def output():
        return join(ConsolePath.root(), "output")

    @staticmethod
    def raw():
        return join(ConsolePath.root(), "raw-sheets-dump")

    @staticmethod
    def data():
        return join(ConsolePath.root(), "data")

    @staticmethod
    def report():
        return join(ConsolePath.root(), "report")

    @staticmethod
    def nx():
        return join(ConsolePath.root(), "nx")

    @staticmethod
    def itemId():
        return join(ConsolePath.root(), "item-id")

    @staticmethod
    def shelfLife():
        return join(ConsolePath.root(), "shelf-life")

def root():
    return join(Path.cwd())


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


def select_file_from(*_folder_path: Tuple[str]) -> str:
    folder_path = join(*_folder_path)
    fileNameList = utils.file_name_sorted(folder_path)
    if len(fileNameList) == 0:
        print(f"❌ No file found in '{folder_path}' folder.")
        exit(0)
    rootFolder = fileNameList[0].rsplit("\\", 1)[0]
    return join(
        rootFolder,
        selectBox(
            prompt=f"Select a file from '{join(*_folder_path[:-1])}'",
            listOptions=[fileName.rsplit("\\", 1)[1] for fileName in fileNameList],
        ),
    )


def selectDomain(domainList: List[str]) -> str:
    return selectBox(prompt="Select domain", listOptions=domainList)


def yesNo(prompt: str):
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
