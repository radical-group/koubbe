from radical.entk import Pipeline, Stage, Task, AppManager
import os

# ------------------------------------------------------------------------------
# Set default verbosity
if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'


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

    # Create a Task object which creates a file named 'output.txt' of size 1 MB
    t1 = Task()
    t1.name = 't1'
    t1.executable = '/bin/date'

    for cnt in range(128):

        # Create a Task object
        t1 = Task()
        t1.name = 't%s' % (cnt + 1)
        t1.executable = '/bin/date'

        # Add the Task to the Stage
        s1.add_tasks(t1)
        s1_task_uids.append(t1.name)

    # Add Stage to the Pipeline
    p.add_stages(s1)

    return p

if __name__ == '__main__':

    # Create Application Manager
    appman = AppManager(hostname=hostname, port=port)

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, and cpus
    # resource is 'local.localhost' to execute locally
    res_dict = {

    #    'resource': 'ncsa.bw_aprun',
    #    'walltime': 10,
    #    'cpus': 32,
    #'project': 'bamm',
    #'queue': 'high'
	'resource': 'local.localhost',
	'walltime': 10,
	'cpus':128
    }

    # Assign resource request description to the Application Manager
    appman.resource_desc = res_dict

    # Assign the workflow as a set or list of Pipelines to the Application Manager
    # Note: The list order is not guaranteed to be preserved
    appman.workflow = set([generate_pipeline()])

    # Run the Application Manager
    appman.run()