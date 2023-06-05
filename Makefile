BASE_DIR := $(shell pwd)

APPLICATION_DIRS := _axpy _streamcluster _blackscholes _canneal _swaptions _particlefilter _pathfinder _jacobi-2d _spmv

VLEN ?= 256
DLEN ?= $(VLEN)

all: run_scalar runspike_v2 runspike_v4 runspike_v8 runspike_v16
	$(MAKE) run_v2d2 run_v4d2 run_v8d2 run_v4d4 run_v8d4 run_v16d4

run_scalar:
	$(MAKE) $(subst _,scalar_,$(APPLICATION_DIRS))
runspike_v2:
	$(MAKE) VLEN=128 $(addsuffix _spike,$(APPLICATION_DIRS))
runspike_v4:
	$(MAKE) VLEN=256 $(addsuffix _spike,$(APPLICATION_DIRS))
runspike_v8:
	$(MAKE) VLEN=512 $(addsuffix _spike,$(APPLICATION_DIRS))
runspike_v16:
	$(MAKE) VLEN=1024 $(addsuffix _spike,$(APPLICATION_DIRS))

run_v2d2 : 
	$(MAKE) VLEN=128  DLEN=128 $(subst _,,$(APPLICATION_DIRS))
run_v4d2 :
	$(MAKE) VLEN=256  DLEN=128 $(subst _,,$(APPLICATION_DIRS))
run_v8d2 :
	$(MAKE) VLEN=512  DLEN=128 $(subst _,,$(APPLICATION_DIRS))
run_v4d4 :
	$(MAKE) VLEN=256  DLEN=256 $(subst _,,$(APPLICATION_DIRS))
run_v8d4 :
	$(MAKE) VLEN=512  DLEN=256 $(subst _,,$(APPLICATION_DIRS))
run_v16d4:
	$(MAKE) VLEN=1024 DLEN=256 $(subst _,,$(APPLICATION_DIRS))

run_original: run_axpy_origin run_streamcluster_origin \
				run_blackscholes_origin run_canneal_origin run_swaptions_origin \
				run_particlefilter_origin run_pathfinder_origin run_jacobi-2d_origin
run_axpy_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _axpy
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _axpy_origin
run_streamcluster_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _streamcluster
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _streamcluster_origin
run_blackscholes_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _blackscholes
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _blackscholes_origin
run_canneal_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _canneal
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _canneal_origin
run_swaptions_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _swaptions
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _swaptions_origin
run_particlefilter_origin: 
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _particlefilter
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _particlefilter_origin
run_pathfinder_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _pathfinder
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _pathfinder_origin
run_jacobi-2d_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _jacobi-2d
	$(MAKE) VLEN=512 DLEN=128 runsniper-ooo-v -C _jacobi-2d_origin

power: $(addprefix power,$(APPLICATION_DIRS))


.PHONY: $(addsuffix _sniper, $(APPLICATION_DIRS))
.PHONY: $(addsuffix _spike, $(APPLICATION_DIRS))
.PHONY: $(subst _,scalar_,$(APPLICATION_DIRS))

only_spike:
	$(MAKE) $(addsuffix _spike, $(APPLICATION_DIRS))

$(addsuffix _spike, $(APPLICATION_DIRS)):
	$(MAKE) -C $(subst _spike,, $@) runspike-v

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
	$(MAKE) -C _$@ VLEN=$(VLEN) DLEN=$(DLEN) runspike-v
	$(MAKE) -C _$@ VLEN=$(VLEN) DLEN=$(DLEN) runsniper-v
	$(MAKE) -C _$@ VLEN=$(VLEN) DLEN=$(DLEN) runmcpat

$(subst _,scalar_,$(APPLICATION_DIRS)):
	$(MAKE) -C _$(subst scalar_,,$@) runspike-s
	$(MAKE) -C _$(subst scalar_,,$@) runsniper-s
#	$(MAKE) -C _$@ runmcpat-s

$(addprefix power,$(APPLICATION_DIRS)):
	$(MAKE) -C $(subst power,,$@) VLEN=$(VLEN) DLEN=$(DLEN) runmcpat

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

# power:
# 	$(MAKE) power_all power_filtered VLEN=$(VLEN)

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
