BASE_DIR := $(shell pwd)

APPLICATION_DIRS := _blackscholes _swaptions _streamcluster _canneal _particlefilter _pathfinder _jacobi-2d _axpy

VLEN = 256

# all: blackscholes swaptions streamcluster canneal particlefilter pathfinder jacobi-2d matmul axpy
all: swaptions streamcluster canneal particlefilter pathfinder jacobi-2d axpy
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
	$(MAKE) -C $(subst _sniper,, $@) runsniper-ooo-v runsniper-io-v runsniper-vio

runsniper:
	$(MAKE) runsniper-ooo-v runsniper-io-v runsniper-vio runsniper-ooo-s runsniper-io-s


blackscholes:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper

swaptions:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper

streamcluster:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper

canneal:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper

particlefilter:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper

pathfinder:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper

jacobi-2d:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper

matmul:
	$(MAKE) -C _$@ VLEN=$(VLEN) runspike-v runspike-s
	$(MAKE) -C _$@ VLEN=$(VLEN) runsniper


axpy:
	$(MAKE) -C _$@ runspike-v
	$(MAKE) -C _$@ runsniper

stats:
	for dir in $(APPLICATION_DIRS); do \
		echo -n $$dir " "; paste $${dir}/ooo.s/*.ooo.s $${dir}/ino.s/*.ino.s $${dir}/ino.v/*.io $${dir}/vio.v/*.vio $${dir}/ooo.v/*.ooo ; \
	done
clean:
	$(MAKE) clean -C _blackscholes
	$(MAKE) clean -C _swaptions
	$(MAKE) clean -C _streamcluster
	$(MAKE) clean -C _canneal
	$(MAKE) clean -C _particlefilter
	$(MAKE) clean -C _pathfinder
	$(MAKE) clean -C _jacobi-2d
	$(MAKE) clean -C _axpy
