#%%

import sqlite3

def get_sqlite_info(app, vlen, dlen, pipe_conf, l2_conf, l2_policy):
    file_str = '_%s/%s.v%s_d%s_%s_%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen, l2_conf, l2_policy)
    return get_sqlite_info_with_file (file_str)
    
def get_sqlite_info_dir (dir_name):
    return get_sqlite_info_with_file (dir_name + '/sim.stats.sqlite3')
    
def get_sqlite_info_with_file (file_str):
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



#%%

import pandas as pd
import utils as ut
import util_cycle as ut_c
import plotly.graph_objects as go
from IPython.display import display

pd.options.plotting.backend = "plotly"
pd.options.display.float_format = "{:.2f}".format

# pref_conf = ["stream-pref.v", "stride-pref.v", "vec-pref.v", "oracle-pref.v"]
pref_conf = ["stride-pref.v", "vec-pref.v", "oracle-pref.v"]
l2_conf = ["l2_none", "l2_stream", "l2_oracle"]
conf = ["none-pref.v", "ooo.s"] + pref_conf
benches = ut.benchmarks
# benches = ['jacobi-2d']

sql_info  = {l2: {d: {v: {b: {c: get_sqlite_info(b, v, d, c, l2, "l1d_pref_load") for c in conf} for b in benches} for v in [d*4]} for d in [128]} for l2 in l2_conf}
# sql_scalar_info = {b: get_sqlite_info_dir('_' + b + "/ooo.s") for b in benches}

df_prefetches = pd.DataFrame(index=benches)

def get_cycle(sql_info, app, pipe_conf, vlen, dlen, l2_conf):
    return sql_info[l2_conf][dlen][vlen][app][pipe_conf]['thread']['time_by_core[0]']['roi-end']
   
# Cycleのテーブルを作る

