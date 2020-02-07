#!/usr/bin/env python
"""
Parallel Hello World
"""

from mpi4py import MPI
#import sys
#import time
#import os

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
host = MPI.Get_processor_name().split('.')[0]

# to execute: 
# $ interact -p RM -N 1 -n 4 -t 8:00:00
# $ /usr/bin/time -v mpirun -n 2 python mpi_hello.py
print("Hello, World! I am process %d of %d on %s.\n" % (rank, size, host))

comm.Barrier()   # wait for everybody to synchronize here
