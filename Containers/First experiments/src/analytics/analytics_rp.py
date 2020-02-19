#!/usr/bin/env python

import os
import sys
import glob
import pprint
import radical.utils as ru
import radical.entk as re
import radical.analytics as ra

# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    #loc = './rp.session.js-104-191.jetstream-cloud.org.karahbit.018288.0029'
    loc = sys.argv[1]
    src = os.path.dirname(loc)
    sid = os.path.basename(loc)
    session = ra.Session(src=loc, sid=sid, stype='radical.pilot')

    # A formatting helper before starting...
    #def ppheader(message):
        #separator = '\n' + 78 * '-' + '\n'
        #print(separator + message + separator)

    # We first filter our session to obtain only the task objects
    units = session.filter(etype='unit', inplace=False)
    #print('#units   : %d' % len(units.get()))

    # We use the 'exec_start' and 'exec_stop' events to find
    # the time taken by RP to execute all tasks
    #ppheader("Time spent to execute the units")
    duration = units.duration(event=[{ru.EVENT: 'exec_start'},{ru.EVENT: 'exec_stop'}])
    print('duration : %.2f' % duration)