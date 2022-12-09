#makefile
rvv_target = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = canneal

SPIKE_OPTS = 1 100 300 input/100.nets 8

include ../runspike.mk

serial: $(serial_target)
$(serial_target):
	for entry in src/*.cpp ; do \
		${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf  -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o  $$entry.o  $$entry ; \
	done
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf  -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2  -o $(serial_target) src/*.cpp.o -lm
	rm src/*.o

vector: $(rvv_target)
$(rvv_target):
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/annealer_thread.o src/annealer_thread.cpp
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/main.o src/main.cpp
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/netlist.o src/netlist.cpp
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/netlist_elem.o src/netlist_elem.cpp
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/rng.o src/rng.cpp
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2  -o $(rvv_target) src/*.o -lm
	rm src/*.o
