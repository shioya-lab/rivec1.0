#makefile

rvv_target    = bin/rvv-test_vlen$(VLEN)
serial_target = bin/serial-test_vlen$(VLEN)

APP_NAME = swaptions

SPIKE_OPTS = -ns 8 -sm 512 -nt 1
# SPIKE_OPTS = -ns 8 -sm 4 -nt 1

RVV_COMPILE_OPTIONS += -Wall
RVV_COMPILE_OPTIONS +=  -DUSE_RISCV_VECTOR
RVV_COMPILE_OPTIONS +=  -I$(SNIPER_ROOT)/include
RVV_COMPILE_OPTIONS += -march=rv64gcv1p0
RVV_COMPILE_OPTIONS += --sysroot=$(SYSROOT_DIR)
RVV_COMPILE_OPTIONS += -g
RVV_COMPILE_OPTIONS += -O2
RVV_COMPILE_OPTIONS +=
RVV_COMPILE_OPTIONS +=
include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	for entry in src/*.cpp ; do \
		riscv64-unknown-elf-g++   -Wall  -I$(SNIPER_ROOT)/include -march=rv64gc1p0 --sysroot=$(SYSROOT_DIR)  -O2 -c -o  $$entry.scalar.o  $$entry ; \
	done
	riscv64-unknown-elf-g++ -Wall  -I$(SNIPER_ROOT)/include  -march=rv64gc1p0 --sysroot=$(SYSROOT_DIR)   -O2  -o $@  src/*.cpp.scalar.o -lm;	\
	rm src/*.scalar.o; \
	riscv64-unknown-elf-objdump -d $@ > ./bin/dump_serial


vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/CumNormalInv.assembly.v$(VLEN).o src/CumNormalInv.assembly.S
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/CumNormalInv.v$(VLEN).o src/CumNormalInv.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/MaxFunction.v$(VLEN).o src/MaxFunction.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/RanUnif.v$(VLEN).o src/RanUnif.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/nr_routines.v$(VLEN).o src/nr_routines.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/icdf.v$(VLEN).o src/icdf.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/HJM_SimPath_Forward_Blocking.v$(VLEN).o src/HJM_SimPath_Forward_Blocking.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/HJM.v$(VLEN).o src/HJM.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/HJM_Swaption_Blocking.v$(VLEN).o src/HJM_Swaption_Blocking.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/HJM_Securities.v$(VLEN).o src/HJM_Securities.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS)    -o $@  src/*.v$(VLEN).o -lm
	rm src/*.v$(VLEN).o
	riscv64-unknown-elf-objdump -D $@ > ./bin/dump_vector
