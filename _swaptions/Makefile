#makefile

rvv_target    = bin/rvv-test
serial_target = bin/serial-test

COMPILER = clang++

APP_NAME = swaptions

SPIKE_OPTS = -ns 8 -sm 512 -nt 1
# SPIKE_OPTS = -ns 8 -sm 4 -nt 1


COMMON_COMPILE_OPTIONS += -Wall
COMMON_COMPILE_OPTIONS += -I$(SNIPER_ROOT)/include
COMMON_COMPILE_OPTIONS += --sysroot=$(SYSROOT_DIR)
COMMON_COMPILE_OPTIONS += -g
COMMON_COMPILE_OPTIONS += -O2

SCALAR_COMPILE_OPTIONS += --target=riscv64-unknown-elf
SCALAR_COMPILE_OPTIONS += -march=rv64gc
SCALAR_COMPILE_OPTIONS += $(COMMON_COMPILE_OPTIONS)

RVV_COMPILE_OPTIONS += --target=riscv64-unknown-elf
RVV_COMPILE_OPTIONS += -march=rv64gcv
RVV_COMPILE_OPTIONS += -DUSE_RISCV_VECTOR
RVV_COMPILE_OPTIONS += $(COMMON_COMPILE_OPTIONS)

include ../../scripts/runspike.mk

scalar: $(serial_target)
$(serial_target):
	mkdir -p bin
	for entry in src/*.cpp ; do \
		$(COMPILER) $(SCALAR_COMPILE_OPTIONS) -c -o  $$entry.scalar.o  $$entry ; \
	done
	$(COMPILER) $(SCALAR_COMPILE_OPTIONS) -o $@  src/*.cpp.scalar.o -lm;	\
	riscv64-unknown-elf-objdump -d $@ > ./bin/dump_serial


vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/CumNormalInv.assembly.vector.o src/CumNormalInv.assembly.S
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/CumNormalInv.vector.o src/CumNormalInv.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/MaxFunction.vector.o src/MaxFunction.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/RanUnif.vector.o src/RanUnif.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/nr_routines.vector.o src/nr_routines.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/icdf.vector.o src/icdf.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/HJM_SimPath_Forward_Blocking.vector.o src/HJM_SimPath_Forward_Blocking.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/HJM.vector.o src/HJM.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/HJM_Swaption_Blocking.vector.o src/HJM_Swaption_Blocking.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS) -c -o src/HJM_Securities.vector.o src/HJM_Securities.cpp
	$(COMPILER) $(RVV_COMPILE_OPTIONS)    -o $@  src/*.vector.o -lm
	riscv64-unknown-elf-objdump -D $@ > ./bin/dump_vector
