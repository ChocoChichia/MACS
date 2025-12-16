#include "vector.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

void VectorNew(vector *v, int elemSize, VectorFreeFunction freeFn, int initialAllocation)
{      

    assert(v!=NULL);
    assert(initialAllocation>=0);

    v->freeFn = freeFn;
    v->elemSize = elemSize;
    v->len = 0;
    v->alloc_len = initialAllocation;
    if ( initialAllocation == 0 ) {
        v->alloc_len = 4;
    }
    
    v->list = malloc(v->alloc_len * v->elemSize);




}

void VectorDispose(vector *v)
{

    for (int i = 0; i < v->len; i++) {
        void* curr = (char*)v->list + i * v->elemSize;
        if (v->freeFn != NULL) {
            v->freeFn(curr); // Free each element
    }
  }

  free(v->list);
  v->len = 0;
  v->alloc_len = 0;
    
}

int VectorLength(const vector *v)
{   
    return v->len; 
     
}

void *VectorNth(const vector *v, int position)
{   
   assert(v!=NULL);
   assert(position>=0 && position< v->len);

   int jump = position * (v->elemSize);
   void* ans = (char) v->list + jump;
   return ans;
}

void VectorReplace(vector *v, const void *elemAddr, int position)
{   
   assert(v!=NULL);
   assert(position>=0 && position< v->len);

   void* element = VectorNth(v,position);
   if (v->freeFn != NULL){
        v->freeFn(element);
   }

   memcpy(element,elemAddr,v->elemSize);
   
}

void increaseCapacity(vector* v){
   
   if (v->len == v->alloc_len){
        int resize = v->alloc_len*2;
        v->alloc_len = resize;
        void* r_list = realloc(v->list,v->elemSize * resize);
        assert(r_list != NULL);
        v->list = r_list;
    }
    
}

void VectorInsert(vector *v, const void *elemAddr, int position)
{   
    assert(v!=NULL);
    assert(position>=0 && position <= v->len);
    increaseCapacity(v);
    void* loc = (char*) v->list + position*v->elemSize;
    // 77 42 9 2 '4'   6 1 8.  len aris 8   7 6 5 4

    for ( int i = v->len; i > position; i --){
        
        void* elem = VectorNth(v,i-1);
        void* place = (char*) v->list + i*v->elemSize;
        memcpy(place,elem,v->elemSize);

    }

    memcpy(loc,elemAddr,v->elemSize);
    v->len += 1;

}

void VectorAppend(vector *v, const void *elemAddr)
{
   VectorInsert(v,elemAddr,v->len);
}

void VectorDelete(vector *v, int position)
{   
   assert(v!=NULL);
   assert(position>=0 && position< v->len);
   
   void* bin = VectorNth(v,position);
   if ( v->freeFn != NULL){
     v->freeFn(bin);
   }
        // 1 2 3 4 5 6 7 8
   for (int i = position; i < v->len; i ++){
        void* loc = (char*) v->list + i*v->elemSize;
        void* curr = (char*) v->len + ((i+1)*v->elemSize);
        memcpy(loc,curr,v->elemSize);
   }

}

void VectorSort(vector *v, VectorCompareFunction compare)
{   
   
}

void VectorMap(vector *v, VectorMapFunction mapFn, void *auxData)
{   
    

}

static const int kNotFound = -1;
int VectorSearch(const vector *v, const void *key, VectorCompareFunction searchFn, int startIndex, bool isSorted)
{   
   

} 