def make_summary_table(l2_conf):
    display("## Number of L1D Prefetch issued. " + l2_conf)
    display(df_prefetches)

    for c in conf:
        for b in benches:
            sql_info[l2_conf][128][512][b][c]['L1-D']['prefetches']['stop'] if 'prefetches' in sql_info[l2_conf][128][512][b][c]['L1-D'] else 0
        df_prefetches[c] = [sql_info[l2_conf][128][512][b][c]['L1-D']['prefetches']['stop'] if 'prefetches' in sql_info[l2_conf][128][512][b][c]['L1-D'] else 0 for b in benches]

    def get_cycle_with_app(app, vlen, dlen):
      return [get_cycle(sql_info, app, p, vlen, dlen, l2_conf) / 500000 for p in conf]

    df_cycle_v8_d2   = pd.DataFrame([get_cycle_with_app(b,  512, 128) for b in benches], columns=["V8-D2 "  + b for b in conf], index=benches)
    df_cycle_v8_d2_rate = (df_cycle_v8_d2["V8-D2 none-pref.v"].T / df_cycle_v8_d2.T).T
    df_cycle_v8_d2_rate.loc["Average"] = df_cycle_v8_d2_rate.mean()
    display(df_cycle_v8_d2)
    display(df_cycle_v8_d2_rate)
    fig = df_cycle_v8_d2_rate.plot.bar(barmode="group", title='Performance Improvement with ' + l2_conf)
    fig.show()

    # ベクトル・ロード・ストアのヒット・ミス率を出す
    num_vec_loads = [[sql_info[l2_conf][128][512][app][pipe_conf]['L1-D']['vec_loads']['roi-end'] if 'vec_loads' in sql_info[l2_conf][128][512][app][pipe_conf]['L1-D'] else 0 \
                        for pipe_conf in conf ] \
                        for app in benches]
    num_vec_stores = [[sql_info[l2_conf][128][512][app][pipe_conf]['L1-D']['vec_stores']['roi-end'] if 'vec_stores' in sql_info[l2_conf][128][512][app][pipe_conf]['L1-D'] else 0 \
                        for pipe_conf in conf] \
                        for app in benches]
    num_vec_load_misses = [[sql_info[l2_conf][128][512][app][pipe_conf]['L1-D']['vec_load-misses']['roi-end'] if 'vec_load-misses' in sql_info[l2_conf][128][512][app][pipe_conf]['L1-D'] else 0 \
                             for pipe_conf in conf] \
                             for app in benches]
    num_vec_store_misses = [[sql_info[l2_conf][128][512][app][pipe_conf]['L1-D']['vec_store-misses']['roi-end'] if 'vec_store-misses' in sql_info[l2_conf][128][512][app][pipe_conf]['L1-D'] else 0 \
                               for pipe_conf in conf] \
                               for app in benches]

    vec_access = pd.DataFrame(num_vec_loads, index=benches, columns=conf) + pd.DataFrame(num_vec_stores, index=benches, columns=conf)
    vec_misses = pd.DataFrame(num_vec_load_misses, index=benches, columns=conf) + pd.DataFrame(num_vec_store_misses, index=benches, columns=conf)
    vec_hit_rate = (vec_access - vec_misses) / vec_access
    vec_hit_rate.loc["Average"] = vec_hit_rate.mean()
    display(vec_hit_rate)
    fig = vec_hit_rate.plot.bar(barmode="group", title='Vector Memory Access L1D Hit Rate with ' + l2_conf)
    fig.show()

    # ロード・ストアのヒット・ミス率を出す
    num_loads = [[sql_info[l2_conf][128][512][app][pipe_conf]['L1-D']['loads']['roi-end'] \
                    for pipe_conf in conf ] \
                    for app in benches]
    num_stores = [[sql_info[l2_conf][128][512][app][pipe_conf]['L1-D']['stores']['roi-end'] \
                    for pipe_conf in conf] \
                    for app in benches]
    num_load_misses = [[sql_info[l2_conf][128][512][app][pipe_conf]['L1-D']['load-misses']['roi-end'] if 'load-misses' in sql_info[l2_conf][128][512][app][pipe_conf]['L1-D'] else 0 \
                         for pipe_conf in conf] \
                         for app in benches]
    num_store_misses = [[sql_info[l2_conf][128][512][app][pipe_conf]['L1-D']['store-misses']['roi-end'] if 'store-misses' in sql_info[l2_conf][128][512][app][pipe_conf]['L1-D'] else 0 \
                           for pipe_conf in conf] \
                           for app in benches]

    num_access = pd.DataFrame(num_loads,       index=benches, columns=conf) + pd.DataFrame(num_stores,       index=benches, columns=conf)
    num_misses = pd.DataFrame(num_load_misses, index=benches, columns=conf) + pd.DataFrame(num_store_misses, index=benches, columns=conf)
    all_hit_rate = (num_access - num_misses) / num_access
    all_hit_rate.loc["Average"] = all_hit_rate.mean()
    display(all_hit_rate)
    fig = all_hit_rate.plot.bar(barmode="group", title='All Memory Access L1D Hit Rate with ' + l2_conf)
    fig.show()


    # プリフェッチを生成した回数
    display("プリフェッチを生成した回数")
    df_prefetches_sum = df_prefetches.copy()
    df_prefetches_sum.loc["Sum"] = df_prefetches_sum.sum()
    display(df_prefetches_sum)

    # ロード・ストアの数に対する生成されたプリフェッチの数
    display("ロード・ストアの数に対する生成されたプリフェッチの数")
    display(num_access)
    pref_per_mem_access = df_prefetches / num_access
    pref_per_mem_access.loc["Average"] = pref_per_mem_access.mean()
    print(pref_per_mem_access)
    fig = (pref_per_mem_access).plot.bar(barmode="group", title='ロード・ストアの数に対する生成されたプリフェッチの数 ' + l2_conf)
    fig.show()

    # 無駄に出したプリフェッチを出す
    hit_prefetches = pd.DataFrame([[sql_info[l2_conf][128][512][b][c]['L1-D']['hits-prefetch']['stop'] if 'hits-prefetch' in \
                                    sql_info[l2_conf][128][512][b][c]['L1-D'] else 0 for c in conf] for b in benches],
                                  index=benches, columns=conf)
    prefetch_hit_rate = (hit_prefetches / df_prefetches)
    prefetch_hit_rate = prefetch_hit_rate.fillna(0.0)
    prefetch_hit_rate.loc["Average"] = prefetch_hit_rate.mean()
    # display(hit_prefetches)
    # display(df_prefetches)
    display(prefetch_hit_rate)
    fig = prefetch_hit_rate.plot.bar(barmode="group", title='Prefetch Useful Rate with ' + l2_conf)
    fig.show()

for l2 in l2_conf:
    make_summary_table(l2)    

#%%
# L2にStream Prefetcherを適用した場合とそうでない場合での性能向上を調べる

pref_conf = ["none-pref.v"]
l2_conf = ["l2_none", "l2_oracle"]
l1d_pref_policy = ["l1d_pref_load", "l1d_pref_keep"]
conf = pref_conf

