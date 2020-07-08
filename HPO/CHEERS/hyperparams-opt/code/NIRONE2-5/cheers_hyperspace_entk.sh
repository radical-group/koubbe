#!/bin/bash

export RADICAL_ENTK_PROFILE="True"
export RADICAL_LOG_LVL="DEBUG"
export RADICAL_LOG_TGT="radical.log"
export RADICAL_PROFILE="TRUE" 
export RADICAL_PILOT_DBURL=mongodb://karahbit:ZDL7HjvKnvEaRfMN@129.114.17.185:27017/gk_db

mkdir -p results/WeakScaling/weak_1
mkdir -p results/WeakScaling/weak_2
mkdir -p results/WeakScaling/weak_3
mkdir -p results/WeakScaling/weak_4
mkdir -p results/WeakScaling/weak_5

for i in {1..10}; do

    echo "Run $i"

    python cheers_hyperspace_entk.py 1 |& tee cheers_hyperspace_entk_$i.log            
    python analytics_re.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak_1
    mv cheers_hyperspace_entk_$i.log results/WeakScaling/weak_1

    python cheers_hyperspace_entk.py 2 |& tee cheers_hyperspace_entk_$i.log            
    python analytics_re.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak_2
    mv cheers_hyperspace_entk_$i.log results/WeakScaling/weak_2

    python cheers_hyperspace_entk.py 3 |& tee cheers_hyperspace_entk_$i.log            
    python analytics_re.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak_3
    mv cheers_hyperspace_entk_$i.log results/WeakScaling/weak_3

    python cheers_hyperspace_entk.py 4 |& tee cheers_hyperspace_entk_$i.log            
    python analytics_re.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak_4
    mv cheers_hyperspace_entk_$i.log results/WeakScaling/weak_4

    python cheers_hyperspace_entk.py 5 |& tee cheers_hyperspace_entk_$i.log            
    python analytics_re.py *session* >> durations.txt
    mv *session* results/WeakScaling/weak_5
    mv cheers_hyperspace_entk_$i.log results/WeakScaling/weak_5
    
done

python filter_durations.py durations.txt > filtered_durations.txt
rm durations.txt
mv filtered_durations.txt results