#makefile

APP_NAME = blackscholes

# SPIKE_OPTS = 1 ./input/in_64K.input prices.txt
# SPIKE_OPTS = 1 ./input/in_512.input prices.txt
SPIKE_OPTS = 1 ./input/in_8.input prices.txt

rvv_target    = bin/rvv-test
serial_target = bin/serial-test

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/blackscholes.cpp -lm
	riscv64-unknown-elf-objdump -D $(serial_target) > $(serial_target).dmp

vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR  -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -o $(rvv_target) src/blackscholes.cpp  -lm
	riscv64-unknown-elf-objdump -D $(rvv_target) > $(rvv_target).dmp
