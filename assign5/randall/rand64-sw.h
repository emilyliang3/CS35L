#ifndef RAND64SW_H
#define RAND64SW_H

void software_rand64_init (char* filename);
unsigned long long software_rand64 (void);
void software_rand64_fini (void);

#endif //RAND64SW_H