#%%
# 面積を算出

import pandas as pd
import matplotlib.pyplot as plt
import utils as ut
import util_area as ut_a
import util_cycle as ut_c
import util_power as ut_p
import numpy as np


df_area_v2_d2 = pd.DataFrame(ut_a.calc_group_area("v128_d128"))
df_area_v8_d2 = pd.DataFrame(ut_a.calc_group_area("v512_d128"))
df_area_v8_d8 = pd.DataFrame(ut_a.calc_group_area("v512_d512"))

df_area_whole = pd.concat([df_area_v2_d2, df_area_v8_d2, df_area_v8_d8], axis=1)

display(df_area_whole)
# df_area_whole = df_area_whole.reindex(elem_index)
df_area_whole.columns = ['V2-D2 Fence', 'V2-D2 NoMerge', 'V2-D2 Proposal', 'V2-D2 OoO',
                          'V8-D2 Fence', 'V8-D2 NoMerge', 'V8-D2 Proposal', 'V8-D2 OoO',
                          'V8-D8 Fence', 'V8-D8 NoMerge', 'V8-D8 Proposal', 'V8-D8 OoO',]
display(df_area_whole)
df_area_whole.T.plot.bar(title="Area estimation with each configuration", 
                         stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.xticks(rotation=45)
plt.savefig("area.pdf", bbox_inches='tight')
plt.savefig("area.png", bbox_inches='tight')

#%%
# Cycleのテーブルを作る

import pandas as pd
import utils as ut
import util_cycle as ut_c

def get_cycle_with_app(app, vlen, dlen):
    return list(map(lambda p: ut_c.get_cycle(app, p, vlen, dlen) / 100000, ut.pipe_conf))
    
df_cycle_v2_d2 = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 128, 128), ut.benchmarks)), 
                                  columns=(map(lambda b: "V2-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)

df_cycle_v8_d2 = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 512, 128), ut.benchmarks)), 
                                  columns=(map(lambda b: "V8-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)

df_cycle_v8_d8 = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 512, 512), ut.benchmarks)), 
                                  columns=(map(lambda b: "V8-D8 " + b, ut.pipe_conf)), index=ut.benchmarks)


#%%
# 全体的な性能グラフを作る

df_cycle_whole = pd.concat([df_cycle_v2_d2, df_cycle_v8_d2, df_cycle_v8_d8], axis=1)
df_cycle_whole.columns = ['V2-D2 Fence', 'V2-D2 NoMerge', 'V2-D2 Proposal', 'V2-D2 OoO',
                          'V8-D2 Fence', 'V8-D2 NoMerge', 'V8-D2 Proposal', 'V8-D2 OoO',
                          'V8-D8 Fence', 'V8-D8 NoMerge', 'V8-D8 Proposal', 'V8-D8 OoO',]

df_cycle_whole_pct = np.reciprocal((df_cycle_whole.T / df_cycle_v2_d2["V2-D2 vio.v.fence"].T).T)
df_cycle_means = df_cycle_whole_pct.mean()
plt.figure()
df_cycle_means.plot.bar(title="Relative Cycle", figsize=(10, 3))
plt.savefig("relative_performance.pdf", bbox_inches='tight')

#%%
# V8-D2のサイクル数でグラフを作る

import pandas as pd
import util_power as ut_p

v2_d2_power = ut_p.get_power_with_vlen_dlen(128, 128)
df_power_detail_v2_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v2_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v2_d2.columns = list(map(lambda b: "V2-D2 " + b, ut.pipe_conf))
df_power_detail_v2_d2.index = ut.benchmarks

v8_d2_power = ut_p.get_power_with_vlen_dlen(512, 128)
df_power_detail_v8_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v8_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v8_d2.columns = list(map(lambda b: "V8-D2 " + b, ut.pipe_conf))
df_power_detail_v8_d2.index = ut.benchmarks

