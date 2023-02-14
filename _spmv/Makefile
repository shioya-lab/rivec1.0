.PONY: power

rvv_target    = spmv_vector_vlen$(VLEN)
serial_target = spmv_scalar_vlen$(VLEN)

run:
	$(MAKE) runsniper-ooo-v runsniper-vio-v runsniper-ino-v  runsniper-vio-ngs-v
	$(MAKE) runsniper-ooo-s runsniper-ino-s

SOURCE_FILES += spmv_main.c
SOURCE_FILES += spmv_vector.S

APP_NAME = spmv

RISCV_GCC_SCALAR_OPTS = \
	-march=rv64g \
	-O3 \
	-funroll-loops \
	-I/home/kimura/work/sniper/sniper/sniper/include/ \
	-DPREALLOCATE=1 -mcmodel=medany

include ../../microbenchmarks/microbenches.mk
include ../../scripts/compile.mk
include ../../scripts/runspike.mk
