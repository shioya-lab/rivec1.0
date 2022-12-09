#makefile
rvv_target = bin/rvv-test
serial_target = bin/serial-test

APP_NAME = particlefilter

SPIKE_OPTS =  -x 128 -y 128 -z 2 -np 256

include ../runspike.mk

start:
	mkdir bin; \
	rm bin/*.*

serial: $(serial_target)
$(serial_target):
	${LLVM}/bin/clang -Wall --target=riscv64-unknown-elf  -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/particlefilter_serial.o src/particlefilter.c
	${LLVM}/bin/clang -Wall --target=riscv64-unknown-elf  -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/particlefilter_serial.o -lm
	rm src/*.o

vector: $(rvv_target)
$(rvv_target):
	${LLVM}/bin/clang -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -DMVL_$$mvl -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/particlefilter.o src/particlefilter.c
	${LLVM}/bin/clang -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -DMVL_$$mvl -march=rv64gv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -o $(rvv_target) src/*.o -lm
	$(GCC_TOOLCHAIN_DIR)/bin/riscv64-unknown-elf-objdump -D $(rvv_target) > $(rvv_target).dmp
	rm src/*.o
