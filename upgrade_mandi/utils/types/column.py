from pydantic import BaseModel


class ColumnDefaultConfig(BaseModel):
    """
    Default configuration for columns.
    This class is used to define the default settings for columns in the domain configuration.
    """

    """ Defines the column name for the configuration."""
    columnName: str = None
