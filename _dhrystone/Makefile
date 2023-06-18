rvv_target    = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = dhrystone

PK = pk

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target): src/dhrystone.c src/dhrystone.h src/dhrystone_main.c
	mkdir -p bin
	${LLVM}/bin/clang -std=c90 -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O3 -c -o src/dhrystone_scalar.o src/dhrystone.c
	${LLVM}/bin/clang -std=c90 -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O3 -c -o src/dhrystone_main_scalar.o src/dhrystone_main.c
	${LLVM}/bin/clang -std=c90 -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gc --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O3 -o $(serial_target) src/dhrystone_scalar.o src/dhrystone_main_scalar.o -lm
	${LLVM}/bin/llvm-objdump -d $(serial_target) > $(serial_target).dmp

vector: $(rvv_target)
$(rvv_target): src/dhrystone.c src/dhrystone.h src/dhrystone_main.c
	mkdir -p bin
	${LLVM}/bin/clang -std=c90 -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -mllvm --scalable-vectorization=on -O3 -c -o src/dhrystone_vector.o src/dhrystone.c
	${LLVM}/bin/clang -std=c90 -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -mllvm --scalable-vectorization=on -O3 -c -o src/dhrystone_main_vector.o src/dhrystone_main.c
	${LLVM}/bin/clang -std=c90 -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -mllvm --scalable-vectorization=on -O3 -c -o src/rvv_common.o src/rvv_common.c
	${LLVM}/bin/clang -std=c90 -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -mllvm --scalable-vectorization=on -O3 -o $(rvv_target) src/dhrystone_vector.o src/dhrystone_main_vector.o src/rvv_common.o -lm
	${LLVM}/bin/llvm-objdump -d $(rvv_target) > $(rvv_target).dmp
