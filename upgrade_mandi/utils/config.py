"""
Configuration file for upgrade-mandi data analysis project.
Store all configuration parameters, file paths, and constants here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from type.domain_types import (
    ColumnConfig,
    DatabaseConfig,
    DomainConfig,
    InvoicePdfConfig,
    Location,
    RawSheetConfig,
)

load_dotenv()

NOTION_AUTH = os.getenv("NOTION_AUTH")
NOTION_SWIGGY_DATABASE_ID = os.getenv("NOTION_SWIGGY_DATABASE_ID")

# Project root directory
PROJECT_SRC = Path(__file__).parent

# Data directories
DATA_DIR = PROJECT_SRC / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"

# Source-specific data directories
# BLINK_IT_DIR = RAW_DATA_DIR / "blink_it"
SWIGGY_DIR = RAW_DATA_DIR / "swiggy"
ZEPTO_DIR = RAW_DATA_DIR / "zepto"

# Output directories
OUTPUT_DIR = PROJECT_SRC / "outputs"
REPORTS_DIR = OUTPUT_DIR / "reports"
INVOICES_DIR_PDF = OUTPUT_DIR / "invoices_pdf"


# Data sources configuration
DATA_SOURCES = {
    # "blink_it": {
    #     "name": "Blink It",
    #     "data_dir": BLINK_IT_DIR,
    #     "file_patterns": ["*.csv", "*.json", "*.xlsx"],
    # },
    "swiggy": {
        "name": "Swiggy",
        "data_dir": SWIGGY_DIR,
        "file_patterns": ["*.csv", "*.json", "*.xlsx"],
    },
    "zepto": {
        "name": "Zepto",
        "data_dir": ZEPTO_DIR,
        "file_patterns": ["*.csv", "*.json", "*.xlsx"],
    },
}

# Analysis parameters
ANALYSIS_CONFIG = {
    "date_format": "%Y-%m-%d",
    "default_encoding": "utf-8",
    "chunk_size": 10000,  # For large file processing
    "random_seed": 42,
}

# Visualization settings
VIZ_CONFIG = {
    "figure_size": (12, 8),
    "dpi": 300,
    "style": "seaborn-v0_8",
    "color_palette": "husl",
}

supplierId = "74227878"

domainConfigClass: DomainConfig = DomainConfig(
    columns=[
        ColumnConfig(
            columnName="Article Code",
            invoicePdf=InvoicePdfConfig(columnName="Article Code", index=1),
            rawSheet=RawSheetConfig(columnName="ITEM_CODE"),
            database=DatabaseConfig(columnName="Article Code"),
        ),
        ColumnConfig(
            columnName="Date",
            invoicePdf=InvoicePdfConfig(columnName="Date", heading=True),
            rawSheet=RawSheetConfig(columnName="Date"),
            database=DatabaseConfig(columnName="Date"),
        ),
        ColumnConfig(
            columnName="Dispatched Qty",
            invoicePdf=InvoicePdfConfig(columnName="Dispatched Qty", index=4),
            rawSheet=RawSheetConfig(columnName="Indents"),
            database=DatabaseConfig(columnName="Dispatched Qty"),
        ),
        ColumnConfig(
            columnName="Item Description",
            invoicePdf=InvoicePdfConfig(columnName="Item Description", index=2),
            rawSheet=RawSheetConfig(columnName="PRODUCT_NAME"),
            database=DatabaseConfig(columnName="Item Description"),
        ),
        ColumnConfig(
            columnName="Invoice No",
            invoicePdf=InvoicePdfConfig(columnName="Invoice No", heading=True),
            database=DatabaseConfig(columnName="Invoice No"),
        ),
        ColumnConfig(
            columnName="Invoice Version",
            database=DatabaseConfig(columnName="Invoice Version"),
        ),
        ColumnConfig(
            columnName="Location",
            invoicePdf=InvoicePdfConfig(columnName="Location", heading=True),
            rawSheet=RawSheetConfig(columnName="STORE_NAME"),
            database=DatabaseConfig(columnName="Location"),
        ),
        ColumnConfig(
            columnName="PO No",
            invoicePdf=InvoicePdfConfig(columnName="PO No", heading=True),
            rawSheet=RawSheetConfig(columnName="PO Number"),
            database=DatabaseConfig(columnName="PO No"),
        ),
        ColumnConfig(
            columnName="Rate",
            invoicePdf=InvoicePdfConfig(columnName="Rate", index=6),
            rawSheet=RawSheetConfig(columnName="Cost"),
            database=DatabaseConfig(columnName="Rate"),
        ),
        ColumnConfig(
            columnName="Recieved Qty",
            invoicePdf=InvoicePdfConfig(columnName="Recieved Qty", index=5),
        ),
        ColumnConfig(
            columnName="Retailer",
            invoicePdf=InvoicePdfConfig(columnName="Retailer", heading=True),
            rawSheet=RawSheetConfig(columnName="Entity Name"),
            database=DatabaseConfig(columnName="Retailer"),
        ),
        ColumnConfig(
            columnName="Sr", invoicePdf=InvoicePdfConfig(columnName="Sr", index=0)
        ),
        ColumnConfig(
            columnName="Total Amount",
            invoicePdf=InvoicePdfConfig(columnName="Total Amount", index=7),
            # rawSheet=RawSheetConfig(columnName="Total"),
            database=DatabaseConfig(columnName="Total Amount"),
        ),
        ColumnConfig(
            columnName="UoM",
            invoicePdf=InvoicePdfConfig(columnName="UoM", index=3),
            rawSheet=RawSheetConfig(columnName="WEIGHT"),
            database=DatabaseConfig(columnName="UoM"),
        ),
        ColumnConfig(
            columnName="Vendor Name",
            invoicePdf=InvoicePdfConfig(columnName="Vendor Name", heading=True),
            rawSheet=RawSheetConfig(columnName="VENDOR"),
            database=DatabaseConfig(columnName="Vendor Name"),
        ),
    ],
    locations=[
        Location(
            locationName="Ayodhya Nagar",
            shippingAddress="Gadewar Lawns Plot No.31, 32, 33, 36, 37 And 38, K. H. No, 72/2, Situated At Gadewar Lawn, Shri Ram Wadi",
            retailer="Rajidi Retail Pvt Ltd",
            code="AN",
            storeId="1403419",
        ),
        Location(
            locationName="Byramji",
            shippingAddress="Unit nos - 59 to 71 Lower Ground Floor Ginger Square City Survey No - 1049",
            retailer="Rajidi Retail Pvt Ltd",
            code="B",
            storeId="1392084",
        ),
        Location(
            locationName="Dharampeth",
            shippingAddress="Plot No. 151, CTS No. 135 Puja Sabhagrah, Ravi Nagar Square, Ram Nagar",
            retailer="Swinsta Ent Private Limited",
            code="DH",
            storeId="1397624",
        ),
        Location(
            locationName="Mahal",
            shippingAddress="Unit no - G-1, Plot no.58, sardar patel timber Dhantoli, NAGPUR - 440027",
            retailer="Rajidi Retail Pvt Ltd",
            code="MH",
            storeId="1393571",
        ),
        Location(
            locationName="Manish Nagar",
            shippingAddress='Ground floor "Jayanti Mansion III", Manish nagar Nagpur Maharashtra',
            retailer="Rajidi Retail Pvt Ltd",
            code="MN",
            storeId="1392532",
        ),
        Location(
            locationName="Nandanvan",
            shippingAddress="Vinayak Tower, Lower Ground Floor, Survey No.212 Gurudev Nagar Main Road, New Nanadanvan",
            retailer="Swinsta Ent Private Limited",
            code="NA",
            storeId="1397035",
        ),
        Location(
            locationName="Sai Mandir",
            shippingAddress="Khasra No 18/2, city Survey No.718, House No. 781/B, Situated at Village Ajni",
            retailer="Swinsta Ent Private Limited",
            code="S",
            storeId="1399707",
        ),
    ],
)


domainConfig = {
    "Swiggy": {
        "columns": {
            "Article Code": {
                "invoice-pdf": {"index": 1},
                "raw-sheet-name": {"name": "ITEM_CODE"},
                "notion-column-name": "Article Code",
            },
            "Date": {
                "invoice-pdf": {"heading": True},
                "raw-sheet-name": {"name": "Date"},
                "notion-column-name": "Date",
            },
            "Dispatched Qty": {
                "invoice-pdf": {
                    "index": 4,
                },
                "raw-sheet-name": {"name": "Indents"},
                "notion-column-name": "Dispatched Qty",
            },
            "Item Description": {
                "invoice-pdf": {
                    "index": 2,
                },
                "raw-sheet-name": {"name": "PRODUCT_NAME"},
                "notion-column-name": "Item Description",
            },
            "Invoice No": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-column-name": "Invoice No",
            },
            "Invoice Version": {
                "notion-column-name": "Invoice Version",
            },
            "Location": {
                "invoice-pdf": {
                    "heading": True,
                },
                "raw-sheet-name": {"name": "STORE_NAME"},
                "notion-column-name": "Location",
            },
            "PO No": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-column-name": "PO No",
                "raw-sheet-name": {"name": "PO Number"},
            },
            "Rate": {
                "invoice-pdf": {
                    "index": 6,
                },
                "raw-sheet-name": {"name": "Cost"},
                "notion-column-name": "Rate",
            },
            "Recieved Qty": {
                "invoice-pdf": {
                    "index": 5,
                },
                "notion-database": False,
            },
            "Retailer": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-column-name": "Retailer",
                "raw-sheet-name": {"name": "Entity Name"},
            },
            "Sr": {
                "invoice-pdf": {
                    "index": 0,
                },
                "notion-database": False,
            },
            "Total Amount": {
                "invoice-pdf": {
                    "index": 7,
                },
                "notion-column-name": "Total Amount",
            },
            "UoM": {
                "invoice-pdf": {
                    "index": 3,
                },
                "raw-sheet-name": {"name": "WEIGHT"},
                "notion-column-name": "UoM",
            },
            "Vendor Name": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-column-name": "Vendor Name",
                "raw-sheet-name": {"name": "VENDOR"},
            },
        },
        "input-columns": [
            "Article Code",
            "Dispatched Qty",
            "Item Description",
            "Rate",
            "Total Amount",
            "UoM",
        ],
        "database-columns": [
            "Article Code",
            "Date",
            "Dispatched Qty",
            "Invoice No",
            "Invoice Version",
            "Item Description",
            "Location",
            "Rate",
            "Total Amount",
            "UoM",
        ],
        "output-columns": [
            "Article Code",
            "Dispatched Qty",
            "Item Description",
            "Rate",
            "Recieved Qty",
            "Sr",
            "Total Amount",
            "UoM",
        ],
        "locations": {
            "Ayodhya Nagar": {
                "shipping-address": "Gadewar Lawns Plot No.31, 32, 33, 36, 37 And 38, K. H. No, 72/2, Situated At Gadewar Lawn, Shri Ram Wadi",
                "retailer": "Rajidi",
                "code": "AN",
                "storeId": "1403419",
            },
            "Byramji": {
                "shipping-address": "Unit nos - 59 to 71 Lower Ground Floor Ginger Square City Survey No - 1049",
                "retailer": "Rajidi",
                "code": "B",
                "storeId": "1392084",
            },
            "Dharampeth": {
                "shipping-address": "Plot No. 151, CTS No. 135 Puja Sabhagrah, Ravi Nagar Square, Ram Nagar",
                "retailer": "Swinsta",
                "code": "DH",
                "storeId": "1397624",
            },
            "Mahal": {
                "shipping-address": "Unit no - G-1, Plot no.58, sardar patel timber Dhantoli, NAGPUR - 440027",
                "retailer": "Rajidi",
                "code": "MH",
                "storeId": "1393571",
            },
            "Manish Nagar": {
                "shipping-address": 'Ground floor "Jayanti Mansion III", Manish nagar Nagpur Maharashtra',
                "retailer": "Rajidi",
                "code": "MN",
                "storeId": "1392532",
            },
            "Nandanvan": {
                "shipping-address": "Vinayak Tower, Lower Ground Floor, Survey No.212 Gurudev Nagar Main Road, New Nanadanvan",
                "retailer": "Swinsta",
                "code": "NA",
                "storeId": "1397035",
            },
            "Sai Mandir": {
                "shipping-address": "Khasra No 18/2, city Survey No.718, House No. 781/B, Situated at Village Ajni",
                "retailer": "Swinsta",
                "code": "S",
                "storeId": "1399707",
            },
        },
    },
    "Zepto": {
        "columns": [
            "No",
            "Article Name",
            "UoM",
            "Invoice Qty.",
            "Rate",
            "Amount",
        ],
        "locations": {
            "Gokulpeth": {"shipping-address": "", "retailer": "Dorgheria"},
            "Mahada": {"shipping-address": "", "retailer": "Dorgheria"},
            "Khamla": {"shipping-address": "", "retailer": "Dorgheria"},
            "Garoba Maidan": {"shipping-address": "", "retailer": "Dorgheria"},
            "Raghuji Nagar": {"shipping-address": "", "retailer": "Dorgheria"},
            "Zingabai Takli": {"shipping-address": "", "retailer": "Dorgheria"},
            "Bhupesh Nagar": {"shipping-address": "", "retailer": "Dorgheria"},
            "Besa": {"shipping-address": "", "retailer": "Dorgheria"},
        },
    },
}
