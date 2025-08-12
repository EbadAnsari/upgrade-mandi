from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Literal, Optional, Union


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
    columnName: Optional[str]


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
    code: str
    storeId: Optional[str]
    invoiceVersion: int = 1

    def poNo(self, date: datetime, supplierId: str) -> str:
        return f'{date.strftime("%Y%m%d")}-{self.storeId}-{supplierId}'

    def invoiceNo(self, date: datetime) -> str:
        return f'{date.strftime("%d%m%Y")}U{self.code}{self.invoiceVersion}'


@dataclass
class CommonDomainConfig:
    columns: List[ColumnConfig] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    domainName: Union[Literal["Swiggy"], Literal["Zepto"]] = None


@dataclass
class VendorConfig:
    vendorName: Union[Literal["Upgrade Mandi"]]
    supplierId: Optional[str] = None


@dataclass
class Swiggy(CommonDomainConfig, VendorConfig):
    # supplierId: Literal["74227878"]
    pass


@dataclass
class Zepto(CommonDomainConfig, VendorConfig):
    pass


SelectDomain = Union[Swiggy, Zepto]
