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

Visit [this link](https://sparse.tamu.edu/LAW) and download all relevant datasets in Matrix Market format. Extract the files with the .mtx extension with the `tar -xzf` command.


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

To prepare the compressed matrix formats, run the following command where the options represent the parallelism degree:
```sh
python3 prepare_data.py 1 8 16
```
In the above example, we prepare matrix formats for 1, 8, and 16 threads.

By default the script compresses teh dataset `enron.mtx` in the `example` directory. To define a different dataset creates a `datasets.py` file containing the definition of `DATA_PATH` and of the list of `.mtx` files. See `sample_datasets.py` for an example. 


### Execute Pagerank
Modify `pagerank.py` to set `DATA_PATH` to the path where the datasets in `.mtx` format are stored.
Then, run `pagerank.py`.
```sh
python3 pagerank.py 1 8 16
```

### Extracting statistics to a CSV

To extract statistics from the PageRank log, first redirect the output of `pagerank.py` to a log.
```sh
python3 pagerank.py 1 8 16 &> out.log
```
Then, run `extract_stats.py` passing the name of the log file as parameter. This will produce a CSV file `out.csv` with metrics extracted from `out.log`.
```sh
python3 extract_stats.py out.log
```

## Licence

This project is licensed under the terms of the Apache License 2.0. The logo [`green-lossless-spmv-logo.svg`](./green-lossless-spmv-logo.svg) is a derivative work of the file [Fluent Emoji flat 1f342.svg](https://commons.wikimedia.org/wiki/File:Fluent_Emoji_flat_1f342.svg) distributed under the MIT License.

If you use the library please cite the following paper:

> Francesco Tosoni, Philip Bille, Valerio Brunacci, Alessio De Angelis, Paolo Ferragina, and Giovanni Manzini. Toward Greener Matrix Operations by Lossless Compressed Formats. arXiv preprint arXiv:2409.18620, 2024. Available at: https://arxiv.org/abs/2409.18620.

```tex
@misc{tosoni2024greenermatrixoperationslossless,
      title={Toward Greener Matrix Operations by Lossless Compressed Formats}, 
      author={Francesco Tosoni and Philip Bille and Valerio Brunacci and Alessio De Angelis and Paolo Ferragina and Giovanni Manzini},
      year={2024},
      eprint={2409.18620},
      archivePrefix={arXiv},
      primaryClass={cs.DS},
      url={https://arxiv.org/abs/2409.18620}, 
}
```

## Acknowledgments

- Thanks to the contributors and the open-source community.
- Special thanks to the [LAW group](https://law.di.unimi.it/) and the [SuiteSparse Matrix Collection](https://sparse.tamu.edu/) for providing the datasets.
