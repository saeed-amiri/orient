import get_prompt
import read_lmp_data as relmp
import angle
import gyration


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

if files.style == 'angle':
    data = relmp.ReadData(files.fname)
    water = angle.Angle(data, files)
elif files.style == 'gyration':
    data = relmp.ReadData(files.fname)
    r_gyration = gyration.RadiusGyration(data, files)
