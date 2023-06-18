#%%

import os
import glob

import pandas as pd

pipe_conf = ['vio.v.fence', 'vio.v.lsu-inorder', 'vio.v.ngs', 'vio.v', 'ooo.v']
pipe_conf2 = ['Fence', 'LSUInO', 'NoMerge', 'Proposal', 'OoO']
d2_index2 = ['V%d-D2 %s' % (v, c) for v in [2,4,8,16] for c in pipe_conf2]
d4_index2 = ['V%d-D4 %s' % (v, c) for v in [4,8,16,32] for c in pipe_conf2]

rivec_benchmarks = ['axpy', 
              'blackscholes', 
              'canneal', 
              'jacobi-2d', 
              'particlefilter', 
              'pathfinder', 
              'streamcluster',
              'swaptions']

benchmarks = rivec_benchmarks + ['spmv', 
                                 'fftw3'
]


def load_csv(conf, app="axpy"):
    base_dir = "_" + app + "/%s/" % conf

    csv_data = dict()
    if os.path.isfile(base_dir  + 'scalar_ooo/sim.stats.mcpat.output.csv'):
        csv_data['s_ooo'] = pd.read_csv(base_dir  + 'scalar_ooo/sim.stats.mcpat.output.csv',    header=None).T.dropna()
        csv_data['s_ooo'].columns=['name', 'value']
    else:
        print("CRITICAL WARNING : " + base_dir + " scalar_ooo/sim.stats.mcpat.output.csv not found")
        
    if os.path.isfile(base_dir  + 'scalar_ino/sim.stats.mcpat.output.csv'):
        csv_data['s_ino'] = pd.read_csv(base_dir  + 'scalar_ino/sim.stats.mcpat.output.csv',    header=None).T.dropna()
        csv_data['s_ino'].columns=['name', 'value']
    else:
        print("CRITICAL WARNING : " + base_dir + " scalar_ino/sim.stats.mcpat.output.csv not found")

    if os.path.isfile(base_dir  + 'vec_ooo/sim.stats.mcpat.output.csv'):
        csv_data['v_ooo']  = pd.read_csv(base_dir  + 'vec_ooo/sim.stats.mcpat.output.csv',       header=None).T.dropna()
        csv_data['v_ooo'].columns=['name', 'value']
    else:
        print("CRITICAL WARNING : " + base_dir + " vec_ooo/sim.stats.mcpat.output.csv not found")
        
    if os.path.isfile(base_dir  + 'vec_ino/sim.stats.mcpat.output.csv'):
        csv_data['v_ino']  = pd.read_csv(base_dir  + 'vec_ino/sim.stats.mcpat.output.csv',       header=None).T.dropna()
        csv_data['v_ino'].columns=['name', 'value']
    else:
        print("CRITICAL WARNING : " + base_dir + " vec_ino/sim.stats.mcpat.output.csv not found")

    if os.path.isfile(base_dir  + 'vec_to_scalar/sim.stats.mcpat.output.csv'):
        csv_data['v_to_s'] = pd.read_csv(base_dir  + 'vec_to_scalar/sim.stats.mcpat.output.csv', header=None).T.dropna()
        csv_data['v_to_s'].columns=['name', 'value']

    if os.path.isfile(base_dir  + 'v_to_s_ngs/sim.stats.mcpat.output.csv'):
        csv_data['v_to_s_ngs'] = pd.read_csv(base_dir  + 'v_to_s_ngs/sim.stats.mcpat.output.csv', header=None).T.dropna()
        csv_data['v_to_s_ngs'].columns=['name', 'value']
    else:
        print(base_dir + " v_to_s_ngs not found")

    if os.path.isfile(base_dir  + 'scalar_to_vec/sim.stats.mcpat.output.csv'):
        csv_data['s_to_v'] = pd.read_csv(base_dir  + 'scalar_to_vec/sim.stats.mcpat.output.csv', header=None).T.dropna()
        csv_data['s_to_v'].columns=['name', 'value']
    else:
        print("CRITICAL WARNING : " + base_dir + " scalar_to_vec not found")
    
    if os.path.isfile(base_dir  + 'dcache/sim.stats.mcpat.output.csv'):
        csv_data['dcache'] = pd.read_csv(base_dir  + 'dcache/sim.stats.mcpat.output.csv', header=None).T.dropna()
        csv_data['dcache'].columns=['name', 'value']
    else:
        print("CRITICAL WARNING : " + base_dir + " dcache not found")
    
    return csv_data


