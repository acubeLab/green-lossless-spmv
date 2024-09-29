<p align="center">
 <img src="green-lossless-spmv-logo.svg" alt="The Green Lossless SpMV" width="200">
</p>

The **Green Lossless Sparse Matrix-Vector Multiplication** (SpMV) project focuses on lossless compression techniques optimizing space, time, and energy for multiplications between binary or ternary matrix formats and real-valued vectors.

## Getting Started

### Prerequisites

Ensure you have the following dependencies installed:

```sh
sudo apt install clang libgtest-dev libgmock-dev
```

### Download Datasets

Visit [this link](https://sparse.tamu.edu/LAW) and download all relevant datasets in Matrix Market format (.mtx extension).

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

Modify `prepare_data.py` to set `DATA_PATH` to the path where the datasets in `.mtx` format are stored.
Then, to prepare the compressed matrix formats, run the following command where the options represent the parallelism degree:
```sh
python3 prepare_data.py 1 8 16
```
In the above example, we prepare matrix formats for 1, 8, and 16 threads.

### Execute Pagerank
Modify `pagerank.py` to set `DATA_PATH` to the path where the datasets in `.mtx` format are stored.
Then, run `pagerank.py`.
```sh
python3 prepare_data.py 1 8 16
```

### Extracting statistics to a CSV

To extract statistics from the PageRank log, first redirect the output of `pagerank.py` to a log.
```sh
python3 prepare_data.py 1 8 16 &> out.log
```
Then, run `extract_stats.py` passing the name of the log file as parameter. This will produce a CSV file `out.csv` with metrics extracted from `out.log`.
```sh
python3 extract_stats.py out.log
```

## Licence

This project is licensed under the terms of the Apache License 2.0. The logo [`green-lossless-spmv-logo.svg`](./green-lossless-spmv-logo.svg) is a derivative work of the file [Fluent Emoji flat 1f342.svg](https://commons.wikimedia.org/wiki/File:Fluent_Emoji_flat_1f342.svg) distributed under the MIT License.

If you use the library please cite the following paper:

> Francesco Tosoni and  .....

```tex
@article{???}
```

## Acknowledgments

- Thanks to the contributors and the open-source community.
- Special thanks to the [LAW group](https://sparse.tamu.edu/LAW) for providing the datasets.
