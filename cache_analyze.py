#!/usr/bin/python3

import lzma
import sys
import re

args = sys.argv

f = lzma.open(args[1])
# f = open(args[1])

trace_enable = False

class cache_info_t:
    cycle = 0
    hit = False
    rw = "/"
    vec_access = False

    def clear(self):
        self.cycle = 0
        self.hit = False

l1_access_hist = dict()
l2_access_hist = dict()
current_cycle = 0

current_l1d_address = 0
current_l2_address = 0

# debug_target = 0x39000
debug_target = 0x0001b080

for s_line in f:

    s_line = s_line.decode()
    # if trace_enable == True:
    #     print(repr(s_line))

    # trace_enable == False and
    match = re.match('CycleTrace (\d+)', s_line)
    if match != None:
        trace_enable = not trace_enable
        print(match.groups()[0])

    if trace_enable == False:
        continue

    state = ''

    match = re.match('Running cycles (\d+)', s_line)
    if match != None:
        current_cycle = int(match.groups()[0])
        # print("cycle = %d" % (current_cycle)

    match = re.search('^l1_dcache (R|W)  ([\da-f]+)\+\d+..\+(\d+)', s_line)
    if match != None:
        current_l1d_address = int(match.groups()[1], 16)
        rw = match.groups()[0]
        # print("current_l1d_address = %08x" % (current_l1d_address))

        if l1_access_hist.get(current_l1d_address) == None:
            l1_access_hist[current_l1d_address] = []
        l1d_info = cache_info_t()
        l1d_info.rw = rw
        l1d_info.cycle = current_cycle
        size = int(match.groups()[2], 16)
        if not (size == 8 or size == 4 or size == 2 or size == 1):
            l1d_info.vec_access = True
        l1_access_hist[current_l1d_address].append(l1d_info)

        if debug_target == current_l1d_address:
            print("%d L1D cache RW = {addr:%08x}" % (current_cycle, current_l1d_address))

    match = re.search('l1_dcache L1 (miss|hit)', s_line)
    if match != None:
        l1_access_hist[current_l1d_address][-1].hit = True if match.groups()[0] == "hit" else False

    match = re.search('l1_dcache insertCacheBlock l3. @ ([\da-f]+) as ', s_line)

    match = re.search('l1_dcache evicting @([\da-f]+) \(state ', s_line)
    if match != None:
        evict_address = int(match.groups()[0], 16)
        if l1_access_hist.get(evict_address) == None:
            l1_access_hist[evict_address] = []
        l1d_info = cache_info_t()
        l1d_info.rw = "E"
        l1d_info.cycle = current_cycle
        size = 32
        if not (size == 8 or size == 4 or size == 2 or size == 1):
            l1d_info.vec_access = True
        l1_access_hist[evict_address].append(l1d_info)

        if debug_target == evict_address:
            print("%d L1D cache Evict = {addr:%08x}" % (current_cycle, evict_address))

    match = re.search('l1_dcache prefetching ([\da-f]+)', s_line)
    if match != None:
        prefetch_address = int(match.groups()[0], 16)
        if l1_access_hist.get(prefetch_address) == None:
            l1_access_hist[prefetch_address] = []
        l1d_info = cache_info_t()
        l1d_info.rw = "P"
        l1d_info.cycle = current_cycle
        size = 32
        if not (size == 8 or size == 4 or size == 2 or size == 1):
            l1d_info.vec_access = True
        l1_access_hist[prefetch_address].append(l1d_info)

        if debug_target == prefetch_address:
            print("%d L1D cache Prefetch = {addr:%08x}" % (current_cycle, prefetch_address))

    # if re.search('l1_dcache access done', s_line) != None:
    #     print("%d L1D cache = {addr:%08x, result:%s}" % \
    #           (l1_access_hist[current_l1d_address][-1].cycle,
    #            "Hit " if l1_access_hist[current_l1d_address][-1].hit else "Miss",
    #            l1_access_hist[current_l1d_address][-1].evict_address))

    match = re.search('l2_cache address ([\da-f]+) state', s_line)
    if match != None:
        current_l2_address = int(match.groups()[0], 16)
        if l2_access_hist.get(current_l2_address) == None:
            l2_access_hist[current_l2_address] = []
        l2d_info = cache_info_t()
        l2d_info.cycle = current_cycle
        l2_access_hist[current_l2_address].append(l2d_info)

    match = re.search('l2_cache Yay, hit!!', s_line)
    if match != None:
        l2_access_hist[current_l2_address][-1].hit = True

    match = re.search('l2_cache evicting @([\da-f]+) \(state ', s_line)
    if match != None:
        l2_access_hist[current_l2_address][-1].evict = int(match.groups()[0], 16)

    # match = re.search('l2_cache returning L2', s_line)
    # if match != None:
    #     print("%d L2  cache = {addr:%08x, result:%s, evict:%08x}" % \
    #           (l2_access_hist[current_l2_address][-1].cycle,
    #            "Hit " if l2_access_hist[current_l2_address][-1].hit else "Miss",
    #            l2_access_hist[current_l2_address][-1].evict_address))

total_scalar_hit_count  = 0
total_scalar_miss_count = 0
total_vector_hit_count  = 0
total_vector_miss_count = 0

l1_access_hist = sorted(l1_access_hist.items())

for k, l in l1_access_hist:

    scalar_hit_count  = 0
    scalar_miss_count = 0
    vector_hit_count  = 0
    vector_miss_count = 0

    print("%08x : %3d times : " % (k, len(l)), end='')
    for hist in l:
        if hist.rw == "P" or hist.rw == "E" :
            continue
        if not hist.vec_access and hist.hit:
            total_scalar_hit_count += 1
            scalar_hit_count += 1
        elif not hist.vec_access and not hist.hit:
            total_scalar_miss_count += 1
            scalar_miss_count += 1
        elif hist.vec_access and hist.hit:
            total_vector_hit_count += 1
            vector_hit_count += 1
        elif hist.vec_access and not hist.hit:
            total_vector_miss_count += 1
            vector_miss_count += 1

    print(" H=%3d,M=%3d " % (scalar_hit_count + vector_hit_count,
                             scalar_miss_count + vector_miss_count), end='')

    for hist in l:
        if hist.rw == "P" or hist.rw == "E":
            print("_", end='')
        else:
            print("%s" % ('V' if hist.vec_access else 'S'), end='')
    print(",", end='')
    for hist in l:
        if hist.rw == "P" or hist.rw == "E":
            print("_", end='')
        else:
            print("%s" % ('H' if hist.hit else 'M'), end='')
    print(",", end='')
    for hist in l:
        print("%s" % (hist.rw), end='')

    print("")

print("-------------------------")
print("ScalarHit=%d, ScalarMiss=%d, VectorHit=%d, VectorMiss=%d" % (total_scalar_hit_count, total_scalar_miss_count, total_vector_hit_count, total_vector_miss_count))
print("ScalarHitRate=%f, VectorHitRate=%f" % (total_scalar_hit_count / (total_scalar_hit_count + total_scalar_miss_count) if total_scalar_hit_count + total_scalar_miss_count != 0 else 0.0,
                                              total_vector_hit_count / (total_vector_hit_count + total_vector_miss_count) if total_vector_hit_count + total_vector_miss_count != 0 else 0.0))

f.close()
