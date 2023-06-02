.PHONY: build_fftw3_vector_lib build_fftw3_scalar_lib

#makefile
rvv_target    = bin/rvv-test
serial_target = bin/serial-test

# SPIKE_OPTS = 256
# SPIKE_OPTS = 8
SPIKE_OPTS =

APP_NAME = fourier

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	mkdir -p obj_scalar
	clang --target=riscv64-unknown-elf  -Wall -I$(SNIPER_ROOT)/include -march=rv64g -O3 -c -o obj_scalar/fourier.o src/fourier.c -I$(abspath fftw3_scalar/api/) -I$(abspath src)
	clang --target=riscv64-unknown-elf  -Wall -I$(SNIPER_ROOT)/include -march=rv64gc -O3 -o $(serial_target) obj_scalar/fourier.o $(abspath fftw3_scalar/.libs/libfftw3.a) -lm
	riscv64-unknown-elf-objdump -D $(serial_target) > $(serial_target).dmp &

vector: $(rvv_target)
$(rvv_target): src/utils.c src/fourier.c
	mkdir -p bin
	mkdir -p obj_vector
	clang --target=riscv64-unknown-elf  -Wall -I$(SNIPER_ROOT)/include -march=rv64gv -O3 -c -o obj_vector/fourier.o src/fourier.c -I$(abspath fftw3/api/) -I$(abspath src)
	clang --target=riscv64-unknown-elf  -Wall -I$(SNIPER_ROOT)/include -march=rv64gv -O3 -o $(rvv_target).large obj_vector/fourier.o $(abspath fftw3/.libs/libfftw3.a) -lm
	riscv64-unknown-elf-strip -p $(rvv_target).large -o $(rvv_target)
	riscv64-unknown-elf-objdump -D $(rvv_target) > $(rvv_target).dmp &

	# clang --target=riscv64-unknown-elf  -Wall -I$(SNIPER_ROOT)/include -march=rv64gv -O2 -o $(rvv_target) src/fourier.o -L$(abspath fftw3/.libs/) -lm -lfftw3

build_fftw3_vector_lib:
	cd fftw3 && \
	./bootstrap.sh --host=riscv64-unknown-elf --disable-threads && \
	./configure --enable-maintainer-mode --enable-rvv --host=riscv64-unknown-elf \
		"CC=clang --target=riscv64-unknown-elf -march=rv64gv -O3 -g" "CXX=clang++ --target=riscv64-unknown-elf -march=rv64gv" && \
	make -j$(shell nproc)

build_fftw3_scalar_lib:
	cd fftw3_scalar && \
	./bootstrap.sh --host=riscv64-unknown-elf --disable-threads && \
	./configure --enable-maintainer-mode --host=riscv64-unknown-elf \
		"CC=clang --target=riscv64-unknown-elf -march=rv64gc -O3 -g" "CXX=clang++ --target=riscv64-unknown-elf -march=rv64gc" && \
	make -j$(shell nproc)
