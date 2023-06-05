#include <stdio.h>
#include <limits.h>
#include <unistd.h>
#include <stdlib.h>
#include "output.h"

bool writebytes (unsigned long long x, int nbytes)
{
  do
  {
    if (putchar (x) < 0)
      return false;
    x >>= CHAR_BIT;
    nbytes--;
  }
  while (0 < nbytes);

  return true;
}

bool writeblocks(int nbytes, void* buffer, int blocksize) {
  int byteswritten = 0;
  while (byteswritten < nbytes) {
    int remainingbytes = nbytes - byteswritten;
    if (remainingbytes < blocksize)
      blocksize = remainingbytes;
    int bytes = write(STDOUT_FILENO, buffer + byteswritten, blocksize);
    if (bytes == -1)
      return false;
    byteswritten += bytes;
  }
  return true;
}

bool writebytesinblocks (int nbytes, unsigned long long (*rand64) (void), int blocksize) {
  if (blocksize > nbytes)
    blocksize = nbytes;
  unsigned long long *buffer = (unsigned long long*)malloc(nbytes * sizeof(unsigned long long));
  if (buffer == NULL) {
    fprintf(stderr, "memory allocation failed\n");
    exit(1);
  }
  for (int i = 0; i < (int)(nbytes/sizeof(unsigned long long)); i++) {
    unsigned long long x = rand64();
    buffer[i] = x;
  }

  bool status = writeblocks(nbytes, buffer, blocksize);
  if (buffer)
    free(buffer);
  return status;
}

bool writebytes_mrand(int nbytes, int blocksize) {
  struct drand48_data buffer;
  srand48_r(31415, &buffer);
  if (blocksize) {
    if (blocksize > nbytes)
      blocksize = nbytes;
    long *writebuffer = (long*)malloc(nbytes * sizeof(long));
    if (writebuffer == NULL) {
      fprintf(stderr, "memory allocation failed\n");
      exit(1);
    }
    for (int i = 0; i < (int)(nbytes/sizeof(long)); i++) {
      long x;
      mrand48_r(&buffer, &x);
      writebuffer[i] = x;
    }
    bool status = writeblocks(nbytes, writebuffer, blocksize);
    if (writebuffer)
      free(writebuffer);
    return status;
  }

  int wordsize = sizeof(long);
  do {
    long x;
    mrand48_r(&buffer, &x);
    int outbytes = nbytes < wordsize ? nbytes : wordsize; 
    if (!writebytes (x, outbytes))
      return false;
    nbytes -= outbytes;
  } while (0 < nbytes);
  return true;
}