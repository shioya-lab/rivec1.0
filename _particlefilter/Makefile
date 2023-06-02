#makefile
rvv_target    = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = particlefilter

SPIKE_OPTS =  -x 128 -y 128 -z 2 -np 256

include ../../scripts/runspike.mk

start:
	echo $(rvv_target)
	echo $(serial_target)

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	${LLVM}/bin/clang -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include  -march=rv64g --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/particlefilter.scalar.o src/particlefilter.c
	${LLVM}/bin/clang -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include  -march=rv64g --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/particlefilter.scalar.o -lm
	rm src/*.scalar.o

vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	${LLVM}/bin/clang -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -DMVL_$$mvl -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/particlefilter.v$(VLEN).o src/particlefilter.c
	${LLVM}/bin/clang -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -DMVL_$$mvl -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -o $(rvv_target) src/*.v$(VLEN).o -lm
	$(GCC_TOOLCHAIN_DIR)/bin/riscv64-unknown-elf-objdump -D $(rvv_target) > $(rvv_target).dmp
	rm src/*.v$(VLEN).o