# 面積算出のための構成要素群

e_elem = dict()

# -------------------------
# with Vector/Scalar Fence
# -------------------------
e_elem['vio.v.fence'] = dict()
e_elem['vio.v.fence']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['vio.v.fence']['Rename'] = ['s_ooo:Renaming_Unit']
e_elem['vio.v.fence']['Scheduler'] = ['s_ooo:Instruction_Window',
                                      's_ooo:FP_Instruction_Window',
                                      's_ooo:ROB']
e_elem['vio.v.fence']['Scalar FU']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['vio.v.fence']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                        ]
e_elem['vio.v.fence']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['vio.v.fence']['Vector Registers'] = ['v_ino:Register_Files']
e_elem['vio.v.fence']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['vio.v.fence']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', '-s_ooo:Data_Cache']
e_elem['vio.v.fence']['Vector LSU'] = ['v_ooo:Load_Store_Unit', '-v_ooo:LoadQ', '-v_ooo:StoreQ', '-v_ino:Data_Cache']

# -----------------------------
# Vector In-order / Scalar LSU InOrder
# -----------------------------
e_elem['vio.v.lsu-inorder'] = dict()
e_elem['vio.v.lsu-inorder']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['vio.v.lsu-inorder']['Rename'] = ['s_ooo:Renaming_Unit',
                              'v_ooo:Renaming_Unit']
e_elem['vio.v.lsu-inorder']['Scheduler'] = ['s_ooo:Instruction_Window',
                                's_ooo:FP_Instruction_Window',
                                'v_ooo:FP_Instruction_Window',
                                's_ooo:ROB']
e_elem['vio.v.lsu-inorder']['Scalar FU']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['vio.v.lsu-inorder']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                  'v_ooo:Results_Broadcast_Bus']
e_elem['vio.v.lsu-inorder']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['vio.v.lsu-inorder']['Vector Registers'] = ['v_ooo:Register_Files']
e_elem['vio.v.lsu-inorder']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['vio.v.lsu-inorder']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', '-s_ooo:Data_Cache']
e_elem['vio.v.lsu-inorder']['Vector LSU'] = ['v_ooo:Load_Store_Unit', '-v_ooo:Data_Cache']

# -----------------------------
# with Porposal and Non-GatherScatter Merge
# -----------------------------
e_elem['vio.v.ngs'] = dict()
e_elem['vio.v.ngs']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['vio.v.ngs']['Rename'] = ['s_ooo:Renaming_Unit']
e_elem['vio.v.ngs']['Scheduler'] = ['s_ooo:Instruction_Window',
                                  's_ooo:FP_Instruction_Window',
                                  's_ooo:ROB']
e_elem['vio.v.ngs']['Scalar FU']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['vio.v.ngs']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                      'v_ooo:Results_Broadcast_Bus']
e_elem['vio.v.ngs']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['vio.v.ngs']['Vector Registers'] = ['v_ino:Register_Files']
e_elem['vio.v.ngs']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['vio.v.ngs']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', 'v_to_s_ngs:LoadQ', '-s_ooo:Data_Cache']
e_elem['vio.v.ngs']['Vector LSU'] = ['v_ooo:Load_Store_Unit', '-v_ooo:LoadQ', '-v_ooo:StoreQ', '-v_ino:Data_Cache']

# -------------------------
# Proposal
# -------------------------
e_elem['vio.v'] = dict()
e_elem['vio.v']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['vio.v']['Rename'] = ['s_ooo:Renaming_Unit']
e_elem['vio.v']['Scheduler'] = ['s_ooo:Instruction_Window',
                                  's_ooo:FP_Instruction_Window',
                                  's_ooo:ROB']
