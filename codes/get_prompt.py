import os
import sys
from colors_text import TextColor as bcolors


class Doc:
    """Read the prompt inputs:
    Select which one of the prompt inputs is a data file and which is
    parameters.
    Inputs:
        The style of the caculatoin must be defeined first, between:
            angle: the angle between water molecules
            gyration: the gyration of the decane molecules

        The input file for data should either have: data or dump or
        traj as an extension.
        The input for the parameters must have a JSON extension
        The order does not matter

        Usage example:
            python(V.v) main.py style XX.data YY.json
        """


class Prompts:
    """get the files names"""
    def __init__(self) -> None:
        self.get_names()

    def get_names(self) -> None:
        print(f'{bcolors.OKCYAN}{self.__class__.__name__}:\n'
              f'\tChecking the input files{bcolors.ENDC}')
        f1: str  # First input file
        f2: str  # First input file
        self.style: str  # Style of the calculation
        self.fname: str  # Name of the data file
        self.jname: str  # Name of the parameters file (JSON)
        self.style = self.get_style()
        f1, f2 = self.check_inputs()
        self.check_exist(f1, f2)
        self.fname, self.jname = self.check_extensions(f1, f2)
        print(f'{bcolors.OKCYAN}\tstyle: `{self.style}`, data: '
              f'`{self.fname}` and paramter: `{self.jname}`\n')

    def get_style(self) -> str:
        """get the style of the caculation"""
        l_styles: list[str]  # List of available styles
        l_styles = ['angle', 'gyration']
        style: str = sys.argv[1]
        if style in l_styles:
            pass
        else:
            exit(f'{bcolors.FAIL}\tError! The selected style is not '
                 f'valid, choose from: {l_styles}{bcolors.ENDC}\n'
                 f'{bcolors.OKGREEN}{Doc.__doc__}{bcolors.ENDC}\n')
        return style

    def check_inputs(self) -> tuple[str, str]:
        """check if there is enough inputs"""
        f_list: list[str]  # list of the inputs
        f_list = sys.argv[2:]
        nfiles: int = len(f_list)
        if nfiles < 2:
            exit(f'\t{bcolors.FAIL}Error! at least two input files; Ex.:\n'
                 f'\tfile.data file.json{bcolors.ENDC}\n'
                 f'{bcolors.OKGREEN}{Doc.__doc__}{bcolors.ENDC}\n')
        elif nfiles > 2:
            print(f'\t{bcolors.WARNING}Warning: Too many input files!\n'
                  f'\t{f_list[2:]} wont be process\n')
        else:
            pass
        return f_list[0], f_list[1]

    def check_exist(self, f1, f2) -> None:
        """check if the files are there"""
        for f in [f1, f2]:
            if not os.path.exists(f):
                exit(f'\t{bcolors.FAIL}Error! File `{f}` '
                     f'does not exist{bcolors.ENDC}\n'
                     f'{bcolors.OKGREEN}{Doc.__doc__}{bcolors.ENDC}\n')
            if os.path.getsize(f) <= 0:
                exit(f'\t{bcolors.FAIL}Error! File `{f}` '
                     f'is empty{bcolors.ENDC}\n'
                     f'{bcolors.OKGREEN}{Doc.__doc__}{bcolors.ENDC}\n')

    def check_extensions(self, f1: str, f2: str) -> tuple[str, str]:
        """check if the files have the right extensions"""
        f1_ext: str  # Extension of the f1
        f2_ext: str  # Extension of the f2
        data_ext: list[str]  # List of type of the data file
        param_ext: list[str]  # List of type of the parameter file
        fname: str  # Name of the data file
        jname: str  # Name of the parameter file
        data_flag: bool = False  # If we have the data file
        param_flag: bool = False  # If we have the param file

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
                 f'{bcolors.OKGREEN}{Doc.__doc__}{bcolors.ENDC}\n')
        return fname, jname
