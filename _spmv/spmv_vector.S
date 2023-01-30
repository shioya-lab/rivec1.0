	.globl	spmv_vector
	.type	spmv_vector, @function
	// void spmv_vector(
	// a0 : int r,
	// a1 : const double* val,
	// a2 : const uint64_t* idx,
	// a3 : const double* x,
	// a4 : const uint64_t* ptr, double* y)
spmv_vector:
	vsetvli	t5,zero,e64,m4,ta,mu
	ble	a0,zero,.L26
	slli	a0,a0,3
	add	t6,a4,a0
	vmv.v.i	v20,0
.whole_loop:
	ld	a0,0(a4)
	ld	a6,8(a4)
	vmv4r.v	v28,v20
	slli	t1,a0,3
	subw	a6,a6,a0
	add	t3,a2,t1
	add	t1,a1,t1
	ble	a6,zero,.final_reduc
.calc_loop:
	vsetvli	a0,a6,e64,m4,ta,mu
	slli	t4,a0,3
	subw	a6,a6,a0
	vle64.v	v12,(t1)
	vle64.v	v24,(t3)
	add	t1,t1,t4
	vsll.vi	v24,v24,3
	add	t3,t3,t4
	vluxei64.v	v8,(a3),v24
	vsetvli	zero,a0,e64,m4,tu,mu
	vfmacc.vv	v28,v8,v12
	bgt	a6,zero,.calc_loop
.final_reduc:
	vsetvli	zero,t5,e64,m1,ta,mu
	vmv.v.i	v24,0
	vsetvli	a0,zero,e64,m4,tu,mu
	addi	a4,a4,8
	vfredusum.vs	v16,v28,v24
	vsetivli	zero,0,e64,m1,ta,mu
	vfmv.f.s	fa5,v16
	fsd	fa5,0(a5)
	addi	a5,a5,8
	bne	t6,a4,.whole_loop
.L26:
	ret
