#makefile

rvv_target    = bin/rvv-test_vlen$(VLEN)
serial_target = bin/serial-test_vlen$(VLEN)

APP_NAME = swaptions

SPIKE_OPTS = -ns 8 -sm 512 -nt 1

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	for entry in src/*.cpp ; do \
		${LLVM}/bin/clang++   -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o  $$entry.scalar.o  $$entry ; \
	done
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include  -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2  -o $@  src/*.cpp.scalar.o -lm;	\
	rm src/*.scalar.o; \
	${LLVM}/bin/llvm-objdump -D --mattr=+v $@ > ./bin/dump_serial


vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/CumNormalInv.v$(VLEN).o src/CumNormalInv.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/MaxFunction.v$(VLEN).o src/MaxFunction.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/RanUnif.v$(VLEN).o src/RanUnif.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/nr_routines.v$(VLEN).o src/nr_routines.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/icdf.v$(VLEN).o src/icdf.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/HJM_SimPath_Forward_Blocking.v$(VLEN).o src/HJM_SimPath_Forward_Blocking.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/HJM.v$(VLEN).o src/HJM.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/HJM_Swaption_Blocking.v$(VLEN).o src/HJM_Swaption_Blocking.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/HJM_Securities.v$(VLEN).o src/HJM_Securities.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR  -I$(SNIPER_ROOT)/include -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2   -o $@  src/*.v$(VLEN).o -lm
	rm src/*.v$(VLEN).o
	${LLVM}/bin/llvm-objdump -D --mattr=+v $@ > ./bin/dump_vector
