#ifndef HASHMAP_H
#define HASHMAP_H

#include <stdint.h>

typedef struct hashmap Hashmap;

enum HASHMAP_value_type {
	HASHMAP_type_int8,
	HASHMAP_type_int16,
	HASHMAP_type_int32,
	HASHMAP_type_int64,

	HASHMAP_type_uint8,
	HASHMAP_type_uint16,
	HASHMAP_type_uint32,
	HASHMAP_type_uint64,
	
	HASHMAP_type_f32,
	HASHMAP_type_f64,
	
	HASHMAP_type_ptr
};

typedef struct {
	enum HASHMAP_value_type type;
	union {
		int8_t  int8;
		int16_t int16;
		int32_t int32;
		int64_t int64;
	
		uint8_t  uint8;
		uint16_t uint16;
		uint32_t uint32;
		uint64_t uint64;
	
		float  f32;
		double f64;
		
		void *ptr;
	};
} HASHMAP_type;

Hashmap      *HASHMAP_create ();
Hashmap      *HASHMAP_put    (Hashmap *hm, char *key, HASHMAP_type value);
HASHMAP_type *HASHMAP_get    (Hashmap *hm, char *key);
void          HASHMAP_iterate(Hashmap *hm, void (*iterFunc) (char * key, HASHMAP_type *value));
void          HASHMAP_destroy(Hashmap *hm, void (*delFunc) (HASHMAP_type *));
void          HASHMAP_freeDestroy(HASHMAP_type *value);

#endif // HASHMAP_H
