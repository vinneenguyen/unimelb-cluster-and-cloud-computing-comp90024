from mpi4py import MPI
import sys

from utils.process import process_chunk

DATAFILE = sys.argv[1]  # json tweet data
SIZE = MPI.COMM_WORLD.Get_size()  # total number of processes
RANK = MPI.COMM_WORLD.Get_rank()  # process number


def main():
    print("Helloworld! I am process %d of %d.\n" % (RANK, SIZE))
    hashcounts, langcounts = process_chunk(DATAFILE, SIZE, RANK)


main()
