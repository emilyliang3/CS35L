#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <stdbool.h>
#include <string.h>
#include "options.h"

int processOptions(int argc, char **argv, char **input_option, char **output_option) {
    // check options
    int c;
    int iflag = 0, oflag = 0;

    while ((c = getopt(argc, argv, ":i:o:")) != -1) {
        switch (c) {
        case 'i':
            if (iflag) {
            fprintf(stderr, "-i can only be called once\n");
            exit(1);
            }
            iflag++;
            *input_option = (char*)malloc((strlen(optarg) + 1) * sizeof(char));
            if (*input_option == NULL) {
                fprintf(stderr, "memory allocation failed\n");
                exit(1);
            }
            strcpy(*input_option, optarg);
            break;
        case 'o':
            if (oflag) {
            fprintf(stderr, "-o can only be called once\n");
            exit(1);
            }
            oflag++;
            *output_option = (char*)malloc((strlen(optarg) + 1) * sizeof(char));
            if (*output_option == NULL) {
                fprintf(stderr, "memory allocation failed\n");
                exit(1);
            }
            strcpy(*output_option, optarg);
            break;
        case ':':
            fprintf(stderr, "option -%c requires an operand\n", optopt);
            exit(1);
        case '?':
            fprintf(stderr, "unrecognized option: -%c\n", optopt);
        }
    }

    // proceess non-option argument(s)
    bool valid = false;
    long long nbytes = -1;
    int nbytesflag = 0;
    for (; optind < argc; optind++) {
        char *endptr;
        errno = 0;
        nbytes = strtoll (argv[optind], &endptr, 10);
        if (errno)
        perror (argv[optind]);
        else {
        valid = !*endptr && 0 <= nbytes;
        if (nbytesflag) {
            fprintf(stderr, "only one non-option argument allowed\n");
            exit(1);
        }
        nbytesflag++;
        }
    }

    if (!valid) {
        fprintf (stderr, "improper usage of %s\n", argv[0]);
        exit(1);
    }

    return nbytes;
}

// returns 1 if input is a file name, 2 if input is "rdrand", 3 if input is "mrand48_r"
int validInput(char *input) {
    if (input[0] == '/')
        return 1;
    char* rd_str = "rdrand";
    char* m_str = "mrand48_r";
    if (!strcmp(input, rd_str))
        return 2;
    if (!strcmp(input, m_str))
        return 3;
    fprintf(stderr, "invalid argument for -i: %s\n", input);
    exit(1);
}

// returns value of output if it is a positive integer, 0 if output is "stdio"
int validOutput(char *output) {
    char* stdio = "stdio";
    if (!strcmp(output, stdio))
        return 0;
    char* endptr;
    errno = 0;
    long long n = strtoll(output, &endptr, 10);
    if (errno || *endptr || (n <= 0)) {
        fprintf(stderr, "invalid argument for -o: %s\n", output);
        exit(1);
    }
    return n;
}