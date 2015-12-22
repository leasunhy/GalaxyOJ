import os

CONFIG_NAME = 'judge'

# compile time limit in seconds
COMPILE_TIME_LIMIT = 10

# compiler options
COMPILER_LIST = ["g++", "gcc", "fpc", "g++"]
COMPILER_NAME_LIST = ["g++ 5.3.0", "gcc 5.3.0", "fpc 3.0.0", "c++11 5.3.0"]
COMPILER_OPTION_LIST = [
        ["-O2", "-Wall", "-lm", "--static", "-DONLINE_JUDGE"],
        ["-O2", "-Wall", "-lm", "--static", "-std=c99","-DONLINE_JUDGE"],
        ["-O1", "-Co", "-Cr", "-Ct", "-Ci"],
        ["-O2", "-Wall", "-lm", "-std=c++11", "--static", "-DONLINE_JUDGE"]]
