#ifndef HASHMAP_H
#define HASHMAP_H

typedef struct hashmap Hashmap;

Hashmap *HASHMAP_create();
Hashmap *HASHMAP_put(Hashmap *hm, char *key, void *value);
void    *HASHMAP_get(Hashmap *hm, char *key);

#endif // HASHMAP_H
