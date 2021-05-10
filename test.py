from ctypes import *
from random import randint

c = CDLL("./hashmap.so")

c.HASHMAP_create.argtypes = None
c.HASHMAP_create.restype  = c_void_p

c.HASHMAP_put.argtypes = [c_void_p, c_char_p, c_void_p]
c.HASHMAP_put.restype  = c_void_p

c.HASHMAP_get.argtypes = [c_void_p, c_char_p]
c.HASHMAP_get.restype  = c_void_p

c.HASHMAP_size.argtypes = [c_void_p]
c.HASHMAP_size.restype  = c_int

c.HASHMAP_iterate.argtypes = [c_void_p, c_void_p]
c.HASHMAP_iterate.restype  = None

c.HASHMAP_delete.argtypes = [c_void_p, c_void_p]
c.HASHMAP_delete.restype  = None

c.TEST_createStack.argtypes= [c_int]
c.TEST_createStack.restype = None

c.TEST_popStack.argtypes= None
c.TEST_popStack.restype = c_char_p

c.TEST_getStackIdx.argtypes= None
c.TEST_getStackIdx.restype = c_int

###########
chars = ['0', '@', 'P', '`', 'p', '!', '1', 'A', 'Q', 'a', 'q', '"', '2', 'B', 'R', 'b', 'r', '#', '3', 'C', 'S', 'c', 's', '$', '4', 'D', 'T', 'd', 't', '%', '5', 'E', 'U', 'e', 'u', '&', '6', 'F', 'V', 'f', 'v', '\'', '7', 'G', 'W', 'g', 'w', '(', '8', 'H', 'X', 'h', 'x', ')', '9', 'I', 'Y', 'i', 'y', '*', ':', 'J', 'Z', 'j', 'z', '+', ';', 'K', '[', 'k', '{', ',', '<', 'L', '\\', 'l', '|', '-', '=', 'M', ']', 'm', '}', '.', '>', 'N', '^', 'n', '~', '/', '?', 'O', '_', 'o']
def randomStr():
	key = ""
	for i in range(randint(1, 128)):
		key += chars[randint(0, len(chars)-1)]
	return create_string_buffer(bytes(key, "ascii"))
###########

# A reference to the string buffer created for keys
# and for values must be retained so that the garbage
# colletor does not yeet them.

print()

pyHashmap = {}

cHashmap = c.HASHMAP_create()
print("hashmap created, address: " + hex(cHashmap))

print("generating keys ... ")
keys = []
for i in range(10000):
	keys.append(randomStr())

print("inserting values ... ")
usedKeys = []
for i in range(10000):
	key = keys[randint(0, len(keys)-1)]
	usedKeys.append(key)
	value = randomStr()

	cHashmap = c.HASHMAP_put(cHashmap, key, value)
	pyHashmap[str(key.value)] = value

print("retrieving values ... ")
total = 100000
right = 0
for i in range(total):
	key = usedKeys[randint(0, len(usedKeys)-1)]

	actual   = str(cast(c.HASHMAP_get(cHashmap, key), c_char_p).value)
	expected = str(pyHashmap[str(key.value)].value)

	if (actual != expected):
		print("oh no: key: %s - actual: %s - expected: %s" % (str(key.value), actual, expected))
	else:
		right+=1

print("results: (%d/%d)" % (right, total))

delTestHashmap = pyHashmap.copy()

## HASHMAP_size
actualSize   = c.HASHMAP_size(cHashmap)
expectedSize = len(pyHashmap)

if actualSize == expectedSize:
	print("size of hashmap is correct")
else:
	print("wrong size - actual: %s - expected: %s" % (actualSize, expectedSize))

## HASHMAP_iterate
c.TEST_createStack(c.HASHMAP_size(cHashmap))

c.HASHMAP_iterate(cHashmap, c.TEST_iterFunc)

for i in range(c.HASHMAP_size(cHashmap)):
	pyHashmap.pop(str(cast(c.TEST_popStack(), c_char_p).value))

if len(pyHashmap) == 0:
	print("iterated through all keys")
else:
	print("did not iterate correctly - missed %d keys" % len(pyHashmap))

## HASHMAP_delete
c.HASHMAP_delete(cHashmap, c.TEST_delFunc)

if c.TEST_getStackIdx() == actualSize:
	print("deleted all keys")
else:
	print("did not delete all keys - missed %d keys" % (actualSize - c.TEST_getStackIdx()))

print()
