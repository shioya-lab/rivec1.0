#makefile
rvv_target = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = jacobi-2d

SPIKE_OPTS = 64 100 jacobi_2d.out

include ../../scripts/runspike.mk


scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/jacobi-2d.o src/jacobi-2d.cpp; \
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -march=rv64g -O2 -o $(serial_target) src/*.o -lm; \
	rm src/*.o; \
	${LLVM}/bin/llvm-objdump --mattr=+v -ds  $(serial_target) > bin/jacobi-2d_serial.dump

vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/jacobi-2d.o src/jacobi-2d.cpp; \
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(rvv_target) src/*.o -lm ; \
	rm src/*.o ; \
	${LLVM}/bin/llvm-objdump --mattr=+v -ds  $(rvv_target) > bin/jacobi-2d_vector.dump ; \

host:
	g++ -O2 -g -Wall -std=c99 -c -o  src/jacobi-2d.o  src/jacobi-2d.cpp ; \
	g++ -O2 -g -Wall -std=c99 -o  bin/jacobi-2d_host.exe  src/*.o  -lm; \
	rm src/*.o; \
	objdump -dC bin/jacobi-2d_host.exe > bin/jacobi-2d_host.dump ;

copy:
	rm -r ../../Test/_jacobi-2d/bin/*.exe; \
	cp -r bin/*exe ../../Test/_jacobi-2d/bin/;
