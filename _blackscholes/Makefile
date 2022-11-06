#makefile

SPIKE_OPTS = 1 ./input/in_64K.input prices.txt

rvv_target = bin/rvv-test
serial_target = bin/serial-test

include ../runspike.mk

serial: $(serial_target)
$(serial_target):
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/blackscholes.cpp -lm

vector: $(rvv_target)
$(rvv_target):
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR   -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -o $(rvv_target)  src/blackscholes.cpp -lm
