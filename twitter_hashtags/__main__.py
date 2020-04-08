from mpi4py import MPI
import sys
from pprint import pprint

from utils.process import process_chunk
from utils.collect import sum_counters

DATAFILE = sys.argv[1]  # json tweet data
COMM = MPI.COMM_WORLD
SIZE = COMM.Get_size()  # total number of processes
RANK = COMM.Get_rank()  # process number


def main():
    root = 0  # root process to gather results to
    top = 10  # number of most common observations

    #Compute process time
    t1 = MPI.Wtime()
    # Run processes
    hashcounts, langcounts = process_chunk(DATAFILE, SIZE, RANK)  # 2 Counters returned
    # print(hashcounts)
    # COMM.barrier()
    # print(langcounts)
    t2 = MPI.Wtime()
    wt = t2 - t1
    for rank in range(SIZE):
        print("Elapsed time: ",wt," for rank: ", RANK)
    # Gather results
    hashcounts = COMM.gather(hashcounts, root=root)  # list of Counters for root RANK
    langcounts = COMM.gather(langcounts, root=root)  # list of Counters for root RANK


    # Export results
    if RANK != root:
        return
    hashcounts_all = sum_counters(hashcounts)
    langcounts_all = sum_counters(langcounts)
    pprint(hashcounts_all.most_common(top))
    pprint(langcounts_all.most_common(top))


main()
