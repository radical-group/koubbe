from radical.entk import Pipeline, Stage, Task, AppManager
import radical.utils as ru
import os

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'

os.environ['RADICAL_ENTK_PROFILE'] = "True"
os.environ['RADICAL_LOG_LVL'] = "DEBUG"
os.environ['RADICAL_LOG_TGT'] = "radical.log"
os.environ['RADICAL_PROFILE'] = "TRUE"
os.environ['RADICAL_PILOT_DBURL'] = "mongodb://karahbit:ZDL7HjvKnvEaRfMN@129.114.17.185:27017/gk_db"

cur_dir = os.path.dirname(os.path.abspath(__file__))
hostname = os.environ.get('RMQ_HOSTNAME','localhost')
port = int(os.environ.get('RMQ_PORT',5672))
username = os.environ.get('RMQ_USERNAME', 'karahbit')
password = os.environ.get('RMQ_PASSWORD', 'ZDL7HjvKnvEaRfMN')

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
        self.copy_input_data   = []
        self.copy_input_data  += ['$SHARED/data_Alcohol.npy']
        self.copy_input_data  += ['$SHARED/cheers_svr_3params.py']
        self.pre_exec    =   []
        self.pre_exec   += ['export PATH="/home/karahbit/.local/bin:$PATH"']    # for virtualenv
        self.pre_exec   += ['module load mpi4py']
        self.pre_exec   += ['source /home/karahbit/ve-cheers/bin/activate']
        self.pre_exec   += ['export MV2_ENABLE_AFFINITY=0'] # to avoid "BAD TERMINATION OF ONE OF YOUR APPLICATION PROCESSES" on Comet
        self.executable  = 'python'
        self.arguments   =   []
        self.arguments  += [script]
        self.arguments  += ['--results', results_dir]
        self.cpu_reqs    = {'processes': (2**hparams)*1, 'thread_type': None, 'threads_per_process': 1, 'process_type': 'MPI'}

if __name__ == '__main__':

    # arguments for AppManager

    hparams = 3
    script = 'cheers_svr_3params.py'
    results_dir = '/home/karahbit/results'   # dir on Comet
    cur_dir = '/home/karahbit/FastFingerPrinting/phase1/src/galloOSIOPT/hyperparams-opt/code/NIRONE2-5' #  dir on local machine

    p = HyperSpacePipeline(name = 'hyperspace_pipeline')

    # Stage 1: single task that spawns n_optimizations using mpirun

    s1 = OptimizationStage(name = 'optimizations')

    t1 = OptimizationTask(name = 'analysis_1', script = script, hparams = hparams, results_dir = results_dir) 

    s1.add_tasks(t1)
    p.add_stages(s1)

    logger.info('adding stage {} with {} tasks'.format(s1.name, s1._task_count))
    logger.info('adding pipeline {} with {} stages'.format(p.name, p._stage_count))

    # Create Application Manager
    appman = AppManager(hostname=hostname, port=port, username=username, password=password)

    res_dict = {

        'resource': 'xsede.comet_ssh',
        'project' : 'unc100',
        'queue' : 'compute',
        'walltime': 90,
        'cpus': (2**hparams)*1, # 1 core per optimization
        'access_schema': 'gsissh'
    }

    # Assign resource manager to the Application Manager
    appman.resource_desc = res_dict
    appman.shared_data   = []
    appman.shared_data += ['%s/data_Alcohol.npy' %cur_dir]
    appman.shared_data += ['%s/cheers_svr_3params.py' %cur_dir]
                    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.workflow = [p]

    # Run the Application Manager
    appman.run()