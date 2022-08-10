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
              f'\tGetting water molecules{bcolors.ENDC}')
        self.get_water(obj)
        del obj

    def get_water(self, obj: relmp.ReadData) -> None:
        """get all the atoms and return water mols"""
        water_df: pd.DataFrame  # water part in the dataframe
        box: tuple[float, float, float]  # Length of the box in x, y, z

        water_df = self.get_water_df(obj.Atoms_df)
        box = self.get_box(obj)
        water_df = self.fix_pbc(water_df, box)
        self.get_angles(water_df)
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

    def fix_pbc(self,
                df: pd.DataFrame,
                box: tuple[float, float, float]) -> pd.DataFrame:
        """apply the correction of the periodic boundry condition
        then, set the nx, ny, nz equal to zero"""
        for i, row in df.iterrows():
            if row['nx'] != 0:
                df.iloc[i]['x'] += box[0]*row['nx']
                df.iloc[i]['nx'] = 0
            if row['ny'] != 0:
                df.iloc[i]['y'] += box[1]*row['ny']
                df.iloc[i]['ny'] = 0
            if row['nz'] != 0:
                df.iloc[i]['z'] += box[2]*row['nz']
                df.iloc[i]['nz'] = 0
        return df

    def get_angles(self, df: pd.DataFrame) -> None:
        """return angle of the moles"""
        # get the mols index list
        mol_list: list[int]  # index for mols of the water molecules
        mol_list = list(set(df['mol']))
        angle_list: list[float] = []  # angles for each mol
        for mol in mol_list:
            row = df.loc[df['mol'] == mol]
            angle_list.append(self.mk_vectors(row))
        average_angles: float  # Average of angles of the data file
        average_angles = np.sum(angle_list)/len(angle_list)
        print(f'{bcolors.OKGREEN}\tAverage angle = '
              f'{average_angles:.4f} [rad] '
              f'(= {np.degrees(average_angles):.4f} [deg]){bcolors.ENDC}\n')
        del df

    def get_box(self, obj: relmp.ReadData) -> tuple[float, float, float]:
        """get the box length in x, y, z direction"""
        boxx: float = np.abs(obj.Xlim[1] - obj.Xlim[0])  # length in x
        boxy: float = np.abs(obj.Ylim[1] - obj.Ylim[0])  # length in y
        boxz: float = np.abs(obj.Zlim[1] - obj.Zlim[0])  # length in z
        del obj
        return boxx, boxy, boxz

    def mk_vectors(self, df: pd.DataFrame) -> float:
        """get each molecule, and return its angle"""
        h_index = 1
        for _, row in df.iterrows():
            x, y, z = row['x'], row['y'], row['z']
            if row['typ'] == 4:
                orgin = np.array([x, y, z])
            elif row['typ'] == 5:
                if h_index == 1:
                    h1 = np.array([x, y, z])
                    h_index += 1
                else:
                    h2 = np.array([x, y, z])
        v1: np.array = orgin-h1  # vector from oxygen towards hydrogen
        v2: np.array = orgin-h2  # vector from oxygen towards hydrogen
        del df
        return self.angle_between_vecs(v1, v2)

    def unit_vector(self, vector: np.array) -> np.array:
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def angle_between_vecs(self, v1: np.array, v2: np.array) -> float:
        """ Returns the angle in radians between vectors 'v1' and 'v2'"""
        v1_u: np.array = self.unit_vector(v1)
        v2_u: np.array = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
