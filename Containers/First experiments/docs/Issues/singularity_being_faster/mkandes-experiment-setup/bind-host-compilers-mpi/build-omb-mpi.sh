#!/usr/bin/env bash

#SBATCH --job-name=build-omb-mpi
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --output=build-omb-mpi.o%j.%N

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
printenv

mkdir -p "${OMB_INSTALL_DIR}"
cd "${OMB_INSTALL_DIR}"

wget "${OMB_ROOT_URL}/osu-micro-benchmarks-${OMB_VERSION}.tar.gz"
tar -xf "osu-micro-benchmarks-${OMB_VERSION}.tar.gz"

cd "osu-micro-benchmarks-${OMB_VERSION}"

./configure --prefix="${OMB_INSTALL_DIR}" CC='mpicc' CXX='mpicxx'
make
make install
