import sys
import re

durations = []                       # The list where we will store results.
substr = "duration".lower()          # Substring to search for.
with open (sys.argv[1], 'rt') as myfile:
    for line in myfile:
        if line.lower().find(substr) != -1:    # if case-insensitive match,
            #durations.append(line.rstrip('\n'))
            #durations.append(''.join(filter(str.isdigit, line)))
            durations.append(re.findall("\d+\.\d+", line)[0])
for duration in durations:
    print(duration)