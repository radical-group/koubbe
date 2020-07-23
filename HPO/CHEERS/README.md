# Hyperparameter Optimization (HPO)

In order to see my Initial Presentation on HPO, please visit [HPO Initial Presentation](https://github.com/karahbit/koubbe/blob/master/HPO/docs/HPO%20Initial%20Presentation.pdf)

For a brief overview of what the CHEERS project is, as well as experiments design and results, please visit the [CHEERS First Approach document](https://github.com/radical-collaboration/FastFingerPrinting/blob/feature/starter_tank/phase1/src/galloOSIOPT/hyperparams-opt/docs/First%20approach.pdf).

### Parallel Bayesian SMBO vs Grid Search

After playing around with HyperSpace and managing to get a working hyperparameter optimization code, the first thing that I did was a comparison of this approach (parallel Bayesian SMBO) against the already existing Grid Search one. You can find it here: [Andy_comparison_3params.ipynb](https://github.com/radical-collaboration/FastFingerPrinting/blob/feature/starter_tank/phase1/src/galloOSIOPT/hyperparams-opt/code/NIRONE2-5/Andy_comparison_3params.ipynb).

Of course, you need to have HyperSpace installed beforehand (I am assuming the user knows how to access the Comet remote HPC in this case):

```
Easy HyperSpace install on XSEDE Comet login node:

$ pip3 install virtualenv --user
$ add virtualenv to .bashrc:
	export PATH="/home/karahbit/.local/bin:$PATH"
$ source .bashrc
$ virtualenv -p python3 ve-cheers
$ module load mpi4py
$ source ve-cheers/bin/activate
$ pip install seaborn scikit-optimize==0.5.2
$ git clone https://github.com/yngtodd/hyperspace.git
$ cd ~/hyperspace
$ pip install .
$ export MV2_ENABLE_AFFINITY=0
$ srun --partition=debug --pty --nodes=2 --ntasks-per-node=24 -t 00:30:00 --wait=0 --export=ALL /bin/bash
$ mkdir /home/karahbit/hyperspace_results
$ mpirun -n 4 python benchmarks/styblinskitang/hyperdrive/benchmark.py --ndims 2 --results /home/karahbit/hyperspace_results
```

Now, because we are interested in running HPO on a remote cluster (Comet in this case), we would need to use RADICAL-Entk in order to submit our tasks (applications, executables, etc.) to the remote machine. I am assuming familiarity with RADICAL-Cybertools (RCT) at this point, before running my next experiment.

If you need to get up to speed with EnTK, I suggest you go to the [introduction](https://radicalentk.readthedocs.io/en/latest/introduction.html), [installation](https://radicalentk.readthedocs.io/en/latest/install.html) and run the [Getting Started](https://radicalentk.readthedocs.io/en/latest/user_guide/get_started.html) script.

### Weak Scaling experiment

As a natural next step, I went ahead and performed weak scaling experiments by running the following on local machine:

```
$ ./cheers_hyperspace_entk.sh
```

note: cheers_hyperspace_entk.sh is located [here](https://github.com/radical-collaboration/FastFingerPrinting/blob/feature/starter_tank/phase1/src/galloOSIOPT/hyperparams-opt/code/NIRONE2-5/cheers_hyperspace_entk.sh).

note2: modify [cheers_hyperspace_entk.py](https://github.com/radical-collaboration/FastFingerPrinting/blob/feature/starter_tank/phase1/src/galloOSIOPT/hyperparams-opt/code/NIRONE2-5/cheers_hyperspace_entk.py) according to your needs (e.g. which dataset, # of hyperparams, which remote cluster, etc.).

### Strong Scaling experiment

HyperSpace as it is has a method called “hyperdrive” which runs each subspace/optimization on its own single rank/core. There is also “dualdrive” which runs 2 subspaces/optimizations per rank/core.

In order to perform strong scaling, we would need to create more of these functions, e.g. quadrive, octadrive, etc (I made those names up), so we can run 4, 8, 16, etc. optimizations per MPI rank respectively.. Eventually, we would like to name this function something like “multidrive”, and specify the number of optimizations we would like per rank/core.

This requires new development, thus more time. I already started experimenting with “dualdrive”, but we can’t perform strong scaling until this is done.

You can find an issue created specifically for this purpose in the HyperSpace GitHub repo:
https://github.com/yngtodd/hyperspace/issues/31

As said before, you can see the results for both experiments in [CHEERS First Approach document](https://github.com/radical-collaboration/FastFingerPrinting/blob/feature/starter_tank/phase1/src/galloOSIOPT/hyperparams-opt/docs/First%20approach.pdf).

## Reference

The local machine used throughout the proyects is a virtual machine with Ubuntu 16.04.6 LTS. 

The radical-stack used is:
```
  python               : 3.8.3
  pythonpath           : 
  virtualenv           : ve-cheers

  radical.analytics    : 0.90.7
  radical.entk         : 1.4.0
  radical.pilot        : 1.4.0
  radical.saga         : 1.4.0
  radical.utils        : 1.4.0
 ```

For specific references, please visit each section's topic.

 1. http://radical.rutgers.edu
 2. http://radical-cybertools.github.io
 3. https://www.sdsc.edu/support/user_guides/comet.html
 4. https://radicalpilot.readthedocs.io/en/stable
 5. https://radicalentk.readthedocs.io/en/latest
 6. https://hyperspace.readthedocs.io/en/latest
 7. https://www.open-mpi.org 

Author: [George Koubbe](https://github.com/karahbit)