#!/usr/bin/env python
__copyright__ = 'Copyright 2013-2018, http://radical.rutgers.edu'
__license__ = 'MIT'


import os
import sys
import glob
import pprint
import radical.utils as ru
import radical.entk as re
import radical.analytics as ra

"""This example illustrates how to obtain durations for arbitrary (non-state)
profile events. Modified from examples under RADICAL Analytics"""

# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    loc = './re.session.two.karahbit.018175.0001'
    src = os.path.dirname(loc)
    sid = os.path.basename(loc)
    session = ra.Session(src=src, sid = sid, stype='radical.entk')

    # A formatting helper before starting...
    def ppheader(message):
        separator = '\n' + 78 * '-' + '\n'
        print separator + message + separator

    # We first filter our session to obtain only the task objects
    tasks = session.filter(etype='task', inplace=False)
    print '#tasks   : %d' % len(tasks.get())

    # We use the 're.states.SUBMITTING' and 're.states.DONE' probes to find
    # the time taken by EnTK to execute all tasks
    ppheader("Time spent to execute the tasks")
    duration = tasks.duration(event=[{ru.EVENT: 'state',
                                    ru.STATE: re.states.SUBMITTING},
                                    {ru.EVENT: 'state',
                                    ru.STATE: re.states.DONE}])
    print 'duration : %.2f' % duration

    # Finally, we produce a list of the number of concurrent tasks between
    # states 're.states.SUBMITTING' and 're.states.DONE' over the course
    # of the entire execution sampled every 10 seconds
    ppheader("concurrent tasks in between SUBMITTING and DONE states")
    concurrency = tasks.concurrency(event=[{ru.EVENT: 'state',
                                            ru.STATE: re.states.SUBMITTING},
                                            {ru.EVENT: 'state',
                                            ru.STATE: re.states.DONE}],
                                    sampling=1)
    pprint.pprint(concurrency)