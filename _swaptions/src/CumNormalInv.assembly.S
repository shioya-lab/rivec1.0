	.globl	_Z19CumNormalInv_vectorPdS_m
	.type	_Z19CumNormalInv_vectorPdS_m, @function
_Z19CumNormalInv_vectorPdS_m:
.LFB867:
	.cfi_startproc
.LVL16:
	lui	a5,%hi(.LC10)
	fld	fa4,%lo(.LC10)(a5)
	vsetvli	zero,a2,e64,m1,ta,mu
	fmv.d.x	fa5,zero
	vfmv.v.f	v29,fa4
	lui	a5,%hi(.LC0)
	fld	fa4,%lo(.LC0)(a5)
.LBB6:
.LBB7:
	li	a4,-2047
	li	a3,1
	slli	a4,a4,52
.LBE7:
.LBE6:
	vfmv.v.f	v10,fa4
.LVL17:
	vle64.v	v9,(a0)
.LVL18:
.LBB11:
.LBB8:
	slli	a3,a3,52
.LBE8:
.LBE11:
	vfsub.vv	v28,v9,v10
.LVL19:
.LBB12:
.LBB9:
	addi	a4,a4,-1
.LBE9:
.LBE12:
	vmfgt.vf	v0,v28,fa5
.LVL20:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfsub.vv	v9,v29,v9,v0.t
.LVL21:
.LBB13:
.LBB10:
	vsetvli	zero,zero,e64,m1,ta,mu
	vmv.v.x	v1,a3
	vmv.v.x	v24,a4
	li	a3,52
	li	a4,1023
	vfmv.v.f	v8,fa5
	vfmax.vv	v26,v9,v1
	vmv.v.x	v30,a3
	vmv.v.x	v23,a4
	lui	a5,%hi(.LC20)
	fld	fa4,%lo(.LC20)(a5)
	vfmv.v.f	v11,fa4
	lui	a5,%hi(.LC21)
	fld	fa4,%lo(.LC21)(a5)
	vfmv.v.f	v25,fa4
	lui	a5,%hi(.LC22)
	fld	fa4,%lo(.LC22)(a5)
	vsrl.vv	v31,v26,v30
	vand.vv	v26,v24,v26
	vor.vv	v26,v26,v10
	vmflt.vv	v0,v26,v11
	vmerge.vvm	v27,v8,v29,v0
	vmerge.vvm	v12,v8,v26,v0
	vfmv.v.f	v22,fa4
	vmfle.vv	v9,v9,v8
.LVL22:
	vsub.vv	v31,v31,v23
	vfsub.vv	v26,v26,v29
	vfcvt.f.x.v	v31,v31
.LVL23:
	vfadd.vv	v26,v26,v12
	vfadd.vv	v31,v31,v29
.LVL24:
	vfmul.vv	v0,v26,v26
	vfsub.vv	v31,v31,v27
.LVL25:
	vsetvli	zero,zero,e64,m1,tu,mu
	vmv1r.v	v27,v25
	vfmadd.vv	v27,v26,v22
	lui	a5,%hi(.LC23)
	fld	fa4,%lo(.LC23)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmv.v.f	v21,fa4
.LVL26:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmadd.vv	v27,v26,v21
	lui	a5,%hi(.LC24)
	fld	fa4,%lo(.LC24)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmv.v.f	v20,fa4
.LVL27:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmadd.vv	v27,v26,v20
	lui	a5,%hi(.LC25)
	fld	fa4,%lo(.LC25)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmv.v.f	v19,fa4
.LVL28:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmadd.vv	v27,v26,v19
	lui	a5,%hi(.LC26)
	fld	fa4,%lo(.LC26)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmv.v.f	v18,fa4
.LVL29:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmadd.vv	v27,v26,v18
	lui	a5,%hi(.LC27)
	fld	fa4,%lo(.LC27)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmv.v.f	v17,fa4
.LVL30:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmadd.vv	v27,v26,v17
	lui	a5,%hi(.LC28)
	fld	fa4,%lo(.LC28)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmv.v.f	v16,fa4
.LVL31:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmadd.vv	v27,v26,v16
	lui	a5,%hi(.LC29)
	fld	fa4,%lo(.LC29)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmv.v.f	v15,fa4
.LVL32:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmadd.vv	v27,v26,v15
	lui	a5,%hi(.LC30)
	fld	fa4,%lo(.LC30)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmul.vv	v27,v27,v0
	vfmv.v.f	v14,fa4
.LVL33:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmacc.vv	v27,v31,v14
	lui	a5,%hi(.LC31)
	fld	fa4,%lo(.LC31)(a5)
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmul.vv	v0,v0,v10
	vfsub.vv	v27,v27,v0
	vmv1r.v	v0,v9
	vfmv.v.f	v13,fa4
.LVL34:
	vmv.v.i	v12,-1
	vfmul.vv	v31,v31,v13
	vfadd.vv	v26,v26,v27
	vfadd.vv	v26,v26,v31
	vmerge.vvm	v26,v26,v12,v0
.LVL35:
.LBE10:
.LBE13:
	vfsgnjn.vv	v26,v26,v26
.LVL36:
.LBB14:
.LBB15:
	vfmax.vv	v1,v26,v1
	vand.vv	v24,v24,v1
	vor.vv	v24,v24,v10
	vmflt.vv	v0,v24,v11
	vmerge.vvm	v27,v8,v24,v0
	vmfle.vv	v26,v26,v8
.LVL37:
	vsrl.vv	v30,v1,v30
.LVL38:
	vmerge.vvm	v8,v8,v29,v0
	vsub.vv	v30,v30,v23
	vfsub.vv	v24,v24,v29
	vfcvt.f.x.v	v30,v30
