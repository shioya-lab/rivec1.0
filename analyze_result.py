#%%
# 面積を算出

import pandas as pd
import matplotlib.pyplot as plt
import utils as ut
import util_area as ut_a
import util_cycle as ut_c
import util_power as ut_p
import numpy as np


df_area_d2_v2_d2 = pd.DataFrame(ut_a.calc_group_area("v128_d128"))
df_area_d2_v4_d2 = pd.DataFrame(ut_a.calc_group_area("v256_d128"))
df_area_d2_v8_d2 = pd.DataFrame(ut_a.calc_group_area("v512_d128"))
df_area_d2_v16_d2 = pd.DataFrame(ut_a.calc_group_area("v1024_d128"))
df_area_whole_d2 = pd.concat([df_area_d2_v2_d2, df_area_d2_v4_d2, df_area_d2_v8_d2, df_area_d2_v16_d2], axis=1)

df_area_d2_v4_d4  = pd.DataFrame(ut_a.calc_group_area("v256_d256"))
df_area_d2_v8_d4  = pd.DataFrame(ut_a.calc_group_area("v512_d256"))
df_area_d2_v16_d4 = pd.DataFrame(ut_a.calc_group_area("v1024_d256"))
df_area_d2_v32_d4 = pd.DataFrame(ut_a.calc_group_area("v2048_d256"))
df_area_whole_d4 = pd.concat([df_area_d2_v4_d4, df_area_d2_v8_d4, df_area_d2_v16_d4, df_area_d2_v32_d4], axis=1)

display(df_area_whole_d2)
# df_area_whole_d2 = df_area_whole_d2.reindex(elem_index)
df_area_whole_d2.columns = ['V2-D2 Fence',  'V2-D2 LSUInO',  'V2-D2 NoMerge',  'V2-D2 Proposal',  'V2-D2 OoO',
                            'V4-D2 Fence',  'V4-D2 LSUInO',  'V4-D2 NoMerge',  'V4-D2 Proposal',  'V4-D2 OoO',
                            'V8-D2 Fence',  'V8-D2 LSUInO',  'V8-D2 NoMerge',  'V8-D2 Proposal',  'V8-D2 OoO',
                            'V16-D2 Fence', 'V16-D2 LSUInO', 'V16-D2 NoMerge', 'V16-D2 Proposal', 'V16-D2 OoO',]
area_graph_d2 = df_area_whole_d2.T.plot(title="Area estimation with each configuration", 
                                  kind='bar',
                                  stacked=True)
handles, labels = area_graph_d2.get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
area_graph_d2.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
plt.ylim(0.0, df_area_whole_d4.sum().max()*1.1)
plt.show()
plt.savefig("area_d2.pdf", bbox_inches='tight')
plt.savefig("area_d2.png", bbox_inches='tight')

display(df_area_whole_d4)
df_area_whole_d4.columns = ['V4-D4 Fence',  'V4-D4 LSUInO',  'V4-D4 NoMerge',  'V4-D4 Proposal',  'V4-D4 OoO',
                            'V8-D4 Fence',  'V8-D4 LSUInO',  'V8-D4 NoMerge',  'V8-D4 Proposal',  'V8-D4 OoO',
                            'V16-D4 Fence', 'V16-D4 LSUInO', 'V16-D4 NoMerge', 'V16-D4 Proposal', 'V16-D4 OoO',
                            'V32-D4 Fence', 'V32-D4 LSUInO', 'V32-D4 NoMerge', 'V32-D4 Proposal', 'V32-D4 OoO',]
area_graph_d4 = df_area_whole_d4.T.plot(title="Area estimation with each configuration", 
                                        kind='bar',
                                        stacked=True)
handles, labels = area_graph_d4.get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
area_graph_d4.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
plt.show()
plt.savefig("area_d4.pdf", bbox_inches='tight')
plt.savefig("area_d4.png", bbox_inches='tight')


#%%
# Cycleのテーブルを作る

import pandas as pd
import utils as ut
import util_cycle as ut_c

def get_cycle_with_app(app, vlen, dlen):
    return list(map(lambda p: ut_c.get_cycle(app, p, vlen, dlen) / 100000, ut.pipe_conf))
    
