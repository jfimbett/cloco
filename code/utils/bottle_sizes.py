"""
Module: bottle_sizes.py
Purpose: Convert wine bottle size strings to liters.
         Used by cleaning pipeline and analysis scripts.

This is a verbatim copy of the utility developed by Lucie Bourdychova,
kept as the single source of truth under code/utils/.
"""

import numpy as np


def convert_to_liters(size):
    """
    Convert a wine bottle size string to the corresponding number of liters.

    Parameters
    ----------
    size : str or numeric
        Raw value from the 'Size' column.

    Returns
    -------
    float or np.nan
        Volume in litres, or np.nan if the size is not recognised.

    Notes
    -----
    Covers all size strings observed in the Bordeaux/Burgundy/Rhone auction
    dataset as of 2024. Unknown strings return np.nan (not None) to keep
    dtype consistency across the DataFrame.
    """
    size = str(size).lower().replace(" ", "")  # normalise input
    if size == "750":
        return 0.75
    elif size in ["375", "piccolo"]:
        return 0.375
    elif size in ["500", "620", "pint"]:
        return 0.5
    elif size == "1l":
        return 1.0
    elif size == "magnum":
        return 1.5
    elif size == "jeroboam(4.5l)":
        return 4.5
    elif size == "imperial-6litre":
        return 6.0
    elif size == "rehoboam":
        return 4.5
    elif size == "methuselah":
        return 6.0
    elif size == "salmanazar-9litre":
        return 9.0
    elif size == "balthazar-12litre":
        return 12.0
    elif size == "nebuchadnezzar-15litre":
        return 15.0
    elif size == "melchior-18litre":
        return 18.0
    elif size == "mariejeanne(2.5l)":
        return 2.5
    elif size == "17l":
        return 17.0
    elif size == "2250":
        return 2.25
    elif size == "flacon":
        return 3.0
    elif size == "mainés":
        return 13.5
    elif size == "13500":
        return 13.5
    elif size == "3l":
        return 3.0
    elif size == "4l":
        return 4.0
    elif size == "5l":
        return 5.0
    elif size == "700":
        return 0.7
    elif size == "5500":
        return 5.5
    elif size == "5400":
        return 5.4
    elif size == "4300":
        return 4.3
    elif size == "12000":
        return 12.0
    elif size == "2000":
        return 2.0
    elif size == "800":
        return 0.8
    elif size == "18000":
        return 18.0
    elif size == "720":
        return 0.72
    elif size == "5800":
        return 5.8
    elif size == "3780":
        return 3.78
    else:
        return np.nan  # unrecognised size
