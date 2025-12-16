#include "hashset.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>

void HashSetNew(hashset *h, int elemSize, int numBuckets,
		HashSetHashFunction hashfn, HashSetCompareFunction comparefn, HashSetFreeFunction freefn)
{	
	assert(elemSize > 0);
	assert(numBuckets>0);
	assert(comparefn!=NULL);
	assert(hashfn != NULL);
	
	h->elemSize = elemSize;
	h->bucket_len = numBuckets;
	h->compFn = comparefn;
	h->freeFn = freefn;
	h->hashFn = hashfn;
	h->len = 0;

	vector* buckets = malloc(numBuckets*sizeof(vector));
	h->buckets = buckets;
	assert(buckets!=NULL);

	for ( int i = 0 ; i < numBuckets; i ++){
		VectorNew(&h->buckets[i],elemSize,freefn,0);
	}
}

void HashSetDispose(hashset *h)
{	
	assert(h!=NULL);
	if (h->len == 0) return;

	for (int i = 0 ; i < h->bucket_len; i ++){
		VectorDispose(&h->buckets[i]);
	}

	//erasing buckets from memory 
	free(h->buckets);
	h->buckets = NULL;

	h->len = 0;
	h->bucket_len = 0;
	
}

int HashSetCount(const hashset *h)
{ 
	return h->len;
 }

void HashSetMap(hashset *h, HashSetMapFunction mapfn, void *auxData)
{	
	assert(h != NULL);
	assert(mapfn != NULL);

	for(int i = 0 ; i < h->bucket_len; i ++){
		vector v = h->buckets[i];
		VectorMap(&v,mapfn,auxData);
	}

}


void HashSetEnter(hashset *h, const void *elemAddr)
{	
	assert(elemAddr != NULL);
	
	int bucket = h->hashFn(elemAddr,h->bucket_len);
	assert( bucket >= 0 && bucket < h->bucket_len);
	vector* v = &h->buckets[bucket];

	//check if element already exists
	int check = VectorSearch(v,elemAddr,h->compFn,0,false);

	//case when element exists
	if(check != -1){
		VectorReplace(v,elemAddr,check);
		return;
	}   
	
	VectorAppend(v,elemAddr);
	h->len += 1;

}

void *HashSetLookup(const hashset *h, const void *elemAddr)
{ 	
	assert(elemAddr != NULL);

	int bucket = h->hashFn(elemAddr, h->bucket_len);
	assert(bucket >= 0 && bucket < h->bucket_len);

	vector *v = &h->buckets[bucket];
	int index = VectorSearch(v, elemAddr, h->compFn, 0, false);

	if (index == -1) return NULL;

	return VectorNth(v,index);; 
}
