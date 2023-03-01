	.section	.sdata,"aw",@progbits
	.p2align	2                               # -- Begin function _Z11__log_2xf32u17__rvv_float32m1_tm
.LCPI5_0:
	.word	0x3f3504f3                      # float 0.707106769
#define SQRTHF_CONST (0x3f3504f3)
.LCPI5_1:
	.word	0x3d9021bb                      # float 0.0703768358
#define LOG_P0_CONST (0x3d9021bb)

.LCPI5_2:
	.word	0xbdebd1b8                      # float -0.115146101
#define LOG_P1_CONST (0xbdebd1b8)

.LCPI5_3:
	.word	0x3def251a                      # float 0.116769984
#define LOG_P2_CONST (0x3def251a)

.LCPI5_4:
	.word	0xbdfe5d4f                      # float -0.12420141
#define LOG_P3_CONST (0xbdfe5d4f)

.LCPI5_5:
	.word	0x3e11e9bf                      # float 0.142493233
#define LOG_P4_CONST (0x3e11e9bf)

.LCPI5_6:
	.word	0xbe2aae50                      # float -0.166680574
#define LOG_P5_CONST (0xbe2aae50)

.LCPI5_7:
	.word	0x3e4cceac                      # float 0.200007141
#define LOG_P6_CONST (0x3e4cceac)

.LCPI5_8:
	.word	0xbe7ffffc                      # float -0.24999994
#define LOG_P7_CONST (0xbe7ffffc)

.LCPI5_9:
	.word	0x3eaaaaaa                      # float 0.333333313
#define LOG_P8_CONST (0x3eaaaaaa)

.LCPI5_10:
	.word	0x3f800000                      # float 1
#define ONE_CONST (0x3f800000)

.LCPI5_11:
	.word	0x3f000000                      # float 0.5
#define ZERO_5_CONST (0x3f800000)

.LCPI5_12:
	.word	0xb95e8083                      # float -2.12194442E-4
#define CEPHES_LOG_Q1_CONST (0xb95e8083)

.LCPI5_13:
	.word	0x3f318000                      # float 0.693359375
#define CEPHES_LOG_Q2_CONST (0x3f318000)

#define VREG_SQRTHF v11
#define VREG_P0     v10
#define VREG_P1     v12
#define VREG_P2     v13
#define VREG_P3     v14
#define VREG_P4     v15
#define VREG_P5     v16
#define VREG_P6     v17
#define VREG_P7     v18
#define VREG_P8     v19
#define VREG_Y      v10

#define VREG_SET(vreg,const,tmp) li tmp, const; vmv.v.x vreg, tmp


    .text
	.globl	__log_vector_2xf32
	.p2align	1
	.type	_Z11__log_2xf32u17__rvv_float32m1_tm,@function
__log_vector_2xf32:   # @_Z11__log_2xf32u17__rvv_float32m1_tm
# %bb.0:
	vsetvli	    zero, a0, e32, m1, ta, mu


    lui	        a0, 2048
	vmv.v.x	    v20, a0

	lui	        a0, 526336
	addiw	    a0, a0, -1
	vmv.v.x	    v21, a0

	li	        a0, 127
	vmv.v.x	    v22, a0




    vmv.v.i	    v27, 0
	vmfle.vv	v9, v8, v27
	vfmax.vv	v8, v8, v20

	li	        a0, 23
	vmv.v.x	    v20, a0

	vsrl.vv	    v20, v8, v20
	vand.vv	    v8, v8, v21

    li          a1, ZERO_5_CONST
    vmv.v.x     v24, a1

	vor.vv	    v8, v8, v24
	vsub.vv	    v20, v20, v22
	vfcvt.f.x.v	v20, v20

    li          a1, SQRTHF_CONST
	vmv.v.x 	VREG_SQRTHF, a1
	vmflt.vv	v0, v8, VREG_SQRTHF

    li          a1, ONE_CONST
    vmv.v.x     v23, a1
    vfadd.vv	v11, v20, v23
	vmerge.vvm	v20, v27, v8, v0
	vfsub.vv	v8, v8, v23
	vmerge.vvm	v21, v27, v23, v0
	vfsub.vv	v11, v11, v21
	vfadd.vv	v8, v8, v20
	vfmul.vv	v20, v8, v8

    li          a1, LOG_P0_CONST
	vmv.v.x 	VREG_P0, a1

    VREG_SET(VREG_P1, LOG_P1_CONST, a1)
	vfmadd.vv	VREG_Y, v8, VREG_P1

    VREG_SET(VREG_P2, LOG_P2_CONST, a1)
	vfmadd.vv	VREG_Y, v8, VREG_P2

    VREG_SET(VREG_P3, LOG_P3_CONST, a1)
	vfmadd.vv	VREG_Y, v8, VREG_P3

    VREG_SET(VREG_P4, LOG_P4_CONST, a1)
	vfmadd.vv	VREG_Y, v8, VREG_P4

    VREG_SET(VREG_P5, LOG_P5_CONST, a1)
	vfmadd.vv	VREG_Y, v8, VREG_P5

    VREG_SET(VREG_P6, LOG_P6_CONST, a1)
    vfmadd.vv	VREG_Y, v8, VREG_P6

    VREG_SET(VREG_P7, LOG_P7_CONST, a1)
    vfmadd.vv	VREG_Y, v8, VREG_P7

    VREG_SET(VREG_P8, LOG_P8_CONST, a1)
    vfmadd.vv	VREG_Y, v8, VREG_P8

	vfmul.vv	VREG_Y, VREG_Y, v20

    VREG_SET(v25, CEPHES_LOG_Q1_CONST, a1)
	vfmacc.vv	VREG_Y, v11, v25

    vfmul.vv	v12, v20, v24
	vfsub.vv	VREG_Y, VREG_Y, v12

    VREG_SET(v26, CEPHES_LOG_Q2_CONST, a1)
	vfmul.vv	v11, v11, v26

	vfadd.vv	v8, v8, VREG_Y
	vfadd.vv	v8, v8, v11
	vmv.v.i	    v10, -1
	vmv.v.v	    v0, v9
	vmerge.vvm	v8, v8, v10, v0
	ret