e_elem['vio.v']['Scalar FU']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['vio.v']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                  'v_ooo:Results_Broadcast_Bus']
e_elem['vio.v']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['vio.v']['Vector Registers'] = ['v_ino:Register_Files']
e_elem['vio.v']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['vio.v']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', 'v_to_s:LoadQ', '-s_ooo:Data_Cache']
e_elem['vio.v']['Vector LSU'] = ['v_ooo:Load_Store_Unit', '-v_ooo:LoadQ', '-v_ooo:StoreQ', '-v_ino:Data_Cache']

# -------------------------
# All-OoO
# -------------------------
e_elem['ooo.v'] = dict()
e_elem['ooo.v']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['ooo.v']['Rename'] = ['s_ooo:Renaming_Unit',
                              'v_ooo:Renaming_Unit']
e_elem['ooo.v']['Scheduler'] = ['s_ooo:Instruction_Window',
                                's_ooo:FP_Instruction_Window',
                                'v_ooo:FP_Instruction_Window',
                                's_ooo:ROB']
e_elem['ooo.v']['Scalar FU']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['ooo.v']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                  'v_ooo:Results_Broadcast_Bus']
e_elem['ooo.v']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['ooo.v']['Vector Registers'] = ['v_ooo:Register_Files']
e_elem['ooo.v']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['ooo.v']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', 'v_to_s:LoadQ', 'v_to_s:StoreQ', '-s_ooo:Data_Cache']
e_elem['ooo.v']['Vector LSU'] = ['v_ooo:Load_Store_Unit', 's_to_v:LoadQ', 's_to_v:StoreQ', '-v_ooo:Data_Cache']

# ------------------------------------
# 各モジュールにおいて、スケールを決める
# ------------------------------------
area_scale = dict()
area_scale['v128_d128']  = {'Vector Registers': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
area_scale['v256_d128']  = {'Vector Registers': 2.0,  'Vector FU': 1.0, 'L1D Cache': 2}
area_scale['v512_d128']  = {'Vector Registers': 4.0,  'Vector FU': 1.0, 'L1D Cache': 2}
area_scale['v1024_d128'] = {'Vector Registers': 8.0,  'Vector FU': 1.0, 'L1D Cache': 2}
area_scale['v256_d256']  = {'Vector Registers': 2.0,  'Vector FU': 2.0, 'L1D Cache': 2}
area_scale['v512_d256']  = {'Vector Registers': 4.0,  'Vector FU': 2.0, 'L1D Cache': 2}
area_scale['v1024_d256'] = {'Vector Registers': 8.0,  'Vector FU': 2.0, 'L1D Cache': 2}
area_scale['v2048_d256'] = {'Vector Registers': 16.0, 'Vector FU': 2.0, 'L1D Cache': 2}

energy_scale = dict()
energy_scale['v128_d128']  = {'Vector Registers': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
energy_scale['v256_d128']  = {'Vector Registers': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
energy_scale['v512_d128']  = {'Vector Registers': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
energy_scale['v1024_d128'] = {'Vector Registers': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
energy_scale['v256_d256']  = {'Vector Registers': 1.0,  'Vector FU': 2.0, 'L1D Cache': 2}
energy_scale['v512_d256']  = {'Vector Registers': 1.0,  'Vector FU': 2.0, 'L1D Cache': 2}
energy_scale['v1024_d256'] = {'Vector Registers': 1.0,  'Vector FU': 2.0, 'L1D Cache': 2}
energy_scale['v2048_d256'] = {'Vector Registers': 1.0,  'Vector FU': 2.0, 'L1D Cache': 2}

#%%
from itertools import chain

keys = list(e_elem['ooo.v'].keys())
l = []
for k in keys:
    p = []
    for c in e_elem:
        p = p + list(e_elem[c][k])
    l = l + list(set(p))
elem_index = l




def get_cycle_rate_with_app(app, vlen, dlen):
    cycle_list = list(map(lambda p: get_cycle(app, p, vlen, dlen), pipe_conf))
    return list(map(lambda e: cycle_list[3] / e, cycle_list))

def get_cycle_rate_with_vlen_dlen(vlen, dlen):
    return list(map(lambda b: get_cycle_rate_with_app(b, vlen, dlen), benchmarks))
