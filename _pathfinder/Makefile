#makefile
rvv_target    = bin/rvv-test_vlen$(VLEN)
serial_target = bin/serial-test_vlen$(VLEN)

APP_NAME = pathfinder

SPIKE_OPTS = 32 32 out

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -march=rv64gcv1p0 -I$(SNIPER_ROOT)/include -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/pathfinder.cpp

vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -I$(SNIPER_ROOT)/include   -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -o $(rvv_target)  src/pathfinder.cpp
