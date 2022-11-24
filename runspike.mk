LLVM = $(HOME)/work/llvm/llvm-myriscvx150/build
GCC_TOOLCHAIN_DIR = $(HOME)/riscv-rvvnext

SNIPER_ROOT = $(abspath ../../../sniper)
SPIKE = $(SNIPER_ROOT)/../riscv-isa-sim/spike
PK = $(HOME)/riscv64imafd/riscv64-unknown-elf/bin/pk
# PK = $(HOME)/riscv64/riscv64-unknown-elf/bin/pk

rvv_sift = $(basename $(notdir $(rvv_target))).sift
serial_sift = $(basename $(notdir $(serial_target))).sift

build:
	$(MAKE) vector
	$(MAKE) runspike-v
	$(MAKE) runsniper-ooo-v runsniper-vio runsniper-io-v

#	$(MAKE) serial


runspike-v : $(rvv_target)
	$(SPIKE) --isa=rv64gcv --sift $(rvv_sift) $(PK) $^ $(SPIKE_OPTS) > spike-v.log 2>&1

runspike-s : $(serial_target)
	$(SPIKE) --isa=rv64gc --sift $(serial_sift) $(PK) $^ $(SPIKE_OPTS) > spike-s.log 2>&1

runspike-debug-v : $(rvv_target)
	$(SPIKE) --isa=rv64gcv -l --log-commits --sift $(rvv_sift) $(PK) $^ $(SPIKE_OPTS) > spike-v.log 2>&1

runspike-debug-s : $(serial_target)
	$(SPIKE) --isa=rv64gc -l --log-commits --sift $(serial_sift) $(PK) $^ $(SPIKE_OPTS) > spike-s.log 2>&1

runsniper-ooo-v: $(rvv_sift)
	mkdir -p ooo.v && \
	cd ooo.v && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-mediumboom.cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).ooo.v.log 2>&1 && \
	grep rdcycle -B2 $(basename $(notdir $(rvv_target))).ooo.v.log | grep Running | awk '{ if(NR%2==1) { start=$$3 } else { print $$3-start} }' > $(basename $(notdir $(rvv_target))).ooo && \
	tar cvfz $(basename $(notdir $(rvv_target))).ooo.v.log.tgz $(basename $(notdir $(rvv_target))).ooo.v.log --remove-files && \
	mv o3_trace.out $(APP_NAME).ooo.out

runsniper-io-v: $(rvv_sift)
	mkdir -p io.v && \
	cd io.v && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-inorderboom.cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).io.v.log 2>&1 && \
	grep rdcycle -B2 $(basename $(notdir $(rvv_target))).io.v.log | grep Running | awk '{ if(NR%2==1) { start=$$3 } else { print $$3-start} }' > $(basename $(notdir $(rvv_target))).io && \
	tar cvfz $(basename $(notdir $(rvv_target))).io.v.log.tgz $(basename $(notdir $(rvv_target))).io.v.log --remove-files && \
	mv o3_trace.out $(APP_NAME).io.out

runsniper-vio: $(rvv_sift)
	mkdir -p vio.v && \
	cd vio.v && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-vinorderboom.cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).vio.log 2>&1 && \
	grep rdcycle -B2 $(basename $(notdir $(rvv_target))).vio.log | grep Running | awk '{ if(NR%2==1) { start=$$3 } else { print $$3-start} }' > $(basename $(notdir $(rvv_target))).vio && \
	tar cvfz $(basename $(notdir $(rvv_target))).vio.log.tgz $(basename $(notdir $(rvv_target))).vio.log --remove-files && \
	mv o3_trace.out $(APP_NAME).vio.out

runsniper-ooo-s: $(serial_sift)
	mkdir -p ooo.s && \
	cd ooo.s && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-mediumboom.cfg --traces=../$^ > $(basename $(notdir $(serial_target))).ooo.s.log 2>&1 && \
	tar cvfz $(basename $(notdir $(serial_target))).ooo.v.log.tgz $(basename $(notdir $(serial_target))).ooo.v.log --remove-files

runsniper-io-s: $(serial_sift)
	mkdir -p io.s && \
	cd io.s && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-inorderboom.cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).io.s.log 2>&1 && \
	tar cvfz $(basename $(notdir $(serial_target))).io.v.log.tgz $(basename $(notdir $(serial_target))).io.v.log --remove-files


clean:
	rm -rf output.txt
	rm -rf io.s
	rm -rf io.v
	rm -rf ooo.s
	rm -rf ooo.v
	rm -rf vio.v
	rm -rf *.sift
	rm -rf *.log
	rm -rf bin/*
