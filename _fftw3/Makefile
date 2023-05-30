.PHONY: build_fftw3_vector_lib build_fftw3_scalar_lib

#makefile
rvv_target    = bin/rvv-test_vlen$(VLEN)
serial_target = bin/serial-test_vlen$(VLEN)

# SPIKE_OPTS = 256
# SPIKE_OPTS = 8
SPIKE_OPTS =

APP_NAME = fourier

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	mkdir -p obj_scalar
	riscv64-unknown-elf-gcc  -Wall -I$(SNIPER_ROOT)/include -march=rv64g -O3 -c -o obj_scalar/fourier.o src/fourier.c -I$(abspath fftw3_scalar/api/) -I$(abspath src)
	riscv64-unknown-elf-gcc  -Wall -I$(SNIPER_ROOT)/include -march=rv64gc -O3 -o $(serial_target) obj_scalar/fourier.o $(abspath fftw3_scalar/.libs/libfftw3.a) -lm
	riscv64-unknown-elf-objdump -D $(serial_target) > $(serial_target).dmp &

vector: $(rvv_target)
$(rvv_target): src/utils.c src/fourier.c
	mkdir -p bin
	mkdir -p obj_vector
	riscv64-unknown-elf-gcc  -Wall -I$(SNIPER_ROOT)/include -march=rv64gv -O3 -c -o obj_vector/fourier.o src/fourier.c -I$(abspath fftw3/api/) -I$(abspath src)
	riscv64-unknown-elf-gcc  -Wall -I$(SNIPER_ROOT)/include -march=rv64gcv -O3 -o $(rvv_target) obj_vector/fourier.o $(abspath fftw3/.libs/libfftw3.a) -lm
	riscv64-unknown-elf-objdump -D $(rvv_target) > $(rvv_target).dmp &

	# riscv64-unknown-elf-gcc  -Wall -I$(SNIPER_ROOT)/include -march=rv64gv -O2 -o $(rvv_target) src/fourier.o -L$(abspath fftw3/.libs/) -lm -lfftw3

build_fftw3_vector_lib:
	cd fftw3 && \
	./bootstrap.sh --host=riscv64-unknown-elf --disable-threads && \
	./configure --enable-maintainer-mode --enable-rvv --host=riscv64-unknown-elf \
		"CC=riscv64-unknown-elf-gcc -march=rv64gcv -O3 -g" "CXX=riscv64-unknown-elf-g++ -march=rv64gcv" && \
	make -j$(shell nproc)

build_fftw3_scalar_lib:
	cd fftw3_scalar && \
	./bootstrap.sh --host=riscv64-unknown-elf --disable-threads && \
	./configure --enable-maintainer-mode --host=riscv64-unknown-elf \
		"CC=riscv64-unknown-elf-gcc -march=rv64gc -O3 -g" "CXX=riscv64-unknown-elf-g++ -march=rv64gc" && \
	make -j$(shell nproc)
