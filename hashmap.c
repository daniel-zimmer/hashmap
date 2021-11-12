#include "hashmap.h"

#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define PERTURB_SHIFT 5
#define HASHMAP_INIT_CAP 16

struct hashmap {
	uint64_t size;
	uint64_t cap;
	struct bucket {
		char        *key;
		uint64_t     hash;
		HASHMAP_type value;
	} bucket[];
};

static uint64_t hash(char *key) {
	uint64_t h_val = *key << 7;
	uint32_t len = 0;
	while (*key != '\0') {
		h_val = h_val * 1000003 ^ *key;
		key++;
		len++;
	}
	return h_val ^ len;
}

static uint32_t collision(uint32_t idx, uint32_t perturb,  uint32_t cap) {
	return ((idx*5) + 1 + perturb) % cap;
}

static Hashmap *create(uint32_t cap) {
	Hashmap *hm = malloc(
		sizeof(struct hashmap) +
		sizeof(struct bucket) * cap
	);

	hm->size = 0;
	hm->cap  = cap;

	for (int i = 0; i < hm->cap; i++) {
		hm->bucket[i].key = NULL;
	}

	return hm;
}

Hashmap *HASHMAP_create() {
	return create(HASHMAP_INIT_CAP);
}

static Hashmap *resize(Hashmap *old) {
	Hashmap *new = create(old->cap<<1);
	new->size = old->size;

	for (uint32_t i = 0; i < old->cap; i++) {
		if (old->bucket[i].key == NULL) continue;

		uint64_t index   = old->bucket[i].hash%new->cap;
		uint32_t perturb = old->bucket[i].hash;

		while (new->bucket[index].key != NULL) {
			index = collision(index, perturb, new->cap);
			perturb >>= PERTURB_SHIFT;
		}

		new->bucket[index].key   = old->bucket[i].key;
		new->bucket[index].hash  = old->bucket[i].hash;
		new->bucket[index].value = old->bucket[i].value;
	}

	free(old);
	return new;
}

Hashmap *HASHMAP_put(Hashmap *hm, char *key, HASHMAP_type value) {
	uint64_t hash_val = hash(key);
	uint32_t perturb  = hash_val;

	if (hm->size > hm->cap>>1) {
		hm = resize(hm);
	}

	uint64_t index = hash_val%hm->cap;
	while (hm->bucket[index].key != NULL) {
		if (
			hm->bucket[index].hash == hash_val &&
			!strcmp(hm->bucket[index].key, key)
		) {
			hm->bucket[index].value = value;
			return hm;
		}
		index = collision(index, perturb, hm->cap);
		perturb >>= PERTURB_SHIFT;
	}

	hm->bucket[index].key   = strdup(key);
	hm->bucket[index].hash  = hash_val;
	hm->bucket[index].value = value;
	hm->size++;

	return hm;
}

HASHMAP_type *HASHMAP_get(Hashmap *hm, char *key) {
	uint64_t hash_val = hash(key);
	uint32_t perturb  = hash_val;

	uint64_t index = hash_val%hm->cap;
	while (hm->bucket[index].key != NULL) {
		if (
			hm->bucket[index].hash == hash_val &&
			!strcmp(hm->bucket[index].key, key)
		) {
			return &hm->bucket[index].value;
		}

		index = collision(index, perturb, hm->cap);
		perturb >>= PERTURB_SHIFT;
	}

	return NULL;
}


uint32_t HASHMAP_size(Hashmap *hm) {
	return hm->size;
}

void HASHMAP_iterate(Hashmap *hm, void (*iterFunc) (char *, HASHMAP_type *)) {
	for (uint32_t i = 0; i < hm->cap; i++) {
		if (hm->bucket[i].key == NULL) continue;
		iterFunc(hm->bucket[i].key, &hm->bucket[i].value);
	}
}

void HASHMAP_freeDestroy(HASHMAP_type *value) {
	if (value->type == HASHMAP_type_ptr) {
		free(value->ptr);
	}
}

void HASHMAP_destroy(Hashmap *hm, void (*delFunc) (HASHMAP_type *)) {
	for (uint32_t i = 0; i < hm->cap; i++) {
		if (hm->bucket[i].key == NULL) continue;

		if (delFunc != NULL) {
			delFunc(&hm->bucket[i].value);
		}
		free(hm->bucket[i].key);
	}
	free(hm);
}

#ifdef TEST

static char **TEST_stack = NULL;
static uint32_t TEST_stackIdx = 0;

void TEST_createStack(uint32_t size) {
	if (TEST_stack != NULL) {
		free(TEST_stack);
	}
	TEST_stack = malloc(size * sizeof(void *));
	TEST_stackIdx = 0;
}

char *TEST_popStack() {
	return TEST_stack[--TEST_stackIdx];
}

void TEST_iterFunc(char *key, void *value) {
	TEST_stack[TEST_stackIdx++] = key;
}

void TEST_delFunc(void *value) {
	TEST_stackIdx++;
}

uint32_t TEST_getStackIdx() {
	return TEST_stackIdx;
}

#endif
