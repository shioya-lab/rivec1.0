#makefile
GCC_TOOLCHAIN_DIR := /newlib/
SYSROOT_DIR := $(GCC_TOOLCHAIN_DIR)/riscv64-unknown-elf

start:
	mkdir bin; \
	rm bin/*.*

scalar: bin/tests_serial.exe

bin/tests_serial.exe:
	mkdir -p bin
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -march=rv64g -O2 --sysroot=$(SYSROOT_DIR) -c -o src/tests.o src/tests.cpp
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -march=rv64g -O2 --sysroot=$(SYSROOT_DIR) -o  src/tests_serial.o -lm
	rm src/*.o
#	${LLVM}/bin/llvm-objdump  -mattr=+m,+f,+d,+a,+c,+epi -ds  $@ > bin/tests_serial.dump

vector: bin/tests_vector.exe
bin/tests_vector.exe:
	mkdir -p bin
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -O2 --sysroot=$(SYSROOT_DIR) -c -o src/tests.o src/tests.cpp ; \
	${LLVM}/bin/clang++ -Wall --target=riscv64-unknown-elf -DUSE_RISCV_VECTOR -march=rv64gcv1p0 -O2 --sysroot=$(SYSROOT_DIR) -o $@ src/*.o -lm ; \
	rm src/*.o ; \
#	${LLVM}/bin/llvm-objdump  -mattr=+m,+f,+d,+a,+c,+epi -ds   $@ > bin/tests_vector.dump ;

host:
	gcc -O2 -fopenmp src/tests.cpp -o bin/tests_host.exe -lm ;

copy:
	rm -r ../../Test/_tests/bin/*.exe; \
	cp -r bin/*exe ../../Test/_tests/bin;

runspike-v : ./bin/tests_vector.exe
	$(SPIKE) --isa=rv64gcv $(PK) $^

runspike-serial : bin/tests_serial.exe
	$(SPIKE) --isa=rv64gc $(PK) $^

clean:
	rm bin/*.dump; \
	rm bin/*.exe;
