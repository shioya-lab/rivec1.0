#define F64_ONE v29
#define F64_R1  v9
#define F64_ZERO v8


    .globl	CumNormalInvAsm_vector
	.type	CumNormalInvAsm_vector, @function
CumNormalInvAsm_vector:
.LFB867:
	.cfi_startproc
.LVL16:
	vsetvli	    zero, a2,e64,m1,ta,mu
	fld	        fa4, .LC0, a5
.LBB6:
.LBB7:
	li	    a4,-2047
	li	    a3,1
	slli	a4,a4,52
.LBE7:
.LBE6:
	vfmv.v.f	v10,fa4
.LVL17:
	vle64.v	F64_R1,(a0)
.LVL18:
.LBB11:
.LBB8:
	slli	a3,a3,52
.LBE8:
.LBE11:
	vfsub.vv	v28,F64_R1,v10
.LVL19:
.LBB12:
.LBB9:
	addi	a4,a4,-1
.LBE9:
.LBE12:
	fmv.d.x	    fa5,zero
	vmfgt.vf	v0,v28,fa5
	vfmv.v.f	F64_ZERO, fa5
.LVL20:
	fld	        fa4, .LC10, a5
	vfmv.v.f	F64_ONE, fa4
	vfsub.vv	F64_R1,F64_ONE,F64_R1,v0.t
.LVL21:
.LBB13:
.LBB10:
	vmv.v.x	v1,a3
	vmv.v.x	v24,a4
	li	a3,52
	li	a4,1023
	vfmax.vv	v26,F64_R1,v1
	vmv.v.x	v30,a3
	vmv.v.x	v23,a4
	fld	        fa4,.LC20, a5
	vfmv.v.f	v11,fa4
	fld	        fa4, .LC21, a5
	vfmv.v.f	v25,fa4
	fld	        fa4, .LC22, a5
	vsrl.vv	    v31,v26,v30
	vand.vv	    v26,v24,v26
	vor.vv	    v26,v26,v10
	vmflt.vv	v0,v26,v11
	vmerge.vvm	v27,F64_ZERO,F64_ONE,v0
	vmerge.vvm	v12,F64_ZERO,v26,v0
	vfmv.v.f	v22,fa4
	vmfle.vv	v9,F64_R1,F64_ZERO
.LVL22:
	vsub.vv	v31,v31,v23
	vfsub.vv	v26,v26,F64_ONE
	vfcvt.f.x.v	v31,v31
.LVL23:
	vfadd.vv	v26,v26,v12
	vfadd.vv	v31,v31,F64_ONE
.LVL24:
	vfmul.vv	v0,v26,v26
	vfsub.vv	v31,v31,v27
.LVL25:
	vmv1r.v	    v27,v25
	vfmadd.vv	v27,v26,v22
	fld	        fa4,.LC23, a5
	vfmv.v.f	v21,fa4
.LVL26:
	vfmadd.vv	v27,v26,v21
	fld	        fa4, .LC24, a5
	vfmv.v.f	v20,fa4
.LVL27:
	vfmadd.vv	v27,v26,v20
	fld	        fa4, .LC25, a5
	vfmv.v.f	v19,fa4
.LVL28:
	vfmadd.vv	v27,v26,v19
	fld	        fa4, .LC26, a5
	vfmv.v.f	v18,fa4
.LVL29:
	vfmadd.vv	v27,v26,v18
	fld	        fa4, .LC27, a5
	vfmv.v.f	v17,fa4
.LVL30:
	vfmadd.vv	v27,v26,v17
	fld	        fa4, .LC28, a5
	vfmv.v.f	v16,fa4
.LVL31:
	vfmadd.vv	v27,v26,v16
	fld	        fa4, .LC29, a5
	vfmv.v.f	v15,fa4
.LVL32:
	vfmadd.vv	v27,v26,v15
	fld	        fa4, .LC30, a5
	vfmul.vv	v27,v27,v0
	vfmv.v.f	v14,fa4
.LVL33:
	vfmacc.vv	v27,v31,v14
	fld	        fa4, .LC31, a5
	vfmul.vv	v0,v0,v10
	vfsub.vv	v27,v27,v0
	vmv1r.v	    v0,v9
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
	vmerge.vvm	v27,F64_ZERO,v24,v0
	vmfle.vv	v26,v26,F64_ZERO
.LVL37:
	vsrl.vv	v30,v1,v30
.LVL38:
	vmerge.vvm	v8,v8,F64_ONE,v0
	vsub.vv	v30,v30,v23
	vfsub.vv	v24,v24,F64_ONE
	vfcvt.f.x.v	v30,v30
.LVL39:
	vfadd.vv	v24,v24,v27
	vfadd.vv	v30,v30,F64_ONE
.LVL40:
	vfmul.vv	v27,v24,v24
	vfsub.vv	v8,v30,v8
.LVL41:
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
	vfmul.vv	v25,v25,v27
.LVL49:
	vfmacc.vv	v25,v8,v14
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
	fld	        fa4, .LC6, a5
.LBB21:
.LBB17:
	vfadd.vv	v25,v24,v25
	vmv1r.v	v0,v26
