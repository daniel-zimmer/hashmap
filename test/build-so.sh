#!/bin/sh

cd ..
gcc -Wall -shared -fPIC hashmap.c -o test/hashmap.so -O3
cd test
