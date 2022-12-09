BASE_DIR := $(shell pwd)

APPLICATION_DIRS := _blackscholes _swaptions _streamcluster _canneal _particlefilter _pathfinder _jacobi-2d _matmul _axpy

# all: blackscholes swaptions streamcluster canneal particlefilter pathfinder jacobi-2d matmul axpy
all: swaptions streamcluster canneal particlefilter pathfinder jacobi-2d axpy

.PHONY: $(addsuffix _sniper, $(APPLICATION_DIRS))

only_sniper:
	$(MAKE) $(addsuffix _sniper, $(APPLICATION_DIRS)) runsniper

$(addsuffix _sniper, $(APPLICATION_DIRS)):
	$(MAKE) -C $(subst _sniper,, $@) runsniper-ooo-v runsniper-io-v runsniper-vio

runsniper:
	$(MAKE) runsniper-ooo-v runsniper-io-v runsniper-vio runsniper-ooo-s runsniper-io-s


blackscholes:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper

swaptions:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper

streamcluster:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper

canneal:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper

particlefilter:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper

pathfinder:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper

jacobi-2d:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper

matmul:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper


axpy:
	$(MAKE) -C _$@ runspike-v
	$(MAKE) -C _$@ runsniper

clean:
	$(MAKE) clean -C _blackscholes
	$(MAKE) clean -C _swaptions
	$(MAKE) clean -C _streamcluster
	$(MAKE) clean -C _canneal
	$(MAKE) clean -C _particlefilter
	$(MAKE) clean -C _pathfinder
	$(MAKE) clean -C _jacobi-2d
	$(MAKE) clean -C _axpy