.LBE17:
.LBE21:
	vfmul.vf	v30,v31,fa4
	fld	        fa4, .LC2, a5
.LBB22:
.LBB18:
	vfadd.vv	v25,v25,v8
.LBE18:
.LBE22:
	vfmul.vf	v27,v31,fa4
	fld	        fa4, .LC7, a5
.LBB23:
.LBB19:
	vmerge.vvm	v25,v25,v12,v0
.LVL51:
.LBE19:
.LBE23:
	vfadd.vf	v30,v30,fa4
	vfmul.vv	v30,v30,v31
	fld	        fa4, .LC11, a5
	vfmul.vf	v24,v25,fa4
.LVL52:
	fld	        fa4, .LC12, a5
	vfadd.vf	v24,v24,fa4
	vfmul.vv	v24,v24,v25
	fld	        fa4, .LC3, a5
	vfadd.vf	v26,v27,fa4
	vfmul.vv	v26,v26,v31
	fld	        fa4, .LC13, a5
	vfadd.vf	v24,v24,fa4
	fld	        fa4, .LC8, a5
	vfadd.vf	v27,v30,fa4
	fld	        fa4, .LC4, a5
	vfmul.vv	v24,v24,v25
	vfmul.vv	v27,v27,v31
	vfadd.vf	v26,v26,fa4
	vfmul.vv	v26,v26,v31
	fld	        fa4, .LC14, a5
	vfadd.vf	v24,v24,fa4
	fld	        fa4, .LC9, a5
	vfadd.vf	v27,v27,fa4
	fld	        fa4, .LC5, a5
	vfmul.vv	v24,v24,v25
	vfmul.vv	v27,v27,v31
	vfadd.vf	v26,v26,fa4
	vfmul.vv	v26,v26,v28
	fld	        fa4, .LC15, a5
	vfadd.vv	v27,v27,F64_ONE
	vfdiv.vv	v26,v26,v27
	vfadd.vf	v24,v24,fa4
	vfmul.vv	v24,v24,v25
	fld	        fa4, .LC16, a5
	vmflt.vf	v0,v28,fa5
	vfsgnjx.vv	v28,v28,v28
	vfadd.vf	v24,v24,fa4
	vfmul.vv	v24,v24,v25
	fld	        fa5, .LC17, a5
	vfadd.vf	v24,v24,fa5
	fld	        fa5, .LC1, a5
	vfmul.vv	v24,v24,v25
	vmflt.vf	v28,v28,fa5
	fld	        fa5,.LC18, a5
	vfadd.vf	v24,v24,fa5
	vfmul.vv	v24,v24,v25
	fld	        fa5, .LC19, a5
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
	.size	CumNormalInvAsm_vector, .-CumNormalInvAsm_vector


.LC0:
	.word	0
	.word	1071644672
	.align	3
.LC1:
	.word	-1374389535
	.word	1071309127
	.align	3
.LC2:
	.word	1463252856
	.word	-1069977367
	.align	3
.LC3:
	.word	-999045380
	.word	1078243858
	.align	3
.LC4:
	.word	-1370184738
	.word	-1070424720
	.align	3
.LC5:
	.word	455631373
	.word	1074007443
	.align	3
.LC6:
	.word	542476871
	.word	1074334704
	.align	3
.LC7:
	.word	117564797
	.word	-1070264337
	.align	3
.LC8:
	.word	-1853796308
	.word	1077351767
	.align	3
.LC9:
	.word	106235693
	.word	-1071582608
	.align	3
.LC10:
	.word	0
	.word	1072693248
	.align	3
.LC11:
	.word	167957933
	.word	1050317765
	.align	3
.LC12:
	.word	1889237846
	.word	1049846229
	.align	3
.LC13:
	.word	99975688
	.word	1057021618
	.align	3
.LC14:
	.word	-1599502266
	.word	1060759086
	.align	3
.LC15:
	.word	-448895099
	.word	1064269379
	.align	3
.LC16:
	.word	1944338999
	.word	1067208365
	.align	3
.LC17:
	.word	644417154
	.word	1069847815
	.align	3
.LC18:
	.word	-812924627
	.word	1072643270
	.align	3
.LC19:
	.word	-1008467096
	.word	1070962994
	.align	3
.LC20:
	.word	1719614413
	.word	1072079006
	.align	3
.LC21:
	.word	1648698458
	.word	1068631095
	.align	3
.LC22:
	.word	185830219
	.word	-1078101449
	.align	3
.LC23:
	.word	1292471960
	.word	1069409443
	.align	3
.LC24:
	.word	-613159636
	.word	-1077949527
	.align	3
.LC25:
	.word	-724749511
	.word	1069694263
	.align	3
.LC26:
	.word	80448187
	.word	-1077586486
	.align	3
.LC27:
	.word	-1894793666
	.word	1070176725
	.align	3
.LC28:
	.word	2130717459
	.word	-1076887553
	.align	3
.LC29:
	.word	1042664854
	.word	1070945621
	.align	3
.LC30:
	.word	1547846378
	.word	-1087647728
	.align	3
.LC31:
	.word	0
	.word	1072050176
