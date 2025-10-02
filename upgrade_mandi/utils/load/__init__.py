import typer

from .b2b import Customer, loadDateB2B
from .swiggy import loadDataSwiggy
from .zepto import loadDataZepto

if __name__ == "__main__":

    def run(
        file: str = typer.Option(..., "--file", "-f", help="Excel file path"),
        domain: str = typer.Option(
            "Swiggy", "--domain", "-d", help="Domain name ('Swiggy', 'Zomato', etc.)"
        ),
        sheetName: str = typer.Option(
            "Sheet1",
            "--sheet-name",
            "-s",
            help="Sheet name of the Excel file (default: 'Sheet1')",
        ),
    ):
        data = loadDataSwiggy(file, sheetName, domain)  # type: ignore
        print(data)

    typer.run(run)
