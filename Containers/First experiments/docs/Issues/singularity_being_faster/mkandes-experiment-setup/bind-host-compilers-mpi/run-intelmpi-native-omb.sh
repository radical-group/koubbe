#!/usr/bin/env bash

#SBATCH --job-name=intelmpi-native-omb-latency
#SBATCH --account=use300
#SBATCH --partition=compute
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --output=intelmpi-native-omb-latency.o%j.%N

declare -xr COMPILER_MODULE='intel/2018.1.163'
declare -xr MPI_MODULE='intelmpi/2018.1.163'

declare -xr OMB_VERSION='5.6.2'
declare -xr OMB_BUILD='mpi'
declare -xr OMB_ROOT_DIR="${PWD}"
declare -xr OMB_ROOT_URL='http://mvapich.cse.ohio-state.edu/download/mvapich'
declare -xr OMB_INSTALL_DIR="${OMB_ROOT_DIR}/${OMB_VERSION}/${COMPILER_MODULE}/${MPI_MODULE}/${OMB_BUILD}"

module purge
module load "${COMPILER_MODULE}"
module load "${MPI_MODULE}"
module list
export PATH="${OMB_INSTALL_DIR}/libexec/osu-micro-benchmarks/mpi/pt2pt:${PATH}"
printenv

time -p mpirun osu_latency
