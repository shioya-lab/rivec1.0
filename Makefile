BASE_DIR := $(shell pwd)

APPLICATION_DIRS := _axpy _streamcluster _blackscholes _canneal _swaptions _particlefilter _pathfinder _jacobi-2d _spmv

VLEN = 256

all: $(subst _,,$(APPLICATION_DIRS))
	$(MAKE) stats

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
	$(MAKE) runsniper-ooo-v runsniper-io-v runsniper-vio-v runsniper-vio-ngs-v

runsniper-s:
	$(MAKE) runsniper-ooo-s runsniper-io-s

$(subst _,,$(APPLICATION_DIRS)):
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s
#	$(MAKE) -C _$@ VLEN=$(VLEN) power-v power-s

$(addprefix power,$(APPLICATION_DIRS)):
	$(MAKE) -C $(subst power,,$@) VLEN=$(VLEN) power-v power-s

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

stats:
	for dir in $(APPLICATION_DIRS); do \
		echo -n $${dir} "\t"; \
		xzgrep "cycles = " $${dir}/spike-s.log.xz | sed 's/cycles = //g'     | xargs echo -n; echo -n " "; \
		paste $${dir}/ino.s/cycle $${dir}/ooo.s/cycle                       | xargs echo -n; echo -n " "; \
		xzgrep "cycles = " $${dir}/spike-v.$(VLEN).log.xz | sed 's/cycles = //g'     | xargs echo -n; echo -n " "; \
		xzgrep "vecinst = " $${dir}/spike-v.$(VLEN).log.xz | sed 's/vecinst = //g' | xargs echo -n; echo -n " "; \
		paste $${dir}/ino.v.v$(VLEN)_d$(DLEN)/cycle $${dir}/vio.v.v$(VLEN)_d$(DLEN)/cycle $${dir}/ooo.v.v$(VLEN)_d$(DLEN)/cycle ; \
	done

power:
	$(MAKE) power_all power_filtered VLEN=$(VLEN)

power_all:
	echo -n "Application," > power.$(VLEN).csv
	head -n1 _spmv/ooo.v.$(VLEN)/sim.stats.mcpat.output.csv >> power.$(VLEN).csv
	for dir in $(APPLICATION_DIRS); do \
		echo -n $${dir}_ino_s_${VLEN}","; tail -n+2 $${dir}/ino.s/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ooo_s_${VLEN}","; tail -n+2 $${dir}/ooo.s/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ino_v_${VLEN}","; tail -n+2 $${dir}/ino.v.$(VLEN)/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_vio_v_${VLEN}","; tail -n+2 $${dir}/vio.v.$(VLEN)/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ooo_v_${VLEN}","; tail -n+2 $${dir}/ooo.v.$(VLEN)/sim.stats.mcpat.output.csv; \
	done >> power.$(VLEN).csv

power_filtered:
	echo -n "Application,," > power.$(VLEN).filtered.csv
	head -n1 _spmv/ooo.v.$(VLEN)/sim.stats.mcpat.output.filtered.csv >> power.$(VLEN).filtered.csv
	for dir in $(APPLICATION_DIRS); do \
		echo -n $${dir}_ino_s_${VLEN}","; tail -n+2 $${dir}/ino.s/sim.stats.mcpat.output.filtered.csv; \
		echo -n $${dir}_ooo_s_${VLEN}","; tail -n+2 $${dir}/ooo.s/sim.stats.mcpat.output.filtered.csv; \
		echo -n $${dir}_ino_v_${VLEN}","; tail -n+2 $${dir}/ino.v.$(VLEN)/sim.stats.mcpat.output.filtered.csv; \
		echo -n $${dir}_vio_v_${VLEN}","; tail -n+2 $${dir}/vio.v.$(VLEN)/sim.stats.mcpat.output.filtered.csv; \
		echo -n $${dir}_ooo_v_${VLEN}","; tail -n+2 $${dir}/ooo.v.$(VLEN)/sim.stats.mcpat.output.filtered.csv; \
	done >> power.$(VLEN).filtered.csv

clean:
	for dir in $(APPLICATION_DIRS); do \
		$(MAKE) clean -C $${dir}; \
	done
