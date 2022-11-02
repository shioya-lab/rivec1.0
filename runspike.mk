runspike-v : $(rvv_target)
	$(SPIKE) --isa=rv64gcv -l --log-commits $(PK) $^ $(SPIKE_OPTS) 2> spike-v.log

runspike-s : $(serial_target)
	$(SPIKE) --isa=rv64gc -l --log-commits $(PK) $^ $(SPIKE_OPTS) 2> spike-s.log
