#!/bin/bash

echo "Building frontend"
cd frontend
bash ./build.sh
cd ..

echo "Building results"
cd ./results
bash build.sh
