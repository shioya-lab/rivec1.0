BASE_DIR := $(shell pwd)

APPLICATION_DIRS := _axpy _streamcluster _blackscholes _canneal _swaptions _particlefilter _pathfinder _jacobi-2d _spmv

VLEN ?= 256
DLEN ?= $(VLEN)

all: $(subst _,,$(APPLICATION_DIRS))
	$(MAKE) perf
	$(MAKE) power_filtered
	$(MAKE) area

power: $(addprefix power,$(APPLICATION_DIRS))


.PHONY: $(addsuffix _sniper, $(APPLICATION_DIRS))
.PHONY: $(addsuffix _spike, $(APPLICATION_DIRS))

only_spike:
	$(MAKE) $(addsuffix _spike, $(APPLICATION_DIRS))

$(addsuffix _spike, $(APPLICATION_DIRS)):
	$(MAKE) -C $(subst _spike,, $@) runspike-v runspike-s

only_sniper:
	$(MAKE) $(addsuffix _sniper, $(APPLICATION_DIRS)) runsniper

$(addsuffix _sniper, $(APPLICATION_DIRS)):
	$(MAKE) -C $(subst _sniper,, $@) runsniper-ooo-v runsniper-io-v runsniper-vio-v

runsniper:
	$(MAKE) runsniper-v runsniper-s

runsniper-v:
	$(MAKE) runsniper-ooo-v runsniper-io-v runsniper-vio-v runsniper-vio-fence-v runsniper-vio-ngs-v

runsniper-s:
	$(MAKE) runsniper-ooo-s runsniper-io-s

$(subst _,,$(APPLICATION_DIRS)):
	$(MAKE) -C _$@ VLEN=$(VLEN) DLEN=$(DLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) DLEN=$(DLEN) runsniper-v runsniper-s
#	$(MAKE) -C _$@ VLEN=$(VLEN) power-v power-s

$(addprefix power,$(APPLICATION_DIRS)):
	$(MAKE) -C $(subst power,,$@) VLEN=$(VLEN) DLEN=$(DLEN) power-v power-s

# swaptions:
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s
#
# streamcluster:
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s
#
# canneal:
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s
#
# particlefilter:
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s
#
# pathfinder:
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s
#
# jacobi-2d:
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s
#
# matmul:
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
# 	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s
#
# axpy:
# 	$(MAKE) -C _$@ runspike-v runspike-s
# 	$(MAKE) -C _$@ runsniper-v runsniper-s
#
# spmv:
# 	$(MAKE) -C _$@ runspike-v runspike-s
# 	$(MAKE) -C _$@ runsniper-v runsniper-s

perf:
	for dir in $(APPLICATION_DIRS); do \
		echo -n $${dir} "\t"; \
		xzgrep "cycles = " $${dir}/spike-s.log.xz | sed 's/cycles = //g'     | xargs echo -n; echo -n " "; \
		paste $${dir}/ino.s/cycle $${dir}/ooo.s/cycle                       | xargs echo -n; echo -n " "; \
		xzgrep "cycles = " $${dir}/spike-v.$(VLEN).log.xz | sed 's/cycles = //g'     | xargs echo -n; echo -n " "; \
		xzgrep "vecinst = " $${dir}/spike-v.$(VLEN).log.xz | sed 's/vecinst = //g' | xargs echo -n; echo -n " "; \
		paste $${dir}/ino.v.v$(VLEN)_d$(DLEN)/cycle \
			  $${dir}/vio.v.fence.v$(VLEN)_d$(DLEN)/cycle \
			  $${dir}/vio.v.ngs.v$(VLEN)_d$(DLEN)/cycle \
			  $${dir}/vio.v.v$(VLEN)_d$(DLEN)/cycle \
			  $${dir}/ooo.v.v$(VLEN)_d$(DLEN)/cycle ; \
	done > perf.v$(VLEN)_d$(DLEN).csv

power:
	$(MAKE) power_all power_filtered VLEN=$(VLEN)

power_all:
	echo -n "Application," > power.v$(VLEN)_d$(DLEN).csv
	head -n1 _spmv/ooo.v.v$(VLEN)_d$(DLEN)/sim.stats.mcpat.output.csv >> power.v$(VLEN)_d$(DLEN).csv
	for dir in $(APPLICATION_DIRS); do \
		echo -n $${dir}_ino_s_v${VLEN}_d${DLEN}","; tail -n+2 $${dir}/ino.s/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ooo_s_v${VLEN}_d${DLEN}","; tail -n+2 $${dir}/ooo.s/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ino_v_v${VLEN}_d${DLEN}","; tail -n+2 $${dir}/ino.v.$(VLEN)/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_vio_v_v${VLEN}_d${DLEN}","; tail -n+2 $${dir}/vio.v.$(VLEN)/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ooo_v_v${VLEN}_d${DLEN}","; tail -n+2 $${dir}/ooo.v.$(VLEN)/sim.stats.mcpat.output.csv; \
	done >> power.$(VLEN).csv

power_filtered:
	echo -n "Application,," > power.v$(VLEN)_d$(DLEN).filtered.csv
	head -n1 _spmv/ooo.v.v$(VLEN)_d$(DLEN)/power.csv >> power.v$(VLEN)_d$(DLEN).filtered.csv
	for dir in $(APPLICATION_DIRS); do \
		tail -n+2 $${dir}/ino.s/power.csv; \
		tail -n+2 $${dir}/ooo.s/power.csv; \
		tail -n+2 $${dir}/ino.v.v$(VLEN)_d$(DLEN)/power.csv; \
		tail -n+2 $${dir}/vio.v.v$(VLEN)_d$(DLEN)/power.csv; \
		tail -n+2 $${dir}/ooo.v.v$(VLEN)_d$(DLEN)/power.csv; \
	done >> power.v$(VLEN)_d$(DLEN).filtered.csv


area:
	echo -n "Application,," > area.v$(VLEN)_d$(DLEN).area.csv
	head -n1 _spmv/ooo.v.v$(VLEN)_d$(DLEN)/area.csv >> area.v$(VLEN)_d$(DLEN).area.csv
	for dir in $(APPLICATION_DIRS); do \
		tail -n+2 $${dir}/ino.s/area.csv; \
		tail -n+2 $${dir}/ooo.s/area.csv; \
		tail -n+2 $${dir}/ino.v.v$(VLEN)_d$(DLEN)/area.csv; \
		tail -n+2 $${dir}/vio.v.v$(VLEN)_d$(DLEN)/area.csv; \
		tail -n+2 $${dir}/ooo.v.v$(VLEN)_d$(DLEN)/area.csv; \
	done >> area.v$(VLEN)_d$(DLEN).area.csv

clean:
	for dir in $(APPLICATION_DIRS); do \
		$(MAKE) clean -C $${dir}; \
	done
