#makefile
rvv_target    = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = streamcluster

SPIKE_OPTS = 3 10 128 128 128 10 none output.txt 1


include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -march=rv64g -I$(SNIPER_ROOT)/include --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/streamcluster.cpp -lm

#	${LLVM}/bin/llvm-objdump -D --mattr=+v $@ > ./bin/dump_serial

vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -I$(SNIPER_ROOT)/include   -march=rv64gv1p0 -mllvm --scalable-vectorization=off -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -o $(rvv_target)  src/streamcluster.cpp -lm

#	${LLVM}/bin/llvm-objdump -D --mattr=+v $@ > ./bin/dump_vector
