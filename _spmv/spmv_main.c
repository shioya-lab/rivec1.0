// See LICENSE for license details.

//**************************************************************************
// Double-precision sparse matrix-vector multiplication benchmark
//--------------------------------------------------------------------------

#include "util.h"
#include <string.h>
#include <stdio.h>
#include "sim_api.h"

//--------------------------------------------------------------------------
// Input/Reference Data

#include "dataset2.h"
// #include "dataset1.h"
// #include "dataset_small.h"
#include "count_utils.h"
#include "sim_api.h"

#ifdef USE_RISCV_VECTOR

#include <riscv_vector.h>

void spmv(int r, const double* val, const uint64_t* idx, const double* x,
          const uint64_t* ptr, double* y)
{
  size_t vl = 0;
  size_t vlmax = vsetvlmax_e64m4();
  for (int i = 0; i < r; i++) {
    uint64_t    base_k   = ptr[i];
    uint64_t *idx_ptr  = (uint64_t *)&idx[base_k];
    uint64_t *val_ptr  = (uint64_t *)&val[ptr[i]];
    vfloat64m4_t v_y = vfmv_v_f_f64m4(0.0, vlmax);
    for (int c_n_count = ptr[i+1]-ptr[i]; c_n_count > 0; ) {
      vl = vsetvl_e64m4(c_n_count);
      vfloat64m4_t v_val_0, v_val_1;
      vuint64m4_t  v_idx_0, v_idx_1;
      vfloat64m4_t v_x_0  , v_x_1  ;

      v_val_0 = vle64_v_f64m4(val_ptr, vl);

      v_idx_0 = vle64_v_u64m4((const uint64_t *)idx_ptr, vl);
      v_idx_0 = vsll_vx_u64m4(v_idx_0, 3, vl);
      v_x_0   = vluxei64_v_f64m4(x, v_idx_0, vl);

      v_y = vfmacc_vv_f64m4(v_y, v_x_0, v_val_0, vl);

      idx_ptr += vl;
      val_ptr += vl;

      c_n_count -= vl;
    }
    vfloat64m1_t v_zero = vfmv_v_f_f64m1(0.0, vlmax);
    vfloat64m1_t v_y_m1 = vfredusum_vs_f64m4_f64m1 (v_y_m1, v_y, v_zero, vlmax);
    double y_i = vfmv_f_s_f64m1_f64 (v_y_m1);
    y[i] = y_i;
  }
}


#else // USE_RISCV_VECTOR
void spmv(int r, const double* val, const uint64_t* idx, const double* x,
          const uint64_t* ptr, double* y)
{
  for (int i = 0; i < r; i++)
  {
    int k;
    y[i] = 0.0;
    for (k = ptr[i]; k < ptr[i+1]; k++) {
      y[i] += val[k]*x[idx[k]];
    }
  }
}


// void spmv(int r, const double* val, const int* idx, const double* x,
//           const int* ptr, double* y)
// {
//   for (int i = 0; i < r; i++)
//   {
//     int k;
//     double yi0 = 0, yi1 = 0, yi2 = 0, yi3 = 0;
//     for (k = ptr[i]; k < ptr[i+1]-3; k+=4)
//     {
//       yi0 += val[k+0]*x[idx[k+0]];
//       yi1 += val[k+1]*x[idx[k+1]];
//       yi2 += val[k+2]*x[idx[k+2]];
//       yi3 += val[k+3]*x[idx[k+3]];
//     }
//     for ( ; k < ptr[i+1]; k++)
//     {
//       yi0 += val[k]*x[idx[k]];
//     }
//     y[i] = (yi0+yi1)+(yi2+yi3);
//   }
// }
//
#endif // USE_RISCV_VECTOR


//--------------------------------------------------------------------------
// Main

int __attribute__((optimize("O0"))) main()
{
  double y[R];

#if PREALLOCATE
#ifdef USE_RISCV_VECTOR
  spmv_vector(R, val, idx, x, ptr, y);
#else // USE_RISCV_VECTOR
  spmv(R, val, idx, x, ptr, y);
#endif // USE_RISCV_VECTOR
#endif

  long long start_cycle = get_cycle();
  long long start_vecinst = get_vecinst();

  SimRoiStart();
  start_konatadump();
#ifdef USE_RISCV_VECTOR
  spmv_vector(R, val, idx, x, ptr, y);
#else // USE_RISCV_VECTOR
  spmv(R, val, idx, x, ptr, y);
#endif // USE_RISCV_VECTOR
  SimRoiEnd();
  stop_konatadump();

  long long end_cycle = get_cycle();
  long long end_vecinst = get_vecinst();
  printf("cycles = %lld\n", end_cycle - start_cycle);
  printf("vecinst = %lld\n", end_vecinst - start_vecinst);

  int result = verifyDouble(R, y, verify_data);
  if (!result) {
    printf("Pass\n");
  } else {
    printf("Error\n");
  }
  return result;
}
