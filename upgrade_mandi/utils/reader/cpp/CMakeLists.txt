cmake_minimum_required(VERSION 4.1)
project(reader)
add_executable(reader main.cpp)

include_directories(${PROJECT_SRC}/utils/reader/cpp/include)