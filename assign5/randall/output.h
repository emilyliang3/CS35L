#ifndef OUTPUT_H
#define OUTPUT_H

#include <stdbool.h>

bool writebytes (unsigned long long x, int nbytes);
bool writeblocks(int nbytes, void* buffer, int blocksize);
bool writebytesinblocks (int nbytes, unsigned long long (*rand64) (void), int blocksize);
bool writebytes_mrand(int nbytes, int blocksize);

#endif //OUTPUT_H