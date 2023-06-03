#makefile
rvv_target    = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = spmv

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64g -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/spmv_main.o src/spmv_main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64g -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/spmv_main.o
	riscv64-unknown-elf-objdump -D $(serial_target) > $(serial_target).dmp

vector: $(rvv_target)
$(rvv_target): src/spmv_main.c src/spmv_vector.S
	mkdir -p bin
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -O1  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/spmv_vector.o src/spmv_vector.S
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -O1  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/spmv_main.o src/spmv_main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gv1p0 -O1  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -o $(rvv_target) src/spmv_vector.o src/spmv_main.o
	riscv64-unknown-elf-objdump -D $(rvv_target) > $(rvv_target).dmp
