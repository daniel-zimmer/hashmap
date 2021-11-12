from ctypes import *
from random import randint

c = CDLL("./hashmap.so")

class HASHMAP_type(Structure):
	_fields_ = [
		("type", c_int),
		("ptr", c_char_p)
	]

c.HASHMAP_create.argtypes = None
c.HASHMAP_create.restype  = c_void_p

c.HASHMAP_put.argtypes = [c_void_p, c_char_p, HASHMAP_type]
c.HASHMAP_put.restype  = c_void_p

c.HASHMAP_get.argtypes = [c_void_p, c_char_p]
c.HASHMAP_get.restype  = POINTER(HASHMAP_type)

c.HASHMAP_size.argtypes = [c_void_p]
c.HASHMAP_size.restype  = c_int

c.HASHMAP_iterate.argtypes = [c_void_p, c_void_p]
c.HASHMAP_iterate.restype  = None

c.HASHMAP_destroy.argtypes = [c_void_p, c_void_p]
c.HASHMAP_destroy.restype  = None

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
	return key
#	return create_string_buffer(bytes(key, "ascii"))
###########

# A reference to the string buffer created for keys
# and for values must be retained so that the garbage
# colletor does not yeet them.

total = 100000

print()

pyHashmap = {}

cHashmap = c.HASHMAP_create()
print("hashmap created, address: " + hex(cHashmap))

keys = []
for i in range(total):
	print("\rgenerating keys ... (%s/%s)"%(i+1, total), end='')
	keys.append(randomStr())
print()

usedKeys = []
hm_vals = []
for i in range(total):
	print("\rinserting values ... (%s/%s)"%(i+1, total), end='')
	key = keys[randint(0, len(keys)-1)]
	usedKeys.append(key)
	value = randomStr()

	hm_val = HASHMAP_type(0, value.encode("ascii"))
	hm_vals.append(hm_val)
	cHashmap = c.HASHMAP_put(cHashmap,
		key.encode("ascii"),
		hm_val
	)
	pyHashmap[key] = value
print()

right = 0
for i in range(total):
	print("\rretrieving values ... (%s/%s)"%(i+1, total), end='')
	key = usedKeys[randint(0, len(usedKeys)-1)]

	actual = c.HASHMAP_get(cHashmap, key.encode("ascii")).contents.ptr.decode("ascii")
	expected = pyHashmap[key]

	if (actual != expected):
		print("oh no: key: %s - actual: %s - expected: %s" % (key, actual, expected))
	else:
		right+=1
print()

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
	pyHashmap.pop(c.TEST_popStack().decode("ascii"))

if len(pyHashmap) == 0:
	print("iterated through all keys")
else:
	print("did not iterate correctly - missed %d keys" % len(pyHashmap))

## HASHMAP_delete
c.HASHMAP_destroy(cHashmap, c.TEST_delFunc)

if c.TEST_getStackIdx() == actualSize:
	print("deleted all keys")
else:
	print("did not delete all keys - missed %d keys" % (actualSize - c.TEST_getStackIdx()))

print()
