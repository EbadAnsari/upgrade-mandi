from typing import List

import pandas as pd
from utils import types


def convert2TableFormat(
    df: pd.DataFrame,
    domain: types.Swiggy,
    selectedColumns: List[str],
):
    if domain.domainName == "Swiggy":
        return {
            location.locationName: df[df["Location"] == location.locationName][
                selectedColumns
            ].reset_index(drop=True)
            for location in domain.locations
        }
