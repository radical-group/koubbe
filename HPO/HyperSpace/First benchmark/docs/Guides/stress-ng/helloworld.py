#!/usr/bin/env python
"""
Parallel Hello World
"""

from mpi4py import MPI
import sys
import time
import os

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

# to execute: $ /usr/bin/time -v mpirun -n 2 python3 helloworld.py
print("Hello, World! I am process %d of %d on %s.\n" % (rank, size, name))

#time.sleep(100)
os.system('/home/karahbit/stress-ng-0.10.10/./stress-ng -c 2 -t 100')