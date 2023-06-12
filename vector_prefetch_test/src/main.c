#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include "utils.h"
#include <stdint.h>

/*************************************************************************
*GET_TIME
*returns a long int representing the time
*************************************************************************/

#include <time.h>
#include <sys/time.h>

#include "sim_api.h"
#include "count_utils.h"

#include "../../common/vector_defines_m4.h"

long long get_time() {
    // struct timeval tv;
    // gettimeofday(&tv, NULL);
    // return (tv.tv_sec * 1000000) + tv.tv_usec;
  return 0;
}

// Returns the number of seconds elapsed between the two specified times
float elapsed_time(long long start_time, long long end_time) {
        return (float) (end_time - start_time) / (1000 * 1000);
}
/*************************************************************************/

#define ARRAY_SIZE (256 * 1024 / sizeof(uint64_t))
uint64_t load_region[ARRAY_SIZE];

int main(int argc, char *argv[])
{
    long long start_cycle = get_cycle();
    SimRoiStart();
    start_konatadump();

    uint64_t *p = load_region;

    long vlmax = __riscv_vsetvlmax_e64m8();

    for (int i = 0; i < ARRAY_SIZE; i+=vlmax) {
        asm volatile ("vle64.v v8, (%0)"::"r"(p));
        p+= vlmax;
    }

    SimRoiEnd();
    stop_konatadump();

    long long end_cycle = get_cycle();
    printf("cycles = %lld\n", end_cycle - start_cycle);
    return 0;
}
