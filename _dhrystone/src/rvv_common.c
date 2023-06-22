/// #include "common.h"
#include <assert.h>
#include <riscv_vector.h>
#include <string.h>

// reference https://github.com/riscv/riscv-v-spec/blob/master/example/strcpy.s
char *rvv_strcpy(char *dst, const char *src) {
  char *save = dst;
  size_t vlmax = __riscv_vsetvlmax_e8m8();
  long first_set_bit = -1;
  size_t vl;
  while (first_set_bit < 0) {
    vint8m8_t vec_src = __riscv_vle8ff_v_i8m8(src, &vl, vlmax);

    vbool1_t string_terminate = __riscv_vmseq_vx_i8m8_b1(vec_src, 0, vl);
    vbool1_t mask = __riscv_vmsif_m_b1(string_terminate, vl);

    __riscv_vse8_v_i8m8_m(mask, dst, vec_src, vl);

    src += vl;
    dst += vl;

    first_set_bit = __riscv_vfirst_m_b1(string_terminate, vl);
  }
  return save;
}

// reference https://github.com/riscv/riscv-v-spec/blob/master/example/strcmp.s
int rvv_strcmp(const char *src1, const char *src2) {
  size_t vlmax = __riscv_vsetvlmax_e8m2();
  long first_set_bit = -1;
  size_t vl, vl1;
  while (first_set_bit < 0) {
    vint8m2_t vec_src1 = __riscv_vle8ff_v_i8m2(src1, &vl, vlmax);
    vint8m2_t vec_src2 = __riscv_vle8ff_v_i8m2(src2, &vl1, vlmax);

    vbool4_t string_terminate = __riscv_vmseq_vx_i8m2_b4(vec_src1, 0, vl);
    vbool4_t no_equal = __riscv_vmsne_vv_i8m2_b4(vec_src1, vec_src2, vl);
    vbool4_t vec_terminate = __riscv_vmor_mm_b4(string_terminate, no_equal, vl);

    first_set_bit = __riscv_vfirst_m_b4(vec_terminate, vl);
    src1 += vl;
    src2 += vl;
  }
  src1 -= vl - first_set_bit;
  src2 -= vl - first_set_bit;
  return *src1 - *src2;
}

void *rvv_memcpy(void *dst, void *src, size_t n) {
  void *save = dst;
  // copy data byte by byte
  for (size_t vl; n > 0; n -= vl, src += vl, dst += vl) {
    vl = __riscv_vsetvl_e8m8(n);
    vuint8m1_t vec_src = __riscv_vle8_v_u8m8(src, vl);
    __riscv_vse8_v_u8m8(dst, vec_src, vl);
  }
  return save;
}
