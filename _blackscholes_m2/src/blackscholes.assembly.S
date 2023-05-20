	.section	.sdata,"aw",@progbits
	.p2align	2                               # -- Begin function BlkSchlsEqEuroNoDiv_vector_asm
.LCPI6_0:
	.word	0x007fffe1                      # float 1.17549001E-38
.LCPI6_1:
	.word	0x42b0c0a5                      # float 88.3762589
.LCPI6_2:
	.word	0xc2b0c0a5                      # float -88.3762589
.LCPI6_3:
	.word	0x3fb8aa3b                      # float 1.44269502
.LCPI6_4:
	.word	0x3f000000                      # float 0.5
.LCPI6_5:
	.word	0x3f800000                      # float 1
.LCPI6_6:
	.word	0x3f318000                      # float 0.693359375
.LCPI6_7:
	.word	0xb95e8083                      # float -2.12194442E-4
.LCPI6_8:
	.word	0x3f3504f3                      # float 0.707106769
.LCPI6_9:
	.word	0x39506967                      # float 1.98756912E-4
.LCPI6_10:
	.word	0x3ab743ce                      # float 0.00139819994
.LCPI6_11:
	.word	0x3d9021bb                      # float 0.0703768358
.LCPI6_12:
	.word	0xbdebd1b8                      # float -0.115146101
.LCPI6_13:
	.word	0x3c088908                      # float 0.00833345205
.LCPI6_14:
	.word	0x3def251a                      # float 0.116769984
.LCPI6_15:
	.word	0x3d2aa9c1                      # float 0.0416657962
.LCPI6_16:
	.word	0xbdfe5d4f                      # float -0.12420141
.LCPI6_17:
	.word	0x3e2aaaaa                      # float 0.166666657
.LCPI6_18:
	.word	0x3e11e9bf                      # float 0.142493233
.LCPI6_19:
	.word	0xbe2aae50                      # float -0.166680574
.LCPI6_20:
	.word	0x3e4cceac                      # float 0.200007141
.LCPI6_21:
	.word	0xbe7ffffc                      # float -0.24999994
.LCPI6_22:
	.word	0x3eaaaaaa                      # float 0.333333313
.LCPI6_23:
	.word	0xbf000000                      # float -0.5
.LCPI6_24:
	.word	0x3ecc422a                      # float 0.398942292
.LCPI6_25:
	.word	0x3e6d3389                      # float 0.231641904
.LCPI6_26:
	.word	0x3ea385fa                      # float 0.319381535
.LCPI6_27:
	.word	0xbeb68f87                      # float -0.356563777
.LCPI6_28:
	.word	0x3fe40778                      # float 1.78147793
.LCPI6_29:
	.word	0xbfe91eea                      # float -1.82125592
.LCPI6_30:
	.word	0x3faa466f                      # float 1.33027446
	.text
	.globl	BlkSchlsEqEuroNoDiv_vector_asm
	.p2align	2
	.type	BlkSchlsEqEuroNoDiv_vector_asm,@function
BlkSchlsEqEuroNoDiv_vector_asm: # @BlkSchlsEqEuroNoDiv_vector_asm
	.cfi_startproc
