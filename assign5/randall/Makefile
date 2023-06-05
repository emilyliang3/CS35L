# Make x86-64 random byte generators.

# Copyright 2015, 2020, 2021 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE = -O2

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --gzip --transform 's,^,randall/,'
TAREXT = tgz

# Variables for testing (check)
NUMBYTES = 1000

SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)

default: randall

randall: $(OBJ)
	$(CC) $(CFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission-tarball: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt *.h *.c
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

repository-tarball:
	$(TAR) -czf randall-git.tgz .git

check: randall
	test $$(./randall $(NUMBYTES) | wc -c) -eq $(NUMBYTES)
	test $$(./randall -i mrand48_r $(NUMBYTES) | wc -c) -eq $(NUMBYTES)
	test $$(./randall -i /dev/random $(NUMBYTES) | wc -c) -eq $(NUMBYTES)
	test $$(./randall -i /dev/urandom $(NUMBYTES) | wc -c) -eq $(NUMBYTES)
	test $$(./randall $(NUMBYTES) -o stdio -i mrand48_r | wc -c) -eq $(NUMBYTES)
	test $$(./randall $(NUMBYTES) -o stdio -i /dev/urandom | wc -c) -eq $(NUMBYTES)
	test $$(./randall $(NUMBYTES) -o 99 | wc -c) -eq $(NUMBYTES)
	test $$(./randall $(NUMBYTES) -o 99 -i mrand48_r | wc -c) -eq $(NUMBYTES)
	test $$(./randall $(NUMBYTES) -o 99 -i rdrand | wc -c) -eq $(NUMBYTES)
	

.PHONY: default clean assignment submission-tarball repository-tarball

clean:
	rm -f *.o *.$(TAREXT) randall
