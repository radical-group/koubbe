from radical.entk import Pipeline, Stage, Task, AppManager
import os
#import traceback
#import sys
#import pickle  
#from glob import glob
import radical.utils as ru
#import shutil

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'

os.environ['RADICAL_ENTK_PROFILE'] = "True"
os.environ['RADICAL_LOG_LVL'] = "DEBUG"
os.environ['RADICAL_LOG_TGT'] = "radical.log"
os.environ['RADICAL_PROFILE'] = "TRUE"
os.environ['RADICAL_PILOT_DBURL'] = "mongodb://rct:rct_test@129.114.17.233:27017/rct_test"

hostname = os.environ.get('RMQ_HOSTNAME','localhost')
port = int(os.environ.get('RMQ_PORT',5672))

logger = ru.Logger(__name__, level='DEBUG')

class HyperSpacePipeline(Pipeline):
    def __init__(self, name):
        super(HyperSpacePipeline, self).__init__()
        self.name = name 

class OptimizationStage(Stage):
    def __init__(self, name):
        super(OptimizationStage, self).__init__()
        self.name = name    

class OptimizationTask(Task):
    def __init__(self, name, script, hparams, results_dir):
        # this task will execute Bayesian optimizations
         
        super(OptimizationTask, self).__init__()
        self.name = name
        self.pre_exec    =   []
        self.pre_exec   += ['export PATH="/home/karahbit/.local/bin:$PATH"']    # for virtualenv
        self.pre_exec   += ['module load mpi4py']
        self.pre_exec   += ['source /home/karahbit/ve-cheers/bin/activate']
        self.pre_exec   += ['export MV2_ENABLE_AFFINITY=0'] # to avoid "BAD TERMINATION OF ONE OF YOUR APPLICATION PROCESSES" on Comet
        self.executable  = 'python'
        self.arguments   =   []
        self.arguments  += [script]
        self.arguments  += ['--ndims', hparams]
        self.arguments  += ['--results', results_dir]
        self.cpu_reqs    = {'processes': 2**hparams, 'thread_type': None, 'threads_per_process': 1, 'process_type': 'MPI'}


if __name__ == '__main__':

    # arguments for AppManager

    hparams = 2
    script = '/home/karahbit/hyperspace/benchmarks/styblinskitang/hyperdrive/benchmark.py'
    results_dir = '/home/karahbit/hyperspace_results'

    p = HyperSpacePipeline(name = 'hyperspace_pipeline')

    # Stage 1: single task that spawns n_optimizations using mpirun

    s1 = OptimizationStage(name = 'optimizations')

    t1 = OptimizationTask(name = 'analysis_1', script = script, hparams = hparams, results_dir = results_dir) 

    s1.add_tasks(t1)
    p.add_stages(s1)

    logger.info('adding stage {} with {} tasks'.format(s1.name, s1._task_count))
    logger.info('adding pipeline {} with {} stages'.format(p.name, p._stage_count))

    # Create Application Manager
    appman = AppManager(hostname=hostname, port=port)

    res_dict = {

        'resource': 'xsede.comet_ssh',
        'project' : 'TG-MCB090174',
        'queue' : 'compute',
        'walltime': 90,
        'cpus': (2**hparams)*1, # 1 core per optimization
        'access_schema': 'gsissh'
    }

    # Assign resource manager to the Application Manager
    appman.resource_desc = res_dict
                    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.workflow = [p]

    # Run the Application Manager
    appman.run()