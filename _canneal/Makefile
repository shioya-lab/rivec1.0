#makefile
rvv_target    = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = canneal

SPIKE_OPTS = 1 100 300 input/100.nets 8
# SPIKE_OPTS = 1 100 300 input/100000.nets 8

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	for entry in src/*.cpp ; do \
		${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include  -march=rv64g --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o  $$entry.scalar.o  $$entry ; \
	done
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include  -march=rv64g --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2  -o $(serial_target) src/*.cpp.scalar.o -lm

#	${LLVM}/bin/llvm-objdump -d $(serial_target) > $(serial_target).dmp

vector: $(rvv_target)
$(rvv_target): $(wildcard src/*.cpp)
	mkdir -p bin
	${LLVM}/bin/clang++ -Wall --std=c++14 --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/annealer_thread.vector.o src/annealer_thread.cpp
	${LLVM}/bin/clang++ -Wall --std=c++14 --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/main.vector.o src/main.cpp
	${LLVM}/bin/clang++ -Wall --std=c++14 --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/netlist.vector.o src/netlist.cpp
	${LLVM}/bin/clang++ -Wall --std=c++14 --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/netlist_elem.vector.o src/netlist_elem.cpp
	${LLVM}/bin/clang++ -Wall --std=c++14 --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64g1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O1 -c -o src/rng.vector.o src/rng.cpp
	${LLVM}/bin/clang++ -Wall --std=c++14 --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2  -o $(rvv_target) src/*.vector.o -lm

#	${LLVM}/bin/llvm-objdump -d $(rvv_target) > $(rvv_target).dmp
