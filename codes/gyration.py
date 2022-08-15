import numpy as np
import pandas as pd
from colors_text import TextColor as bcolors


class Doc:
    """calculating gyration for decane and surfactants
    based on:
        https://en.wikipedia.org/wiki/Radius_of_gyration

    This script is only for a single snapshot (data from write_data)
    Radius of gyration or R for polymer contain N atom:

        R^2 = (1/N)sum(\abs({r_k - r_{mean}}))^2

    Input:
        Polymer chain coordinates from read_lammps

    """


class RadiusGyration:
    """find the gyration of the input"""
    def __init__(self) -> None:
        pass
