import json
import pandas as pd
from colors_text import TextColor as bcolors


class Doc:
    """read parameters file
    Input:
        is a file with same name as the main data file of LAMMPS which
        is json written by the combination code.
    Output:
        type and name of the atoms
        """


class ReadJson:
    """read the json file"""
    def __init__(self, fname) -> None:
        print(f'{bcolors.OKCYAN}{self.__class__.__name__}:\n'
              f'\tReading parameter file: `{fname}`{bcolors.ENDC}\n')
        self.get_param(fname)

    def get_param(self, fname: str) -> pd.DataFrame:
        with open(fname, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(data["files"][0]['atoms'])
        self.param = data
        del data
        return df
