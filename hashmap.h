#ifndef HASHMAP_H
#define HASHMAP_H

typedef struct hashmap Hashmap;

Hashmap *HASHMAP_create ();
Hashmap *HASHMAP_put    (Hashmap *hm, char *key, void *value);
void    *HASHMAP_get    (Hashmap *hm, char *key);
void     HASHMAP_iterate(Hashmap *hm, void (*iterFunc) (char * key, void * value));
void     HASHMAP_delete (Hashmap *hm, void (*delFunc) (void *));
void     HASHMAP_freeDel(void *value);

#endif // HASHMAP_H
