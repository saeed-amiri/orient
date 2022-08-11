import os
import sys
from colors_text import TextColor as bcolors


class Doc:
    """Read the prompt inputs
    Select which one of the prompt inputs is a data file and which is
    parameters.
    Inputs:
        The input file for data should either have: data or dump or
        traj as an extension.
        The input for the parameters must have a JSON extension
        The order does not matter  """


class Prompts:
    """get the files names"""
    def __init__(self) -> None:
        self.get_names()

    def get_names(self) -> None:
        f1: str  # First input file
        f2: str  # First input file
        f1, f2 = self.check_inputs()
        self.check_extensions(f1, f2)

    def check_inputs(self) -> tuple[str, str]:
        """check if there is enough inputs"""
        f_list: list[str]  # list of the inputs
        f_list = sys.argv[1:]
        nfiles: int = len(f_list)
        if nfiles < 2:
            exit(f'\t{bcolors.FAIL}Error! at least two input files; Ex.:\n'
                 f'\tfile.data file.json{bcolors.ENDC}\n')
        elif nfiles > 2:
            print(f'\t{bcolors.OKBLUE}Warning: Too many input files!\n'
                  f'\t {f_list[3:]} wont be process\n')
        else:
            pass
        return f_list[0], f_list[1]

    def check_extensions(self, f1: str, f2: str) -> None:
        """check if the files have the right extensions"""
