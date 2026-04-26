#makefile

rvv_target    = bin/rvv-test_vlen$(VLEN)
serial_target = bin/serial-test_vlen$(VLEN)

serial:
	for entry in src/*.cpp ; do \
		${RISCV}/bin/clang++ -march=rv64g -O2 -fno-vectorize -c -o  $$entry.o  $$entry ; \
	done
	${RISCV}/bin/clang++ -march=rv64g -O2 -fno-vectorize -o bin/swaptions_serial.exe src/*.cpp.o -lm;	\
	${RISCV}/bin/llvm-objdump  --mattr=+m,+f,+d,+a,+c -ds  bin/swaptions_serial.exe > bin/swaptions_serial.dump;	\
	rm src/*.o; \

vector:
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/CumNormalInv.o src/CumNormalInv.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/MaxFunction.o src/MaxFunction.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/RanUnif.o src/RanUnif.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/nr_routines.o src/nr_routines.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/icdf.o src/icdf.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/HJM_SimPath_Forward_Blocking.o src/HJM_SimPath_Forward_Blocking.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/HJM.o src/HJM.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/HJM_Swaption_Blocking.o src/HJM_Swaption_Blocking.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -c -o src/HJM_Securities.o src/HJM_Securities.cpp;	\
	${RISCV}/bin/clang++ -march=rv64gcv -DUSE_RISCV_VECTOR -O2 -fno-vectorize -o bin/swaptions_vector.exe src/*.o -lm;	\
	${RISCV}/bin/llvm-objdump  --mattr=+m,+f,+d,+a,+c,+v -ds  bin/swaptions_vector.exe > bin/swaptions_vector.dump ; \
	rm src/*.o ;

vector: $(rvv_target)
$(rvv_target):
	mkdir -p bin
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/CumNormalInv.assembly.v$(VLEN).o src/CumNormalInv.assembly.S
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/CumNormalInv.v$(VLEN).o src/CumNormalInv.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/MaxFunction.v$(VLEN).o src/MaxFunction.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/RanUnif.v$(VLEN).o src/RanUnif.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/nr_routines.v$(VLEN).o src/nr_routines.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/icdf.v$(VLEN).o src/icdf.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/HJM_SimPath_Forward_Blocking.v$(VLEN).o src/HJM_SimPath_Forward_Blocking.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/HJM.v$(VLEN).o src/HJM.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/HJM_Swaption_Blocking.v$(VLEN).o src/HJM_Swaption_Blocking.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS) -c -o src/HJM_Securities.v$(VLEN).o src/HJM_Securities.cpp
	riscv64-unknown-elf-g++ $(RVV_COMPILE_OPTIONS)    -o $@  src/*.v$(VLEN).o -lm
	rm src/*.v$(VLEN).o
	riscv64-unknown-elf-objdump -D $@ > ./bin/dump_vector
