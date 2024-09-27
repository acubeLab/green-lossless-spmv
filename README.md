<p align="center">
  <img src="green-lossless-spmv-logo.svg" alt="The Green Lossless SpMV" width="200">
</p>

The **Green Lossless Sparse Matrix-Vector Multiplication** (SpMV) project focuses on lossless compression techniques aimed at optimizing space, time, and energy for multiplications between binary or ternary matrix formats and real-valued vectors.

## Getting Started

### Prerequisites

Ensure you have the following dependencies installed:

```sh
sudo apt install clang libgtest-dev libgmock-dev
```

### Download Datasets

Visit [this link](https://sparse.tamu.edu/LAW) and download all relevant datasets in Matrix Market format (.mtx extension).

### Building the Project

To build the project, follow these steps:

```sh
git submodule update --init --recursive
mkdir build && cd build && cmake ..
make -j 12
```

## Usage

TODO


## License

This project is licensed under the terms of the Apache License 2.0. The logo [`green-lossless-spmv-logo.svg`](./green-lossless-spmv-logo.svg) is a derivative work of the file [Fluent Emoji flat 1f342.svg](https://commons.wikimedia.org/wiki/File:Fluent_Emoji_flat_1f342.svg) distributed under the MIT License.

If you use the library please cite the following paper:

> Francesco Tosoni and  .....

```tex
@article{???}
```

## Acknowledgments

- Thanks to the contributors and the open-source community.
- Special thanks to the [LAW group](https://sparse.tamu.edu/LAW) for providing the datasets.
