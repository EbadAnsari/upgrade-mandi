from dataclasses import dataclass, field
from typing import List, Literal, Optional, Union


class Date:
    date: int
    month: int
    year: int

    def __init__(cls, dateString: str):
        split = dateString.split("-")
        if len(split) != 3:
            raise ValueError(f"Invalid date string: {dateString}")

        cls.date, cls.month, cls.year = (num.strip() for num in split)

    def toString(
        self,
        sep="-",
        order: Union[Literal["DMY"], Literal["MDY"], Literal["YMD"]] = "DMY",
    ):
        if len(self.date) == 1:
            self.date = f"0{self.date}"
        if len(self.month) == 1:
            self.month = f"0{self.month}"

        if order == "DMY":
            return f"{self.date}{sep}{self.month}{sep}{self.year}"
        elif order == "MDY":
            return f"{self.month}{sep}{self.date}{sep}{self.year}"
        elif order == "YMD":
            return f"{self.year}{sep}{self.month}{sep}{self.date}"
        else:
            raise ValueError(f"Invalid order: {order}")


@dataclass
class ColumnDefaultConfig:
    """
    Default configuration for columns.
    This class is used to define the default settings for columns in the domain configuration.
    """

    """ Defines the column name for the configuration."""
    columnName: str = None


@dataclass
class Mobile:
    countryCode: str
    number: str

    @property
    def plain(self):
        return f"{self.countryCode}{self.number}"

    @property
    def withSpaces(self):
        chunks = [self.number[i : i + 3] for i in range(0, len(self.number), 3)]
        return f"{self.countryCode} {' '.join(chunks)}"

    @property
    def withHyphens(self):
        chunks = [self.number[i : i + 3] for i in range(0, len(self.number), 3)]
        return f"{self.countryCode}-{'-'.join(chunks)}"

    @property
    def withDots(self):
        chunks = [self.number[i : i + 3] for i in range(0, len(self.number), 3)]
        return f"{self.countryCode}.{' .'.join(chunks)}"

    @property
    def witBrackets(self):
        first = self.number[:3]
        second = self.number[3:6]
        third = self.number[6:]
        return f"{self.countryCode} ({first}) {second}-{third}"

    @property
    def e164(self):
        return f"{self.countryCode}{self.number}"

    def __str__(self):
        return self.format_plain()


@dataclass
class RawSheetConfig(ColumnDefaultConfig):
    pass


@dataclass
class InvoicePdfConfig(ColumnDefaultConfig):
    index: Optional[int] = None
    heading: Optional[bool] = None


@dataclass
class DatabaseConfig(ColumnDefaultConfig):
    columnName: Optional[str]


@dataclass
class ColumnConfig(ColumnDefaultConfig):
    invoicePdf: Optional[InvoicePdfConfig] = None
    rawSheet: Optional[RawSheetConfig] = None
    database: Optional[DatabaseConfig] = None


# DROGHERIA SELLERS PVT LTD,
# DS-NAG-Gokulpeth
# 151 Agrawal building,
# Ravi NagarSquare,
# Gokul peth ward,
# Nagpur 440033


@dataclass
class Address:
    street: str
    # area: str
    city: str
    # state: str
    postal_code: str
    country: str

    def __str__(self):
        # How the address is displayed
        return f"{self.street}, {self.area}, {self.city}, {self.state}, {self.postal_code}, {self.country}"


@dataclass
class VendorConfig:
    name: Union[Literal["Upgrade Mandi"]]
    code: str
    email: str
    mobile: Mobile
    dispatchedAddress: Optional[str] = None
    supplierId: Optional[str] = None


@dataclass
class Location:
    locationName: str
    shippingAddress: str
    retailer: str
    code: str
    storeId: Optional[str] = None
    invoiceVersion: int = 1

    def poNo(self, date: Date, supplierId: str) -> str:
        return f'{date.toString(sep="", order="YMD")}-{self.storeId}-{supplierId}'

    def invoiceNo(self, date: Date, vendorCode: str) -> str:
        return f'{date.toString(sep="")}{vendorCode}{self.code}{self.invoiceVersion}'


@dataclass
class CommonDomainConfig:
    vendor: VendorConfig
    columns: List[ColumnConfig] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    domainName: Union[Literal["Swiggy"], Literal["Zepto"]] = None


@dataclass
class Swiggy(CommonDomainConfig):
    # supplierId: Literal["74227878"]
    pass


@dataclass
class Zepto(CommonDomainConfig):
    pass


DomainSelection = Union[Swiggy, Zepto]
