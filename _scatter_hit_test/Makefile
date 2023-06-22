#makefile
rvv_target    = bin/rvv-test
serial_target = bin/serial-test

# SPIKE_OPTS = 256
# SPIKE_OPTS = 8
SPIKE_OPTS = 256

APP_NAME = axpy

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):

vector: $(rvv_target)
$(rvv_target): src/utils.c src/main.c
	mkdir -p bin
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -O2 --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/utils.o src/utils.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -O2 --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/main.o src/main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -O2 --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -o $(rvv_target) src/main.o src/utils.o -lm

#	${LLVM}/bin/llvm-objdump -D $(rvv_target) > $(rvv_target).dmp
