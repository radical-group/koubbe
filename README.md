# koubbe

Below you have a brief summary of the main work that I have been doing during my time in [Radical-Lab](http://radical.rutgers.edu "Radical-Lab") at Rutgers Universiry. For detailed information (descriptions, instructions, source code, results, etc.), please visit each section's topic.

## Table of Contents

[Radical-Cybertools (RCT)](https://github.com/radical-group/koubbe/blob/master/README.md#radical-cybertools-rct)  
[Hyperparameter Optimization (HPO)](https://github.com/radical-group/koubbe/blob/master/README.md#hyperparameter-optimization-hpo)  
[Containers](https://github.com/radical-group/koubbe/blob/master/README.md#containers)  
[FACTS](https://github.com/radical-group/koubbe/blob/master/README.md#facts)  
[Misc](https://github.com/radical-group/koubbe/blob/master/README.md#misc)  
[Installation of stress-ng executable](https://github.com/radical-group/koubbe/blob/master/README.md#installation-of-stress-ng-executable)  
[Installation of mpi4py on XSEDE Bridges using GCC compiler](https://github.com/radical-group/koubbe/blob/master/README.md#installation-of-mpi4py-on-xsede-bridges-using-gcc-compiler)  
[Reference](https://github.com/radical-group/koubbe/blob/master/README.md#reference) 

## Radical-Cybertools (RCT)

Download RCT stack as per instructed on [EnTK installation website](https://radicalentk.readthedocs.io/en/latest/install.html):

```
$ virtualenv -p python3.7 \<VE name\>  
$ source \<path-to-VE\>/bin/activate  
$ pip install radical.entk  
$ pip install radical.analytics
```

### Simple RP exercise

Here I ran the getting started example provided with RP and verified correct functionality:

```
$ cd \<path-to-VE\>/radical.pilot/examples  
$ python 00_getting_started.py xsede.bridges
```

### Simple EnTK exercise

Here I wrote three suggested applications to get familiar with EnTK (the duration of the tasks can be arbitrary short):
 
 1. 128 tasks concurrently, where each task is 1 core  
 2. 8 tasks where each task is 16 cores 
 3. 16 concurrent batches of 8 tasks (each of 1 core, but where in each batch each task runs sequentially i.e., one after the other.

## Hyperparameter Optimization (HPO)

In order to see my Initial Presentation on HPO, please visit [HPO Initial Presentation](https://docs.google.com/presentation/d/12yYCymB0-m4qGEPdgg0XKipuziSUmEoVhI32XXhDOtc/edit?usp=sharing)

To install HyperSpace (on Bridges login node, make sure MPICH or OpenMPI is available):

If Anaconda (or Miniconda) not installed:  
```
$ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  
$ bash Miniconda3-latest-Linux-x86_64.sh  
```

Else:  
```
$ conda create --name \<VE name\> python=3.7  
$ conda activate \<VE name\>  
$ pip install mpi4py  
$ git clone https://github.com/yngtodd/hyperspace.git  
$ cd hyperspace  
$ pip install .
```

First thing I did was to reproduce results for the HyperSpace Styblinski-Tang benchmark (on Bridges compute node):

```
$ cd benchmarks/styblinskitang/hyperdrive   
$ mpirun -n 4 python3 benchmark.py --ndims 2 --results \</path/to/save/results\>   
```

In order to visualize the results, install HyperSpace on your local machine this time and follow:

```
$ conda install mpi4py (through conda this time so MPI packages get installed as well)   
$ conda install scikit-learn seaborn   
```

Follow the Jupyter Notebook located in the repo [here](https://github.com/radical-group/koubbe/blob/master/HPO/HyperSpace/First%20benchmark/results/vis_results.ipynb) in order to visualize results

## Containers

 In order to see my Initial Presentation on Containers, please visit [Containers Initial Presentation](https://docs.google.com/presentation/d/1ZA0dlyVj5jCw4b_unFurkM9Q9E7sMrNNn_DfLtdanfA/edit?usp=sharing)

The experiments design is located [here](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/docs/First%20Container%20Experiments%20Design%20Dec%2012%2C%202019.pdf).

### Experiment 1

To run experiment 1, make sure stress-ng executable is installed on Bridges and radical stack is installed on local machine. Then, execute on local machine:

```
 $ ./stress_rp.sh
 ```

note: modify [stress_rp.py](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp1/stress_rp.py) accordingly to run via RP the  executable or the containerized executable.

### Experiment 2

To run experiment 2 on Bridges, execute on login node:

```
$ module load singularity  
$ singularity build centos-openmpi.sif docker://centos:centos7  
$ wget https://raw.githubusercontent.com/wesleykendall/mpitutorial/gh-pages/tutorials/mpi-hello-world/code/mpi_hello_world.c  
$ interact -p RM -N 2 -n 8 -t 8:00:00
```

Now, on compute node:

```
$ module load singularity  
$ export SINGULARITYENV_PREPEND_PATH=/opt/intel/compilers_and_libraries_2019.5.281/linux/mpi/intel64/bin/  
$ export SINGULARITYENV_LD_LIBRARY_PATH=/opt/intel/compilers_and_libraries_2019.5.281/linux/mpi/intel64/lib:/opt/intel/compilers_and_libraries_2019.5.281/linux/mpi/intel64/libfabric/lib  
$ mpicc mpi_hello_world.c -o hello_world_intel  
$ mpirun -n 4 -ppn 2 singularity exec --bind /opt/intel/compilers_and_libraries_2019.5.281/linux/mpi/intel64 $HOME/centos-openmpi.sif $HOME/hello_world_intel
```

## FACTS

My work consisted on helping out in running simple FACTS "modules" on XSEDE Bridges and verifying correct functionality. 
 
After this initial testing was done, I proceeded to package the [FACTS repo](https://github.com/radical-collaboration/facts) into a python pip package and uploaded it to the pip server for easy download of general users.

## Misc

Here you have general information about my work, readings, meetings, weekly summaries, etc.

## Installation of stress-ng executable

To install stress-ng on Bridges login node:

```
$ wget http://kernel.ubuntu.com/~cking/tarballs/stress-ng/stress-ng-0.09.34.tar.xz  
$ tar xvf stress-ng-0.09.34.tar.xz  
$ cd stress-ng-0.09.34  
$ make  
```

Request 1 node, 4 cores on RM partition for 8 hours: 
```
$ interact -p RM -N 1 -n 4 -t 8:00:00  
```

Measure Total Time of Execution of stress-ng python script through MPI:  
```
/usr/bin/time -v mpirun -n 2 python3 helloworld.py  
```

To see core usage on each node: 
```
$ ssh r001  
$ htop
```

note: helloworld.py is located in the repo [here](https://github.com/radical-group/koubbe/blob/master/HPO/HyperSpace/First%20benchmark/docs/Guides/stress-ng/helloworld.py)

## Installation of mpi4py on XSEDE Bridges using GCC compiler

If Anaconda (or Miniconda) not installed:  
```
$ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  
$ bash Miniconda3-latest-Linux-x86_64.sh
```

Else:  
```
$ conda create --name \<VE name\> python=3.7  
$ conda activate \<VE name\>  
$ wget https://bitbucket.org/mpi4py/mpi4py/downloads/mpi4py-3.0.3.tar.gz  
$ tar -zxf mpi4py-3.0.3.tar.gz  
$ cd mpi4py-3.0.3  
```

modify mpi.cfg as instructed in [mpi4py installation](https://mpi4py.readthedocs.io/en/stable/install.html#using-pip-or-easy-install):

```
\# Open MPI example  
\# ----------------  
[openmpi]  
mpi_dir              = /usr/mpi/gcc/openmpi-2.1.2-hfi  
mpicc                = %(mpi_dir)s/bin/mpicc  
mpicxx               = %(mpi_dir)s/bin/mpicxx  
#include_dirs        = %(mpi_dir)s/include  
#libraries           = mpi  
library_dirs         = %(mpi_dir)s/lib64:/opt/packages/gcc/9.2.0/bin/gcc  
runtime_library_dirs = %(library_dirs)s  
```

```
$ python setup.py build --mpi=openmpi  
$ python setup.py install  
```

## Reference

The local machine used throughout the proyects is a virtual machine with Ubuntu 16.04.6 LTS. 

The radical-stack used is:
```
  python               : 3.7.6
  pythonpath           : 
  virtualenv           : /home/karahbit/ve-rct3

  radical.analytics    : 0.90.7
  radical.entk         : 1.0.2
  radical.pilot        : 1.1.1
  radical.saga         : 1.1.2
  radical.utils        : 1.1.1
 ```

For specific references, please visit each section's topic.

 1. http://radical.rutgers.edu
 2. http://radical-cybertools.github.io
 3. https://www.psc.edu/bridges/user-guide
 4. https://www.sdsc.edu/support/user_guides/comet.html
 5. https://radicalpilot.readthedocs.io/en/stable
 6. https://radicalentk.readthedocs.io/en/latest
 7. https://hyperspace.readthedocs.io/en/latest
 8. https://sylabs.io/guides/3.5/user-guide/
 9. https://www.open-mpi.org
 10. https://wiki.ubuntu.com/Kernel/Reference/stress-ng
