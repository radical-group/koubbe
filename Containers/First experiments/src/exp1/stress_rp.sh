#!/bin/bash

export RADICAL_PILOT_PROFILE="True"
export RADICAL_LOG_LVL="DEBUG"
export RADICAL_LOG_TGT="radical.log"
export RADICAL_PROFILE="TRUE" 
export RADICAL_PILOT_DBURL=mongodb://rct:rct_test@two.radical-project.org/rct_test

mkdir -p results/WeakScaling/weak-1c
mkdir -p results/WeakScaling/weak-2c
mkdir -p results/WeakScaling/weak-4c
mkdir -p results/WeakScaling/weak-8c
mkdir -p results/WeakScaling/weak-16c
mkdir -p results/WeakScaling/weak-32c

for i in {1..10}; do

    echo "Run $i"

    python stress_rp.py 1 xsede.bridges |& tee stress_rp_$i.log            #1 cores (1 Node)
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-1c
    mv stress_rp_$i.log results/WeakScaling/weak-1c

    python stress_rp.py 2 xsede.bridges |& tee stress_rp_$i.log            #2 cores (1 Node)
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-2c
    mv stress_rp_$i.log results/WeakScaling/weak-2c

    python stress_rp.py 4 xsede.bridges |& tee stress_rp_$i.log            #4 cores (1 Node)
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-4c
    mv stress_rp_$i.log results/WeakScaling/weak-4c

    python stress_rp.py 8 xsede.bridges |& tee stress_rp_$i.log            #8 cores (1 Node)
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-8c
    mv stress_rp_$i.log results/WeakScaling/weak-8c

    python stress_rp.py 16 xsede.bridges |& tee stress_rp_$i.log            #16 cores (1 Node)
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-16c
    mv stress_rp_$i.log results/WeakScaling/weak-16c

    python stress_rp.py 32 xsede.bridges |& tee stress_rp_$i.log            #32 cores (2 Nodes)
    python analytics_rp.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak-32c
    mv stress_rp_$i.log results/WeakScaling/weak-32c
    
done

python filter_durations.py durations.txt > filtered_durations.txt
rm durations.txt
mv filtered_durations.txt results