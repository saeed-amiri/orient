import numpy as np
import pandas as pd
from colors_text import TextColor as bcolors
import read_lmp_data as relmp
import read_json as rejs
import get_prompt


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
    def __init__(self,
                 obj: relmp.ReadData,
                 files: get_prompt.Prompts) -> None:
        print(f'{bcolors.OKCYAN}{self.__class__.__name__}:\n'
              f'\tGetting chain molecules{bcolors.ENDC}')
        self.get_chain(obj.Atoms_df, files)

    def get_chain(self,
                  df: pd.DataFrame,  # All the atoms in system
                  files: get_prompt.Prompts  # Data in the info file
                  ) -> None:
        """get the atoms from datafile based on the type"""
        param = rejs.ReadJson(files.jname)  # Name of atoms in the JSON file
        atom_types: dict[str, int]  # Name and type of each atom in the chain
        atom_types = self.get_types(param.df, files.atoms)
        self.chain_df(atom_types, df)

    def get_types(self,
                  df: pd.DataFrame,  # All the atoms coords in the system
                  atoms: list[str]  # Name of the atoms of the chian
                  ) -> dict[str, int]:
        """find the int number for each atom in the json file"""
        param_atoms: list[str]  # Type of atoms in jname
        param_atoms = list(df['name'])
        atom_types: list[int] = []  # List of the types of the atoms
        if not all(x in param_atoms for x in atoms):
            exit(f'\t{bcolors.FAIL}Error! There is no type for one or'
                 f' more of atoms: `{atoms}` in json file{bcolors.ENDC}\n')
        type_dict: dict[str, int]  # Name and type of each atom
        type_dict = {k: v for k, v in zip(df['name'], df['typ']) if k in atoms}
        return type_dict

    def chain_df(self,
                 atoms_types: dict[str, int],  # Wanted atoms name and type
                 df: pd.DataFrame  # All the atoms coords in the system
                 ) -> pd.DataFrame:
        """get the atoms coords for all the chain"""
        i_df: pd.DataFrame  # data for each type
        df_list: list[pd.DataFrame] = []  # append dataframe for each atom
        chains: pd.DataFrame  # Main data to return
        name: str  # Name of each atom
        typ: int  # Type of each atoms
        for name, typ in atoms_types.items():
            i_df = df.loc[df['typ'] == typ]
            df_list.append(i_df)
        chains = pd.concat(df_list)
        chains.sort_values(by=['atom_id'], axis=0, inplace=True)
        return chains
