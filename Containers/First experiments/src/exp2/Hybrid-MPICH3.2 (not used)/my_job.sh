#!/bin/bash
#SBATCH --job-name=singularity-mpi  # create a name for your job
#SBATCH --partition=RM              # queue name
#SBATCH --nodes=2                   # node count
#SBATCH --ntasks=8                  # total number of tasks
#SBATCH --ntasks-per-node=4         # tasks per node
#SBATCH --cpus-per-task=1           # cpu-cores per task
#SBATCH --time=05:00:00             # total run time limit (HH:MM:SS)
#SBATCH --export=ALL                # export all env variables
#SBATCH -e slurm-%j.err             # create error log
#SBATCH -o slurm-%j.out             # create output log

#echo commands to stdout
set -x

unset XDG_RUNTIME_DIR

module load singularity mpi/gcc_mvapich

mpirun -n 4 -ppn 2 singularity exec $HOME/ubuntu-mpich3-2.sif /opt/mpitest
