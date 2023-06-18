BASE_DIR := $(shell pwd)

APPLICATION_DIRS := _axpy _streamcluster _blackscholes _canneal _swaptions _particlefilter _pathfinder _jacobi-2d _spmv _fftw3

VLEN ?= 256
DLEN ?= $(VLEN)

all: build_tests
	$(MAKE) run_scalar runspike_v2 runspike_v4 runspike_v8 runspike_v16 runspike_v32
	$(MAKE) run_v2d2 run_v4d2 run_v8d2 run_v16d2 run_v4d4 run_v8d4 run_v16d4 run_v32d4

build_tests:
	$(MAKE) $(addsuffix _build,$(APPLICATION_DIRS))
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
runspike_v32:
	$(MAKE) VLEN=1024 $(addsuffix _spike,$(APPLICATION_DIRS))

run_v2d2 : 
	$(MAKE) VLEN=128  DLEN=128 $(subst _,,$(APPLICATION_DIRS))
run_v4d2 :
	$(MAKE) VLEN=256  DLEN=128 $(subst _,,$(APPLICATION_DIRS))
run_v8d2 :
	$(MAKE) VLEN=512  DLEN=128 $(subst _,,$(APPLICATION_DIRS))
run_v16d2 :
	$(MAKE) VLEN=1024 DLEN=128 $(subst _,,$(APPLICATION_DIRS))
run_v4d4 :
	$(MAKE) VLEN=256  DLEN=256 $(subst _,,$(APPLICATION_DIRS))
run_v8d4 :
	$(MAKE) VLEN=512  DLEN=256 $(subst _,,$(APPLICATION_DIRS))
run_v16d4:
	$(MAKE) VLEN=1024 DLEN=256 $(subst _,,$(APPLICATION_DIRS))
run_v32d4:
	$(MAKE) VLEN=2048 DLEN=256 $(subst _,,$(APPLICATION_DIRS))

run_original: run_axpy_origin run_streamcluster_origin \
				run_blackscholes_origin run_canneal_origin run_swaptions_origin \
				run_particlefilter_origin run_pathfinder_origin run_jacobi-2d_origin
run_axpy_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _axpy
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _axpy_origin
run_streamcluster_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _streamcluster
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _streamcluster_origin
run_blackscholes_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _blackscholes
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _blackscholes_origin
run_canneal_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _canneal
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _canneal_origin
run_swaptions_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _swaptions
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _swaptions_origin
run_particlefilter_origin: 
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _particlefilter
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _particlefilter_origin
run_pathfinder_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _pathfinder
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _pathfinder_origin
run_jacobi-2d_origin:
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _jacobi-2d
	$(MAKE) VLEN=512 DLEN=128 runsniper-vio-v -C _jacobi-2d_origin

power: $(addprefix power,$(APPLICATION_DIRS))


.PHONY: $(addsuffix _sniper, $(APPLICATION_DIRS))
.PHONY: $(addsuffix _spike, $(APPLICATION_DIRS))
.PHONY: $(subst _,scalar_,$(APPLICATION_DIRS))

only_spike:
	$(MAKE) $(addsuffix _spike, $(APPLICATION_DIRS))

$(addsuffix _build, $(APPLICATION_DIRS)):
	$(MAKE) -C $(subst _build,, $@) vector scalar

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

clean:
	for dir in $(APPLICATION_DIRS); do \
		$(MAKE) clean -C $${dir}; \
	done
