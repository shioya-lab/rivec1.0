//
// RISC-V VECTOR LOG FUNCTION Version by Cristóbal Ramírez Lazo, "Barcelona 2019"
// This RISC-V Vector implementation is based on the original code presented by Julien Pommier

/*
   AVX implementation of sin, cos, sincos, exp and log

   Based on "sse_mathfun.h", by Julien Pommier
   http://gruntthepeon.free.fr/ssemath/

   Copyright (C) 2012 Giovanni Garberoglio
   Interdisciplinary Laboratory for Computational Science (LISC)
   Fondazione Bruno Kessler and University of Trento
   via Sommarive, 18
   I-38123 Trento (Italy)

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.

  (this is the zlib license)
*/

inline _MMR_f64 __log_exp_1xf64(_MMR_f64 x , unsigned long int gvl) {
  /* Not supported now*/
}



inline void __log_exp_2xf32(_MMR_f32 log_x , _MMR_f32 exp_x, _MMR_f32 *res_log , _MMR_f32 *res_exp, unsigned long int gvl) {

  /* LOG IMPL */ const float s_cephes_SQRTHF     = 0.707106781186547524;

  /* LOG IMPL */ const float s_cephes_log_p0     =  7.0376836292E-2;
  /* LOG IMPL */ const float s_cephes_log_p1     = -1.1514610310E-1;
  /* LOG IMPL */ const float s_cephes_log_p2     =  1.1676998740E-1;
  /* LOG IMPL */ const float s_cephes_log_p3     = -1.2420140846E-1;
  /* LOG IMPL */ const float s_cephes_log_p4     =  1.4249322787E-1;
  /* LOG IMPL */ const float s_cephes_log_p5     = -1.6668057665E-1;
  /* LOG IMPL */ const float s_cephes_log_p6     =  2.0000714765E-1;
  /* LOG IMPL */ const float s_cephes_log_p7     = -2.4999993993E-1;
  /* LOG IMPL */ const float s_cephes_log_p8     =  3.3333331174E-1;

  /* LOG IMPL */ float s_min_norm_pos = 1.17549e-38; // 0x00800000

  /* LOG IMPL */ const uint32_t zero_p5 = 0x3f000000; // 0.5
  /* LOG IMPL */ const float s_cephes_log_q1     = -2.12194440e-4;
  /* LOG IMPL */ const float s_cephes_log_q2     = 0.693359375;

  /* EXP IMPL */ const float s_cephes_exp_C1 = 0.693359375;
  /* EXP IMPL */ const float s_cephes_exp_C2 = -2.12194440e-4;

  /* EXP IMPL */ const float s_cephes_exp_p0 = 1.9875691500E-4;
  /* EXP IMPL */ const float s_cephes_exp_p1 = 1.3981999507E-3;
  /* EXP IMPL */ const float s_cephes_exp_p2 = 8.3334519073E-3;
  /* EXP IMPL */ const float s_cephes_exp_p3 = 4.1665795894E-2;
  /* EXP IMPL */ const float s_cephes_exp_p4 = 1.6666665459E-1;
  /* EXP IMPL */ const float s_cephes_exp_p5 = 5.0000001201E-1;

  /* EXP IMPL */ _MMR_f32   exp_tmp;
  /* EXP IMPL */ _MMR_f32   exp_tmp2;
  /* EXP IMPL */ _MMR_f32   exp_tmp4;
  /* EXP IMPL */ _MMR_f32   exp_fx;

  /* EXP IMPL */ _MMR_f32   exp_z;
  /* EXP IMPL */ _MMR_f32   exp_y;

  /* EXP IMPL */ _MMR_MASK_i32  exp_mask;
  /* EXP IMPL */ _MMR_i32  exp_imm0;
  /* EXP IMPL */ _MMR_i32  exp_tmp3;

  /* LOG IMPL */ _MMR_MASK_i32 invalid_mask = _MM_VFLE_f32_f(log_x, 0.0f, gvl);

  /* LOG IMPL */ log_x = _MM_MAX_f32_f(log_x, s_min_norm_pos, gvl);  /* cut off denormalized stuff */

  /* LOG IMPL */ // can be done with AVX2
  /* LOG IMPL */ _MMR_i32 log_imm0 = _MMR_u32_to_i32(_MM_SRL_i32(_MMR_f32_to_u32(log_x), _MM_SET_u32(23,gvl), gvl));

  /* LOG IMPL */ /* keep only the fractional part */
  /* LOG IMPL */ _MMR_i32 _x_i = _MM_AND_i32_x(_MMR_f32_to_i32(log_x), ~0x7f800000, gvl);
  /* LOG IMPL */ _x_i = _MM_OR_i32_x(_x_i, zero_p5, gvl);
  /* LOG IMPL */ log_x = _MMR_i32_to_f32(_x_i);

  /* LOG IMPL */ // this is again another AVX2 instruction
  /* LOG IMPL */ log_imm0 = _MM_SUB_i32_x(log_imm0, 0x7f , gvl);
  /* LOG IMPL */ _MMR_f32 e = _MM_VFCVT_F_X_f32(log_imm0, gvl);

  /* EXP IMPL */ // const float s_exp_hi        = 88.3762626647949;
  /* EXP IMPL */ exp_x = _MM_MIN_f32_f(exp_x, 88.3762626647949 /* s_exp_hi */, gvl);
  /* EXP IMPL */ // const float s_exp_lo        = -88.3762626647949;
  /* EXP IMPL */ exp_x = _MM_MAX_f32_f(exp_x, -88.3762626647949 /* s_exp_lo */, gvl);

  /* EXP IMPL */ const float s_cephes_LOG2EF = 1.44269504088896341;
  /* EXP IMPL */ exp_fx    = _MM_MUL_f32_f(exp_x, s_cephes_LOG2EF, gvl);
  /* EXP IMPL */ exp_fx    = _MM_ADD_f32_f(exp_fx, 0.5, gvl);

  /* EXP IMPL */ exp_tmp3  = _MM_VFCVT_X_F_i32(exp_fx,gvl);
  /* EXP IMPL */ exp_tmp   = _MM_VFCVT_F_X_f32(exp_tmp3,gvl);

  /* EXP IMPL */ exp_mask  = _MM_VFLT_f32(exp_fx,exp_tmp,gvl);
  /* EXP IMPL */ exp_tmp2  = _MM_MERGE_f32(_MM_SET_f32(0.0,gvl), _MM_SET_f32(1.0,gvl), exp_mask,gvl);
  /* EXP IMPL */ exp_fx    = _MM_SUB_f32(exp_tmp,exp_tmp2,gvl);
  /* EXP IMPL */ exp_tmp   = _MM_MUL_f32_f(exp_fx, s_cephes_exp_C1,gvl);
  /* EXP IMPL */ exp_z     = _MM_MUL_f32_f(exp_fx, s_cephes_exp_C2,gvl);
  /* EXP IMPL */ exp_x     = _MM_SUB_f32(exp_x,exp_tmp,gvl);
  /* EXP IMPL */ exp_x     = _MM_SUB_f32(exp_x,exp_z,gvl);

  /* LOG IMPL */ _MMR_MASK_i32 mask = _MM_VFLT_f32_f(log_x, s_cephes_SQRTHF , gvl);
  /* LOG IMPL */ _MMR_f32 x_raw = log_x;
  /* LOG IMPL */ log_x = _MM_SUB_f32_f(log_x, 1.0, gvl);
  /* LOG IMPL */ e = _MM_ADD_f32_f(e, 1.0 ,gvl);

  /* EXP IMPL */ exp_z     = _MM_MUL_f32  (exp_x, exp_x, gvl);
  /* EXP IMPL */ exp_y     = _MM_MUL_f32_f(exp_x, s_cephes_exp_p0,gvl);
  /* EXP IMPL */ exp_y     = _MM_ADD_f32_f(exp_y, s_cephes_exp_p1,gvl);

  /* LOG IMPL */ _MMR_f32 log_tmp  = _MM_MERGE_f32(_MM_SET_f32(0.0f,gvl), x_raw, mask,gvl);

  /* LOG IMPL */ e = _MM_SUB_f32(e, _MM_MERGE_f32(_MM_SET_f32(0.0f, gvl),
  /* LOG IMPL */                                  _MM_SET_f32(1.0f, gvl), mask, gvl),gvl);

  /* LOG IMPL */ log_x = _MM_ADD_f32(log_x, log_tmp, gvl);

  /* LOG IMPL */ _MMR_f32 log_z = _MM_MUL_f32(log_x, log_x, gvl);

  /* LOG IMPL */ _MMR_f32 log_y;
  /* LOG IMPL */ log_y = _MM_MACC_f32(log_x, _MM_SET_f32(s_cephes_log_p0, gvl), _MM_SET_f32(s_cephes_log_p1, gvl), gvl);
  /* EXP IMPL */ exp_y = _MM_MADD_f32(exp_y, exp_x, _MM_SET_f32(s_cephes_exp_p2, gvl), gvl);
  /* LOG IMPL */ log_y = _MM_MADD_f32(log_y, log_x, _MM_SET_f32(s_cephes_log_p2, gvl), gvl);
  /* EXP IMPL */ exp_y = _MM_MADD_f32(exp_y, exp_x, _MM_SET_f32(s_cephes_exp_p3, gvl), gvl);
  /* LOG IMPL */ log_y = _MM_MADD_f32(log_y, log_x, _MM_SET_f32(s_cephes_log_p3, gvl), gvl);
  /* EXP IMPL */ exp_y = _MM_MADD_f32(exp_y, exp_x, _MM_SET_f32(s_cephes_exp_p4, gvl), gvl);
  /* LOG IMPL */ log_y = _MM_MADD_f32(log_y, log_x, _MM_SET_f32(s_cephes_log_p4, gvl), gvl);
  /* EXP IMPL */ exp_y = _MM_MADD_f32(exp_y, exp_x, _MM_SET_f32(s_cephes_exp_p5, gvl), gvl);
  /* LOG IMPL */ log_y = _MM_MADD_f32(log_y, log_x, _MM_SET_f32(s_cephes_log_p5, gvl), gvl);
  /* LOG IMPL */ log_y = _MM_MADD_f32(log_y, log_x, _MM_SET_f32(s_cephes_log_p6, gvl), gvl);
  /* LOG IMPL */ log_y = _MM_MADD_f32(log_y, log_x, _MM_SET_f32(s_cephes_log_p7, gvl), gvl);
  /* LOG IMPL */ log_y = _MM_MADD_f32(log_y, log_x, _MM_SET_f32(s_cephes_log_p8, gvl), gvl);
  /* LOG IMPL */ log_y = _MM_MUL_f32  (log_y, log_x, gvl);

  /* EXP IMPL */ exp_y = _MM_MADD_f32 (exp_y, exp_z, exp_x, gvl);
  /* EXP IMPL */ exp_y = _MM_ADD_f32_f(exp_y, 1.0, gvl);

  /* LOG IMPL */ log_y = _MM_MUL_f32(log_y, log_z, gvl);

  /* LOG IMPL */ log_tmp = _MM_MUL_f32_f(e, s_cephes_log_q1,gvl);
  /* LOG IMPL */ log_y = _MM_ADD_f32(log_y, log_tmp, gvl);
  /* LOG IMPL */ log_tmp = _MM_MUL_f32_f(log_z, 0.5, gvl);
  /* LOG IMPL */ log_y = _MM_SUB_f32(log_y, log_tmp, gvl);

  /* EXP IMPL */ exp_imm0  = _MM_VFCVT_X_F_i32(exp_fx,gvl);
  /* EXP IMPL */ exp_imm0  = _MM_ADD_i32_x(exp_imm0, 0x7f,gvl);
  /* EXP IMPL */ exp_imm0  = _MM_SLL_i32_x(exp_imm0, 23,gvl);

  /* LOG IMPL */ log_tmp = _MM_MUL_f32_f(e, s_cephes_log_q2,gvl);
  /* LOG IMPL */ log_x = _MM_ADD_f32(log_x, log_y, gvl);
  /* LOG IMPL */ log_x = _MM_ADD_f32(log_x, log_tmp, gvl);
  /* LOG IMPL */ log_x = _MM_MERGE_f32(log_x,_MMR_i32_to_f32(_MM_SET_i32(0xffffffff,gvl)), invalid_mask,gvl);

  /* EXP IMPL */ exp_tmp4  = _MMR_i32_to_f32(exp_imm0);
  /* EXP IMPL */ exp_y = _MM_MUL_f32(exp_y, exp_tmp4,gvl);

  *res_log = log_x;
  *res_exp = exp_y;
}
