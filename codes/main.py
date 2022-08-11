import sys
import get_prompt
import read_lmp_data as relmp
import orient
import read_json as rejs


class Doc:
    """read data files from LAMMPS and give spatial orientation.
    For water it will give water orientation,
    For decane it will give the parameter order.
    Input:
        Two main input must be abale to read:
            1- Parameter:
                - JSON file to get the types, ... of the atoms
            2- Data files:
                - data: from `write_data` command
                - traj: from `dump` command
    Output:
        Files contains informations

    Usage:
        python[version] main.py file.data file.json
    """


files = get_prompt.Prompts()
fname = sys.argv[1]  # The data file
jname: str = sys.argv[2]  # The parameters file (json file)
param = rejs.ReadJson(jname)
data = relmp.ReadData(fname)
water = orient.Data(data)
