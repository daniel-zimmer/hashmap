build: hashmap.o

clean:
	rm -rf hashmap.o

.PHONY: build clean


hashmap.o: hashmap.c hashmap.h
	gcc -Wall -O3 -c $< -o $@
