#!/bin/bash
python3 producer.py &
python3 consumer.py -n 0 &
python3 consumer.py -n 1