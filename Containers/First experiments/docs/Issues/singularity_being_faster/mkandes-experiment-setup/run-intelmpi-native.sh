#!/usr/bin/env bash

#SBATCH --job-name=intelmpi-native
#SBATCH --account=use300
#SBATCH --partition=debug
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=24
#SBATCH --time=00:30:00
#SBATCH --output=intelmpi-native.o%j.%N

declare -xr COMPILER_MODULE='intel/2018.1.163'
declare -xr MPI_MODULE='intelmpi/2018.1.163'

module purge
module load "${COMPILER_MODULE}"
module load "${MPI_MODULE}"
module list
printenv

time -p mpiicc mpi_hello_world.c -o hello_world_intel_intelmpi.x
time -p mpirun ./hello_world_intel_intelmpi.x