# %bb.0:
	ld	t0, 0(sp)
	vle32.v	v8, (a3)
	vle32.v	v10, (a2)
	vle32.v	v18, (a4)
	vle32.v	v16, (a5)
	vle32.v	v20, (a6)
	vfdiv.vv	v10, v10, v8
	vfsqrt.v	v22, v20
	vfmul.vv	v8, v18, v20
	vfneg.v	v12, v8
	#APP
	fence
	#NO_APP
	lui	a1, %hi(.LCPI6_0)
	flw	ft0, %lo(.LCPI6_0)(a1)
	fmv.w.x	ft1, zero
	vmfle.vf	v8, v10, ft1
	vfmax.vf	v10, v10, ft0
	li	a1, 23
	vmv.v.x	v14, a1
	vsrl.vv	v14, v10, v14
	lui	a1, 526336
	addiw	a1, a1, -1
	vand.vx	v10, v10, a1
	lui	a1, 258048
	vor.vx	v26, v10, a1
	li	a1, 127
	vsub.vx	v10, v14, a1
	vfcvt.f.x.v	v28, v10
	lui	a4, %hi(.LCPI6_1)
	flw	ft3, %lo(.LCPI6_1)(a4)
	vfmin.vf	v10, v12, ft3
	lui	a4, %hi(.LCPI6_2)
	flw	ft4, %lo(.LCPI6_2)(a4)
	vfmax.vf	v24, v10, ft4
	lui	a4, %hi(.LCPI6_3)
	flw	ft5, %lo(.LCPI6_3)(a4)
	vfmul.vf	v10, v24, ft5
	lui	a4, %hi(.LCPI6_4)
	flw	ft2, %lo(.LCPI6_4)(a4)
	vfadd.vf	v10, v10, ft2
	vfcvt.x.f.v	v12, v10
	lui	a4, %hi(.LCPI6_5)
	flw	ft0, %lo(.LCPI6_5)(a4)
	vfcvt.f.x.v	v14, v12
	vmflt.vv	v0, v10, v14
	vmv.v.i	v10, 0
	vfmv.v.f	v12, ft0
	vmerge.vvm	v30, v10, v12, v0
	lui	a4, %hi(.LCPI6_6)
	flw	ft6, %lo(.LCPI6_6)(a4)
	vfsub.vv	v14, v14, v30
	lui	a4, %hi(.LCPI6_7)
	flw	ft7, %lo(.LCPI6_7)(a4)
	vfmul.vf	v30, v14, ft6
	lui	a4, %hi(.LCPI6_8)
	flw	fa0, %lo(.LCPI6_8)(a4)
	vfmul.vf	v0, v14, ft7
	vfsub.vv	v24, v24, v30
	vfsub.vv	v24, v24, v0
	vmflt.vf	v0, v26, fa0
	vfsub.vf	v2, v26, ft0
	lui	a4, %hi(.LCPI6_9)
	flw	fa0, %lo(.LCPI6_9)(a4)
	lui	a4, %hi(.LCPI6_10)
	flw	fa1, %lo(.LCPI6_10)(a4)
	vfadd.vf	v28, v28, ft0
	vmerge.vvm	v6, v10, v26, v0
	vmerge.vvm	v26, v10, v12, v0
	vfsub.vv	v26, v28, v26
	vfadd.vv	v28, v2, v6
	vfmul.vv	v0, v28, v28
	vfmul.vv	v30, v24, v24
	vfmul.vf	v4, v24, fa0
	vfadd.vf	v4, v4, fa1
	lui	a4, %hi(.LCPI6_11)
	flw	fa3, %lo(.LCPI6_11)(a4)
	lui	a4, %hi(.LCPI6_12)
	flw	fa4, %lo(.LCPI6_12)(a4)
	lui	a4, %hi(.LCPI6_13)
	flw	fa2, %lo(.LCPI6_13)(a4)
	vfmul.vf	v2, v28, fa3
	vfmul.vv	v4, v4, v24
	vfadd.vf	v2, v2, fa4
	vfadd.vf	v4, v4, fa2
	lui	a4, %hi(.LCPI6_14)
	flw	fa4, %lo(.LCPI6_14)(a4)
	lui	a4, %hi(.LCPI6_15)
	flw	fa3, %lo(.LCPI6_15)(a4)
	vfmul.vv	v2, v2, v28
	vfmul.vv	v4, v4, v24
	vfadd.vf	v2, v2, fa4
	vfadd.vf	v4, v4, fa3
	vfmul.vv	v2, v2, v28
	lui	a4, %hi(.LCPI6_16)
	flw	fa5, %lo(.LCPI6_16)(a4)
	vfmul.vv	v4, v4, v24
	lui	a4, %hi(.LCPI6_17)
	flw	fa4, %lo(.LCPI6_17)(a4)
	vfadd.vf	v2, v2, fa5
	lui	a4, %hi(.LCPI6_18)
	flw	fa5, %lo(.LCPI6_18)(a4)
	vfadd.vf	v4, v4, fa4
	vfmul.vv	v2, v2, v28
	vfmul.vv	v4, v4, v24
	vfadd.vf	v2, v2, fa5
	vfadd.vf	v4, v4, ft2
	lui	a4, %hi(.LCPI6_19)
	flw	fa5, %lo(.LCPI6_19)(a4)
	lui	a4, %hi(.LCPI6_20)
	flw	fa6, %lo(.LCPI6_20)(a4)
	vfmul.vv	v2, v2, v28
	vfadd.vf	v2, v2, fa5
	vfmul.vv	v2, v2, v28
	vfadd.vf	v2, v2, fa6
	lui	a4, %hi(.LCPI6_21)
	flw	fa5, %lo(.LCPI6_21)(a4)
	lui	a4, %hi(.LCPI6_22)
	flw	fa6, %lo(.LCPI6_22)(a4)
	vfmul.vv	v2, v2, v28
	vfadd.vf	v2, v2, fa5
	vfmul.vv	v2, v2, v28
	vfadd.vf	v2, v2, fa6
	vfmul.vv	v2, v2, v28
	vfmadd.vv	v4, v30, v24
	vfadd.vf	v24, v4, ft0
	vfmul.vv	v30, v2, v0
	vfmul.vf	v2, v26, ft7
	vfadd.vv	v30, v30, v2
	vfmul.vf	v0, v0, ft2
	vfsub.vv	v30, v30, v0
	vfcvt.x.f.v	v14, v14
	vadd.vx	v14, v14, a1
	vsll.vi	v14, v14, 23
	vfmul.vf	v26, v26, ft6
	vfadd.vv	v28, v28, v30
	vfadd.vv	v26, v28, v26
	vmv.v.i	v28, -1
	vmv1r.v	v0, v8
	vmerge.vvm	v8, v26, v28, v0
	vfmul.vv	v14, v24, v14
	#APP
	fence
	#NO_APP
	vfmul.vv	v24, v16, v16
	vfmul.vf	v24, v24, ft2
	vfadd.vv	v18, v18, v24
	vfmadd.vv	v18, v20, v8
	vfmul.vv	v8, v16, v22
	vfdiv.vv	v20, v18, v8
	lui			a4, %hi(.LCPI6_23)
	flw			fa5, %lo(.LCPI6_23)(a4)
	vfsub.vv	v16, v20, v8
	vfabs.v	    v18, v20
	vfmul.vv	v8, v18, v18
	vfmul.vf	v8, v8, fa5
	vfmin.vf	v8, v8, ft3
	vfmax.vf	v22, v8, ft4
	vfmul.vf	v8, v22, ft5
	vfadd.vf	v8, v8, ft2
	vfcvt.x.f.v	v24, v8
	vfcvt.f.x.v	v24, v24
	vmflt.vv	v0, v8, v24
	vmflt.vf	v8, v20, ft1
	vmerge.vvm	v20, v10, v12, v0
	vfsub.vv	v20, v24, v20
	vfmul.vf	v24, v20, ft6
	vfmul.vf	v26, v20, ft7
	vfcvt.x.f.v	v20, v20
	vadd.vx	    v20, v20, a1
	vfsub.vv	v22, v22, v24
	vfsub.vv	v22, v22, v26
	vfmul.vv	v24, v22, v22
	vfmul.vf	v26, v22, fa0
	vfadd.vf	v26, v26, fa1
	vfmul.vv	v26, v26, v22
	vfadd.vf	v26, v26, fa2
	vfmul.vv	v26, v26, v22
	vfadd.vf	v26, v26, fa3
	vfmul.vv	v26, v26, v22
	vfadd.vf	v26, v26, fa4
	vfmul.vv	v26, v26, v22
	vfadd.vf	v26, v26, ft2
	vfmadd.vv	v26, v24, v22
	vfadd.vf	v22, v26, ft0
	lui			a4, %hi(.LCPI6_24)
	flw			fa6, %lo(.LCPI6_24)(a4)
	lui			a4, %hi(.LCPI6_25)
	flw			fa7, %lo(.LCPI6_25)(a4)
	vsll.vi	    v20, v20, 23
	vfmul.vv	v20, v22, v20
	vfmul.vf	v22, v20, fa6
	vfmul.vf	v18, v18, fa7
	vfadd.vf	v18, v18, ft0
	vfrdiv.vf	v18, v18, ft0
	vfmul.vv	v20, v18, v18
	vfmul.vv	v24, v20, v18
	lui	a4, %hi(.LCPI6_26)
	flw	ft8, %lo(.LCPI6_26)(a4)
	lui	a4, %hi(.LCPI6_27)
	flw	ft9, %lo(.LCPI6_27)(a4)
	vfmul.vv	v26, v24, v18
	vfmul.vv	v28, v26, v18
	vfmul.vf	v18, v18, ft8
	vfmul.vf	v30, v20, ft9
	lui	a4, %hi(.LCPI6_28)
	flw	ft10, %lo(.LCPI6_28)(a4)
	lui	a4, %hi(.LCPI6_29)
	addi	a4, a4, %lo(.LCPI6_29)
	vlse32.v	v20, (a4), zero
	lui	a4, %hi(.LCPI6_30)
	flw	ft11, %lo(.LCPI6_30)(a4)
	vfmul.vf	v24, v24, ft10
	vfadd.vv	v24, v30, v24
	vfmacc.vv	v24, v20, v26
	vfmul.vf	v26, v28, ft11
	vfadd.vv	v24, v24, v26
	vfadd.vv	v18, v24, v18
	vfmul.vv	v18, v18, v22
	vfrsub.vf	v18, v18, ft0
	vmv1r.v	    v0, v8
	vfsub.vv	v18, v12, v18, v0.t
	vfabs.v	    v22, v16
	vfmul.vv	v8, v22, v22
	vfmul.vf	v8, v8, fa5
	vfmin.vf	v8, v8, ft3
	vfmax.vf	v24, v8, ft4
	vfmul.vf	v8, v24, ft5
	vfadd.vf	v8, v8, ft2
	vfcvt.x.f.v	v26, v8
	vfcvt.f.x.v	v26, v26
	vmflt.vv	v0, v8, v26
	vmflt.vf	v8, v16, ft1
	vmerge.vvm	v16, v10, v12, v0
	vfsub.vv	v16, v26, v16
	vfmul.vf	v26, v16, ft6
	vfmul.vf	v28, v16, ft7
	vfsub.vv	v24, v24, v26
	vfsub.vv	v24, v24, v28
	vfmul.vv	v26, v24, v24
	vfmul.vf	v28, v24, fa0
	vfadd.vf	v28, v28, fa1
	vfmul.vv	v28, v28, v24
	vfadd.vf	v28, v28, fa2
	vfmul.vv	v28, v28, v24
	vfadd.vf	v28, v28, fa3
	vfmul.vv	v28, v28, v24
	vfadd.vf	v28, v28, fa4
	vfmul.vv	v28, v28, v24
	vfadd.vf	v28, v28, ft2
	vfmadd.vv	v28, v26, v24
	vfadd.vf	v24, v28, ft0
	vfcvt.x.f.v	v16, v16
	vadd.vx		v16, v16, a1
	vsll.vi		v16, v16, 23
	vfmul.vv	v16, v24, v16
	vfmul.vf	v16, v16, fa6
	vfmul.vf	v22, v22, fa7
	vfadd.vf	v22, v22, ft0
	vfrdiv.vf	v22, v22, ft0
	vfmul.vv	v24, v22, v22
	vfmul.vv	v26, v24, v22
	vfmul.vv	v28, v26, v22
	vfmul.vv	v30, v28, v22
	vfmul.vf	v22, v22, ft8
	vfmul.vf	v24, v24, ft9
	vfmul.vf	v26, v26, ft10
	vfadd.vv	v24, v24, v26
	vfmacc.vv	v24, v20, v28
	vfmul.vf	v20, v30, ft11
	vfadd.vv	v20, v24, v20
	vfadd.vv	v20, v20, v22
	vfmul.vv	v16, v20, v16
	vle32.v	v20, (a3)
	vfrsub.vf	v16, v16, ft0
	vle32.v	v22, (a7)
	vmv1r.v	v0, v8
	vfsub.vv	v16, v12, v16, v0.t
	vfmul.vv	v8, v14, v20
	vle32.v	v12, (a2)
	vmseq.vv	v0, v10, v22
	vfrsub.vf	v10, v18, ft0
	vmerge.vvm	v10, v10, v18, v0
	vfmul.vv	v10, v12, v10
	vfrsub.vf	v12, v16, ft0
	vmerge.vvm	v12, v12, v16, v0
	vfmul.vv	v8, v8, v12
	vfsub.vv	v8, v8, v10
	vfabs.v	v8, v8
	vse32.v	v8, (a0)
	ret
.Lfunc_end6:
	.size	BlkSchlsEqEuroNoDiv_vector_asm, .Lfunc_end6-BlkSchlsEqEuroNoDiv_vector_asm
	.cfi_endproc
                                        # -- End function
