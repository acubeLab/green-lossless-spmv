cmake_minimum_required(VERSION 3.12)
project(raspi-energy)

add_executable(rmult_plain util/right_multiply_plain.cpp)
add_executable(page_rank_plain util/page_rank_plain.cpp)

add_subdirectory(matrix_gn)
add_subdirectory(k2tree_basic_v0.1)
add_subdirectory(zuckerli)

