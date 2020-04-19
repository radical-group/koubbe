#!/bin/bash

export RADICAL_ENTK_PROFILE="True"
export RADICAL_LOG_LVL="DEBUG"
export RADICAL_LOG_TGT="radical.log"
export RADICAL_PROFILE="TRUE" 
export RADICAL_PILOT_DBURL=mongodb://rct:rct_test@two.radical-project.org/rct_test

mkdir -p results

for i in {1..10}; do

    echo "Run $i"

    python FACTS.py ./experiments/test_xsede/ |& tee facts_re_$i.log            
    python analytics_re.py *session* >> durations.txt
    mv *session* results/
    mv facts_re_$i.log results/
    
done

python filter_durations.py durations.txt > filtered_durations.txt
rm durations.txt
mv filtered_durations.txt results