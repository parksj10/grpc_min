import numpy as np


def read_data_bytes(fullname: str) -> bytes:
    """Reads data bytes from flb file after header

    Args:
        full in filepath, e.g. /path/to/in_file.flz

    Returns:
        bytes: raw data bytes from flb file
    """
    with open(fullname, mode='rb') as binary_file:
        # start from beginning of file
        binary_file.seek(0)
        all_bytes: bytes = binary_file.read()
        return all_bytes[1536:]


def reshape_flb_data(raw_data: bytes,
                     remove_header_bytes: bool = False) -> np.ndarray:
    """Reshape incoming flb data (packed 12 bit structure, see below) to expanded 16 bit int array

    Args:
        raw_data (bytes): raw, packed data bytes of flb file
        remove_header (bool, optional): remove header bytes from raw data if necessary. Defaults to False.

    Returns:
        np.ndarray: output 16 bit, unpacked data array
                
    NOTE: see function for datastructure representation
    """

    # Data
    # Structure:
    #               ---------------------------------
    #               | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    #               |-------------------------------|
    #               |         data1[7:0]            |
    #               |-------------------------------|
    #               | data2[3:0]    | data1[11:8]   |
    #               |-------------------------------|
    #               |           data2[11:4]         |
    #               ---------------------------------
    #                              vv
    # ----------------------------------------------------------------------
    # | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    # | ------------------------------------|-------------------------------|
    # |               empty                 |         data1[7:0]            |
    # | ------------------------------------|-------------------------------|
    # |               empty                 |   data2[3:0]  |  data1[11:8]  |
    # | ------------------------------------|-------------------------------|
    # |               empty                 |         data2[11:4]           |
    # -----------------------------------------------------------------------
    #                              vv
    # ARRAY 1
    # ----------------------------------------------------------------------
    # | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    # | ------------------------------------|-------------------------------|
    # |       empty       |  data1[11:8]    |         data1[7:0]            |
    # -----------------------------------------------------------------------
    # ARRAY 2
    # ----------------------------------------------------------------------
    # | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    # | ------------------------------------|-------------------------------|
    # |       empty       |            data2[11:4]          |  data2[3:0]   |
    # -----------------------------------------------------------------------
    #                              vv
    # OUTPUT (single channel interleved)
    # ----------------------------------------------------------------------
    # | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    # | ------------------------------------|-------------------------------|
    # |       empty       |  data1[11:8]    |         data1[7:0]            |
    # | ------------------------------------|-------------------------------|
    # |       empty       |            data2[11:4]          |  data2[3:0]   |
    # -----------------------------------------------------------------------

    if remove_header_bytes:
        temp_data = np.frombuffer(raw_data, dtype=np.uint8, offset=1536)
    else:
        temp_data = np.frombuffer(raw_data, dtype=np.uint8)

    # recast as 16 bit int for processing
    temp_data = np.array(temp_data, dtype=np.uint16)  # type: ignore
    reshape_data = temp_data.reshape(
        -1, 3)  # reshape to nx3 matrix, -1 causes dimension to be inferred
    # moving bits to above data structure
    # bitwise operations, 15 in binary --> 0000 0000 0000 1111
    temp_data_2 = reshape_data[:, 0] | ((reshape_data[:, 1] << 8) & 0xF)
    temp_data_3 = ((reshape_data[:, 1] >> 4) & 0xF) | (reshape_data[:, 2] << 4)
    # interleave arrays
    output = np.empty((temp_data_2.size + temp_data_3.size),
                      dtype=temp_data_2.dtype)  # type: ignore
    output[0::2] = temp_data_2
    output[1::2] = temp_data_3

    return output
