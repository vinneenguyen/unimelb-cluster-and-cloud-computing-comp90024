# -*- coding: utf-8 -*-

from mpi4py import MPI
import sys

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()

def main():
    print("Helloworld! I am process %d of %d.\n" % (rank, size))
    
main()
