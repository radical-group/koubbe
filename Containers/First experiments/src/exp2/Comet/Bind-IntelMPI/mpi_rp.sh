#!/bin/bash

export RADICAL_PILOT_PROFILE="True"
export RADICAL_LOG_LVL="DEBUG"
export RADICAL_LOG_TGT="radical.log"
export RADICAL_PROFILE="TRUE" 
export RADICAL_PILOT_DBURL=mongodb://rct:rct_test@two.radical-project.org/rct_test

mkdir -p results/WeakScaling/weak-1t
mkdir -p results/WeakScaling/weak-2t
mkdir -p results/WeakScaling/weak-4t
mkdir -p results/WeakScaling/weak-8t

for i in {1..5}; do

    echo "Run $i"

    python mpi_rp.py 1 george.comet_ssh |& tee mpi_rp_$i.log            
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-1t
    mv mpi_rp_$i.log results/WeakScaling/weak-1t

    python mpi_rp.py 2 george.comet_ssh |& tee mpi_rp_$i.log            
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-2t
    mv mpi_rp_$i.log results/WeakScaling/weak-2t

    python mpi_rp.py 4 george.comet_ssh |& tee mpi_rp_$i.log            
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-4t
    mv mpi_rp_$i.log results/WeakScaling/weak-4t

    python mpi_rp.py 8 george.comet_ssh |& tee mpi_rp_$i.log            
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-8t
    mv mpi_rp_$i.log results/WeakScaling/weak-8t
    
done

python filter_durations.py durations.txt > filtered_durations.txt
rm durations.txt
mv filtered_durations.txt results