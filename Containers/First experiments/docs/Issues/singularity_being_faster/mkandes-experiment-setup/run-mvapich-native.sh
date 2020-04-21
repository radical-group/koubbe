#!/usr/bin/env bash

#SBATCH --job-name=mvapich-native
#SBATCH --account=use300
#SBATCH --partition=debug
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=24
#SBATCH --time=00:30:00
#SBATCH --output=mvapich-native.o%j.%N

declare -xr COMPILER_MODULE='intel/2018.1.163'
declare -xr MPI_MODULE='mvapich2_ib/2.3.2'

module purge
module load "${COMPILER_MODULE}"
module load "${MPI_MODULE}"
module list
printenv

time -p mpicc mpi_hello_world.c -o hello_world_intel_mvapich2_ib.x
time -p ibrun ./hello_world_intel_mvapich2_ib.x
