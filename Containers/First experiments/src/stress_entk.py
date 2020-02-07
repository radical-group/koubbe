#!/usr/bin/env python

from radical.entk import Pipeline, Stage, Task, AppManager
import os
import traceback
import sys
import time

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'True'

# Description of how the RabbitMQ process is accessible
# No need to change/set any variables if you installed RabbitMQ has a system
# process. If you are running RabbitMQ under a docker container or another
# VM, set "RMQ_HOSTNAME" and "RMQ_PORT" in the session where you are running
# this script.
#hostname = os.environ.get('RMQ_HOSTNAME', 'two.radical-project.org')
#port = int(os.environ.get('RMQ_PORT', 33235))
hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))

if __name__ == '__main__':

    start_time = time.time()

    pipelines = set()
    p = Pipeline()
    s = Stage()
   
    for cnt in range(8):
    
        t = Task()
        t.name = 't%s' % (cnt + 1)
        t.pre_exec = ['export PATH=/home/karahbit/stress-ng-0.10.16:$PATH']
        t.executable = ['stress-ng'] 
        t.arguments = ['-c', '1', '-t', '100']
        t.cpu_reqs = {'processes': 1, 'thread_type': None, 'threads_per_process': 1, 'process_type': None}

        s.add_tasks(t)

    p.add_stages(s)
    pipelines.add(p)

    # Resource and AppManager
    amgr = AppManager(hostname = hostname, port = port)
    amgr.workflow = pipelines
    amgr.shared_data = []
   
    amgr.resource_desc = {
       'resource': 'local.localhost',
	    'walltime': 10,
	    'cpus': 8
    }
       
    amgr.run()

    print("--- %s seconds ---" % (time.time() - start_time))