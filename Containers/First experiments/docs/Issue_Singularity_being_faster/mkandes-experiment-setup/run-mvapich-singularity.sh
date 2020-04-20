#!/usr/bin/env bash

#SBATCH --job-name=mvapich-singularity
#SBATCH --account=use300
#SBATCH --partition=debug
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=24
#SBATCH --time=00:30:00
#SBATCH --output=mvapich-singularity.o%j.%N

declare -xr COMPILER_MODULE='intel/2018.1.163'
declare -xr MPI_MODULE='mvapich2_ib/2.3.2'

module purge
module load "${COMPILER_MODULE}"
module load "${MPI_MODULE}"
module list
export SINGULARITYENV_PREPEND_PATH=/opt/mvapich2/intel/ib/bin:/opt/intel/2018.1.163/compilers_and_libraries_2018.1.163/linux/bin/intel64
export SINGULARITYENV_LD_LIBRARY_PATH=/etc/libibverbs.d:/opt/mvapich2/intel/ib/lib:/opt/intel/2018.1.163/compilers_and_libraries_2018.1.163/linux/compiler/lib/intel64_lin:/opt/intel/2018.1.163/compilers_and_libraries_2018.1.163/linux/ipp/../compiler/lib/intel64:/opt/intel/2018.1.163/compilers_and_libraries_2018.1.163/linux/ipp/lib/intel64:/opt/intel/2018.1.163/compilers_and_libraries_2018.1.163/linux/mkl/lib/intel64:/opt/intel/2018.1.163/compilers_and_libraries_2018.1.163/linux/tbb/lib/intel64/gcc4.4
printenv

time -p singularity exec --cleanenv --bind /etc,/opt,/usr,/oasis,/scratch centos.simg mpicc mpi_hello_world.c -o hello_world_intel_mvapich2_ib.x
time -p ibrun singularity exec --bind /etc,/opt,/usr,/oasis,/scratch centos.simg ./hello_world_intel_mvapich2_ib.x

