BASE_DIR := $(shell pwd)

APPLICATION_DIRS := _blackscholes _swaptions _streamcluster _canneal _particlefilter _pathfinder _jacobi-2d _matmul _axpy

# all: blackscholes swaptions streamcluster canneal particlefilter pathfinder jacobi-2d matmul axpy
all: swaptions streamcluster canneal particlefilter pathfinder jacobi-2d axpy

blackscholes:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v runsniper-ooo-s runsniper-io-s

swaptions:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v runsniper-ooo-s runsniper-io-s

streamcluster:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v runsniper-ooo-s runsniper-io-s

canneal:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v runsniper-ooo-s runsniper-io-s

particlefilter:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v runsniper-ooo-s runsniper-io-s

pathfinder:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v runsniper-ooo-s runsniper-io-s

jacobi-2d:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v runsniper-ooo-s runsniper-io-s

matmul:
	$(MAKE) -C _$@ runspike-v runspike-s
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v runsniper-ooo-s runsniper-io-s

axpy:
	$(MAKE) -C _$@ runspike-v
	$(MAKE) -C _$@ runsniper-ooo-v runsniper-io-v

clean:
	$(MAKE) clean -C _blackscholes
	$(MAKE) clean -C _swaptions
	$(MAKE) clean -C _streamcluster
	$(MAKE) clean -C _canneal
	$(MAKE) clean -C _particlefilter
	$(MAKE) clean -C _pathfinder
	$(MAKE) clean -C _jacobi-2d
	$(MAKE) clean -C _axpy
