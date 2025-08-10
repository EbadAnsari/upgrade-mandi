from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class ColumnDefaultConfig:
    """
    Default configuration for columns.
    This class is used to define the default settings for columns in the domain configuration.
    """

    """ Defines the column name for the configuration."""
    columnName: str = None


@dataclass
class RawSheetConfig(ColumnDefaultConfig):
    pass


@dataclass
class InvoicePdfConfig(ColumnDefaultConfig):
    index: Optional[int] = None
    heading: Optional[bool] = None


@dataclass
class DatabaseConfig(ColumnDefaultConfig):
    columnName: str = None


@dataclass
class ColumnConfig(ColumnDefaultConfig):
    invoicePdf: Optional[InvoicePdfConfig] = None
    rawSheet: Optional[RawSheetConfig] = None
    database: Optional[DatabaseConfig] = None


@dataclass
class Location:
    locationName: str
    shippingAddress: str
    retailer: str
    code: str = None
    storeId: str = None


@dataclass
class DomainConfig:
    columns: List[ColumnConfig] = field(default_factory=list)
    locations: List[Location] = field(default_factory=dict)


domainConfig: DomainConfig = DomainConfig(
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
