from typing import List

import pandas as pd
from utils.types import domain as d


def convert2TableFormat(
    df: pd.DataFrame,
    domain: d.Swiggy,
    selectedColumns: List[str],
):
    if domain.domainName == "Swiggy":
        return {
            location.name: df[df["Location"] == location.name][
                selectedColumns
            ].reset_index(drop=True)
            for location in domain.locations
        }
