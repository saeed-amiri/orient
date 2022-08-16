import os
import sys
import typing
from colors_text import TextColor as bcolors


class Doc:
    """Read the prompt input file:
    read the file which contains information about what the script must
    do:
    Select which one of the prompt inputs is a data file and which is
    parameters.
    Ex. of input:
        style = angle
        json = YY.data
        data = XX.data
        atoms = O H
    style should be chosen from:
        angle: Calculate the HOH angle for water molecules.
        gyration: Calculate the gyration radius of the decane or
        surfactants.
    if style is gyration then there must be a key:
        tails = CH3
        it is needed for calculating the radius of gyration and it must
        be in the `atoms` key
    JSON file MUST have JSON extension, and the combination script wr-
    ites it. It contains the name, type, and mass of each atom.
    The data file must have one of the following extensions:
        data: written by write_data command in LAMMPS
        dump or lammpstrj was written by dump command in LAMMPS

        Usage example:
            python(V.v) main.py input
        """


class Prompts:
    """get the files names"""
    def __init__(self) -> None:
        self.get_infos()

    def get_infos(self) -> None:
        """read the prompt file to get initial information"""
        info_dict: dict[str, typing.Any]  # Infos in the  prompt file
        fname: str  # Name of the input file
        style: str  # The style of the calculation
        files: list[str]  # The input files
        atoms: str  # Atoms to calculate the simulations
        fname = self.check_infos()
        print(f'{bcolors.OKCYAN}{self.__class__.__name__}:\n'
              f'\tChecking the input file: `{fname}`{bcolors.ENDC}')
        info_dict = self.read_infos(fname)
        style, files = info_dict['style'], info_dict['files']
        self.tails, atoms = info_dict['tails'], info_dict['atoms']
        self.fname, self.jname = self.check_extensions(files)
        self.style = self.get_style(style)
        self.atoms = self.get_atoms(atoms)
        print(f'{bcolors.OKCYAN}'
              f'\tstyle:\t  `{self.style}`\n'
              f'\tdata:\t  `{self.fname}`\n'
              f'\tparamter: `{self.jname}`\n'
              f'\tatoms:\t  `{" & ".join(self.atoms)}`\n'
              f'\ttails:\t  `{self.tails}`{bcolors.ENDC}\n')

    def check_infos(self) -> str:
        """read the prompt file to get initial information"""
        fname: str  # Name of the input file from prompt
        try:
            fname = sys.argv[1]
        except IndexError:
            exit(f'\t{bcolors.FAIL}Error! Input file needed!\n'
                 f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        if not os.path.exists(fname):
            exit(f'\t{bcolors.FAIL}Error! File `{fname}` '
                 f'does not exist{bcolors.ENDC}\n'
                 f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        if os.path.getsize(fname) <= 0:
            exit(f'\t{bcolors.FAIL}Error! File `{fname}` '
                 f'is empty{bcolors.ENDC}\n'
                 f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        return fname

    def read_infos(self,
                   fname: str  # The input file from prompt
                   ) -> dict[str, typing.Any]:
        """read info file to get the information for the calculation"""
        line: str  # Each line of the file
        style: str  # The style of the calculation
        atoms: str  # The name of the atoms to be consider
        tails: str = 'None'  # The name of the tail atom for radius of gyration
        files: list[str] = []  # To save the input files
        return_dict: dict[str, typing.Any] = dict()  # Return keys and values
        atoms_flag: bool = False  # Check if there are atoms defeind
        files_flag: bool = False  # Check if there are files defeind
        style_flage: bool = False  # Check if there is `style` keyword
        tails_flage: bool = False  # Check if there is `tails` keyword
        with open(fname, 'r') as f:
            while True:
                line = f.readline()
                if line.strip().startswith('#'):
                    pass
                elif (line.strip().startswith('data') or
                      line.strip().startswith('json')):
                    f_i = line.split('=')[1].strip()
                    files.append(f_i)
                elif line.strip().startswith('style'):
                    style = line.split('=')[1].strip()
                    return_dict['style'] = style
                    style_flage = True
                elif line.strip().startswith('atoms'):
                    atoms = line.split('=')[1].strip()
                    return_dict['atoms'] = atoms
                    atoms_flag = True
                elif line.strip().startswith('tails'):
                    tails = line.split('=')[1].strip()
                    tails_flage = True
                else:
                    if line.strip():
                        print(f'\t{bcolors.WARNING}Warning: Undefined '
                              f'keyword: `{line}`, Ignored!{bcolors.ENDC}\n')
                if not line:
                    break
        if files:
            files_flag = True
        for flag in (atoms_flag, files_flag, style_flage):
            if not flag:
                exit(f'\t{bcolors.FAIL}Error in input file: `{fname}`:'
                     f'{bcolors.ENDC}\n'
                     f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        files = self.check_files(files)
        return_dict['files'] = files
        if style == 'gyration':
            if not tails_flage:
                exit(f'\t{bcolors.FAIL}Error! Name of the tail atom(s) needed.'
                     f'{bcolors.ENDC}\n'
                     f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
            elif tails not in atoms.strip().split(' '):
                exit(f'\t{bcolors.FAIL}Error! `tails` atom(s): `{tails}`'
                     f' did not found in atoms: `{atoms}`.{bcolors.ENDC}\n'
                     f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        return_dict['tails'] = tails
        return return_dict

    def get_style(self,
                  style: str  # The style written in the info file
                  ) -> str:
        """get the style of the caculation"""
        l_styles: list[str]  # List of available styles
        l_styles = ['angle', 'gyration']
        if style and style in l_styles:
            pass
        else:
            exit(f'{bcolors.FAIL}\tError! The selected style: `{style}`'
                 f' is not valid, choose from: {l_styles}{bcolors.ENDC}\n'
                 f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        return style

    def check_files(self,
                    f_list: list[str]  # File names in info file
                    ) -> list[str]:
        """check if there is enough input files"""
        nfiles: int = len(f_list)
        if nfiles < 2:
            exit(f'\t{bcolors.FAIL}Error! at least two input files; Ex.:\n'
                 f'\tfile.data file.json{bcolors.ENDC}\n'
                 f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        elif nfiles > 2:
            print(f'\t{bcolors.WARNING}Warning: Too many input files!\n'
                  f'\t`{f_list[2:]}` wont be process\n')
        else:
            pass
        self.check_exist(f_list)  # Check if the files are there!
        return f_list[:2]

    def check_exist(self,
                    f_list: list[str]  # File names in info file
                    ) -> None:
        """check if the files are there"""
        for f in f_list:
            if not os.path.exists(f):
                exit(f'\t{bcolors.FAIL}Error! File `{f}` '
                     f'does not exist{bcolors.ENDC}\n'
                     f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
            if os.path.getsize(f) <= 0:
                exit(f'\t{bcolors.FAIL}Error! File `{f}` '
                     f'is empty{bcolors.ENDC}\n'
                     f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')

    def check_extensions(self,
                         f_list: list[str]  # File names in info file
                         ) -> tuple[str, str]:
        """check if the files have the right extensions"""
        f1_ext: str  # Extension of the f1
        f2_ext: str  # Extension of the f2
        data_ext: list[str]  # List of type of the data file
        param_ext: list[str]  # List of type of the parameter file
        fname: str  # Name of the data file
        jname: str  # Name of the parameter file
        data_flag: bool = False  # If we have the data file
        param_flag: bool = False  # If we have the param file
        f1: str = f_list[0]
        f2: str = f_list[1]
        f1_ext = f1.split('.')[1].strip()
        f2_ext = f2.split('.')[1].strip()
        data_ext = ['data', 'dump', 'lammpstrj']
        param_ext = ['json']
        for f, ext in zip([f1, f2], [f1_ext, f2_ext]):
            if ext in data_ext:
                fname = f
                data_flag = True
            if ext in param_ext:
                jname = f
                param_flag = True
        if not (param_flag and data_flag):
            exit(f'{bcolors.FAIL}Error! The input file were not right '
                 f'ones!{bcolors.ENDC}\n'
                 f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        return fname, jname

    def get_atoms(self,
                  atoms: str  # Atoms name from `atoms` line of the info file
                  ) -> list[str]:
        """get the defeind atoms in the info fils"""
        atom_list: list[str]  # To return as a list
        atom_list = atoms.split(' ')
        atom_list = [atom for atom in atom_list if atom]
        atom_list = self.capitaliz_names(atom_list)
        if len(atom_list) != len(set(atom_list)):
            print(f'{bcolors.WARNING}\tThere is a duplicated atom in '
                  f'list: `{atom_list}`, Ignored!')
            atom_list = list(dict.fromkeys(atom_list))  # Drop the duplicates
        if not atoms:
            exit(f'{bcolors.FAIL}\tError! No atom(s) defined! {bcolors.ENDC}\n'
                 f'{bcolors.OKGREEN}\n{Doc.__doc__}{bcolors.ENDC}\n')
        return atom_list

    def capitaliz_names(self,
                        names: list[str]  # List of the atoms name,...
                        ) -> list[str]:
        """make sure all the name are capitalized"""
        names = [name.upper() for name in names]
        return names


if __name__ == '__main__':
    files = Prompts()
