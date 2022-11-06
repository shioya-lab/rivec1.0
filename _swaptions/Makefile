#makefile

rvv_target = bin/rvv-test
serial_target = bin/serial-test

SPIKE_OPTS = -ns 8 -sm 512 -nt 1

include ../runspike.mk

serial: $(serial_target)
$(serial_target):
	for entry in src/*.cpp ; do \
		${LLVM}/bin/clang++   -Wall --target=riscv64-unknown-elf -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o  $$entry.o  $$entry ; \
	done
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf  -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2  -o $@  src/*.cpp.o -lm;	\
	rm src/*.o; \
	${LLVM}/bin/llvm-objdump -D --mattr=+v $@ > ./bin/dump_serial


vector: $(rvv_target)
$(rvv_target):
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/CumNormalInv.o src/CumNormalInv.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/MaxFunction.o src/MaxFunction.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/RanUnif.o src/RanUnif.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/nr_routines.o src/nr_routines.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/icdf.o src/icdf.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR)  -O2 -c -o src/HJM_SimPath_Forward_Blocking.o src/HJM_SimPath_Forward_Blocking.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/HJM.o src/HJM.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/HJM_Swaption_Blocking.o src/HJM_Swaption_Blocking.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2 -c -o src/HJM_Securities.o src/HJM_Securities.cpp
	${LLVM}/bin/clang++  -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -O2   -o $@  src/*.o -lm
	rm src/*.o
	${LLVM}/bin/llvm-objdump -D --mattr=+v $@ > ./bin/dump_vector
