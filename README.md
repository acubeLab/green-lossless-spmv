<p align="center">
 <img src="logo.svg" alt="The logo of the project" width="200">
</p>

The **Green Lossless Sparse Matrix-Vector Multiplication** (SpMV) project focuses on lossless compression techniques optimizing space, time, and energy for multiplications between binary or ternary matrix formats and real-valued vectors.

## Getting Started

### Prerequisites

#### general

* Python version 3.8 or later

```sh
sudo apt install clang g++ gcc cmake
```

#### mm-repair

* [sdsl-lite](https://github.com/simongog/sdsl-lite) (`git clone https://github.com/simongog/sdsl-lite.git` + 
`cd sdsl-lite` + `./install.sh`)

* [psutil](https://pypi.org/project/psutil/) (`pip install psutil`)

#### zuckerli

```sh
sudo apt install libgtest-dev libgmock-dev 
```

#### perf

```sh
sudo apt install linux-tools-common linux-tools-generic linux-tools-`uname -r`
```

### Download Datasets

Visit [this link](https://sparse.tamu.edu/LAW) and download all relevant datasets in Matrix Market format. Extract the files with the `.mtx` extension with the `tar -xzf` command.


### Building the Project

To build the project, follow these steps.

First load the submodules:
```sh
git submodule update --init --recursive
```

Then, compile all targets:
```sh
mkdir build && cd build && cmake .. && make -j 12 && cd ..
```

The `mm-repair` library does not use `cmake`; hence, one has to compile it separately: 
```sh
cd mm-repair && make -j 12 && cd ..
```


## Usage

### Compress the datasets

To prepare the compressed matrix formats, run the following command where the arguments represent the parallelism degree:
```sh
python3 prepare_data.py 1 8 16
```
In the above example, we prepare matrix formats for 1, 8, and 16 threads.

By default the script compresses the matrix `cnr-2000.mtx` in the `example` directory. To define a different dataset create a `datasets.py` file containing the appropriate definition of the directory `DATA_PATH` and of the list of `.mtx` files. See `sample_datasets.py` for an example. 


### Execute Pagerank


Run `pagerank.py` passing as arguments the number of threads: 
```sh
[sudo] python3 pagerank.py 1 8 16  &> out.log
```
**Note:** In the background, `pagerank.py` utilizes the `perf` tool to monitor cache accesses, clock cycles, instructions, and more. Typically, this requires executing the script with superuser privileges. To eliminate the need to run `pagerank.py` as a superuser, ask your system administrator to adjusti the `/proc/sys/kernel/perf_event_paranoid` setting to 0 with the command
```sh
 sudo sh -c 'echo 0 >  /proc/sys/kernel/perf_event_paranoid'
```
to permit access to performance monitoring and observability operations to unprivileged users;
see [this guide](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html) for further information. Additionally, please verify the available energy events for RAPL on your machine. You can check the energy events by running either:
```bash
ls /sys/bus/event_source/devices/power/events
```
or
```bash
sudo perf list | grep energy
```
By default, the script reports `power/energy-pkg/` (energy consumption at the package level) and `power/energy-ram/` (energy used by the RAM). These events were measurable on our machine. However, on other machines, you may find `power/energy-cpu/` (energy consumption at cores level) available. If this is the case, we recommend modifying the `PREAMBLE` global variable in the `pagerank.py` script accordingly.

### Extracting statistics to a CSV

To extract statistics from the PageRank log, run `extract_stats.py` passing the name of the log file as parameter:
```sh
python3 extract_stats.py out.log
```
this will produce a CSV file `out.csv` with metrics extracted from `out.log`.

The `out.csv` file contains the following columns:

* `DATASET`: The name of the dataset.
* `START`: The timestamp indicating when the algorithm commenced.
* `ALGO`: The compression algorithm used.
* `PARDEGREE`: The degree of parallelism, i.e., the number of active threads.
* `MAXITER`: The total number of PageRank iterations performed.
* `DAMPF`: The damping factor used in PageRank.
* `TOPK`: The number of highest-scoring vertices included in the PageRank output.
* `NNODES`: The total number of vertices in the input graph.
* `NDANGLING`: The number of dangling nodes in the input graph.
* `NEDGES`: The total number of edges in the input graph.
* `SUM`: The sum of PageRank values (should equal 1).
* `L1DCL`: The number of L1 data cache loads (including both hits and misses).
* `L1DCLM`: The number of L1 data cache load misses.
* `L1DCS`: The number of L1 data cache stores.
* `LLCL`: The number of last-level cache loads (including both hits and misses).
* `LLCLM`: The number of last-level cache load misses.
* `LLCS`: The number of last-level cache stores.
* `CYCLES`: The total number of clock cycles.
* `INSTR`: The total number of instructions executed.
* `ENERGY_PKG`: The energy consumption at the socket level, as measured by RAPL.
* `ENERGY_CORES`: The energy consumption at the core level, as measured by RAPL.
* `ENERGY_RAM`: The energy consumption at the RAM level, as measured by RAPL.
* `ELAPSED`: The total completion time.
* `PMU`: The peak memory usage in kilobytes.
* `DISK`: The disk space used, measured in bytes.


## License

This project is licensed under the terms of the Apache License 2.0.  
The logo [`logo.svg`](./logo.svg) is a derivative work based on the file [File:Betelblatt.svg](https://commons.wikimedia.org/wiki/File:Betelblatt.svg), uploaded by the user Furfur on Wikimedia Commons and licensed under CC BY-SA 4.0.

If you use the library please cite the following paper:

> F. Tosoni, P. Bille, V. Brunacci, A. d. Angelis, P. Ferragina and G. Manzini, "Toward Greener Matrix Operations by Lossless Compressed Formats," in IEEE Access, vol. 13, pp. 56756-56779, 2025, doi: [10.1109/ACCESS.2025.3555119](https://doi.org/10.1109/ACCESS.2025.3555119). keywords: {Sparse matrices;Energy consumption;Energy efficiency;Software;Vectors;Servers;Internet of Things;Big Data;Meters;Machine learning algorithms;Green computing;lossless compression techniques;compressed matrix formats;matrix-to-vector multiplications;computation-friendly compression;PageRank}, 

```tex
@ARTICLE{tosoni2024greenermatrixoperationslossless,
  author={Tosoni, Francesco and Bille, Philip and Brunacci, Valerio and Angelis, Alessio de and Ferragina, Paolo and Manzini, Giovanni},
  journal={IEEE Access}, 
  title={Toward Greener Matrix Operations by Lossless Compressed Formats}, 
  year={2025},
  volume={13},
  number={},
  pages={56756-56779},
  keywords={Sparse matrices;Energy consumption;Energy efficiency;Software;Vectors;Servers;Internet of Things;Big Data;Meters;Machine learning algorithms;Green computing;lossless compression techniques;compressed matrix formats;matrix-to-vector multiplications;computation-friendly compression;PageRank},
  doi={10.1109/ACCESS.2025.3555119}}
```

## Acknowledgments

- Thanks to the contributors and the open-source community.
- Special thanks to the [LAW group](https://law.di.unimi.it/) and the [SuiteSparse Matrix Collection](https://sparse.tamu.edu/) for providing the datasets.
