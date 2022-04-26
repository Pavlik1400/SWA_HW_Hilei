#!/bin/bash

# 3 other processes
python3 counting_no_lock.py -n 0 &
python3 counting_no_lock.py -n 1 &
python3 counting_no_lock.py -n 2
