import numpy as np
import h5py

from fuel.datasets import H5PYDataset


def split_hdf5_file(name, train_data, val_data, varlen=False):
    """Generates a split HDF5 file.

    Args:
    name -> string, filepath to save the dataset
    train_data -> numpy array, training data
    val_data -> same as train_data, but validation.
    varlen -> boolean flag indicates whether or not data has variable length.
    """

    if varlen:
        our_dtype = h5py.special_dtype(vlen=np.dtype("int32"))
    else:
        our_dtype = "int32"

    all_data = np.vstack((train_data, val_data))
    split_at = train_data.shape[0]
    data_size = all_data.shape

    with h5py.File(name, mode="w") as f:
        dataset = f.create_dataset("character_seqs", data_size, dtype=our_dtype)
        dataset[...] = all_data

        split_dict = {"train": {"character_seqs": (0, split_at)},
                      "valid": {"character_seqs": (split_at, data_size[1])}}
        f.attrs["split"] = H5PYDataset.create_split_array(split_dict)


def random_train_val_split(data, val_size):
    """Splits data into training and validation sets randomly.

    Expets a numpy array `data` argument and an int `val_size` specifying how big
    the validation size should be.
    Returns tuple (training_data, validation_data)
    """

    val_indices = np.random.choice(a=len(data), replace=False, size=val_size)
    val_set = data[val_indices]
    train_set = np.delete(data, val_indices, 0)
    return (train_set, val_set)