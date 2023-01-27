LLVM = /riscv
GCC_TOOLCHAIN_DIR = /riscv
SYSROOT_DIR := $(GCC_TOOLCHAIN_DIR)/riscv64-unknown-elf

SNIPER_ROOT = $(abspath ../../sniper)
SPIKE = $(SNIPER_ROOT)/../riscv-isa-sim/spike
PK ?= $(SYSROOT_DIR)/bin/pk
# PK = $(HOME)/riscv64/riscv64-unknown-elf/bin/pk

rvv_target    ?= $(APP_NAME).vector
serial_target ?= $(APP_NAME).scalar

rvv_sift    = $(basename $(notdir $(rvv_target))).sift
# serial_sift = $(basename $(notdir $(serial_target))).sift

VLEN ?= 256

ifeq ($(APP_NAME),)
	$(error "APP_NAME should be set")
endif

SNIPER_DEBUG ?=
ifeq ($(DEBUG),on)
	SNIPER_DEBUG += --gdb-wait
endif

.PHONY: build vector scalar
.PHONY: runspike-s runspike-v
.PHONY: runsniper runsniper-v runsniper-s
.PHONY: runsniper-ooo-v runsniper-vio-v runsniper-ino-v
.PHONY: runsniper-ooo-s runsniper-ino-s

build:
	$(MAKE) vector scalar
	$(MAKE) runspike-s runspike-v
	$(MAKE) runsniper

runsniper:
	$(MAKE) runsniper-v runsniper-s

runsniper-v:
	$(MAKE) runsniper-ooo-v runsniper-vio-v runsniper-ino-v

runsniper-s:
	$(MAKE) runsniper-ooo-s runsniper-ino-s

runspike-v : $(rvv_target)
	$(MAKE) $(rvv_sift)

$(rvv_sift): $(rvv_target)
	$(SPIKE) --isa=rv64gcv --varch=vlen:$(VLEN),elen:64 --sift $@ $(PK) $^ $(SPIKE_OPTS) > spike-v.log 2>&1
	xz -f spike-v.log
# tar cvfz spike-v.log.tgz spike-v.log --remove-files

runspike-s : $(serial_target)
	$(MAKE) $(serial_sift)

$(serial_sift): $(serial_target)
	$(SPIKE) --isa=rv64gc --varch=vlen:$(VLEN),elen:64 --sift $@ $(PK) $^ $(SPIKE_OPTS) > spike-s.log 2>&1
	xz -f spike-s.log
# tar cvfz spike-s.log.tgz spike-s.log --remove-files

runspike-debug-v : $(rvv_target)
	$(SPIKE) --isa=rv64gcv -l --log-commits --sift $(rvv_sift) $(PK) $^ $(SPIKE_OPTS) > spike-v.log 2>&1

runspike-debug-s : $(serial_target)
	$(SPIKE) --isa=rv64gc -l --log-commits --sift $(serial_sift) $(PK) $^ $(SPIKE_OPTS) > spike-s.log 2>&1

runsniper-ooo-v: $(rvv_sift)
	mkdir -p ooo.v.$(VLEN) && \
	cd ooo.v.$(VLEN) && \
	$(SNIPER_ROOT)/run-sniper $(SNIPER_DEBUG) --power -v -c $(SNIPER_ROOT)/config/riscv-base.cfg -c $(SNIPER_ROOT)/config/riscv-mediumboom.vlen$(VLEN).cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).ooo.v.$(VLEN).log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(rvv_target))).ooo.v.$(VLEN).log > cycle && \
	mv o3_trace.out $(APP_NAME).ooo.out

#	xz -f $(basename $(notdir $(rvv_target))).ooo.v.$(VLEN).log && \
#	mv o3_trace.out $(APP_NAME).ooo.out && \
#	$(MAKE) -f $(abspath ../runspike.mk) sniper2mcpat APP_NAME=$(APP_NAME) VLEN=$(VLEN) DIR=ooo.v.$(VLEN)


