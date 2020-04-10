from mpi4py import MPI
import sys

from utils.process import process_chunk
from utils.collect import sum_counters
from utils.export import print_hashcounts, print_langcounts

DATAFILE = sys.argv[1]  # json tweet data
COMM = MPI.COMM_WORLD
SIZE = COMM.Get_size()  # total number of processes
RANK = COMM.Get_rank()  # process number


def main():
    root = 0  # root process to gather results to
    top = 10  # number of most common observations

    # Compute process time
    # t1 = MPI.Wtime()

    # Run processes
    hashcounts, langcounts, nlines = process_chunk(DATAFILE, SIZE, RANK)  # (Counter, Counter, number of lines) returned
    # print(hashcounts)
    # COMM.barrier()
    # print(langcounts)

    # Gather results
    hashcounts = COMM.gather(hashcounts, root=root)  # list of Counters for root RANK
    langcounts = COMM.gather(langcounts, root=root)  # list of Counters for root RANK
    nlines = COMM.gather(nlines, root=root)  # list of numbers for root RANK
	
    # t2 = MPI.Wtime()
    # wt = t2 - t1
    # print("Elapsed time: ",wt," for rank: ", RANK)

    # Export results
    if RANK != root:
        return
    hashcounts_all = sum_counters(hashcounts)
    langcounts_all = sum_counters(langcounts)
    nlines_all = sum(nlines)
    print_hashcounts(hashcounts_all, top)
    print()
    print_langcounts(langcounts_all, top)
    print()
    print(f"Number of processed lines (tweets): {nlines_all}")
   
main()