df_cycle_v2_d2  = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 128, 128), ut.benchmarks)), 
                                    columns=(map(lambda b: "V2-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_cycle_v4_d2  = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 256, 128), ut.benchmarks)), 
                                    columns=(map(lambda b: "V4-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_cycle_v8_d2  = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 512, 128), ut.benchmarks)), 
                                    columns=(map(lambda b: "V8-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_cycle_v16_d2  = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 1024, 128), ut.benchmarks)), 
                                     columns=(map(lambda b: "V16-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_cycle_v4_d4  = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 256, 256), ut.benchmarks)), 
                                    columns=(map(lambda b: "V4-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_cycle_v8_d4  = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 512, 256), ut.benchmarks)), 
                                    columns=(map(lambda b: "V8-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_cycle_v16_d4 = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 1024, 256), ut.benchmarks)), 
                                    columns=(map(lambda b: "V16-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_cycle_v32_d4 = pd.DataFrame(list(map(lambda b: get_cycle_with_app(b, 2048, 256), ut.benchmarks)), 
                                    columns=(map(lambda b: "V32-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)

#%%
# V4-D2 のテーブルを作る

# V2-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v2_d2_pct = np.reciprocal((df_cycle_v2_d2.T / df_cycle_v2_d2["V2-D2 ooo.v"].T).T)
df_cycle_v2_d2_pct.loc['GeoMean'] = df_cycle_v2_d2_pct.mean()
df_cycle_v2_d2_pct.plot.bar(title="V2-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig("v2_d2_perf.pdf", bbox_inches='tight')

display(df_cycle_v2_d2)
display(df_cycle_v2_d2_pct.loc['GeoMean'])

# V4-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v4_d2_pct = np.reciprocal((df_cycle_v4_d2.T / df_cycle_v4_d2["V4-D2 ooo.v"].T).T)
df_cycle_v4_d2_pct.loc['GeoMean'] = df_cycle_v4_d2_pct.mean()
df_cycle_v4_d2_pct.plot.bar(title="V4-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig("v4_d2_perf.pdf", bbox_inches='tight')

display(df_cycle_v4_d2)
display(df_cycle_v4_d2_pct.loc['GeoMean'])

# V8-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v8_d2_pct = np.reciprocal((df_cycle_v8_d2.T / df_cycle_v8_d2["V8-D2 ooo.v"].T).T)
df_cycle_v8_d2_pct.loc['GeoMean'] = df_cycle_v8_d2_pct.mean()
df_cycle_v8_d2_pct.plot.bar(title="V8-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig("v8_d2_perf.pdf", bbox_inches='tight')

display(df_cycle_v8_d2)
display(df_cycle_v8_d2_pct.loc['GeoMean'])

# V16-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v16_d2_pct = np.reciprocal((df_cycle_v16_d2.T / df_cycle_v16_d2["V16-D2 ooo.v"].T).T)
df_cycle_v16_d2_pct.loc['GeoMean'] = df_cycle_v16_d2_pct.mean()
df_cycle_v16_d2_pct.plot.bar(title="V16-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig("v16_d2_perf.pdf", bbox_inches='tight')

display(df_cycle_v16_d2)
display(df_cycle_v16_d2_pct.loc['GeoMean'])


#%%
# V4-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v4_d4_pct = np.reciprocal((df_cycle_v4_d4.T / df_cycle_v4_d4["V4-D4 ooo.v"].T).T)
df_cycle_v4_d4_pct.loc['GeoMean'] = df_cycle_v4_d4_pct.mean()
df_cycle_v4_d4_pct.plot.bar(title="V4-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig("v4_d4_perf.pdf", bbox_inches='tight')

display(df_cycle_v4_d4)
display(df_cycle_v4_d4_pct.loc['GeoMean'])

# V8-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v8_d4_pct = np.reciprocal((df_cycle_v8_d4.T / df_cycle_v8_d4["V8-D4 ooo.v"].T).T)
df_cycle_v8_d4_pct.loc['GeoMean'] = df_cycle_v8_d4_pct.mean()
df_cycle_v8_d4_pct.plot.bar(title="V8-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig("v8_d4_perf.pdf", bbox_inches='tight')

display(df_cycle_v8_d4)
display(df_cycle_v8_d4_pct.loc['GeoMean'])

# V16-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v16_d4_pct = np.reciprocal((df_cycle_v16_d4.T / df_cycle_v16_d4["V16-D4 ooo.v"].T).T)
df_cycle_v16_d4_pct.loc['GeoMean'] = df_cycle_v16_d4_pct.mean()
df_cycle_v16_d4_pct.plot.bar(title="V16-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig("v16_d4_perf.pdf", bbox_inches='tight')

display(df_cycle_v16_d4)
display(df_cycle_v16_d4_pct.loc['GeoMean'])

# V32-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v32_d4_pct = np.reciprocal((df_cycle_v32_d4.T / df_cycle_v32_d4["V32-D4 ooo.v"].T).T)
df_cycle_v32_d4_pct.loc['GeoMean'] = df_cycle_v32_d4_pct.mean()
df_cycle_v32_d4_pct.plot.bar(title="V32-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig("v32_d4_perf.pdf", bbox_inches='tight')

display(df_cycle_v32_d4)
display(df_cycle_v32_d4_pct.loc['GeoMean'])


#%%
## 全体的な性能グラフを作る
# D2シリーズ
df_cycle_whole_d2 = pd.concat([df_cycle_v2_d2, df_cycle_v4_d2, df_cycle_v8_d2, df_cycle_v16_d2], axis=1)
display(df_cycle_whole_d2)
df_cycle_whole_d2.columns = ['V2-D2 Fence',  'V2-D2 LSUInO',  'V2-D2 NoMerge',  'V2-D2 Proposal',  'V2-D2 OoO',
                             'V4-D2 Fence',  'V4-D2 LSUInO',  'V4-D2 NoMerge',  'V4-D2 Proposal',  'V4-D2 OoO',
                             'V8-D2 Fence',  'V8-D2 LSUInO',  'V8-D2 NoMerge',  'V8-D2 Proposal',  'V8-D2 OoO',
                             'V16-D2 Fence', 'V16-D2 LSUInO', 'V16-D2 NoMerge', 'V16-D2 Proposal', 'V16-D2 OoO']

df_cycle_whole_d2_pct = np.reciprocal((df_cycle_whole_d2.T / df_cycle_v2_d2["V2-D2 vio.v.fence"].T).T)
df_cycle_means_d2 = df_cycle_whole_d2_pct.mean()
display(df_cycle_means_d2)
plt.figure()
df_cycle_means_d2.plot.line(style=['bo-'], title="Relative Performance of V2-D2 / V4-D2 / V8-D2 / V16-D2", figsize=(10, 3))
plt.savefig("relative_performance.pdf", bbox_inches='tight')

# D4シリーズ
df_cycle_whole_d4 = pd.concat([df_cycle_v4_d4, df_cycle_v8_d4, df_cycle_v16_d4, df_cycle_v32_d4], axis=1)
display(df_cycle_whole_d4)
df_cycle_whole_d4.columns = ['V4-D4 Fence',  'V4-D4 LSUInO',  'V4-D4 NoMerge',  'V4-D4 Proposal',  'V4-D4 OoO',
                             'V8-D4 Fence',  'V8-D4 LSUInO',  'V8-D4 NoMerge',  'V8-D4 Proposal',  'V8-D4 OoO',
                             'V16-D4 Fence', 'V16-D4 LSUInO', 'V16-D4 NoMerge', 'V16-D4 Proposal', 'V16-D4 OoO',
                             'V32-D4 Fence', 'V32-D4 LSUInO', 'V32-D4 NoMerge', 'V32-D4 Proposal', 'V32-D4 OoO']

df_cycle_whole_d4_pct = np.reciprocal((df_cycle_whole_d4.T / df_cycle_v4_d4["V4-D4 vio.v.fence"].T).T)
df_cycle_means_d4 = df_cycle_whole_d4_pct.mean()
display(df_cycle_means_d4)
plt.figure()
df_cycle_means_d4.plot.line(style=['bo-'], title="Relative Performance of V4-D4 / V8-D4 / V16-D4 / V32-D2", figsize=(10, 3))
plt.savefig("relative_performance.pdf", bbox_inches='tight')


  #%%
# V4-D2のサイクル数でグラフを作る

import pandas as pd
import util_power as ut_p

v2_d2_power = ut_p.get_power_with_vlen_dlen(128, 128)
df_power_detail_v2_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v2_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v2_d2.columns = list(map(lambda b: "V2-D2 " + b, ut.pipe_conf))
df_power_detail_v2_d2.index = ut.benchmarks

v4_d2_power = ut_p.get_power_with_vlen_dlen(256, 128)
df_power_detail_v4_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v4_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v4_d2.columns = list(map(lambda b: "V4-D2 " + b, ut.pipe_conf))
df_power_detail_v4_d2.index = ut.benchmarks

v8_d2_power = ut_p.get_power_with_vlen_dlen(512, 128)
df_power_detail_v8_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v8_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v8_d2.columns = list(map(lambda b: "V8-D2 " + b, ut.pipe_conf))
df_power_detail_v8_d2.index = ut.benchmarks

df_energy_v2_d2 = df_power_detail_v2_d2 * df_cycle_v2_d2
df_energy_v2_d2 = df_energy_v2_d2.sum()

df_energy_v4_d2 = df_power_detail_v4_d2 * df_cycle_v4_d2
df_energy_v4_d2 = df_energy_v4_d2.sum()

df_energy_v8_d2 = df_power_detail_v8_d2 * df_cycle_v8_d2
df_energy_v8_d2 = df_energy_v8_d2.sum()

#%%

df_power_detail_all = pd.concat([df_power_detail_v2_d2,
                          df_power_detail_v4_d2,
                          df_power_detail_v8_d2])
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


#%%

# V4-D2のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v4_d2 = ut_p.get_group_power_with_vlen_dlen(256, 128)

df_power_detail_v4_d2 = pd.DataFrame(power_v4_d2,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v4_d2.columns = list(map(lambda b: "V4-D2 " + b, df_power_detail_v4_d2.columns))

df_power_v4_d2  = pd.DataFrame()
df_energy_v4_d2 = pd.DataFrame()

for c in df_power_detail_v4_d2.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v4_d2.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v4_d2.loc[b].loc[c]
  # 行の追加
  df_power_v4_d2  = pd.concat([df_power_v4_d2, p],  axis=1)
  df_energy_v4_d2 = pd.concat([df_energy_v4_d2, e], axis=1)

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
  df_power_v8_d2  = pd.concat([df_power_v8_d2, p], axis=1)
  df_energy_v8_d2 = pd.concat([df_energy_v8_d2, e], axis=1)

# v16-D2のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v16_d2 = ut_p.get_group_power_with_vlen_dlen(1024, 128)

df_power_detail_v16_d2 = pd.DataFrame(power_v16_d2,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v16_d2.columns = list(map(lambda b: "V16-D2 " + b, df_power_detail_v16_d2.columns))

df_power_v16_d2  = pd.DataFrame()
df_energy_v16_d2 = pd.DataFrame()

for c in df_power_detail_v16_d2.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v16_d2.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v16_d2.loc[b].loc[c]
  # 行の追加
  df_power_v16_d2  = pd.concat([df_power_v16_d2, p], axis=1)
  df_energy_v16_d2 = pd.concat([df_energy_v16_d2, e], axis=1)



#%%
# V4-D4のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v4_d4 = ut_p.get_group_power_with_vlen_dlen(256, 256)

df_power_detail_v4_d4 = pd.DataFrame(power_v4_d4,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v4_d4.columns = list(map(lambda b: "V4-D4 " + b, df_power_detail_v4_d4.columns))

df_power_v4_d4 = pd.DataFrame()
df_energy_v4_d4 = pd.DataFrame()

for c in df_power_detail_v4_d4.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v4_d4.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v4_d4.loc[b].loc[c]
  # 行の追加
  df_power_v4_d4  = pd.concat([df_power_v4_d4, p], axis=1)
  df_energy_v4_d4 = pd.concat([df_energy_v4_d4, e], axis=1)


#%%

# V8-D4のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v8_d4 = ut_p.get_group_power_with_vlen_dlen(512, 256)

df_power_detail_v8_d4 = pd.DataFrame(power_v8_d4,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v8_d4.columns = list(map(lambda b: "V8-D4 " + b, df_power_detail_v8_d4.columns))

df_power_v8_d4  = pd.DataFrame()
df_energy_v8_d4 = pd.DataFrame()

for c in df_power_detail_v8_d4.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v8_d4.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v8_d4.loc[b].loc[c]
  # 行の追加
  df_power_v8_d4  = pd.concat([df_power_v8_d4, p],  axis=1)
  df_energy_v8_d4 = pd.concat([df_energy_v8_d4, e], axis=1)

#%%

# V16-D4のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v16_d4 = ut_p.get_group_power_with_vlen_dlen(1024, 256)

df_power_detail_v16_d4 = pd.DataFrame(power_v16_d4,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v16_d4.columns = list(map(lambda b: "V16-D4 " + b, df_power_detail_v16_d4.columns))

df_power_v16_d4  = pd.DataFrame()
df_energy_v16_d4 = pd.DataFrame()

for c in df_power_detail_v16_d4.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v16_d4.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v16_d4.loc[b].loc[c]
  # 行の追加
  df_power_v16_d4  = pd.concat([df_power_v16_d4, p], axis=1)
  df_energy_v16_d4 = pd.concat([df_energy_v16_d4, e], axis=1)


# V32-D4のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_v32_d4 = ut_p.get_group_power_with_vlen_dlen(2048, 256)

df_power_detail_v32_d4 = pd.DataFrame(power_v32_d4,
                               index=ut.benchmarks).fillna(0.0) 
df_power_detail_v32_d4.columns = list(map(lambda b: "V32-D4 " + b, df_power_detail_v32_d4.columns))

df_power_v32_d4  = pd.DataFrame()
df_energy_v32_d4 = pd.DataFrame()

for c in df_power_detail_v32_d4.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_detail_v32_d4.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v32_d4.loc[b].loc[c]
  # 行の追加
  df_power_v32_d4  = pd.concat([df_power_v32_d4, p], axis=1)
  df_energy_v32_d4 = pd.concat([df_energy_v32_d4, e], axis=1)


#%%
# 全部の電力を比較

df_power_whole_d2 = pd.concat([df_power_v2_d2, df_power_v4_d2, df_power_v8_d2], axis=1)
df_power_whole_d4 = pd.concat([df_power_v4_d4, df_power_v8_d4, df_power_v16_d4], axis=1)

display(df_power_whole_d2)
df_power_whole_d2.T.plot.bar(title="Power Estimation of V2-D2 / V4-D2 / V8-D2 / V16-D2", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.ylim(0.0, df_power_whole_d4.sum().max()*1.1)

display(df_power_whole_d4)
df_power_whole_d4.T.plot.bar(title="Power Estimation of V4-D4 / V8-D4 / V8-D4 / V32-D4", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.ylim(0.0, df_power_whole_d4.sum().max()*1.1)


#%%
# 全部のエネルギーを計算
df_energy_whole_d2 = pd.concat([df_energy_v2_d2, df_energy_v4_d2, df_energy_v8_d2, df_energy_v16_d2], axis=1)
df_energy_whole_d2.columns = ['V2-D2 Fence',  'V2-D2 LSUInO',  'V2-D2 NoMerge',  'V2-D2 Proposal',  'V2-D2 OoO',
                              'V4-D2 Fence',  'V4-D2 LSUInO',  'V4-D2 NoMerge',  'V4-D2 Proposal',  'V4-D2 OoO',
                              'V8-D2 Fence',  'V8-D2 LSUInO',  'V8-D2 NoMerge',  'V8-D2 Proposal',  'V8-D2 OoO',
                              'V16-D2 Fence', 'V16-D2 LSUInO', 'V16-D2 NoMerge', 'V16-D2 Proposal', 'V16-D2 OoO',]

df_energy_whole_d4 = pd.concat([df_energy_v4_d4, df_energy_v8_d4, df_energy_v16_d4, df_energy_v32_d4], axis=1)
df_energy_whole_d4.columns = ['V4-D4 Fence',  'V4-D4 LSUInO',  'V4-D4 NoMerge',  'V4-D4 Proposal',  'V4-D4 OoO',
                              'V8-D4 Fence',  'V8-D4 LSUInO',  'V8-D4 NoMerge',  'V8-D4 Proposal',  'V8-D4 OoO',
                              'V16-D4 Fence', 'V16-D4 LSUInO', 'V16-D4 NoMerge', 'V16-D4 Proposal', 'V16-D4 OoO',
                              'V32-D4 Fence', 'V32-D4 LSUInO', 'V32-D4 NoMerge', 'V32-D4 Proposal', 'V32-D4 OoO',]

display(df_energy_whole_d2)
energy_graph = df_energy_whole_d2.T.plot(kind='bar', title="Energy Estimation of V4-D4 V8-D4 V16-D4", stacked=True)
handles, labels = energy_graph.get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
energy_graph.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
plt.ylim(0.0, df_energy_whole_d4.sum().max() * 1.1)
plt.show()

plt.savefig("relative_energy.pdf", bbox_inches='tight')

display(df_energy_whole_d4)
energy_graph = df_energy_whole_d4.T.plot(kind='bar', title="Energy Estimation of V4-D4 V8-D4 V16-D4", stacked=True)
handles, labels = energy_graph.get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
energy_graph.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
plt.show()


# %%
# D2 : 性能とエネルギーの分布図を作る

import numpy as np

df_energy_whole_d2_pct = df_energy_whole_d2 / df_energy_whole_d2.sum().min()

d2_index_list = ['V2-D2', 'V4-D2', 'V8-D2', 'V16-D2']

df_perf_d2_fence    = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='Fence$').mean(),    columns=['VecInO Fence']   ).set_axis(d2_index_list)
df_perf_d2_lsuino   = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='LSUInO$').mean(),   columns=['VecInO LSUInO']  ).set_axis(d2_index_list)
df_perf_d2_nomerge  = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='NoMerge$').mean(),  columns=['VecInO NoMerge'] ).set_axis(d2_index_list)
df_perf_d2_proposal = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='Proposal$').mean(), columns=['VecInO Proposal']).set_axis(d2_index_list)
df_perf_d2_ooo      = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='OoO$').mean(),      columns=['VecOoO']         ).set_axis(d2_index_list)

df_energy_d2_fence    = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='Fence$').sum(),    columns=['VecInO Fence']   ).set_axis(d2_index_list)
df_energy_d2_lsuino   = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='LSUInO$').sum(),   columns=['VecInO LSUInO']  ).set_axis(d2_index_list)
df_energy_d2_nomerge  = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='NoMerge$').sum(),  columns=['VecInO NoMerge'] ).set_axis(d2_index_list)
df_energy_d2_proposal = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='Proposal$').sum(), columns=['VecInO Proposal']).set_axis(d2_index_list)
df_energy_d2_ooo      = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='OoO$').sum(),      columns=['VecOoO']         ).set_axis(d2_index_list)

df_area_d2_fence    = pd.DataFrame(df_area_whole_d2.filter(regex='Fence$').sum(),    columns=['VecInO Fence']   ).set_axis(d2_index_list)
df_area_d2_lsuino   = pd.DataFrame(df_area_whole_d2.filter(regex='LSUInO$').sum(),   columns=['VecInO LSUInO']  ).set_axis(d2_index_list)
df_area_d2_nomerge  = pd.DataFrame(df_area_whole_d2.filter(regex='NoMerge$').sum(),  columns=['VecInO NoMerge'] ).set_axis(d2_index_list)
df_area_d2_proposal = pd.DataFrame(df_area_whole_d2.filter(regex='Proposal$').sum(), columns=['VecInO Proposal']).set_axis(d2_index_list)
df_area_d2_ooo      = pd.DataFrame(df_area_whole_d2.filter(regex='OoO$').sum(),      columns=['VecOoO']         ).set_axis(d2_index_list)

plt.scatter(df_energy_d2_fence, df_perf_d2_fence, label='VecInO Fence', color='blue')
plt.plot   (df_energy_d2_fence, df_perf_d2_fence, color='blue')
plt.axline((0, 0), (df_energy_d2_fence['VecInO Fence']['V4-D2'], 
                    df_perf_d2_fence  ['VecInO Fence']['V4-D2']), color='blue', lw=0.5)

plt.scatter(df_energy_d2_nomerge, df_perf_d2_nomerge, label='VecInO NoMerge', color='green')
plt.plot   (df_energy_d2_nomerge, df_perf_d2_nomerge, label='VecInO NoMerge', color='green')
plt.axline((0, 0), (df_energy_d2_nomerge['VecInO NoMerge']['V4-D2'], 
                    df_perf_d2_nomerge  ['VecInO NoMerge']['V4-D2']), color='green', lw=0.5)

plt.scatter(df_energy_d2_proposal, df_perf_d2_proposal, label='VecInO Proposal', color='purple')
plt.plot   (df_energy_d2_proposal, df_perf_d2_proposal, label='VecInO Proposal', color='purple')
plt.axline((0, 0), (df_energy_d2_proposal['VecInO Proposal']['V4-D2'], 
                    df_perf_d2_proposal  ['VecInO Proposal']['V4-D2']), color='purple', lw=0.5)

plt.scatter(df_energy_d2_ooo, df_perf_d2_ooo, label='VecOoO', color='red')
plt.plot   (df_energy_d2_ooo, df_perf_d2_ooo, label='VecOoO', color='red')
plt.axline((0, 0), (df_energy_d2_ooo['VecOoO']['V4-D2'], 
                    df_perf_d2_ooo  ['VecOoO']['V4-D2']), color='red', lw=0.5)

plt.xlim(0.0, df_energy_whole_d2_pct.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d2_pct.mean().max() * 1.1)
plt.xlabel("Energy (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
plt.savefig("energy_perf_d2.pdf", bbox_inches='tight')

#%%
# D4 : 性能とエネルギーの分布図を作る

df_energy_whole_d4_pct = df_energy_whole_d4 / df_energy_whole_d4.sum().min()

d4_index_list = ['V4-D4', 'V8-D4', 'V16-D4', 'V32-D4']

df_perf_d4_fence    = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='Fence$').mean(),    columns=['VecInO Fence']   ).set_axis(d4_index_list)
df_perf_d4_lsuino   = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='LSUInO$').mean(),   columns=['VecInO LSUInO']  ).set_axis(d4_index_list)
df_perf_d4_nomerge  = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='NoMerge$').mean(),  columns=['VecInO NoMerge'] ).set_axis(d4_index_list)
df_perf_d4_proposal = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='Proposal$').mean(), columns=['VecInO Proposal']).set_axis(d4_index_list)
df_perf_d4_ooo      = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='OoO$').mean(),      columns=['VecOoO']         ).set_axis(d4_index_list)

df_energy_d4_fence    = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='Fence$').sum(),    columns=['VecInO Fence']   ).set_axis(d4_index_list)
df_energy_d4_lsuino   = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='LSUInO$').sum(),   columns=['VecInO LSUInO']  ).set_axis(d4_index_list)
df_energy_d4_nomerge  = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='NoMerge$').sum(),  columns=['VecInO NoMerge'] ).set_axis(d4_index_list)
df_energy_d4_proposal = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='Proposal$').sum(), columns=['VecInO Proposal']).set_axis(d4_index_list)
df_energy_d4_ooo      = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='OoO$').sum(),      columns=['VecOoO']         ).set_axis(d4_index_list)

