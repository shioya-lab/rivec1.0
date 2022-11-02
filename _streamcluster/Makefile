#makefile
GCC_TOOLCHAIN_DIR := /newlib/
SYSROOT_DIR := $(GCC_TOOLCHAIN_DIR)/riscv64-unknown-elf

LLVM := /llvm/build/
SPIKE := spike
PK := pk

rvv_target = bin/rvv-test
serial_target = bin/serial-test

serial: $(serial_target)
$(serial_target):
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -o $(serial_target) src/streamcluster.cpp -lm
	${LLVM}/bin/llvm-objdump -D --mattr=+v $@ > ./bin/dump_serial

vector: $(rvv_target)
$(rvv_target):
	${LLVM}/bin/clang++ --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR   -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -o $(rvv_target)  src/streamcluster.cpp -lm
	${LLVM}/bin/llvm-objdump -D --mattr=+v $@ > ./bin/dump_vector



runspike-v : $(rvv_target)
	echo >output.txt; \
	$(SPIKE) --isa=rv64gcv -l --log-commits $(PK) $(rvv_target) 3 10 128 128 128 10 none output.txt 1 2> spike-v.log

runspike-s : $(serial_target)
	echo >output.txt; \
	$(SPIKE) --isa=rv64gcv -l --log-commits $(PK) $(serial_target) 3 10 128 128 128 10 none output.txt 1 2> spike-s.log
