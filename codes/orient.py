import read_lmp_data as relmp

class Doc:
    """read data files from LAMMPS and give spatial orientation.
    For water it will give water orientation,
    For decane it will give the parameter order.
    Input:
        Two main input must be abale to read:
            data: from `write_data` command
            traj: from `dump` command
    Output:
        Files contains informations
    """