df_area_d4_fence    = pd.DataFrame(df_area_whole_d4.filter(regex='Fence$').sum(),    columns=['VecInO Fence']   ).set_axis(d4_index_list)
df_area_d4_lsuino   = pd.DataFrame(df_area_whole_d4.filter(regex='LSUInO$').sum(),   columns=['VecInO LSUInO']  ).set_axis(d4_index_list)
df_area_d4_nomerge  = pd.DataFrame(df_area_whole_d4.filter(regex='NoMerge$').sum(),  columns=['VecInO NoMerge'] ).set_axis(d4_index_list)
df_area_d4_proposal = pd.DataFrame(df_area_whole_d4.filter(regex='Proposal$').sum(), columns=['VecInO Proposal']).set_axis(d4_index_list)
df_area_d4_ooo      = pd.DataFrame(df_area_whole_d4.filter(regex='OoO$').sum(),      columns=['VecOoO']         ).set_axis(d4_index_list)

plt.scatter(df_energy_d4_fence, df_perf_d4_fence, label='VecInO Fence', color='blue')
plt.plot   (df_energy_d4_fence, df_perf_d4_fence, color='blue')
plt.axline((0, 0), (df_energy_d4_fence['VecInO Fence']['V4-D4'], 
                    df_perf_d4_fence  ['VecInO Fence']['V4-D4']), color='blue', lw=0.5)

