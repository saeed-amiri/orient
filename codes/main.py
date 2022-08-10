import sys
import read_lmp_data as relmp
import orient


class Doc:
    """read data files from LAMMPS and give spatial orientation.
    For water it will give water orientation,
    For decane it will give the parameter order.
    Input:
        Two main input must be abale to read:
            1- Parameter:
                - Some sort of inputs to get the types of the atoms, ...
            2- Data files:
                - data: from `write_data` command
                - traj: from `dump` command
    Output:
        Files contains informations
    """


fname = sys.argv[1]
data = relmp.ReadData(fname)
water = orient.Data(data)
