#makefile
rvv_target    = bin/rvv-test
serial_target = bin/serial-test

# SPIKE_OPTS = 256
SPIKE_OPTS = 32

APP_NAME = axpy

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/axpy_scalar.o src/axpy.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/main.o src/main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/utils.o src/utils.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/axpy_scalar.o src/main.o src/utils.o -lm
	riscv64-unknown-elf-objdump -D $(serial_target) > $(serial_target).dmp

vector: $(rvv_target)
$(rvv_target): src/utils.c src/axpy.c src/main.c
	mkdir -p bin
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -O1  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/utils.o src/utils.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -O1  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/axpy_vector.o src/axpy.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -O1  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/main.o src/main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -O1  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -o $(rvv_target) src/axpy_vector.o src/main.o src/utils.o -lm
	riscv64-unknown-elf-objdump -D $(rvv_target) > $(rvv_target).dmp