plt.scatter(df_energy_d4_nomerge, df_perf_d4_nomerge, label='VecInO NoMerge', color='green')
plt.plot   (df_energy_d4_nomerge, df_perf_d4_nomerge, label='VecInO NoMerge', color='green')
plt.axline((0, 0), (df_energy_d4_nomerge['VecInO NoMerge']['V4-D4'], 
                    df_perf_d4_nomerge  ['VecInO NoMerge']['V4-D4']), color='green', lw=0.5)

plt.scatter(df_energy_d4_proposal, df_perf_d4_proposal, label='VecInO Proposal', color='purple')
plt.plot   (df_energy_d4_proposal, df_perf_d4_proposal, label='VecInO Proposal', color='purple')
plt.axline((0, 0), (df_energy_d4_proposal['VecInO Proposal']['V4-D4'], 
                    df_perf_d4_proposal  ['VecInO Proposal']['V4-D4']), color='purple', lw=0.5)

plt.scatter(df_energy_d4_ooo, df_perf_d4_ooo, label='VecOoO', color='red')
plt.plot   (df_energy_d4_ooo, df_perf_d4_ooo, label='VecOoO', color='red')
plt.axline((0, 0), (df_energy_d4_ooo['VecOoO']['V4-D4'], 
                    df_perf_d4_ooo  ['VecOoO']['V4-D4']), color='red', lw=0.5)

