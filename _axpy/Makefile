#makefile
rvv_target    = bin/rvv-test_vlen$(VLEN)
serial_target = bin/serial-test_vlen$(VLEN)

start:
	rm bin/*.*

serial:
	echo "serial"
	${RISCV}/bin/clang -march=rv64g -O2 -c -o src/utils.o src/utils.c
	${RISCV}/bin/clang -march=rv64g -O2 -c -o src/axpy.o src/axpy.c
	${RISCV}/bin/clang -march=rv64g -O2 -c -o src/main.o src/main.c
	${RISCV}/bin/clang -march=rv64g -O2 -o bin/axpy_serial.exe src/*.o -lm
	rm src/*.o
	${RISCV}/bin/llvm-objdump --mattr=+m,+f,+d,+a,+c -ds  bin/axpy_serial.exe > bin/axpy_serial.dump

vector:
	echo "vector"
	${RISCV}/bin/clang -march=rv64gcv -DUSE_RISCV_VECTOR  -fno-vectorize -O2 -c -o src/axpy.o src/axpy.c
	${RISCV}/bin/clang -march=rv64gcv -DUSE_RISCV_VECTOR  -fno-vectorize -c -o src/main.o src/main.c
	${RISCV}/bin/clang -march=rv64gcv -DUSE_RISCV_VECTOR  -fno-vectorize -O2 -c -o src/utils.o src/utils.c
	${RISCV}/bin/clang -march=rv64gcv -DUSE_RISCV_VECTOR  -fno-vectorize -O2 -o bin/axpy_vector.exe src/*.o -lm
	rm src/*.o
	${RISCV}/bin/llvm-objdump  --mattr=+m,+f,+d,+a,+c,+v -ds  bin/axpy_vector.exe > bin/axpy_vector.dump

vector: $(rvv_target)
$(rvv_target): src/utils.c src/axpy.c src/main.c
	mkdir -p bin
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/utils.o src/utils.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/axpy_vector.o src/axpy.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -c -o src/main.o src/main.c
	${LLVM}/bin/clang  -Wall --target=riscv64-unknown-elf -I$(SNIPER_ROOT)/include -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -menable-experimental-extensions -O2  --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -o $(rvv_target) src/axpy_vector.o src/main.o src/utils.o -lm
