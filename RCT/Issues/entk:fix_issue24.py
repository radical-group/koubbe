#!/usr/bin/env python

from radical.entk import Pipeline, Stage, Task, AppManager
import os

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

os.environ['RADICAL_ENTK_PROFILE'] = "True"
os.environ['RADICAL_LOG_LVL'] = "DEBUG"
os.environ['RADICAL_LOG_TGT'] = "radical.log"
os.environ['RADICAL_PROFILE'] = "TRUE"
os.environ['RADICAL_PILOT_DBURL'] = "mongodb://karahbit:ZDL7HjvKnvEaRfMN@129.114.17.185:27017/gk_db"

# Description of how the RabbitMQ process is accessible
# No need to change/set any variables if you installed RabbitMQ has a system
# process. If you are running RabbitMQ under a docker container or another
# VM, set "RMQ_HOSTNAME" and "RMQ_PORT" in the session where you are running
# this script.
hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))
username = os.environ.get('RMQ_USERNAME', 'karahbit')
password = os.environ.get('RMQ_PASSWORD', 'ZDL7HjvKnvEaRfMN')


def generate_pipeline():

    p = Pipeline()
    s1 = Stage()

    t1 = Task()
    t1.executable = '/bin/sleep'
    t1.arguments = ['3']

    s1.add_tasks(t1)

    p.add_stages(s1)
    s2 = Stage()
    t2 = Task()
    t2.executable = '/bin/sleep'
    t2.arguments = ['3']

    s2.add_tasks(t2)
    p.add_stages(s2)
    s3 = Stage()

    t3 = Task()
    t3.executable = '/bin/sleep'
    t3.arguments = ['3']

    s3.add_tasks(t3)
    p.add_stages(s3)

    return p


if __name__ == '__main__':

    appman   = AppManager(hostname=hostname, port=port, username=username, password=password, autoterminate=False)
    res_dict = {
        'resource': 'local.localhost',
        'walltime': 10,
        'cpus'    :  8
    }
    appman.resource_desc = res_dict


    pipelines = list()
    for cnt in range(2):
        pipelines.append(generate_pipeline())

    appman.workflow = set(pipelines)
    appman.run()

    print('1 ===================================================')


    pipelines = list()
    for cnt in range(2):
        pipelines.append(generate_pipeline())

    appman.workflow = set(pipelines)
    appman.run()

    print('2 ===================================================')

    appman.terminate()

    print('t ===================================================')