plt.xlim(0.0, df_energy_whole_d4_pct.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d4_pct.mean().max() * 1.1)
plt.xlabel("Energy (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
plt.savefig("energy_perf_d4.pdf", bbox_inches='tight')


# %%
# 性能の折れ線グラフを作る
import matplotlib.pyplot as plt

plt.plot(df_perf_d2_fence)
plt.plot(df_perf_d2_lsuino)
plt.plot(df_perf_d2_nomerge)
plt.plot(df_perf_d2_proposal)
plt.plot(df_perf_d2_ooo)
plt.ylim(0.0, 2.0)
plt.show()

plt.cla()

plt.plot(df_perf_d4_fence)
plt.plot(df_perf_d4_lsuino)
plt.plot(df_perf_d4_nomerge)
plt.plot(df_perf_d4_proposal)
plt.plot(df_perf_d4_ooo)
plt.ylim(0.0, 2.0)


# %%
# 各ベンチマークにおける相対性能グラフを作成

for b in ut.benchmarks:
  display(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="Fence$")    .loc[b]).set_axis(d2_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="Fence$")   .loc[b]).set_axis(d2_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="LSUInO$")  .loc[b]).set_axis(d2_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="NoMerge$") .loc[b]).set_axis(d2_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="Proposal$").loc[b]).set_axis(d2_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="OoO$")     .loc[b]).set_axis(d2_index_list))
  plt.title("Performance rate of %s with %s" % (b, d2_index_list))
  plt.ylim(0.0)
  plt.show()
  plt.cla()

