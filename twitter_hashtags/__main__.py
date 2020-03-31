import sys
from mpi4py import MPI

DATAFILE = sys.argv[1]  # json tweet data
SIZE = MPI.COMM_WORLD.Get_size()  # total number of processors
RANK = MPI.COMM_WORLD.Get_rank()  # processor number


def main():
    print("Helloworld! I am process %d of %d.\n" % (rank, size))


main()
