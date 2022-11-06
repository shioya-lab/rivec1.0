#makefile

rvv_target = bin/rvv-test
serial_target = bin/serial-test

SPIKE_OPTS = 256

include ../runspike.mk

serial: $(serial_target)
$(serial_target):
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -march=rv64gc1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -c -o src/axpy.o src/axpy.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -march=rv64gc1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/main.o src/main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -march=rv64gc1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/utils.o src/utils.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -march=rv64gc1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -o $(serial_target) src/*.o -lm

vector: $(rvv_target)
$(rvv_target): src/utils.c src/axpy.c src/main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -c -o src/utils.o src/utils.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -c -o src/axpy.o src/axpy.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/main.o src/main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -o $(rvv_target) src/*.o -lm
