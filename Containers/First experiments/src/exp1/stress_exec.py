#!/usr/bin/env python3

import os

os.system('singularity exec ~/alexeiled_stress-ng_alpine-2020-01-14-b494d591b80f.simg /stress-ng -c 1 -t 100')