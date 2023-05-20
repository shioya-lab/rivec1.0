	.section	.sdata,"aw",@progbits
	.p2align	2                               # -- Begin function BlkSchlsEqEuroNoDiv_vector_asm
.LCPI7_0:
	.word	0x3f3504f3                      # float 0.707106769
.LCPI7_1:
	.word	0x3d9021bb                      # float 0.0703768358
.LCPI7_2:
	.word	0xbdebd1b8                      # float -0.115146101
.LCPI7_3:
	.word	0x3def251a                      # float 0.116769984
.LCPI7_4:
	.word	0xbdfe5d4f                      # float -0.12420141
.LCPI7_5:
	.word	0x3e11e9bf                      # float 0.142493233
.LCPI7_6:
	.word	0xbe2aae50                      # float -0.166680574
.LCPI7_7:
	.word	0x3e4cceac                      # float 0.200007141
.LCPI7_8:
	.word	0xbe7ffffc                      # float -0.24999994
.LCPI7_9:
	.word	0x3eaaaaaa                      # float 0.333333313
.LCPI7_10:
	.word	0x3f800000                      # float 1
.LCPI7_11:
	.word	0x3f000000                      # float 0.5
.LCPI7_12:
	.word	0xb95e8083                      # float -2.12194442E-4
.LCPI7_13:
	.word	0x3f318000                      # float 0.693359375
.LCPI7_14:
	.word	0x42b0c0a5                      # float 88.3762589
.LCPI7_15:
	.word	0xc2b0c0a5                      # float -88.3762589
.LCPI7_16:
	.word	0x3fb8aa3b                      # float 1.44269502
.LCPI7_17:
	.word	0x39506967                      # float 1.98756912E-4
.LCPI7_18:
	.word	0x3ab743ce                      # float 0.00139819994
.LCPI7_19:
	.word	0x3c088908                      # float 0.00833345205
.LCPI7_20:
	.word	0x3d2aa9c1                      # float 0.0416657962
.LCPI7_21:
	.word	0x3e2aaaaa                      # float 0.166666657
.LCPI7_22:
	.word	0xbf000000                      # float -0.5
.LCPI7_23:
	.word	0x3ecc422a                      # float 0.398942292
.LCPI7_24:
	.word	0x3e6d3389                      # float 0.231641904
.LCPI7_25:
	.word	0x3ea385fa                      # float 0.319381535
.LCPI7_26:
	.word	0xbeb68f87                      # float -0.356563777
.LCPI7_27:
	.word	0x3fe40778                      # float 1.78147793
.LCPI7_28:
	.word	0xbfe91eea                      # float -1.82125592
.LCPI7_29:
	.word	0x3faa466f                      # float 1.33027446


#define CONST_LCPI7_0    (0x3f3504f3)                      // float 0.707106769
#define CONST_LCPI7_1	(0x3d9021bb)                      // float 0.0703768358
#define CONST_LCPI7_2	(0xbdebd1b8)                      // float -0.115146101
#define CONST_LCPI7_3	(0x3def251a)                      // float 0.116769984
#define CONST_LCPI7_4	(0xbdfe5d4f)                      // float -0.12420141
#define CONST_LCPI7_5	(0x3e11e9bf)                      // float 0.142493233
#define CONST_LCPI7_6	(0xbe2aae50)                      // float -0.166680574
#define CONST_LCPI7_7	(0x3e4cceac)                      // float 0.200007141
#define CONST_LCPI7_8	(0xbe7ffffc)                      // float -0.24999994
#define CONST_LCPI7_9	(0x3eaaaaaa)                      // float 0.333333313
#define CONST_LCPI7_10	(0x3f800000)                      // float 1
#define CONST_LCPI7_11	(0x3f000000)                      // float 0.5
#define CONST_LCPI7_12	(0xb95e8083)                      // float -2.12194442E-4
#define CONST_LCPI7_13	(0x3f318000)                      // float 0.693359375
#define CONST_LCPI7_14	(0x42b0c0a5)                      // float 88.3762589
#define CONST_LCPI7_15	(0xc2b0c0a5)                      // float -88.3762589
#define CONST_LCPI7_16	(0x3fb8aa3b)                      // float 1.44269502
#define CONST_LCPI7_17	(0x39506967)                      // float 1.98756912E-4
#define CONST_LCPI7_18	(0x3ab743ce)                      // float 0.00139819994
#define CONST_LCPI7_19	(0x3c088908)                      // float 0.00833345205
#define CONST_LCPI7_20	(0x3d2aa9c1)                      // float 0.0416657962
#define CONST_LCPI7_21	(0x3e2aaaaa)                      // float 0.166666657
#define CONST_LCPI7_22	(0xbf000000)                      // float -0.5
#define CONST_LCPI7_23	(0x3ecc422a)                      // float 0.398942292
#define CONST_LCPI7_24	(0x3e6d3389)                      // float 0.231641904
#define CONST_LCPI7_25	(0x3ea385fa)                      // float 0.319381535
#define CONST_LCPI7_26	(0xbeb68f87)                      // float -0.356563777
#define CONST_LCPI7_27	(0x3fe40778)                      // float 1.78147793
#define CONST_LCPI7_28	(0xbfe91eea)                      // float -1.82125592
#define CONST_LCPI7_29	(0x3faa466f)                      // float 1.33027446