for b in ut.benchmarks:
  display(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="Fence$")    .loc[b]).set_axis(d4_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="Fence$")   .loc[b]).set_axis(d4_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="LSUInO$")  .loc[b]).set_axis(d4_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="NoMerge$") .loc[b]).set_axis(d4_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="Proposal$").loc[b]).set_axis(d4_index_list))
  plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="OoO$")     .loc[b]).set_axis(d4_index_list))
  plt.title("Performance rate of %s with %s" % (b, d4_index_list))
  plt.ylim(0.0)
  plt.show()
  plt.cla()

  
# %%
# 性能と面積の分布図を作る

df_area_whole_d2_pct = df_area_whole_d2.sum() / df_area_whole_d2.sum().min()
df_area_whole_d4_pct = df_area_whole_d4.sum() / df_area_whole_d4.sum().min()

plt.scatter(df_area_d2_fence, df_perf_d2_fence, lw=2, label='VecInO Fence', color='blue')
plt.plot   (df_area_d2_fence, df_perf_d2_fence, lw=2, color='blue')
plt.axline((0, 0), (df_area_d2_fence['VecInO Fence']['V4-D2'], 
                    df_perf_d2_fence['VecInO Fence']['V4-D2']), color='blue', lw=0.5)

plt.scatter(df_area_d2_nomerge, df_perf_d2_nomerge, label='VecInO NoMerge', color='green')
plt.plot   (df_area_d2_nomerge, df_perf_d2_nomerge, label='VecInO NoMerge', color='green')
plt.axline((0, 0), (df_area_d2_nomerge['VecInO NoMerge']['V4-D2'], 
                    df_perf_d2_nomerge['VecInO NoMerge']['V4-D2']), color='green', lw=0.5)

