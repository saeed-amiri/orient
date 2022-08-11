import os
import sys

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
        self.check_inputs()
        self.check_extensions()
    
    def check_inputs(self) -> None:
        """check if there is enough inputs"""

    def check_extensions(self, f1: str, f2: str) -> None:
        """check if the files have the right extensions"""
        