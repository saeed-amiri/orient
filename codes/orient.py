import numpy as np
import pandas as pd
import read_lmp_data as relmp
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
    def __init__(self, obj: relmp.ReadData) -> None:
        print(f'{bcolors.OKCYAN}{self.__class__.__name__}:\n'
              f'\tGetting water moleculs{bcolors.ENDC}')
        self.get_water(obj)
        del obj

    def get_water(self, obj: relmp.ReadData) -> None:
        """get all the atoms and return water mols"""
        water_df: pd.DataFrame  # water part in the dataframe
        box: tuple[float, float, float]  # Length of the box in x, y, z

        water_df = self.get_water_df(obj.Atoms_df)
        box = self.get_box(obj)
        self.get_angles(water_df, box)
        del obj
        return water_df

    def get_water_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """get all the atoms and return water as a DataFrame"""
        # Sort the data frame
        df.sort_values(by=['atom_id'], axis=0, inplace=True)
        # Get O and Hydrogen
        # This should be fixed !!
        water_df = df.loc[(df['typ'] == 4) | (df['typ'] == 5)].copy()
        water_df.reset_index(inplace=True)
        water_df.drop(['index'], inplace=True, axis=1)
        del df
        return water_df

    def get_angles(self,
                   df: pd.DataFrame,
                   box: tuple[float, float, float]) -> None:
        """return angle of the moles"""
        # get the mols index list
        mol_list: list[int]  # index for mols of the water molecules
        mol_list = list(set(df['mol']))
        for mol in mol_list:
            row = df.loc[df['mol'] == mol]
            x, y, z = row['x'], row['y'], row['z']

    def get_box(self, obj: relmp.ReadData) -> tuple[float, float, float]:
        """get the box length in x, y, z direction"""
        boxx: float = np.abs(obj.Xlim[1] - obj.Xlim[0])
        boxy: float = np.abs(obj.Ylim[1] - obj.Ylim[0])
        boxz: float = np.abs(obj.Zlim[1] - obj.Zlim[0])
        del obj
        return boxx, boxy, boxz
