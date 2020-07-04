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
 
 The results of these applications are posted [here](https://github.com/radical-group/koubbe/blob/master/RCT/First%20Example%20on%20EnTK/results/results.pdf)

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

note: stress_rp.sh is located [here](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp1/stress_rp.sh).

note2: modify [stress_rp.py](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp1/stress_rp.py) accordingly to run via RP the executable or the containerized executable.

### Experiment 2

We are going to run a Singularity containerized MPI executable on Bind mode [(what is Bind mode?)](https://sylabs.io/guides/3.5/user-guide/mpi.html). Same as with experiment 1, we are going to execute on local machine:

```
 $ ./mpi_rp.sh
 ```

 ##### On Bridges:
 
note: For further instructions on how to build the container and install/compile the executable, go [here](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp2/Bridges/Bind-Intel19.5/instructions.txt)
 
note2: mpi_rp.sh is located [here](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp2/Bridges/Bind-Intel19.5/mpi_rp.sh)

note3: modify [mpi_rp.py](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp2/Bridges/Bind-Intel19.5/mpi_rp.py) accordingly to run via RP the executable or the containerized executable.

##### On Comet:

note: For further instructions on how to build the container and install/compile the executable, go [here](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp2/Comet/Bind-IntelMPI/instructions.txt)
 
note2: mpi_rp.sh is located [here](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp2/Comet/Bind-IntelMPI/mpi_rp.sh)

note3: modify [mpi_rp.py](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/src/exp2/Comet/Bind-IntelMPI/mpi_rp.py) accordingly to run via RP the executable or the containerized executable.

## FACTS

### Getting started

My initial work consisted on helping out in running simple FACTS "modules" on XSEDE Bridges and verifying correct functionality. 
 
After this testing was done, I proceeded to package the [FACTS repo](https://github.com/radical-collaboration/facts) into a python pip package and uploaded it to the pip server for easy download of general users.

Lastly, I was tasked with the containerization of the FACTS framework. As it is right now, automation is achieved by creating a virtual environment and installing FACTS along with its dependencies through PIP. This framework will launch the executables for the required modules on a remote machine, being an HPC cluster, etc. 

So, why do we need containers? What is the benefit that containers are going to bring to FACTS?

We envision this at two levels:

1) We containerize at the framework level. This will allow us to take FACTS apart into individual modules, completely independent from one another, with their own container each. The end user won’t have to know about anything else, no virtual environment, no dependencies, no other steps. We would take full advantage of the portability and reproducibility benefits of containers. Therefore, the end user can simply execute the containerized module on the local machine. We can use Docker for this purpose.
2) We containerize at the executable level. There is a growing number of modules inside FACTS. Each module has 4 stages: pre-processing, fit, project, post-processing. Each stage has one executable (python3 script). We can use Singularity for this purpose.

Few notes to keep in mind:

- Input data is not going to be included in the container. We can integrate (bind mount) it to the Docker container at the time of execution. Singularity already offers integration features that make this easier.

- Where are we going to obtain the containers from?	As said before, each container would be representing a FACTS module. The containers can be downloaded from Docker Hub or the Singularity equivalent, for example, with every container being specific to the application and remote resource. Lastly, the end user would just need to execute the container.

### Containerization at the executable level

As an initial approach, I started containerizing at the executable level (Singularity) on Comet with the kopp14 module and data that Greg sent me. Once done, I characterized performance and looked for any overheads. You can read how to run the container from the following file: [facts_re.sh](https://github.com/radical-group/koubbe/blob/master/FACTS/Containerizing%20FACTS/Executable%20level/src/Comet/facts/facts_re.sh). You can find the results in the last slide of the presentation [here](https://github.com/radical-group/koubbe/blob/master/Containers/First%20experiments/docs/Containers%20Initial%20Presentation.pdf).

note: keep in mind that you would have to build the Singularity container from the definition file I provided by running the following command:

```
$ sudo singularity build kopp14_landwaterstorage.sif kopp14_landwaterstorage.def
```

### Containerization at the framework level

This was not a requirement at the moment, but for fun I proceeded to create a Dockerfile containerizing FACTS at the framework level. You can find the file [here](https://github.com/radical-group/koubbe/blob/master/FACTS/Containerizing%20FACTS/Framework%20level/Dockerfile)


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
$ tar -zxf mpi4py-3.0.3.tar.gz && rm mpi4py-3.0.3.tar.gz
$ cd mpi4py-3.0.3  
```

modify mpi.cfg as instructed in [mpi4py installation](https://mpi4py.readthedocs.io/en/stable/install.html#using-pip-or-easy-install):

```
# Open MPI example  
# ----------------  
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
  radical.pilot        : 1.3.0
  radical.saga         : 1.3.0
  radical.utils        : 1.3.0
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
 9. https://containers-at-tacc.readthedocs.io/en/latest/
 10. https://www.open-mpi.org
 11. https://wiki.ubuntu.com/Kernel/Reference/stress-ng
