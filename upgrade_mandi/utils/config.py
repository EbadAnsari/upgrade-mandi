"""
Configuration file for upgrade-mandi data analysis project.
Store all configuration parameters, file paths, and constants here.
"""

import os
from pathlib import Path

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

# File naming conventions
FILE_NAMING = {"date_format": "%Y-%m-%d", "timestamp_format": "%Y%m%d_%H%M%S"}
