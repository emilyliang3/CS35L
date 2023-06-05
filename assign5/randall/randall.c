/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#include "options.h"
#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"

/* Main program, which outputs N bytes of random data.  */
int main (int argc, char **argv)
{
  char *input_option = NULL;
  char *output_option = NULL;
  int nbytes = processOptions(argc, argv, &input_option, &output_option);

  // check for valid input option
  int rdflag = 0;
  int mrndflag = 0;
  int swflag = 0;
  char* filename = "/dev/random";
  if (input_option) {
    int input_type = validInput(input_option);
    switch (input_type) {
      case 1: // file
        swflag ++;
        filename = input_option;
        break;
      case 2: // rd_rand
        rdflag++;
        break;
      case 3: // mrand48_r
        mrndflag++;
        break;
    }
  }

  //check for valid output option
  int blockSize = 0;
  if (output_option) {
    blockSize = validOutput(output_option);
  }

  /* If there's no work to do, don't worry about which library to use.  */
  if (nbytes == 0)
    return 0;
  
  /* Now that we know we have work to do, arrange to use the appropriate library.  */
  unsigned long long (*rand64) (void);
  if (rdrand_supported () && !swflag)
      rand64 = hardware_rand64;
  else if (rdflag) {
    fprintf(stderr, "-i rdrand: hardware random number generation not available\n");
    exit(1);
  }
  else
    {
      rand64 = software_rand64;
      swflag++;
    }

  if (swflag)
    software_rand64_init(filename);
  int wordsize;
  int output_errno = 0;

  // for mrand48_r
  if (mrndflag) {
    if (!writebytes_mrand(nbytes, blockSize)) {
      fprintf(stderr, "mrand48_r: error writing bytes\n");
      exit(1);
    }
  }

  else {
    if (blockSize) {
      if (!writebytesinblocks(nbytes, rand64, blockSize)) {
        fprintf(stderr, "-o %d: error writing bytes\n", blockSize);
        exit(1);
      }
    }
    else {
      wordsize = sizeof rand64 ();
      do {
        unsigned long long x = rand64 ();
        int outbytes = nbytes < wordsize ? nbytes : wordsize;
        if (!writebytes (x, outbytes)) {
          fprintf(stderr, "error writing bytes\n");
          exit(1);
        }
        nbytes -= outbytes;
      } while (0 < nbytes);
    }
  }

  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  if (swflag)
    software_rand64_fini();

  // freeing dynamically allocated memory 
  if (input_option)
    free(input_option);
  if (output_option)
    free(output_option);

  return !!output_errno;
}
