#%%

import os
import glob

import pandas as pd

pipe_conf = ['vio.v.fence', 'vio.v.lsu-inorder', 'vio.v.ngs', 'vio.v', 'ooo.v']
pipe_conf2 = ['SV Fence', 'SV MEM Fence', 'Prop1', 'PROP', 'BASE']
conf_filename = {'SV Fence': 'vio.v.fence', 
                 'SV MEM Fence': 'vio.v.lsu-inorder', 
                 'Prop1': 'vio.v.ngs', 
                 'PROP': 'vio.v', 
                 'BASE': 'ooo.v'
                 }
d2_index2 = ['V%d-D2 %s' % (v, c) for v in [2,4,8,16] for c in pipe_conf2]
d4_index2 = ['V%d-D4 %s' % (v, c) for v in [4,8,16,32] for c in pipe_conf2]

rivec_benchmarks = [
    'axpy', 
    'blackscholes', 
    'canneal', 
    'jacobi-2d', 
    'particlefilter', 
    'pathfinder', 
    'streamcluster',
    'swaptions'
]

benchmarks = rivec_benchmarks + [
    'spmv', 
    'fftw3'
]

bench_and_dhry = benchmarks + ['dhrystone']

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
e_elem['SV Fence'] = dict()
e_elem['SV Fence']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['SV Fence']['Rename'] = ['s_ooo:Renaming_Unit']
e_elem['SV Fence']['Scheduler'] = ['s_ooo:Instruction_Window',
                                      's_ooo:FP_Instruction_Window',
                                      's_ooo:ROB']
e_elem['SV Fence']['Scalar FU + RF']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['SV Fence']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                        ]
e_elem['SV Fence']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['SV Fence']['Vecotr RF'] = ['v_ino:Register_Files']
e_elem['SV Fence']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['SV Fence']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', '-s_ooo:Data_Cache']
e_elem['SV Fence']['Vector LSU'] = ['v_ooo:Load_Store_Unit', '-v_ooo:LoadQ', '-v_ooo:StoreQ', '-v_ooo:Data_Cache']

# -----------------------------
# Vector In-order / Scalar LSU InOrder
# -----------------------------
e_elem['SV MEM Fence'] = dict()
e_elem['SV MEM Fence']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['SV MEM Fence']['Rename'] = ['s_ooo:Renaming_Unit']
e_elem['SV MEM Fence']['Scheduler'] = ['s_ooo:Instruction_Window',
                                            's_ooo:FP_Instruction_Window',
                                            's_ooo:ROB']
e_elem['SV MEM Fence']['Scalar FU + RF']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                            's_ooo:Integer_ALUs__Count',
                                            's_ooo:Results_Broadcast_Bus',
                                            's_ooo:Register_Files']
# e_elem['SV MEM Fence']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                  'v_ooo:Results_Broadcast_Bus']
e_elem['SV MEM Fence']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['SV MEM Fence']['Vecotr RF'] = ['v_ino:Register_Files']
e_elem['SV MEM Fence']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['SV MEM Fence']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', '-s_ooo:Data_Cache']
e_elem['SV MEM Fence']['Vector LSU'] = ['v_ooo:Load_Store_Unit', '-v_ooo:LoadQ', '-v_ooo:StoreQ', '-v_ooo:Data_Cache']

# -----------------------------
# with Porposal and Non-GatherScatter Merge
# -----------------------------
e_elem['Prop1'] = dict()
e_elem['Prop1']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['Prop1']['Rename'] = ['s_ooo:Renaming_Unit']
e_elem['Prop1']['Scheduler'] = ['s_ooo:Instruction_Window',
                                  's_ooo:FP_Instruction_Window',
                                  's_ooo:ROB']
e_elem['Prop1']['Scalar FU + RF']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['Prop1']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                      'v_ooo:Results_Broadcast_Bus']
e_elem['Prop1']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['Prop1']['Vecotr RF'] = ['v_ino:Register_Files']
e_elem['Prop1']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['Prop1']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', 'v_to_s_ngs:LoadQ', '-s_ooo:Data_Cache']
e_elem['Prop1']['Vector LSU'] = ['v_ooo:Load_Store_Unit', '-v_ooo:LoadQ', '-v_ooo:StoreQ', '-v_ooo:Data_Cache']

# -------------------------
# Proposal
# -------------------------
e_elem['PROP'] = dict()
e_elem['PROP']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['PROP']['Rename'] = ['s_ooo:Renaming_Unit']
e_elem['PROP']['Scheduler'] = ['s_ooo:Instruction_Window',
                                  's_ooo:FP_Instruction_Window',
                                  's_ooo:ROB']
e_elem['PROP']['Scalar FU + RF']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['PROP']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                  'v_ooo:Results_Broadcast_Bus']
e_elem['PROP']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['PROP']['Vecotr RF'] = ['v_ino:Register_Files']
e_elem['PROP']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['PROP']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', 'v_to_s:LoadQ', '-s_ooo:Data_Cache']
e_elem['PROP']['Vector LSU'] = ['v_ooo:Load_Store_Unit', '-v_ooo:LoadQ', '-v_ooo:StoreQ', '-v_ooo:Data_Cache']