plt.scatter(df_area_d2_proposal, df_perf_d2_proposal, label='VecInO Proposal', color='purple')
plt.plot   (df_area_d2_proposal, df_perf_d2_proposal, label='VecInO Proposal', color='purple')
plt.axline((0, 0), (df_area_d2_proposal['VecInO Proposal']['V4-D2'], 
                    df_perf_d2_proposal['VecInO Proposal']['V4-D2']), color='purple', lw=0.5)

plt.scatter(df_area_d2_ooo, df_perf_d2_ooo, label='VecOoO', color='red')
plt.plot   (df_area_d2_ooo, df_perf_d2_ooo, label='VecOoO', color='red')
plt.axline((0, 0), (df_area_d2_ooo['VecOoO']['V4-D2'], 
                    df_perf_d2_ooo['VecOoO']['V4-D2']), color='red', lw=0.5)

plt.xlabel("Area (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
plt.xlim(0.0, df_area_whole_d2.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d2_pct.mean().max() * 1.1)
plt.savefig("area_perf.pdf", bbox_inches='tight')

df_area_whole_d2_pct.to_csv("relative_area.csv")

# %%
# 全体表示用の一覧を出力

display(pd.concat([df_cycle_whole_d2_pct.mean(), df_energy_whole_d2_pct.sum(), df_area_whole_d2_pct], axis=1))
display(pd.concat([df_cycle_whole_d4_pct.mean(), df_energy_whole_d4_pct.sum(), df_area_whole_d4_pct], axis=1))



# %%
# オリジナル実装のサイクル数を取得する

import pandas as pd
import matplotlib.pyplot as plt
import utils as ut
import util_area as ut_a
import util_cycle as ut_c
import util_power as ut_p
import numpy as np

df_cycle_v8_d2  = pd.Series(list(map(lambda b: ut_c.get_cycle(b, 'vio.v', 512, 128), ut.rivec_benchmarks)),
                                        index=ut.rivec_benchmarks)

df_cycle_origin_v8_d2  = pd.Series(list(map(lambda b: ut_c.get_cycle(b, 'vio.v', 512, 128), map(lambda b: b + "_origin", ut.rivec_benchmarks))),
                                        index=ut.rivec_benchmarks)

t = df_cycle_origin_v8_d2 / df_cycle_v8_d2
display(pd.concat([df_cycle_origin_v8_d2, df_cycle_v8_d2],axis=1))
display(t)
# %%
# L1Dの情報を取得する

import pandas as pd
import dcaches as dc
import utils as ut
import util_cycle as ut_c

def get_dcache_info_with_app(app, vlen, dlen, op):
    return list(map(lambda p: dc.get_dcache_info(app, p, vlen, dlen, op), ut.pipe_conf))
def get_insts_with_app(app, vlen, dlen):
    return list(map(lambda p: ut_c.get_insts(app, p, vlen, dlen), ut.pipe_conf))
    
df_dc_loads_v2_d2  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 128, 128, 'loads'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V2-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)