sql_info  = {l1d: {l2: {d: {v: {b: {c: get_sqlite_info(b, v, d, c, l2, l1d) for c in conf} for b in benches} for v in [d*4]} 
                        for d in [128]} 
                   for l2 in l2_conf} 
             for l1d in l1d_pref_policy}

# df_prefetches = pd.DataFrame(index=benches)

stats = {l2 : sql_info["l1d_pref_load"][l2][128][512] for l2 in l2_conf}

df_cycle_v8_d2   = pd.DataFrame([[stats[p][b]['none-pref.v']['thread']['time_by_core[0]']['roi-end'] for p in l2_conf] for b in benches] , 
                                columns=["V8-D2 "  + c for c in l2_conf], index=benches)
df_cycle_v8_d2_rate = (df_cycle_v8_d2["V8-D2 l2_none"].T / df_cycle_v8_d2.T).T
df_cycle_v8_d2_rate.loc["Average"] = df_cycle_v8_d2_rate.mean()
display(df_cycle_v8_d2_rate)
fig = df_cycle_v8_d2_rate.plot.bar(barmode="group", title='Performance comparison with L2 without prefetching and L2 hit 100%')
fig.show()


# %%
# Vector-Prefetcherにて、L1へのロードを行った場合とL2へのKeepを行った場合の差分を調べる

import util_cycle as ut_c

pref_conf = ["vec-pref.v"]
l2_conf = ["l2_none"]
l1d_pref_policy = ["l1d_pref_load", "l1d_pref_keep"]
conf = pref_conf

sql_info  = {l1d: {l2: {d: {v: {b: {c: get_sqlite_info(b, v, d, c, l2, l1d) for c in conf} for b in benches} for v in [d*4]} 
                        for d in [128]} 
                   for l2 in l2_conf} 
             for l1d in l1d_pref_policy}

# df_prefetches = pd.DataFrame(index=benches)

stats = {l1d : sql_info[l1d]["l2_none"][128][512] for l1d in l1d_pref_policy}

df_cycle_v8_d2   = pd.DataFrame([[stats[p][b]['vec-pref.v']['thread']['time_by_core[0]']['roi-end'] for p in l1d_pref_policy] for b in benches] , 
                                columns=["V8-D2 "  + c for c in l1d_pref_policy], index=benches)
df_cycle_v8_d2_rate = (df_cycle_v8_d2["V8-D2 l1d_pref_load"].T / df_cycle_v8_d2.T).T
df_cycle_v8_d2_rate.loc["Average"] = df_cycle_v8_d2_rate.mean()
display(df_cycle_v8_d2_rate)
fig = df_cycle_v8_d2_rate.plot.bar(barmode="group", title='Performance Improvement of L1D keep from L1D Load')
fig.show()

# %%
# プリフェッチを生成した回数を調べる

import pandas as pd
import utils as ut
import util_cycle as ut_c
import plotly.graph_objects as go
from IPython.display import display

pd.options.plotting.backend = "plotly"
pd.options.display.float_format = "{:.2f}".format

pref_conf = ["vec-pref.v"]
conf = pref_conf
l2_conf = ["l2_stream"]

sql_info  = {l2: {d: {v: {b: {c: get_sqlite_info(b, v, d, c, l2, "l1d_pref_keep") for c in conf} for b in benches} for v in [d*4]} 
                        for d in [128]} 
                   for l2 in l2_conf}

# プリフェッチを生成した回数
display("プリフェッチを生成した回数")
df_prefetches = [sql_info['l2_stream'][128][512][b]['vec-pref.v']['L2']['prefetches']['stop'] \
    if 'prefetches' in sql_info['l2_stream'][128][512][b]['vec-pref.v']['L2'] else 0 for b in benches]
display(df_prefetches)

# 無駄に出したプリフェッチを出す
hit_prefetches = [sql_info['l2_stream'][128][512][b]['vec-pref.v']['L2']['hits-prefetch']['stop'] \
        if 'hits-prefetch' in sql_info['l2_stream'][128][512][b]['vec-pref.v']['L2'] else 0 for b in benches]
display(hit_prefetches)

prefetch_hit_rate = pd.DataFrame((pd.DataFrame(hit_prefetches, index=benches) / pd.DataFrame(df_prefetches, index=benches)),
                                 index=benches)
display(prefetch_hit_rate, )
# %%
