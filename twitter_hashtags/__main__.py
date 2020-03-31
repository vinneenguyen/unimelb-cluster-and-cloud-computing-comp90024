# -*- coding: utf-8 -*-

import sys
from mpi4py import MPI

filename = sys.argv[1] # data file
size = MPI.COMM_WORLD.Get_size() # total number of processors
rank = MPI.COMM_WORLD.Get_rank() # processor number

def main():
    print("Helloworld! I am process %d of %d.\n" % (rank, size))
    
main()