df_dc_stores_v2_d2  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 128, 128, 'stores'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V2-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)

df_dc_load_misses_v2_d2  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 128, 128, 'load-misses'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V2-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)

df_dc_store_misses_v2_d2  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 128, 128, 'store-misses'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V2-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_dc_insts_v2_d2  = pd.DataFrame(list(map(lambda b: get_insts_with_app(b, 128, 128), ut.benchmarks)), 
                                    columns=(map(lambda b: "V2-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)

# display(df_dc_loads_v16_d2)
# display(df_dc_stores_v16_d2)
display(df_dc_loads_v2_d2)
display(df_dc_load_misses_v2_d2)
display(df_dc_insts_v2_d2)
display((df_dc_load_misses_v2_d2 + df_dc_store_misses_v2_d2) / df_dc_insts_v2_d2 * 1000)

df_dc_loads_v16_d2  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 1024, 128, 'loads'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V16-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_dc_load_misses_v16_d2  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 1024, 128, 'load-misses'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V16-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_dc_store_misses_v16_d2  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 1024, 128, 'store-misses'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V16-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_dc_insts_v16_d2  = pd.DataFrame(list(map(lambda b: get_insts_with_app(b, 1024, 128), ut.benchmarks)), 
                                    columns=(map(lambda b: "V16-D2 " + b, ut.pipe_conf)), index=ut.benchmarks)
display(df_dc_loads_v16_d2)
display(df_dc_load_misses_v16_d2)
display(df_dc_insts_v16_d2)
display((df_dc_load_misses_v16_d2 + df_dc_store_misses_v16_d2) / df_dc_insts_v16_d2 * 1000)

df_dc_loads_v4_d4  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 256, 256, 'loads'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V4-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)

df_dc_stores_v4_d4  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 256, 256, 'stores'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V4-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)

df_dc_load_misses_v4_d4  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 256, 256, 'load-misses'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V4-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)

df_dc_store_misses_v4_d4  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 256, 256, 'store-misses'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V4-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_dc_insts_v4_d4  = pd.DataFrame(list(map(lambda b: get_insts_with_app(b, 256, 256), ut.benchmarks)), 
                                    columns=(map(lambda b: "V4-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)

display(df_dc_loads_v4_d4)
display(df_dc_load_misses_v4_d4)
display(df_dc_insts_v4_d4)
display((df_dc_load_misses_v4_d4 + df_dc_store_misses_v4_d4) / df_dc_insts_v4_d4 * 1000)

df_dc_loads_v32_d4  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 2048, 256, 'loads'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V32-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_dc_load_misses_v32_d4  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 2048, 256, 'load-misses'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V32-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_dc_store_misses_v32_d4  = pd.DataFrame(list(map(lambda b: get_dcache_info_with_app(b, 2048, 256, 'store-misses'), ut.benchmarks)), 
                                    columns=(map(lambda b: "V32-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)
df_dc_insts_v32_d4  = pd.DataFrame(list(map(lambda b: get_insts_with_app(b, 2048, 256), ut.benchmarks)), 
                                    columns=(map(lambda b: "V32-D4 " + b, ut.pipe_conf)), index=ut.benchmarks)
display(df_dc_loads_v32_d4)
display(df_dc_load_misses_v32_d4)
display(df_dc_insts_v32_d4)
display((df_dc_load_misses_v32_d4 + df_dc_store_misses_v32_d4) / df_dc_insts_v32_d4 * 1000)

# %%
