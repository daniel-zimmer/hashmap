build: hashmap.o

clean:
	rm -rf hashmap.o

.PHONY: build clean test

###################################

hashmap.o: hashmap.c hashmap.h
	gcc -Wall -O3 -c $< -o $@

test:
	gcc -Wall -shared -fPIC hashmap.c -o hashmap.so -O3 -DTEST
	python3 test.py
	rm -rf hashmap.so
