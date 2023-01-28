.PONY: power

rvv_target = spmv_vector
serial_target = spmv_scalar

run:
	$(MAKE) runsniper-ooo-v runsniper-vio-v runsniper-ino-v  runsniper-vio-ngs-v  
	$(MAKE) runsniper-ooo-s runsniper-ino-s

SOURCE_FILES += spmv_main.c

APP_NAME = spmv

power: 
	echo -n "Application," > spmv_power.$(VLEN).csv
	head -n1 ooo.v.$(VLEN)/sim.stats.mcpat.output.csv >> spmv_power.$(VLEN).csv
	echo -n ino_s     "," >> spmv_power.$(VLEN).csv; tail -n+2 ino.s/sim.stats.mcpat.output.csv >> spmv_power.$(VLEN).csv
	echo -n ooo_s     "," >> spmv_power.$(VLEN).csv; tail -n+2 ooo.s/sim.stats.mcpat.output.csv >> spmv_power.$(VLEN).csv
	echo -n ino_v     "," >> spmv_power.$(VLEN).csv; tail -n+2 ino.v.$(VLEN)/sim.stats.mcpat.output.csv >> spmv_power.$(VLEN).csv
	echo -n vio_v     "," >> spmv_power.$(VLEN).csv; tail -n+2 vio.v.$(VLEN)/sim.stats.mcpat.output.csv >> spmv_power.$(VLEN).csv
	echo -n vio_ngs_v "," >> spmv_power.$(VLEN).csv; tail -n+2 vio.v.ngs.$(VLEN)/sim.stats.mcpat.output.csv >> spmv_power.$(VLEN).csv
	echo -n ooo_v     "," >> spmv_power.$(VLEN).csv; tail -n+2 ooo.v.$(VLEN)/sim.stats.mcpat.output.csv >> spmv_power.$(VLEN).csv

include ../../microbenchmarks/microbenches.mk
include ../../scripts/compile.mk
include ../../scripts/runspike.mk
