#include <stdio.h>
#include <stdlib.h>
#include "rand64-sw.h"

/* Input stream containing random bytes.  */
static FILE *urandstream;

/* Initialize the software rand64 implementation.  */
void
software_rand64_init (char* filename)
{
  urandstream = fopen (filename, "r");
  if (! urandstream) {
    fprintf(stderr, "file %s could not be opened\n", filename);
    exit(1);
  }
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 (void)
{
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1) {
    fprintf(stderr, "error reading from file\n");
    exit(1);
  }
  return x;
}

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void)
{
  fclose (urandstream);
}