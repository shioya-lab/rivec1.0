/// #include "common.h"
#include <assert.h>
#include <riscv_vector.h>
#include <string.h>

// reference https://github.com/riscv/riscv-v-spec/blob/master/example/strcpy.s
char *rvv_strcpy(char *dst, const char *src) {
  char *save = dst;
  size_t vlmax = __riscv_vsetvlmax_e8m1();
  long first_set_bit = -1;
  size_t vl;
  while (first_set_bit < 0) {
    vint8m1_t vec_src = __riscv_vle8ff_v_i8m1(src, &vl, vlmax);
    // printf("rvv_strcpy new vl = %d, %d, %s\n", vl, strlen(src), src);
    vbool8_t string_terminate = __riscv_vmseq_vx_i8m1_b8(vec_src, 0, vl);
    vbool8_t mask = __riscv_vmsif_m_b8(string_terminate, vl);

    __riscv_vse8_v_i8m1_m(mask, dst, vec_src, vl);

    src += vl;
    dst += vl;

    first_set_bit = __riscv_vfirst_m_b8(string_terminate, vl);
  }
  return save;
}

// reference https://github.com/riscv/riscv-v-spec/blob/master/example/strcmp.s
int rvv_strcmp(const char *src1, const char *src2) {
  size_t vlmax = __riscv_vsetvlmax_e8m2();
  long first_set_bit = -1;
  size_t vl, vl1;
  while (first_set_bit < 0) {
    vint8m1_t vec_src1 = __riscv_vle8ff_v_i8m1(src1, &vl, vlmax);
    vint8m1_t vec_src2 = __riscv_vle8ff_v_i8m1(src2, &vl1, vlmax);

    // printf("rvv_strcmp new vl = %d, %d, %s\n", vl, strlen(src1), src1);

    vbool8_t string_terminate = __riscv_vmseq_vx_i8m1_b8(vec_src1, 0, vl);
    vbool8_t no_equal = __riscv_vmsne_vv_i8m1_b8(vec_src1, vec_src2, vl);
    vbool8_t vec_terminate = __riscv_vmor_mm_b8(string_terminate, no_equal, vl);

    first_set_bit = __riscv_vfirst_m_b8(vec_terminate, vl);
    src1 += vl;
    src2 += vl;
  }
  src1 -= vl - first_set_bit;
  src2 -= vl - first_set_bit;
  return *src1 - *src2;
}

void *rvv_memcpy(void *dst, void *src, size_t n) {
  void *save = dst;
  // printf("rvv_memcpy %d\n", n);
  // copy data byte by byte
  for (size_t vl; n > 0; n -= vl, src += vl, dst += vl) {
    vl = __riscv_vsetvl_e8m1(n);
    vuint8m1_t vec_src = __riscv_vle8_v_u8m1(src, vl);
    __riscv_vse8_v_u8m1(dst, vec_src, vl);
  }
  return save;
}
