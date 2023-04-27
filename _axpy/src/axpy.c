#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>

#ifdef USE_RISCV_VECTOR

#include "../../common/vector_defines.h"

void axpy_intrinsics(double a, double *dx, double *dy, int n) {
  int i;

  // long gvl = __builtin_epi_vsetvl(n, __epi_e64, __epi_m1);
  long gvl = __riscv_vsetvl_e64m8(n); //PLCT

  _MMR_8xf64 v_a = _MM_SET_f64_m8(a, gvl);

  for (i = 0; i < n;) {
    // gvl = __builtin_epi_vsetvl(n - i, __epi_e64, __epi_m1);
    gvl = __riscv_vsetvl_e64m8(n - i); //PLCT

    {
      _MMR_8xf64 v_dx = _MM_LOAD_f64_m8(dx, gvl);
      _MMR_8xf64 v_dy = _MM_LOAD_f64_m8(dy, gvl);
      _MMR_8xf64 v_res = _MM_MACC_f64_m8(v_dy, v_a, v_dx, gvl);
      _MM_STORE_f64_m8(dy, v_res, gvl);
    }

    dx += gvl;
    dy += gvl;
    i += gvl;
  }

FENCE();
}

#else // USE_RISCV_VECTOR

#define FENCE()   asm volatile( "fence" : : );

void axpy_intrinsics(double a, double *dx, double *dy, int n) {

  for (int i = 0; i < n; i++) {
    dy[i] = a * dx[i] + dy[i];
  }

  FENCE();
}

#endif // USE_RISCV_VECTOR
