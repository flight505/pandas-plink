from numpy import zeros
from tqdm import tqdm

from _bed_reader import ffi, lib

@ffi.def_extern()
def cb_iter(pb):
    ffi.from_handle(pb).update(1)


def read_bed(filepath, nrows, ncols, verbose):
    X = zeros((nrows, ncols), int)

    ptr = ffi.cast("uint64_t *", X.ctypes.data)

    nit = 10 if nrows > 10 else nrows

    with tqdm(total=nit, disable=not verbose) as pb:
        pb = ffi.new_handle(pb)
        lib.read_bed(filepath, nrows, ncols, ptr, nit, lib.cb_iter, pb)

    return X