runsniper-ino-v: $(rvv_sift)
	mkdir -p ino.v.$(VLEN) && \
	cd ino.v.$(VLEN) && \
	$(SNIPER_ROOT)/run-sniper $(SNIPER_DEBUG) --power -v -c $(SNIPER_ROOT)/config/riscv-base.cfg -c $(SNIPER_ROOT)/config/riscv-inorderboom.vlen$(VLEN).cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).ino.v.$(VLEN).log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(rvv_target))).ino.v.$(VLEN).log > cycle && \
	xz -f $(basename $(notdir $(rvv_target))).ino.v.$(VLEN).log && \
	mv o3_trace.out $(APP_NAME).ino.out && \
	$(MAKE) -f $(abspath ../runspike.mk) sniper2mcpat APP_NAME=$(APP_NAME) VLEN=$(VLEN) DIR=ino.v.$(VLEN)

runsniper-vio-v: $(rvv_sift)
	mkdir -p vio.v.$(VLEN) && \
	cd vio.v.$(VLEN) && \
	$(SNIPER_ROOT)/run-sniper $(SNIPER_DEBUG) --power -v -c $(SNIPER_ROOT)/config/riscv-base.cfg -c $(SNIPER_ROOT)/config/riscv-vinorderboom.vlen$(VLEN).cfg --traces=../$^ > $(basename $(notdir $(rvv_target))).vio.log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(rvv_target))).vio.log > cycle && \
	xz -f $(basename $(notdir $(rvv_target))).vio.log && \
	mv o3_trace.out $(APP_NAME).vio.out && \
	$(MAKE) -f $(abspath ../runspike.mk) sniper2mcpat APP_NAME=$(APP_NAME) VLEN=$(VLEN) DIR=vio.v.$(VLEN)


runsniper-ooo-s: $(serial_sift)
	mkdir -p ooo.s && \
	cd ooo.s && \
	$(SNIPER_ROOT)/run-sniper $(SNIPER_DEBUG) --power -v -c $(SNIPER_ROOT)/config/riscv-base.cfg -c $(SNIPER_ROOT)/config/riscv-mediumboom.vlen$(VLEN).cfg --traces=../$^ > $(basename $(notdir $(serial_target))).ooo.s.log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(serial_target))).ooo.s.log > cycle && \
	xz -f $(basename $(notdir $(serial_target))).ooo.s.log && \
	mv o3_trace.out $(APP_NAME).ooo.s.out && \
	$(MAKE) -f $(abspath ../runspike.mk) sniper2mcpat APP_NAME=$(APP_NAME) VLEN=$(VLEN) DIR=ooo.s


runsniper-ino-s: $(serial_sift)
	mkdir -p ino.s && \
	cd ino.s && \
	$(SNIPER_ROOT)/run-sniper $(SNIPER_DEBUG) --power -v -c $(SNIPER_ROOT)/config/riscv-base.cfg -c $(SNIPER_ROOT)/config/riscv-inorderboom.vlen$(VLEN).cfg --traces=../$^ > $(basename $(notdir $(serial_target))).ino.s.log 2>&1 && \
	awk '{ if($$1 == "CycleTrace") { if (cycle==0) { cycle=$$2 } else { print $$2 - cycle; cycle=0;} }}'  $(basename $(notdir $(serial_target))).ino.s.log > cycle && \
	xz -f $(basename $(notdir $(serial_target))).ino.s.log && \
	mv o3_trace.out $(APP_NAME).ino.s.out && \
	$(MAKE) -f $(abspath ../runspike.mk) sniper2mcpat APP_NAME=$(APP_NAME) VLEN=$(VLEN) DIR=ino.s

sniper2mcpat:
	python3 ../../sniper2mcpat/sniper2mcpat.py $(DIR)/sim.stats.sqlite3 ../mcpat_common/mcpat.template.vec$(VLEN).xml

clean:
	rm -rf $(rvv_target) $(serial_target)
	rm -rf output.txt
	rm -rf ino.s
	rm -rf ooo.s
	rm -rf ino.v.*
	rm -rf ooo.v.*
	rm -rf vio.v.*
	rm -rf *.sift
	rm -rf *.log
	rm -rf bin/*
	rm -rf *.xz
	rm -rf *.dmp
