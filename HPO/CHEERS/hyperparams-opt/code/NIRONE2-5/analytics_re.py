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

    #loc = './re.session.js-17-185.jetstream-cloud.org.karahbit.018451.0005'
    loc = "./" + sys.argv[1] + "/"
    src = os.path.dirname(loc)
    #src = print(os.path.dirname(os.path.abspath(__file__)))
    sid = os.path.basename(loc)
    session = ra.Session(src=src, sid = sid, stype='radical.entk')

    # A formatting helper before starting...
    #def ppheader(message):
        #separator = '\n' + 78 * '-' + '\n'
        #print separator + message + separator

    # We first filter our session to obtain only the task objects
    tasks = session.filter(etype='task', inplace=False)
    #print '#tasks   : %d' % len(tasks.get())

    # We use the 're.states.SUBMITTING' and 're.states.COMPLETED' probes to find
    # the time taken by EnTK to execute all tasks
    #ppheader("Time spent to execute the tasks")
    duration = tasks.duration(event=[{ru.EVENT: 'state',
                                    ru.STATE: re.states.SUBMITTING},
                                    {ru.EVENT: 'state',
                                    ru.STATE: re.states.COMPLETED}])
    print('duration : %.2f' % duration)