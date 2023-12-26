#makefile
rvv_target    = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = jacobi-2d

SPIKE_OPTS = 64 100 jacobi_2d.out
# SPIKE_OPTS = 64 10 jacobi_2d.out

include ../../scripts/runspike.mk


scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O3 -c -o src/jacobi-2d.scalar.o src/jacobi-2d.cpp; \
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -march=rv64g -O3 -o $(serial_target) src/*.scalar.o -lm; \
	${LLVM}/bin/llvm-objdump -d -S $(serial_target) > $(serial_target).dmp

#	riscv64-unknown-elf-objdump -d $(serial_target) > bin/jacobi-2d_serial.dump

vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions -fno-unroll-loops --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -g -c -o src/jacobi-2d.vector.o src/jacobi-2d.cpp
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions -fno-unroll-loops --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -g -o $(rvv_target) src/*.vector.o -lm
	${LLVM}/bin/llvm-objdump -d -S $(rvv_target) > $(rvv_target).dmp

host:
	g++ -O2 -g -Wall -std=c99 -c -o  src/jacobi-2d.vector.o  src/jacobi-2d.cpp ; \
	g++ -O2 -g -Wall -std=c99 -o  bin/jacobi-2d_host.exe  src/*.vector.o  -lm; \
	rm src/*.vector.o; \
	objdump -dC bin/jacobi-2d_host.exe > bin/jacobi-2d_host.dump ;

copy:
	rm -r ../../Test/_jacobi-2d/bin/*.exe; \
	cp -r bin/*exe ../../Test/_jacobi-2d/bin/;
