#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include "utils.h" 

/*************************************************************************
*GET_TIME
*returns a long int representing the time
*************************************************************************/

#include <riscv_vector.h>

#include <time.h>
#include <sys/time.h>

#include "sim_api.h"
#include "count_utils.h"

long long get_time() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (tv.tv_sec * 1000000) + tv.tv_usec;
}
// Returns the number of seconds elapsed between the two specified times
float elapsed_time(long long start_time, long long end_time) {
        return (float) (end_time - start_time) / (1000 * 1000);
}
/*************************************************************************/

uint32_t global_region[1024];

void scatter_hit_test ()
{
    for (int i = 0; i < 1024; i+=64) {
    size_t vlmax = __riscv_vsetvlmax_e32m1();
    vuint32m1_t v_index = __riscv_vsll_vx_u32m1(__riscv_vid_v_u32m1(vlmax), 2, vlmax);
    __riscv_vsuxei32_v_u32m1 (global_region, v_index, v_index, vlmax);

    *(volatile uint32_t *)(global_region + i);
    }
}



int main(int argc, char *argv[])
{
    long long start,end;
    start = get_time();


    end = get_time();
    printf("init_vector time: %f\n", elapsed_time(start, end));

    scatter_hit_test();

    start = get_time();
    long long start_cycle = get_cycle();
    long long start_vecinst = get_vecinst();
    SimRoiStart();
    start_konatadump();
    scatter_hit_test();
    SimRoiEnd();
    stop_konatadump();

    long long end_cycle = get_cycle();
    long long end_vecinst = get_vecinst();
    end = get_time();
    printf ("done\n");

    return 0;
}
