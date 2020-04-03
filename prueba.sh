#! /bin/bash

for f in ./data/*
do
    python3 solver.py $f dc
done