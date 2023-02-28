	.section	.sdata,"aw",@progbits
	.p2align	2                               # -- Begin function _Z11__log_2xf32u17__rvv_float32m1_tm
.LCPI5_0:
	.word	0x3f3504f3                      # float 0.707106769
.LCPI5_1:
	.word	0x3d9021bb                      # float 0.0703768358
.LCPI5_2:
	.word	0xbdebd1b8                      # float -0.115146101
.LCPI5_3:
	.word	0x3def251a                      # float 0.116769984
.LCPI5_4:
	.word	0xbdfe5d4f                      # float -0.12420141
.LCPI5_5:
	.word	0x3e11e9bf                      # float 0.142493233
.LCPI5_6:
	.word	0xbe2aae50                      # float -0.166680574
.LCPI5_7:
	.word	0x3e4cceac                      # float 0.200007141
.LCPI5_8:
	.word	0xbe7ffffc                      # float -0.24999994
.LCPI5_9:
	.word	0x3eaaaaaa                      # float 0.333333313
.LCPI5_10:
	.word	0x3f800000                      # float 1
.LCPI5_11:
	.word	0x3f000000                      # float 0.5
.LCPI5_12:
	.word	0xb95e8083                      # float -2.12194442E-4
.LCPI5_13:
	.word	0x3f318000                      # float 0.693359375
	.text
	.globl	__log_vector_2xf32
	.p2align	1
	.type	_Z11__log_2xf32u17__rvv_float32m1_tm,@function
__log_vector_2xf32:   # @_Z11__log_2xf32u17__rvv_float32m1_tm
# %bb.0:
	lui	    a1, %hi(.LCPI5_0)
	addi	a1, a1, %lo(.LCPI5_0)
	vsetvli	zero, a0, e32, m1, ta, mu
	vlse32.v	v11, (a1), zero
	lui	    a0, %hi(.LCPI5_1)
	addi	a0, a0, %lo(.LCPI5_1)
	vlse32.v	v10, (a0), zero
	lui	    a0, %hi(.LCPI5_2)
	addi	a0, a0, %lo(.LCPI5_2)
	vlse32.v	v12, (a0), zero
	lui	    a0, %hi(.LCPI5_3)
	addi	a0, a0, %lo(.LCPI5_3)
	vlse32.v	v13, (a0), zero
	lui	    a0, %hi(.LCPI5_4)
	addi	a0, a0, %lo(.LCPI5_4)
	vlse32.v	v14, (a0), zero
	lui	    a0, %hi(.LCPI5_5)
	addi	a0, a0, %lo(.LCPI5_5)
	vlse32.v	v15, (a0), zero
	lui	    a0, %hi(.LCPI5_6)
	addi	a0, a0, %lo(.LCPI5_6)
	vlse32.v	v16, (a0), zero
	lui	    a0, %hi(.LCPI5_7)
	addi	a0, a0, %lo(.LCPI5_7)
	vlse32.v	v17, (a0), zero
	lui	    a0, %hi(.LCPI5_8)
	addi	a0, a0, %lo(.LCPI5_8)
	vlse32.v	v18, (a0), zero
	lui	    a0, %hi(.LCPI5_9)
	addi	a0, a0, %lo(.LCPI5_9)
	vlse32.v	v19, (a0), zero
	lui	    a0, 2048
	vmv.v.x	v20, a0
	lui	    a0, 526336
	addiw	a0, a0, -1
	vmv.v.x	v21, a0
	li	    a0, 127
	vmv.v.x	v22, a0
	lui	    a0, %hi(.LCPI5_10)
	addi	a0, a0, %lo(.LCPI5_10)
	vlse32.v	v23, (a0), zero
	lui	    a0, %hi(.LCPI5_11)
	addi	a0, a0, %lo(.LCPI5_11)
	vlse32.v	v24, (a0), zero
	lui	    a0, %hi(.LCPI5_12)
	addi	a0, a0, %lo(.LCPI5_12)
	vlse32.v	v25, (a0), zero
	lui	    a0, %hi(.LCPI5_13)
	addi	a0, a0, %lo(.LCPI5_13)
	vlse32.v	v26, (a0), zero
	vmv.v.i	v27, 0
	vmfle.vv	v9, v8, v27
	vfmax.vv	v8, v8, v20
	li	a0, 23
	vmv.v.x	v20, a0
	vsrl.vv	v20, v8, v20
	vand.vv	v8, v8, v21
	vor.vv	v8, v8, v24
	vsub.vv	v20, v20, v22
	vfcvt.f.x.v	v20, v20
	vmflt.vv	v0, v8, v11
	vfadd.vv	v11, v20, v23
	vmerge.vvm	v20, v27, v8, v0
	vfsub.vv	v8, v8, v23
	vmerge.vvm	v21, v27, v23, v0
	vfsub.vv	v11, v11, v21
	vfadd.vv	v8, v8, v20
	vfmul.vv	v20, v8, v8
	vsetvli	zero, zero, e32, m1, tu, mu
	vfmadd.vv	v10, v8, v12
	vfmadd.vv	v10, v8, v13
	vfmadd.vv	v10, v8, v14
	vfmadd.vv	v10, v8, v15
	vfmadd.vv	v10, v8, v16
	vfmadd.vv	v10, v8, v17
	vfmadd.vv	v10, v8, v18
	vfmadd.vv	v10, v8, v19
	vsetvli	zero, zero, e32, m1, ta, mu
	vfmul.vv	v10, v10, v20
	vsetvli	zero, zero, e32, m1, tu, mu
	vfmacc.vv	v10, v11, v25
	vsetvli	zero, zero, e32, m1, ta, mu
	vfmul.vv	v12, v20, v24
	vfsub.vv	v10, v10, v12
	vfmul.vv	v11, v11, v26
	vfadd.vv	v8, v8, v10
	vfadd.vv	v8, v8, v11
	vmv.v.i	v10, -1
	vmv.v.v	v0, v9
	vmerge.vvm	v8, v8, v10, v0
	ret