#define VREG_SET(vreg,const,tmp) li tmp, const; vmv.v.x vreg, tmp

    .text
	.globl	BlkSchlsEqEuroNoDiv_vector_asm
	.p2align	1
	.type	BlkSchlsEqEuroNoDiv_vector_asm,@function
BlkSchlsEqEuroNoDiv_vector_asm: # @BlkSchlsEqEuroNoDiv_vector_asm
# %bb.0:
	addi	sp, sp, -16
	csrr	a1, vlenb
	slli	a1, a1, 1
	sub	    sp, sp, a1
	csrr	a1, vlenb
	slli	a1, a1, 1
	add	    a1, a1, sp
	ld	    a1, 16(a1)
	vsetvli	zero, a1, e32, m1, ta, mu
	vle32.v	v10, (a3)
	vle32.v	v8, (a2)
	addi	a1, sp, 16
	vs1r.v	v8, (a1)                        # Unknown-size Folded Spill
	vfdiv.vv	v15, v8, v10

    lui	        a1, 2048
	vmv.v.x	    v28, a1
	lui	        a1, 526336
	addiw	    a1, a1, -1
	vmv.v.x	    v29, a1
	li	        a1, 127
	vmv.v.x	    v13, a1

    vmv.v.i	    v12, 0
	vmfle.vv	v8, v15, v12
	vfmax.vv	v28, v15, v28
	li	        a1, 23
	vmv.v.x		v15, a1
	vsrl.vv		v30, v28, v15
	vand.vv		v28, v28, v29
    VREG_SET(v14, CONST_LCPI7_11, a1)
	vor.vv		v28, v28, v14
	vsub.vv		v29, v30, v13
	vfcvt.f.x.v	v29, v29

    VREG_SET(v19, CONST_LCPI7_0, a1)
	vmflt.vv	v0, v28, v19
    VREG_SET(v11, CONST_LCPI7_10, a1)
	vfadd.vv	v19, v29, v11
	vmerge.vvm	v29, v12, v28, v0
	vfsub.vv	v28, v28, v11
	vmerge.vvm	v30, v12, v11, v0
	vfsub.vv	v19, v19, v30
	vfadd.vv	v28, v28, v29
	vfmul.vv	v29, v28, v28
    VREG_SET(v18, CONST_LCPI7_1, a1)

    VREG_SET(v20, CONST_LCPI7_2, a1)
	vfmadd.vv	v18, v28, v20

    VREG_SET(v20, CONST_LCPI7_3, a1)
	vfmadd.vv	v18, v28, v20

    VREG_SET(v20, CONST_LCPI7_4, a1)
	vfmadd.vv	v18, v28, v20

    VREG_SET(v20, CONST_LCPI7_5, a1)
	vfmadd.vv	v18, v28, v20

    VREG_SET(v20, CONST_LCPI7_6, a1)
	vfmadd.vv	v18, v28, v20

    VREG_SET(v20, CONST_LCPI7_7, a1)
	vfmadd.vv	v18, v28, v20

    VREG_SET(v20, CONST_LCPI7_8, a1)
    vfmadd.vv	v18, v28, v20

    VREG_SET(v20, CONST_LCPI7_9, a1)
	vfmadd.vv	v18, v28, v20

	vfmul.vv	v18, v18, v29
    VREG_SET(v16, CONST_LCPI7_12, a1)
	vfmacc.vv	v18, v19, v16
	vfmul.vv	v20, v29, v14
	vfsub.vv	v18, v18, v20
    VREG_SET(v17, CONST_LCPI7_13, a1)
	vfmul.vv	v19, v19, v17
	vfadd.vv	v18, v28, v18
	vle32.v	    v29, (a4)
	vle32.v	    v27, (a5)
	vle32.v	    v28, (a6)
	vfadd.vv	v18, v18, v19
	vmv.v.i	    v19, -1
	vmv.v.v	    v0, v8
	vmerge.vvm	v30, v18, v19, v0
	vfsqrt.v	v8, v28
	vfmul.vv	v18, v29, v28
	vfneg.v	    v19, v18

    VREG_SET(v24, CONST_LCPI7_14, a1)
    vfmin.vv	v19, v19, v24

    VREG_SET(v25, CONST_LCPI7_15, a1)
	vfmax.vv	v19, v19, v25

	vmv.v.v	v31, v14

    VREG_SET(v26, CONST_LCPI7_16, a1)
	vfmacc.vv	v31, v19, v26

	vfcvt.x.f.v	v0, v31
	vfcvt.f.x.v	v1, v0
	vmflt.vv	v0, v31, v1
	vmerge.vvm	v31, v12, v11, v0
	vfsub.vv	v31, v1, v31
	vfmul.vv	v0, v31, v17
	vfmul.vv	v1, v31, v16
	vfsub.vv	v19, v19, v0
	vfsub.vv	v19, v19, v1
	vfmul.vv	v0, v19, v19

    VREG_SET(v18, CONST_LCPI7_17, a1)
	vmv.v.v	v1, v18

    VREG_SET(v20, CONST_LCPI7_18, a1)
	vfmadd.vv	v1, v19, v20

    VREG_SET(v21, CONST_LCPI7_19, a1)
	vfmadd.vv	v1, v19, v21

    VREG_SET(v22, CONST_LCPI7_20, a1)
	vfmadd.vv	v1, v19, v22

    VREG_SET(v23, CONST_LCPI7_21, a1)
	vfmadd.vv	v1, v19, v23

    vfmadd.vv	v1, v19, v14
	vfmadd.vv	v1, v0, v19
	vfadd.vv	v19, v1, v11
	vfcvt.x.f.v	v31, v31
	vadd.vv	    v31, v31, v13
	vsll.vv	    v31, v31, v15
	vfmul.vv	v19, v19, v31
	vfmul.vv	v31, v27, v27
	vfmul.vv	v31, v31, v14
	vfadd.vv	v29, v29, v31
	vfmadd.vv	v29, v28, v30
	vfmul.vv	v8, v27, v8
	vfdiv.vv	v29, v29, v8
	vfsub.vv	v27, v29, v8

    VREG_SET(v28, CONST_LCPI7_22, a1)

    vmflt.vv	v9, v29, v12
	vfabs.v	    v31, v29
	vfmul.vv	v29, v31, v31
	vfmul.vv	v29, v29, v28
	vfmin.vv	v29, v29, v24
	vfmax.vv	v29, v29, v25
	vmv.v.v	v30, v14
	vfmacc.vv	v30, v29, v26
	vfcvt.x.f.v	v0, v30
	vfcvt.f.x.v	v1, v0
	vmflt.vv	v0, v30, v1
	vmerge.vvm	v30, v12, v11, v0
	vfsub.vv	v30, v1, v30
	vfmul.vv	v0, v30, v17
	vfmul.vv	v1, v30, v16
	vfsub.vv	v29, v29, v0
	vfsub.vv	v29, v29, v1
	vfmul.vv	v0, v29, v29
	vmv.v.v	v1, v18
	vfmadd.vv	v1, v29, v20
	vfmadd.vv	v1, v29, v21
	vfmadd.vv	v1, v29, v22
	vfmadd.vv	v1, v29, v23
	vfmadd.vv	v1, v29, v14
	vfmadd.vv	v1, v0, v29
	vfadd.vv	v0, v1, v11
	vfcvt.x.f.v	v29, v30
	vadd.vv	v1, v29, v13

    vsll.vv	    v1, v1, v15
	vfmul.vv	v0, v0, v1

    VREG_SET(v30, CONST_LCPI7_23, a1)
	vfmul.vv	v0, v0, v30

    VREG_SET(v29, CONST_LCPI7_24, a1)
	vmv.v.v	    v1, v29
	vfmadd.vv	v1, v31, v11
	vfdiv.vv	v31, v11, v1
	vfmul.vv	v3, v31, v31
	vfmul.vv	v5, v3, v31
	vfmul.vv	v6, v5, v31

    VREG_SET(v1, CONST_LCPI7_26, a1)
	vfmul.vv	v3, v3, v1
    VREG_SET(v2, CONST_LCPI7_27, a1)
	vfmul.vv	v5, v5, v2
	vfadd.vv	v7, v3, v5


    vfmul.vv	v8, v6, v31

    VREG_SET(v4, CONST_LCPI7_25, a1)
	vfmul.vv	v31, v31, v4
    VREG_SET(v3, CONST_LCPI7_28, a1)
	vfmacc.vv	v7, v6, v3

    VREG_SET(v5, CONST_LCPI7_29, a1)

    vfmul.vv	v8, v8, v5
	vfadd.vv	v8, v7, v8
	vfadd.vv	v8, v8, v31
	vfmul.vv	v8, v8, v0
	vfsub.vv	v31, v11, v8
	vmv.v.v	v0, v9
	vfsub.vv	v31, v11, v31, v0.t
	vmflt.vv	v8, v27, v12
	vfabs.v	v9, v27
	vfmul.vv	v27, v9, v9
	vfmul.vv	v27, v27, v28
	vfmin.vv	v24, v27, v24
	vfmax.vv	v24, v24, v25
	vmv.v.v	v25, v14
	vfmacc.vv	v25, v24, v26
	vfcvt.x.f.v	v26, v25
	vfcvt.f.x.v	v26, v26
	vmflt.vv	v0, v25, v26
	vmerge.vvm	v25, v12, v11, v0
	vfsub.vv	v25, v26, v25
	vfmul.vv	v17, v25, v17
	vfmul.vv	v16, v25, v16
	vfsub.vv	v17, v24, v17
	vfsub.vv	v16, v17, v16
	vfmul.vv	v17, v16, v16
	vfmadd.vv	v18, v16, v20
	vfmadd.vv	v18, v16, v21
	vfmadd.vv	v18, v16, v22
	vfmadd.vv	v18, v16, v23
	vfmadd.vv	v18, v16, v14
	vfmadd.vv	v18, v17, v16
	vfadd.vv	v14, v18, v11
	vfcvt.x.f.v	v16, v25
	vadd.vv	v13, v16, v13
	vsll.vv	v13, v13, v15
	vfmul.vv	v13, v14, v13
	vfmul.vv	v13, v13, v30
	vfmadd.vv	v29, v9, v11
	vfdiv.vv	v9, v11, v29
	vfmul.vv	v14, v9, v9
	vfmul.vv	v15, v14, v9
	vfmul.vv	v16, v15, v9
	vfmul.vv	v17, v16, v9
	vfmul.vv	v9, v9, v4
	vfmul.vv	v14, v14, v1
	vfmul.vv	v15, v15, v2
	vfadd.vv	v14, v14, v15
	vfmacc.vv	v14, v16, v3
	vfmul.vv	v15, v17, v5
	vfadd.vv	v14, v14, v15
	vfadd.vv	v9, v14, v9
	vfmul.vv	v9, v9, v13
	vfsub.vv	v9, v11, v9
	vmv.v.v	v0, v8
	vfsub.vv	v9, v11, v9, v0.t
	vle32.v	v8, (a7)
	vfmul.vv	v10, v19, v10
	vmseq.vv	v0, v12, v8
	vfsub.vv	v8, v11, v31
	vmerge.vvm	v8, v8, v31, v0
	addi	a1, sp, 16
	vl1r.v	v12, (a1)                       # Unknown-size Folded Reload
	vfmul.vv	v8, v12, v8
	vfsub.vv	v11, v11, v9
	vmerge.vvm	v9, v11, v9, v0
	vfmul.vv	v9, v10, v9
	vfsub.vv	v8, v9, v8
	vfabs.v	v8, v8
	vse32.v	v8, (a0)
	csrr	a0, vlenb
	slli	a0, a0, 1
	add	sp, sp, a0
	addi	sp, sp, 16
	ret