# -------------------------
# All-OoO
# -------------------------
e_elem['BASE'] = dict()
e_elem['BASE']['Fetch']  = ['s_ooo:Instruction_Fetch_Unit']
e_elem['BASE']['Rename'] = ['s_ooo:Renaming_Unit',
                              'v_ooo:Renaming_Unit']
e_elem['BASE']['Scheduler'] = ['s_ooo:Instruction_Window',
                                's_ooo:FP_Instruction_Window',
                                'v_ooo:FP_Instruction_Window',
                                's_ooo:ROB']
e_elem['BASE']['Scalar FU + RF']  = ['s_ooo:Floating_Point_Units__FPUs___Count',
                                 's_ooo:Integer_ALUs__Count',
                                 's_ooo:Results_Broadcast_Bus',
                                 's_ooo:Register_Files']
# e_elem['BASE']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count',
#                                  'v_ooo:Results_Broadcast_Bus']
e_elem['BASE']['Vector FU']  = ['v_ooo:Floating_Point_Units__FPUs___Count']
e_elem['BASE']['Vecotr RF'] = ['v_ooo:Register_Files']
e_elem['BASE']['L1D Cache'] = ['dcache:Data_Cache']
e_elem['BASE']['Scalar LSU'] = ['s_ooo:Load_Store_Unit', 's_ooo:Memory_Management_Unit', 'v_to_s:LoadQ', 'v_to_s:StoreQ', '-s_ooo:Data_Cache']
e_elem['BASE']['Vector LSU'] = ['v_ooo:Load_Store_Unit', 's_to_v:LoadQ', 's_to_v:StoreQ', '-v_ooo:Data_Cache']

# ------------------------------------
# 各モジュールにおいて、スケールを決める
# ------------------------------------
area_scale = dict()
area_scale['v128_d128']  = {'Vecotr RF': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
area_scale['v256_d128']  = {'Vecotr RF': 2.0,  'Vector FU': 1.0, 'L1D Cache': 2}
area_scale['v512_d128']  = {'Vecotr RF': 4.0,  'Vector FU': 1.0, 'L1D Cache': 2}
area_scale['v1024_d128'] = {'Vecotr RF': 8.0,  'Vector FU': 1.0, 'L1D Cache': 2}
area_scale['v256_d256']  = {'Vecotr RF': 2.0,  'Vector FU': 2.0, 'L1D Cache': 2}
area_scale['v512_d256']  = {'Vecotr RF': 4.0,  'Vector FU': 2.0, 'L1D Cache': 2}
area_scale['v1024_d256'] = {'Vecotr RF': 8.0,  'Vector FU': 2.0, 'L1D Cache': 2}
area_scale['v2048_d256'] = {'Vecotr RF': 16.0, 'Vector FU': 2.0, 'L1D Cache': 2}

energy_scale = dict()
energy_scale['v128_d128']  = {'Vecotr RF': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
energy_scale['v256_d128']  = {'Vecotr RF': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
energy_scale['v512_d128']  = {'Vecotr RF': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
energy_scale['v1024_d128'] = {'Vecotr RF': 1.0,  'Vector FU': 1.0, 'L1D Cache': 2}
energy_scale['v256_d256']  = {'Vecotr RF': 1.0,  'Vector FU': 2.0, 'L1D Cache': 2}
energy_scale['v512_d256']  = {'Vecotr RF': 1.0,  'Vector FU': 2.0, 'L1D Cache': 2}
energy_scale['v1024_d256'] = {'Vecotr RF': 1.0,  'Vector FU': 2.0, 'L1D Cache': 2}
energy_scale['v2048_d256'] = {'Vecotr RF': 1.0,  'Vector FU': 2.0, 'L1D Cache': 2}

#%%
from itertools import chain

keys = list(e_elem['BASE'].keys())
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

#%%

import sqlite3

def get_sqlite_info(app, vlen, dlen, pipe_conf):
    file_str = '_%s/%s.v%s_d%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen)
    print("Opening %s ..." % (file_str))
    try:
        sql3_conn = sqlite3.connect(file_str)
    except sqlite3.OperationalError:
        print ('sqlite3 file error ' + file_str)
        exit()

    prefix = sql3_conn.execute("SELECT * FROM 'prefixes'").fetchall()
    names  = sql3_conn.execute("SELECT * FROM 'names'").fetchall()
    values = sql3_conn.execute("SELECT * FROM 'values'").fetchall()
      
    sql_dict = dict()
    for elem in values:
        prefix_id  = elem[0]
        id         = elem[1]
        # ore_id = elem[2]
        value     = elem[3]
        
        assert(names[id-1][0] == id)
        module = names[id-1][1]
        info_name = names[id-1][2]
        if not sql_dict.get(module):
            sql_dict[module] = dict()
        if not sql_dict[module].get(info_name):
            sql_dict[module][info_name] = dict()
        sql_dict[module][info_name][prefix[prefix_id-1][1]] = value
     
    return sql_dict

# %%