v8_d8_power = ut_p.get_power_with_vlen_dlen(512, 512)
df_power_detail_v8_d8 = pd.DataFrame(map(lambda i: pd.DataFrame(v8_d8_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v8_d8.columns = list(map(lambda b: "V8-D8 " + b, ut.pipe_conf))
df_power_detail_v8_d8.index = ut.benchmarks

df_energy_v2_d2 = df_power_detail_v2_d2 * df_cycle_v2_d2
df_energy_v2_d2 = df_energy_v2_d2.sum()

df_energy_v8_d2 = df_power_detail_v8_d2 * df_cycle_v8_d2
df_energy_v8_d2 = df_energy_v8_d2.sum()

df_energy_v8_d8 = df_power_detail_v8_d8 * df_cycle_v8_d8
df_energy_v8_d8 = df_energy_v8_d8.sum()

#%%

df_power_detail_all = pd.concat([df_power_detail_v2_d2,
                          df_power_detail_v8_d2,
                          df_power_detail_v8_d8])
display(df_power_detail_all.sum())
df_power_detail_all.sum().plot.bar(title="Power Estimation", figsize=(10, 3))

#%%
# V2-D2のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v2_d2 = ut_p.get_group_power_with_vlen_dlen(128, 128)

df_power_detail_v2_d2 = pd.DataFrame(power_v2_d2,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v2_d2.columns = list(map(lambda b: "V2-D2 " + b, df_power_detail_v2_d2.columns))

df_power_v2_d2 = pd.DataFrame()
df_energy_v2_d2 = pd.DataFrame()

for c in df_power_detail_v2_d2.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v2_d2.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v2_d2.loc[b].loc[c]
  # 行の追加
  df_power_v2_d2  = pd.concat([df_power_v2_d2, p], axis=1)
  df_energy_v2_d2 = pd.concat([df_energy_v2_d2, e], axis=1)

# display(df_energy_v2_d2)
# df_energy_v2_d2.T.plot.bar(title="V2-D2 : Energy Estimation", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')


#%%

# V8-D2のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v8_d2 = ut_p.get_group_power_with_vlen_dlen(512, 128)

df_power_detail_v8_d2 = pd.DataFrame(power_v8_d2,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v8_d2.columns = list(map(lambda b: "V8-D2 " + b, df_power_detail_v8_d2.columns))

df_power_v8_d2  = pd.DataFrame()
df_energy_v8_d2 = pd.DataFrame()

for c in df_power_detail_v8_d2.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v8_d2.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v8_d2.loc[b].loc[c]
  # 行の追加
  df_power_v8_d2  = pd.concat([df_power_v8_d2, p],  axis=1)
  df_energy_v8_d2 = pd.concat([df_energy_v8_d2, e], axis=1)

# display(df_energy_v8_d2)
# df_energy_v8_d2.T.plot.bar(title="V8-D2 : Energy Estimation", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

#%%

# V8-D8のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v8_d8 = ut_p.get_group_power_with_vlen_dlen(512, 512)

df_power_detail_v8_d8 = pd.DataFrame(power_v8_d8,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v8_d8.columns = list(map(lambda b: "V8-D8 " + b, df_power_detail_v8_d8.columns))

df_power_v8_d8  = pd.DataFrame()
df_energy_v8_d8 = pd.DataFrame()

for c in df_power_detail_v8_d8.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v8_d8.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v8_d8.loc[b].loc[c]
  # 行の追加
  df_power_v8_d8  = pd.concat([df_power_v8_d8, p], axis=1)
  df_energy_v8_d8 = pd.concat([df_energy_v8_d8, e], axis=1)

# display(df_energy_v8_d8)
# df_energy_v8_d8.T.plot.bar(title="V8-D8 : Energy Estimation", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

#%%
# 全部の電力を比較

df_power_whole = pd.concat([df_power_v2_d2, df_power_v8_d2, df_power_v8_d8], axis=1)
display(df_power_whole)
df_power_whole.T.plot.bar(title="Power Estimation", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

#%%
# 全部のエネルギーを計算
df_energy_whole = pd.concat([df_energy_v2_d2, df_energy_v8_d2, df_energy_v8_d8], axis=1)
df_energy_whole.columns = ['V2-D2 Fence', 'V2-D2 NoMerge', 'V2-D2 Proposal', 'V2-D2 OoO',
                           'V8-D2 Fence', 'V8-D2 NoMerge', 'V8-D2 Proposal', 'V8-D2 OoO',
                           'V8-D8 Fence', 'V8-D8 NoMerge', 'V8-D8 Proposal', 'V8-D8 OoO',]
display(df_energy_whole)
df_energy_whole.T.plot.bar(title="Energy Estimation", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')


# %%
# 性能とエネルギーの分布図を作る

import numpy as np

df_energy_whole_pct = df_energy_whole / df_energy_whole.max().max()

df_perf_fence = pd.DataFrame([df_cycle_whole_pct['V2-D2 Fence'].mean(),
                              df_cycle_whole_pct['V8-D2 Fence'].mean(),
                              df_cycle_whole_pct['V8-D8 Fence'].mean()],
                              columns=['VecInO Fence'],
                              index=['V2-D2', 'V8-D2', 'V8-D8'])
df_perf_nomerge = pd.DataFrame([df_cycle_whole_pct['V2-D2 NoMerge'].mean(),
                                df_cycle_whole_pct['V8-D2 NoMerge'].mean(),
                                df_cycle_whole_pct['V8-D8 NoMerge'].mean()],
                                columns=['VecInO NoMerge'],
                             index=['V2-D2', 'V8-D2', 'V8-D8'])
df_perf_proposal = pd.DataFrame([df_cycle_whole_pct['V2-D2 Proposal'].mean(),
                                 df_cycle_whole_pct['V8-D2 Proposal'].mean(),
                                 df_cycle_whole_pct['V8-D8 Proposal'].mean()],
                                 columns=['VecInO Proposal'],
                             index=['V2-D2', 'V8-D2', 'V8-D8'])
df_perf_ooo = pd.DataFrame([df_cycle_whole_pct['V2-D2 OoO'].mean(),
                            df_cycle_whole_pct['V8-D2 OoO'].mean(),
                            df_cycle_whole_pct['V8-D8 OoO'].mean()],
                            columns=['VecOoO'],
                                   index=['V2-D2', 'V8-D2', 'V8-D8'])

df_energy_fence = pd.DataFrame([df_energy_whole_pct['V2-D2 Fence'].sum(),
                                df_energy_whole_pct['V8-D2 Fence'].sum(),
                                df_energy_whole_pct['V8-D8 Fence'].sum()],
                                columns=['VecInO Fence'],
                                index=['V2-D2', 'V8-D2', 'V8-D8'])
df_energy_nomerge = pd.DataFrame([df_energy_whole_pct['V2-D2 NoMerge'].sum(),
                                  df_energy_whole_pct['V8-D2 NoMerge'].sum(),
                                  df_energy_whole_pct['V8-D8 NoMerge'].sum()],
                                  columns=['VecInO NoMerge'],
                                  index=['V2-D2', 'V8-D2', 'V8-D8'])
df_energy_proposal = pd.DataFrame([df_energy_whole_pct['V2-D2 Proposal'].sum(),
                                   df_energy_whole_pct['V8-D2 Proposal'].sum(),
                                   df_energy_whole_pct['V8-D8 Proposal'].sum()],
                                   columns=['VecInO Proposal'],
                                index=['V2-D2', 'V8-D2', 'V8-D8'])
df_energy_ooo = pd.DataFrame([df_energy_whole_pct['V2-D2 OoO'].sum(),
                              df_energy_whole_pct['V8-D2 OoO'].sum(),
                              df_energy_whole_pct['V8-D8 OoO'].sum()],
                              columns=['VecOoO'],
                                   index=['V2-D2', 'V8-D2', 'V8-D8'])

df_area_fence = pd.DataFrame([df_area_whole['V2-D2 Fence'].sum(),
                                df_area_whole['V8-D2 Fence'].sum(),
                                df_area_whole['V8-D8 Fence'].sum()],
                                columns=['VecInO Fence'],
                                index=['V2-D2', 'V8-D2', 'V8-D8'])
df_area_nomerge = pd.DataFrame([df_area_whole['V2-D2 NoMerge'].sum(),
                                  df_area_whole['V8-D2 NoMerge'].sum(),
                                  df_area_whole['V8-D8 NoMerge'].sum()],
                                  columns=['VecInO NoMerge'],
                                  index=['V2-D2', 'V8-D2', 'V8-D8'])
df_area_proposal = pd.DataFrame([df_area_whole['V2-D2 Proposal'].sum(),
                                   df_area_whole['V8-D2 Proposal'].sum(),
                                   df_area_whole['V8-D8 Proposal'].sum()],
                                   columns=['VecInO Proposal'],
                                index=['V2-D2', 'V8-D2', 'V8-D8'])
df_area_ooo = pd.DataFrame([df_area_whole['V2-D2 OoO'].sum(),
                              df_area_whole['V8-D2 OoO'].sum(),
                              df_area_whole['V8-D8 OoO'].sum()],
                              columns=['VecOoO'],
                                   index=['V2-D2', 'V8-D2', 'V8-D8'])

plt.scatter(df_energy_fence, df_perf_fence, label='VecInO Fence', color='blue')
plt.plot   (df_energy_fence, df_perf_fence, color='blue')
plt.axline((0, 0), (df_energy_fence['VecInO Fence']['V8-D2'], 
                    df_perf_fence  ['VecInO Fence']['V8-D2']), color='blue', lw=0.5)

plt.scatter(df_energy_nomerge, df_perf_nomerge, label='VecInO NoMerge', color='green')
plt.plot   (df_energy_nomerge, df_perf_nomerge, label='VecInO NoMerge', color='green')
plt.axline((0, 0), (df_energy_nomerge['VecInO NoMerge']['V8-D2'], 
                    df_perf_nomerge  ['VecInO NoMerge']['V8-D2']), color='green', lw=0.5)

plt.scatter(df_energy_proposal, df_perf_proposal, label='VecInO Proposal', color='purple')
plt.plot   (df_energy_proposal, df_perf_proposal, label='VecInO Proposal', color='purple')
plt.axline((0, 0), (df_energy_proposal['VecInO Proposal']['V8-D2'], 
                    df_perf_proposal  ['VecInO Proposal']['V8-D2']), color='purple', lw=0.5)

plt.scatter(df_energy_ooo, df_perf_ooo, label='VecOoO', color='red')
plt.plot   (df_energy_ooo, df_perf_ooo, label='VecOoO', color='red')
plt.axline((0, 0), (df_energy_ooo['VecOoO']['V8-D2'], 
                    df_perf_ooo  ['VecOoO']['V8-D2']), color='red', lw=0.5)

plt.xlim(0.0, df_energy_whole_pct.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_pct.mean().max() * 1.1)
plt.xlabel("Energy (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
plt.savefig("energy_perf.pdf", bbox_inches='tight')

display(df_cycle_whole_pct)
display(df_energy_whole_pct.sum().max())


# %%
# 性能と面積の分布図を作る

plt.scatter(df_area_fence, df_perf_fence, lw=2, label='VecInO Fence', color='blue')
plt.plot   (df_area_fence, df_perf_fence, lw=2, color='blue')
plt.axline((0, 0), (df_area_fence['VecInO Fence']['V8-D2'], 
                    df_perf_fence['VecInO Fence']['V8-D2']), color='blue', lw=0.5)

plt.scatter(df_area_nomerge, df_perf_nomerge, label='VecInO NoMerge', color='green')
plt.plot   (df_area_nomerge, df_perf_nomerge, label='VecInO NoMerge', color='green')
plt.axline((0, 0), (df_area_nomerge['VecInO NoMerge']['V8-D2'], 
                    df_perf_nomerge['VecInO NoMerge']['V8-D2']), color='green', lw=0.5)

plt.scatter(df_area_proposal, df_perf_proposal, label='VecInO Proposal', color='purple')
plt.plot   (df_area_proposal, df_perf_proposal, label='VecInO Proposal', color='purple')
plt.axline((0, 0), (df_area_proposal['VecInO Proposal']['V8-D2'], 
                    df_perf_proposal['VecInO Proposal']['V8-D2']), color='purple', lw=0.5)

plt.scatter(df_area_ooo, df_perf_ooo, label='VecOoO', color='red')
plt.plot   (df_area_ooo, df_perf_ooo, label='VecOoO', color='red')
plt.axline((0, 0), (df_area_ooo['VecOoO']['V8-D2'], 
                    df_perf_ooo['VecOoO']['V8-D2']), color='red', lw=0.5)

plt.xlabel("Area (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
plt.xlim(0.0, df_area_whole.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_pct.mean().max() * 1.1)
plt.savefig("area_perf.pdf", bbox_inches='tight')

# %%
