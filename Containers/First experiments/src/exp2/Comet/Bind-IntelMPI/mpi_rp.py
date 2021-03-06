#!/usr/bin/env python

import os
import sys
import time

verbose  = os.environ.get('RADICAL_PILOT_VERBOSE', 'REPORT')
os.environ['RADICAL_PILOT_VERBOSE'] = verbose

os.environ['RADICAL_PILOT_PROFILE'] = "True"
os.environ['RADICAL_LOG_LVL'] = "DEBUG"
os.environ['RADICAL_LOG_TGT'] = "radical.log"
os.environ['RADICAL_PROFILE'] = "TRUE"

import radical.pilot as rp
import radical.utils as ru

if __name__ == '__main__':

    start_time = time.time()

    # we use a reporter class for nicer output
    report = ru.Reporter(name='radical.pilot')
    report.title('Getting Started (RP version %s)' % rp.version)

    # use the resource specified as argument, fall back to localhost
    if   len(sys.argv)  > 3: report.exit('Usage:\t%s [tasks] [resource]\n\n' % sys.argv[0])
    elif len(sys.argv) == 3: tasks = int(sys.argv[1]); resource = sys.argv[2]
    elif len(sys.argv) == 2: tasks = int(sys.argv[1]); resource = 'local.localhost'
    else                   : tasks = 1; resource = 'local.localhost'

    # Create a new session. No need to try/except this: if session creation
    # fails, there is not much we can do anyways...
    session = rp.Session()

    # all other pilot code is now tried/excepted.  If an exception is caught, we
    # can rely on the session object to exist and be valid, and we can thus tear
    # the whole RP stack down via a 'session.close()' call in the 'finally'
    # clause...
    try:

        report.header('submit pilots')

        # Add a Pilot Manager. Pilot managers manage one or more ComputePilots.
        pmgr = rp.PilotManager(session=session)

        # Define an [n]-core local pilot that runs for [x] minutes
        # Here we use a dict to initialize the description object
        if (resource == 'local.localhost'):
            pd_init = {'resource'      : resource,
                    'runtime'       : 10,  # pilot runtime (min)
                    'exit_on_error' : True,
                    'cores'         : tasks*48
                    }
        else:
            pd_init = {'resource'      : resource,
                    'runtime'       : 30,  # pilot runtime (min)
                    'exit_on_error' : True,
                    'project'       : 'TG-MCB090174',
                    'queue'         : 'compute',
                    'access_schema' : 'gsissh',
                    'cores'         : tasks*48
                    }
        pdesc = rp.ComputePilotDescription(pd_init)

        # Launch the pilot.
        pilot = pmgr.submit_pilots(pdesc)

        report.header('submit units')

        # Register the ComputePilot in a UnitManager object.
        umgr = rp.UnitManager(session=session)
        umgr.add_pilots(pilot)

        # Create a workload of ComputeUnits.

        n = tasks   # number of units to run
        t_num = 1  # number of threads   (OpenMP)
        p_num = n*48  # number of processes (MPI)
        report.info('create %d unit description(s)\n\t' % n)

        cuds = list()
        for i in range(0, n):

            # create a new CU description, and fill it.
            # Here we don't use dict initialization.
            cud = rp.ComputeUnitDescription()
            #---------- Executable_Comet ----------
            # To run, place executable in Comet and compile: $ mpicc -o hello_world_intel mpi_hello_world.c
            # if on Bridges directly, run with: mpirun -n 4 -ppn 2 -host r001,r002 ./hello_world_intel
            #cud.executable  = '/home/karahbit/hello_world_intel'
            #---------- Singularity_Comet ---------
            cud.pre_exec    = []
            cud.pre_exec   += ['export SINGULARITYENV_PREPEND_PATH=/opt/intel/2018.1.163/compilers_and_libraries_2018.1.163/linux/mpi/intel64/bin/']
            cud.pre_exec   += ['export SINGULARITYENV_LD_LIBRARY_PATH=/opt/intel/2018.1.163/compilers_and_libraries_2018.1.163/linux/mpi/intel64/lib']
            cud.executable   = 'singularity'
            cud.arguments    = []
            cud.arguments   += ['exec']
            cud.arguments   += ['--bind', '/opt']
            cud.arguments   += ['/home/karahbit/mkandes/centos.simg']
            cud.arguments   += ['/home/karahbit/mkandes/hello_world_intel']
            cud.cpu_processes       = p_num
            cud.cpu_process_type    = rp.MPI
            cud.cpu_threads         = t_num
            cuds.append(cud)
            report.progress()
        report.ok('>>ok\n')

        # Submit the previously created ComputeUnit descriptions to the
        # PilotManager. This will trigger the selected scheduler to start
        # assigning ComputeUnits to the ComputePilots.
        umgr.submit_units(cuds)

        # Wait for all compute units to reach a final state (DONE, CANCELED or FAILED).
        report.header('gather results')
        umgr.wait_units()


    except Exception as e:
        # Something unexpected happened in the pilot code above
        report.error('caught Exception: %s\n' % e)
        ru.print_exception_trace()
        raise

    except (KeyboardInterrupt, SystemExit):
        # the callback called sys.exit(), and we can here catch the
        # corresponding KeyboardInterrupt exception for shutdown.  We also catch
        # SystemExit (which gets raised if the main threads exits for some other
        # reason).
        ru.print_exception_trace()
        report.warn('exit requested\n')

    finally:
        # always clean up the session, no matter if we caught an exception or
        # not.  This will kill all remaining pilots.
        report.header('finalize')
        session.close(download=True)

    report.header()

    print("--- %s seconds ---" % (time.time() - start_time))