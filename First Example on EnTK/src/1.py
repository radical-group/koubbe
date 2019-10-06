from radical.entk import Pipeline, Stage, Task, AppManager
import os
import time


# ------------------------------------------------------------------------------
# Set default verbosity
if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

os.environ['RADICAL_ENTK_PROFILE'] = "True"
os.environ['RADICAL_LOG_LVL'] = "DEBUG"
os.environ['RADICAL_LOG_TGT'] = "radical.log"
os.environ['RADICAL_PROFILE'] = "TRUE"

# Description of how the RabbitMQ process is accessible
# No need to change/set any variables if you installed RabbitMQ has a system
# process. If you are running RabbitMQ under a docker container or another
# VM, set "RMQ_HOSTNAME" and "RMQ_PORT" in the session where you are running
# this script.
hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))


def generate_pipeline():

    # Create a Pipeline object
    p = Pipeline()
    p.name = 'p1'

    # Create a Stage object
    s1 = Stage()
    s1.name = 's1'
    s1_task_uids = []

    for cnt in range(128):

        # Create a Task object
        t1 = Task()
        t1.name = 't%s' % (cnt + 1)
        # to make a python script executable: 
        # 1) add to first line "shebang": #!/usr/bin/env python
        # 2) chmod +x SerialCode.py
        # The executable always has to be in the Target Machine
        t1.executable = '~/SerialCode.py'

        # Add the Task to the Stage
        s1.add_tasks(t1)
        s1_task_uids.append(t1.name)

    # Add Stage to the Pipeline
    p.add_stages(s1)

    return p

if __name__ == '__main__':

    start_time = time.time()

    # Create Application Manager
    appman = AppManager(hostname=hostname, port=port)

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, and cpus
    # resource is 'local.localhost' to execute locally
    res_dict = {

    #    'resource': 'ncsa.bw_aprun',
    #    'walltime': 10,
    #    'cpus': 32,
    'project': 'mc3bggp',
    'queue': 'RM',
    'access_schema' : 'gsissh',
	'resource': 'xsede.bridges',
    #'resource': 'local.localhost',
	'walltime': 30,
	'cpus':128
    }

    # Assign resource request description to the Application Manager
    appman.resource_desc = res_dict

    # Assign the workflow as a set or list of Pipelines to the Application Manager
    # Note: The list order is not guaranteed to be preserved
    appman.workflow = set([generate_pipeline()])

    # Run the Application Manager
    appman.run()

    print("--- %s seconds ---" % (time.time() - start_time))