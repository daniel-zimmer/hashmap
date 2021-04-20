from ctypes import *
from random import randint
import timeit

c = CDLL("./hashmap.so")

c.HASHMAP_create.argtypes = None
c.HASHMAP_create.restype  = c_void_p

c.HASHMAP_put.argtypes = [c_void_p, c_char_p, c_void_p]
c.HASHMAP_put.restype  = c_void_p

c.HASHMAP_get.argtypes = [c_void_p, c_char_p]
c.HASHMAP_get.restype  = c_void_p

###########
chars = ['0', '@', 'P', '`', 'p', '!', '1', 'A', 'Q', 'a', 'q', '"', '2', 'B', 'R', 'b', 'r', '#', '3', 'C', 'S', 'c', 's', '$', '4', 'D', 'T', 'd', 't', '%', '5', 'E', 'U', 'e', 'u', '&', '6', 'F', 'V', 'f', 'v', '\'', '7', 'G', 'W', 'g', 'w', '(', '8', 'H', 'X', 'h', 'x', ')', '9', 'I', 'Y', 'i', 'y', '*', ':', 'J', 'Z', 'j', 'z', '+', ';', 'K', '[', 'k', '{', ',', '<', 'L', '\\', 'l', '|', '-', '=', 'M', ']', 'm', '}', '.', '>', 'N', '^', 'n', '~', '/', '?', 'O', '_', 'o']
def randomStr():
	key = ""
	for i in range(randint(1, 16)):
		key += chars[randint(0, len(chars)-1)]
	return create_string_buffer(bytes(key, "ascii"))
###########

# A reference to the string buffer created for keys
# and for values must be retained so that the garbage
# colletor does not yeet it.

pyHashmap = {}

cHashmap = c.HASHMAP_create()
print("hashmap created, address: " + hex(cHashmap))

print("generating keys ... ")
keys = []
keysStr = []
sameValue = create_string_buffer(b"batata")
total = 100000
for i in range(total):
	newKey = randomStr()
	keys.append(newKey)
	keysStr.append(str(newKey.value))


print("py dict")
start_time = timeit.default_timer()
for i in range(total):
	pyHashmap[keysStr[i]] = sameValue
insert_time = timeit.default_timer() - start_time

print("insert time: " + str(insert_time))

start_time = timeit.default_timer()
for i in range(total):
	value = pyHashmap[str(keys[i].value)]
retrieve_time = timeit.default_timer() - start_time 

print("retrieve time: " + str(retrieve_time))

print("total time: " + str(insert_time + retrieve_time))

print("c hashmap")

start_time = timeit.default_timer()
for i in range(total):
	cHashmap = c.HASHMAP_put(cHashmap, keys[i], sameValue)
insert_time = timeit.default_timer() - start_time

print("insert time: " + str(insert_time))

start_time = timeit.default_timer()
for i in range(total):
	value = c.HASHMAP_get(cHashmap, keys[i])
retrieve_time = timeit.default_timer() - start_time 

print("retrieve time: " + str(retrieve_time))

print("total time: " + str(insert_time + retrieve_time))

