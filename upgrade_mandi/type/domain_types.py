from dataclasses import dataclass, field
from typing import List, Optional


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
    supplierId: str = "74227878"
    columns: List[ColumnConfig] = field(default_factory=list)
    locations: List[Location] = field(default_factory=dict)