.LVL39:
	vfadd.vv	v24,v24,v27
	vfadd.vv	v30,v30,v29
.LVL40:
	vfmul.vv	v27,v24,v24
	vfsub.vv	v8,v30,v8
.LVL41:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmadd.vv	v25,v24,v22
.LVL42:
	vfmadd.vv	v25,v24,v21
.LVL43:
	vfmadd.vv	v25,v24,v20
.LVL44:
	vfmadd.vv	v25,v24,v19
.LVL45:
	vfmadd.vv	v25,v24,v18
.LVL46:
	vfmadd.vv	v25,v24,v17
.LVL47:
	vfmadd.vv	v25,v24,v16
.LVL48:
	vfmadd.vv	v25,v24,v15
	vsetvli	zero,zero,e64,m1,ta,mu
	vfmul.vv	v25,v25,v27
.LVL49:
	vsetvli	zero,zero,e64,m1,tu,mu
	vfmacc.vv	v25,v8,v14
	vsetvli	zero,zero,e64,m1,ta,mu
.LBE15:
.LBE14:
	vfmul.vv	v31,v28,v28
.LBB20:
.LBB16:
	vfmul.vv	v27,v27,v10
	vfmul.vv	v8,v8,v13
	vfsub.vv	v25,v25,v27
.LVL50:
.LBE16:
.LBE20:
	lui	a5,%hi(.LC6)
	fld	fa4,%lo(.LC6)(a5)
.LBB21:
.LBB17:
	vfadd.vv	v25,v24,v25
	vmv1r.v	v0,v26
.LBE17:
.LBE21:
	vfmul.vf	v30,v31,fa4
	lui	a5,%hi(.LC2)
	fld	fa4,%lo(.LC2)(a5)
.LBB22:
.LBB18:
	vfadd.vv	v25,v25,v8
.LBE18:
.LBE22:
	vfmul.vf	v27,v31,fa4
	lui	a5,%hi(.LC7)
	fld	fa4,%lo(.LC7)(a5)
.LBB23:
.LBB19:
	vmerge.vvm	v25,v25,v12,v0
.LVL51:
.LBE19:
.LBE23:
	vfadd.vf	v30,v30,fa4
	vfmul.vv	v30,v30,v31
	lui	a5,%hi(.LC11)
	fld	fa4,%lo(.LC11)(a5)
	vfmul.vf	v24,v25,fa4
.LVL52:
	lui	a5,%hi(.LC12)
	fld	fa4,%lo(.LC12)(a5)
	vfadd.vf	v24,v24,fa4
	vfmul.vv	v24,v24,v25
	lui	a5,%hi(.LC3)
	fld	fa4,%lo(.LC3)(a5)
	vfadd.vf	v26,v27,fa4
	vfmul.vv	v26,v26,v31
	lui	a5,%hi(.LC13)
	fld	fa4,%lo(.LC13)(a5)
	vfadd.vf	v24,v24,fa4
	lui	a5,%hi(.LC8)
	fld	fa4,%lo(.LC8)(a5)
	vfadd.vf	v27,v30,fa4
	lui	a5,%hi(.LC4)
	fld	fa4,%lo(.LC4)(a5)
	vfmul.vv	v24,v24,v25
	vfmul.vv	v27,v27,v31
	vfadd.vf	v26,v26,fa4
	vfmul.vv	v26,v26,v31
	lui	a5,%hi(.LC14)
	fld	fa4,%lo(.LC14)(a5)
	vfadd.vf	v24,v24,fa4
	lui	a5,%hi(.LC9)
	fld	fa4,%lo(.LC9)(a5)
	vfadd.vf	v27,v27,fa4
	lui	a5,%hi(.LC5)
	fld	fa4,%lo(.LC5)(a5)
	vfmul.vv	v24,v24,v25
	vfmul.vv	v27,v27,v31
	vfadd.vf	v26,v26,fa4
	vfmul.vv	v26,v26,v28
	lui	a5,%hi(.LC15)
	fld	fa4,%lo(.LC15)(a5)
	vfadd.vv	v27,v27,v29
	vfdiv.vv	v26,v26,v27
	vfadd.vf	v24,v24,fa4
	vfmul.vv	v24,v24,v25
	lui	a5,%hi(.LC16)
	fld	fa4,%lo(.LC16)(a5)
	vmflt.vf	v0,v28,fa5
	vfsgnjx.vv	v28,v28,v28
	vfadd.vf	v24,v24,fa4
	vfmul.vv	v24,v24,v25
	lui	a5,%hi(.LC17)
	fld	fa5,%lo(.LC17)(a5)
	vfadd.vf	v24,v24,fa5
	lui	a5,%hi(.LC1)
	fld	fa5,%lo(.LC1)(a5)
	vfmul.vv	v24,v24,v25
	vmflt.vf	v28,v28,fa5
	lui	a5,%hi(.LC18)
	fld	fa5,%lo(.LC18)(a5)
	vfadd.vf	v24,v24,fa5
	vfmul.vv	v24,v24,v25
	lui	a5,%hi(.LC19)
	fld	fa5,%lo(.LC19)(a5)
	vfadd.vf	v24,v24,fa5
.LVL53:
	vfsgnjn.vv	v25,v24,v24
	vmerge.vvm	v24,v24,v25,v0
.LVL54:
	vmv1r.v	v0,v28
	vmerge.vvm	v24,v24,v26,v0
	vse64.v	v24,(a1)
	ret
	.cfi_endproc
.LFE867:
	.size	_Z19CumNormalInv_vectorPdS_m, .-_Z19CumNormalInv_vectorPdS_m
