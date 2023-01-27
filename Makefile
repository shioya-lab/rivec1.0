BASE_DIR := $(shell pwd)

APPLICATION_DIRS := _axpy _streamcluster _blackscholes _canneal _swaptions _particlefilter _pathfinder _jacobi-2d _spmv

VLEN = 256

all: $(subst _,,$(APPLICATION_DIRS))
	$(MAKE) stats

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
	$(MAKE) runsniper-ooo-v runsniper-io-v runsniper-vio-v

runsniper-s:
	$(MAKE) runsniper-ooo-s runsniper-io-s

blackscholes:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s

swaptions:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s

streamcluster:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s

canneal:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s

particlefilter:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s

pathfinder:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s

jacobi-2d:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s

matmul:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper-v runsniper-s

axpy:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-v runsniper-s

spmv:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-v runsniper-s

stats:
	for dir in $(APPLICATION_DIRS); do \
		echo -n $${dir} "\t"; \
		xzgrep "cycles = " $${dir}/spike-s.log.xz | sed 's/cycles = //g'     | xargs echo -n; echo -n " "; \
		paste $${dir}/ooo.s/cycle $${dir}/ino.s/cycle                      | xargs echo -n; echo -n " "; \
		xzgrep "cycles = " $${dir}/spike-v.log.xz | sed 's/cycles = //g'     | xargs echo -n; echo -n " "; \
		xzgrep "vecinst = " $${dir}/spike-v.log.xz | sed 's/vecinst = //g' | xargs echo -n; echo -n " "; \
		paste $${dir}/ino.v.$(VLEN)/cycle $${dir}/vio.v.$(VLEN)/cycle $${dir}/ooo.v.$(VLEN)/cycle ; \
	done

power:
	echo -n "Application," > power.$(VLEN).csv
	head -n1 _spmv/ooo.v.$(VLEN)/sim.stats.mcpat.output.csv >> power.$(VLEN).csv
	for dir in $(APPLICATION_DIRS); do \
		echo -n $${dir}_ino_s ","; tail -n+2 $${dir}/ino.s/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ooo_s ","; tail -n+2 $${dir}/ooo.s/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ino_v ","; tail -n+2 $${dir}/ino.v.$(VLEN)/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_vio_v ","; tail -n+2 $${dir}/vio.v.$(VLEN)/sim.stats.mcpat.output.csv; \
		echo -n $${dir}_ooo_v ","; tail -n+2 $${dir}/ooo.v.$(VLEN)/sim.stats.mcpat.output.csv; \
	done >> power.$(VLEN).csv

clean:
	$(MAKE) clean -C _blackscholes
	$(MAKE) clean -C _swaptions
	$(MAKE) clean -C _streamcluster
	$(MAKE) clean -C _canneal
	$(MAKE) clean -C _particlefilter
	$(MAKE) clean -C _pathfinder
	$(MAKE) clean -C _jacobi-2d
	$(MAKE) clean -C _axpy
