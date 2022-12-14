LLVM = /riscv
GCC_TOOLCHAIN_DIR = /riscv
SYSROOT_DIR := $(GCC_TOOLCHAIN_DIR)/riscv64-unknown-elf

SNIPER_ROOT = $(abspath ../../../sniper)
SPIKE = $(SNIPER_ROOT)/../riscv-isa-sim/spike
PK ?= $(SYSROOT_DIR)/bin/pk
# PK = $(HOME)/riscv64/riscv64-unknown-elf/bin/pk

rvv_sift = $(basename $(notdir $(rvv_target))).sift
serial_sift = $(basename $(notdir $(serial_target))).sift

build:
	$(MAKE) vector scalar
	$(MAKE) runspike-s runspike-v
	$(MAKE) runsniper

runsniper:
	$(MAKE) runsniper-ooo-v runsniper-vio runsniper-ino-v runsniper-ooo-s runsniper-ino-s

runspike-v : $(rvv_target)
	$(MAKE) $(rvv_sift)

$(rvv_sift): $(rvv_target)
	$(SPIKE) --isa=rv64gcv --sift $@ $(PK) $^ $(SPIKE_OPTS) > spike-v.log 2>&1
	xz -f spike-v.log
# tar cvfz spike-v.log.tgz spike-v.log --remove-files

runspike-s : $(serial_target)
	$(MAKE) $(serial_sift)

$(serial_sift): $(serial_target)
	$(SPIKE) --isa=rv64gc --sift $@ $(PK) $^ $(SPIKE_OPTS) > spike-s.log 2>&1
	xz -f spike-s.log
# tar cvfz spike-s.log.tgz spike-s.log --remove-files

runspike-debug-v : $(rvv_target)
	$(SPIKE) --isa=rv64gcv -l --log-commits --sift $(rvv_sift) $(PK) $^ $(SPIKE_OPTS) > spike-v.log 2>&1

runspike-debug-s : $(serial_target)
	$(SPIKE) --isa=rv64gc -l --log-commits --sift $(serial_sift) $(PK) $^ $(SPIKE_OPTS) > spike-s.log 2>&1

runsniper-ooo-v: $(rvv_sift)
	mkdir -p ooo.v && \
	cd ooo.v && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-mediumboom.cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).ooo.v.log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(rvv_target))).ooo.v.log > $(basename $(notdir $(rvv_target))).ooo && \
	xz -f $(basename $(notdir $(rvv_target))).ooo.v.log && \
	mv o3_trace.out $(APP_NAME).ooo.out && \
	xz -f $(APP_NAME).ooo.out

#	tar cvfz $(basename $(notdir $(rvv_target))).ooo.v.log.tgz $(basename $(notdir $(rvv_target))).ooo.v.log --remove-files && \
#	tar cvfz $(APP_NAME).ooo.out.tgz $(APP_NAME).ooo.out --remove-files

runsniper-ino-v: $(rvv_sift)
	mkdir -p ino.v && \
	cd ino.v && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-inorderboom.cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).ino.v.log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(rvv_target))).ino.v.log > $(basename $(notdir $(rvv_target))).io && \
	xz -f $(basename $(notdir $(rvv_target))).ino.v.log && \
	mv o3_trace.out $(APP_NAME).ino.out && \
	xz -f $(APP_NAME).ino.out

# tar cvfz $(basename $(notdir $(rvv_target))).ino.v.log.tgz $(basename $(notdir $(rvv_target))).ino.v.log --remove-files && \
# tar cvfz $(APP_NAME).ino.out.tgz $(APP_NAME).ino.out --remove-files

runsniper-vio: $(rvv_sift)
	mkdir -p vio.v && \
	cd vio.v && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-vinorderboom.cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).vio.log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(rvv_target))).vio.log > $(basename $(notdir $(rvv_target))).vio && \
	xz -f $(basename $(notdir $(rvv_target))).vio.log && \
	mv o3_trace.out $(APP_NAME).vio.out && \
	xz -f $(APP_NAME).vio.out

# tar cvfz $(basename $(notdir $(rvv_target))).vio.log.tgz $(basename $(notdir $(rvv_target))).vio.log --remove-files && \
# tar cvfz $(APP_NAME).vio.out.tgz $(APP_NAME).vio.out --remove-files

runsniper-ooo-s: $(serial_sift)
	mkdir -p ooo.s && \
	cd ooo.s && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-mediumboom.cfg --traces=../$^ > $(basename $(notdir $(serial_target))).ooo.s.log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(serial_target))).ooo.s.log > $(basename $(notdir $(serial_target))).ooo.s && \
	xz -f $(basename $(notdir $(serial_target))).ooo.s.log && \
	mv o3_trace.out $(APP_NAME).ooo.s.out && \
	xz -f $(APP_NAME).ooo.s.out


runsniper-ino-s: $(serial_sift)
	mkdir -p ino.s && \
	cd ino.s && \
	$(SNIPER_ROOT)/run-sniper -v -c $(SNIPER_ROOT)/config/riscv-inorderboom.cfg --traces=../$^ > $(basename $(notdir $(serial_target))).ino.s.log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(serial_target))).ino.s.log > $(basename $(notdir $(serial_target))).ino.s && \
	xz -f $(basename $(notdir $(serial_target))).ino.s.log && \
	mv o3_trace.out $(APP_NAME).ino.s.out && \
	xz -f $(APP_NAME).ino.s.out

clean:
	rm -rf $(rvv_target) $(serial_target)
	rm -rf output.txt
	rm -rf ino.s
	rm -rf ino.v
	rm -rf ooo.s
	rm -rf ooo.v
	rm -rf vio.v
	rm -rf *.sift
	rm -rf *.log
	rm -rf bin/*
	rm -rf *.xz
