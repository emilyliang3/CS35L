#ifndef OPTIONS_H
#define OPTIONS_H

int processOptions(int argc, char **argv, char **input_option, char **output_option);
int validInput(char *input);
int validOutput(char *output);

#endif //OPTIONS_H