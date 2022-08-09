import numpy as np
import pandas as pd
from colors_text import TextColor as bcolors


class Doc:
    """read data files from LAMMPS and give spatial orientation.
    It will give water orientation,
    Input:
        Two main input must be abale to read:
            data: from `write_data` command
    Output:
        Files contains informations
    """


class Data:
    """get data and calculate the orientation for water"""
    def __init__(self, df: pd.DataFrame) -> None:
        print(f'{bcolors.OKCYAN}{self.__class__.__name__}:\n'
              f'\tGetting water moleculs{bcolors.ENDC}')
        self.get_water_df(df)

    def get_water_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """get all the atoms and return water mols"""
        # Sort the data frame
        df.sort_values(by=['atom_id'], axis=0, inplace=True)
        water_df = df.loc[(df['typ'] == 4) | (df['typ'] == 5)].copy()
        water_df.reset_index(inplace=True)
        water_df.drop(['index'], inplace=True, axis=1)
        del df
        return water_df
