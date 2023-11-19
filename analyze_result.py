#%%
# SQLからデータをロードする
import pandas as pd
import matplotlib.pyplot as plt
import utils as ut
import util_area as ut_a
import util_cycle as ut_c
import util_power as ut_p
import numpy as np
from IPython.display import display

# SQLからすべての情報を取得する
sql_info  = {d: {v: {b: {c: ut.get_sqlite_info(b, v, d, c) for c in ut.pipe_conf} for b in ut.bench_and_dhry} for v in [d*1, d*2, d*4, d*8]} for d in [128, 256]}

#%%
# 面積を算出

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

df_area_whole_d2.columns = ut.d2_index2
display(df_area_whole_d2)
area_graph_d2 = df_area_whole_d2.T.plot(title="Area estimation with each configuration", 
                                  kind='bar',
                                  stacked=True)
handles, labels = area_graph_d2.get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
area_graph_d2.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
plt.ylim(0.0, df_area_whole_d4.sum().max()*1.1)
plt.show()
# plt.savefig("area_d2.pdf", bbox_inches='tight')
# plt.savefig("area_d2.png", bbox_inches='tight')
df_area_whole_d2.to_csv("csv/area_d2.csv")

df_area_whole_d4.columns = ut.d4_index2
display(df_area_whole_d4)
area_graph_d4 = df_area_whole_d4.T.plot(title="Area estimation with each configuration", 
                                        kind='bar',
                                        stacked=True)
handles, labels = area_graph_d4.get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
area_graph_d4.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
plt.show()
# plt.savefig("area_d4.pdf", bbox_inches='tight')
# plt.savefig("area_d4.png", bbox_inches='tight')
df_area_whole_d4.to_csv("csv/area_d4.csv")


#%%
# Cycleのテーブルを作る

import pandas as pd
import utils as ut
import util_cycle as ut_c

def get_cycle_with_app(app, vlen, dlen):
  print("App = %s, vlen = %d, dlen = %d" % (app, vlen, dlen))
  return [ut_c.get_cycle(sql_info, app, p, vlen, dlen) / 100000 for p in ut.pipe_conf]

df_cycle_v2_d2   = pd.DataFrame([get_cycle_with_app(b,  128, 128) for b in ut.benchmarks], columns=["V2-D2 "  + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_cycle_v4_d2   = pd.DataFrame([get_cycle_with_app(b,  256, 128) for b in ut.benchmarks], columns=["V4-D2 "  + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_cycle_v8_d2   = pd.DataFrame([get_cycle_with_app(b,  512, 128) for b in ut.benchmarks], columns=["V8-D2 "  + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_cycle_v16_d2  = pd.DataFrame([get_cycle_with_app(b, 1024, 128) for b in ut.benchmarks], columns=["V16-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_cycle_v4_d4   = pd.DataFrame([get_cycle_with_app(b,  256, 256) for b in ut.benchmarks], columns=["V4-D4 "  + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_cycle_v8_d4   = pd.DataFrame([get_cycle_with_app(b,  512, 256) for b in ut.benchmarks], columns=["V8-D4 "  + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_cycle_v16_d4  = pd.DataFrame([get_cycle_with_app(b, 1024, 256) for b in ut.benchmarks], columns=["V16-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_cycle_v32_d4  = pd.DataFrame([get_cycle_with_app(b, 2048, 256) for b in ut.benchmarks], columns=["V32-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)

#%%
# V4-D2 のテーブルを作る

# V2-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v2_d2_pct = np.reciprocal((df_cycle_v2_d2.T / df_cycle_v2_d2["V2-D2 BASE"].T).T)
df_cycle_v2_d2_pct.loc['GeoMean'] = df_cycle_v2_d2_pct.mean()
df_cycle_v2_d2_pct.plot.bar(title="V2-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_cycle_v2_d2_pct.to_csv('csv/df_cycle_v2_d2.csv')

display(df_cycle_v2_d2)
display(df_cycle_v2_d2_pct.loc['GeoMean'])

# V4-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v4_d2_pct = np.reciprocal((df_cycle_v4_d2.T / df_cycle_v4_d2["V4-D2 BASE"].T).T)
df_cycle_v4_d2_pct.loc['GeoMean'] = df_cycle_v4_d2_pct.mean()
df_cycle_v4_d2_pct.plot.bar(title="V4-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_cycle_v4_d2_pct.to_csv('csv/df_cycle_v4_d2.csv')

display(df_cycle_v4_d2)
display(df_cycle_v4_d2_pct.loc['GeoMean'])

# V8-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v8_d2_pct = np.reciprocal((df_cycle_v8_d2.T / df_cycle_v8_d2["V8-D2 BASE"].T).T)
df_cycle_v8_d2_pct.loc['GeoMean'] = df_cycle_v8_d2_pct.mean()
df_cycle_v8_d2_pct.plot.bar(title="V8-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_cycle_v8_d2_pct.to_csv('csv/df_cycle_v8_d2.csv')

display(df_cycle_v8_d2)
display(df_cycle_v8_d2_pct.loc['GeoMean'])

# V16-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v16_d2_pct = np.reciprocal((df_cycle_v16_d2.T / df_cycle_v16_d2["V16-D2 BASE"].T).T)
df_cycle_v16_d2_pct.loc['GeoMean'] = df_cycle_v16_d2_pct.mean()
df_cycle_v16_d2_pct.plot.bar(title="V16-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_cycle_v16_d2_pct.to_csv('csv/df_cycle_v16_d2.csv')

display(df_cycle_v16_d2)
display(df_cycle_v16_d2_pct.loc['GeoMean'])


#%%
# V4-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v4_d4_pct = np.reciprocal((df_cycle_v4_d4.T / df_cycle_v4_d4["V4-D4 BASE"].T).T)
df_cycle_v4_d4_pct.loc['GeoMean'] = df_cycle_v4_d4_pct.mean()
df_cycle_v4_d4_pct.plot.bar(title="V4-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_cycle_v4_d4_pct.to_csv('csv/df_cycle_v4_d4.csv')

display(df_cycle_v4_d4)
display(df_cycle_v4_d4_pct.loc['GeoMean'])

# V8-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v8_d4_pct = np.reciprocal((df_cycle_v8_d4.T / df_cycle_v8_d4["V8-D4 BASE"].T).T)
df_cycle_v8_d4_pct.loc['GeoMean'] = df_cycle_v8_d4_pct.mean()
df_cycle_v8_d4_pct.plot.bar(title="V8-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_cycle_v8_d4_pct.to_csv('csv/df_cycle_v8_d4.csv')

display(df_cycle_v8_d4)
display(df_cycle_v8_d4_pct.loc['GeoMean'])

# V16-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v16_d4_pct = np.reciprocal((df_cycle_v16_d4.T / df_cycle_v16_d4["V16-D4 BASE"].T).T)
df_cycle_v16_d4_pct.loc['GeoMean'] = df_cycle_v16_d4_pct.mean()
df_cycle_v16_d4_pct.plot.bar(title="V16-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_cycle_v16_d4_pct.to_csv('csv/df_cycle_v16_d4.csv')

display(df_cycle_v16_d4)
display(df_cycle_v16_d4_pct.loc['GeoMean'])

# V32-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v32_d4_pct = np.reciprocal((df_cycle_v32_d4.T / df_cycle_v32_d4["V32-D4 BASE"].T).T)
df_cycle_v32_d4_pct.loc['GeoMean'] = df_cycle_v32_d4_pct.mean()
df_cycle_v32_d4_pct.plot.bar(title="V32-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_cycle_v32_d4_pct.to_csv('csv/df_cycle_v32_d4.csv')

display(df_cycle_v32_d4)
display(df_cycle_v32_d4_pct.loc['GeoMean'])


#%%
## 全体的な性能グラフを作る
# D2シリーズ
df_cycle_whole_d2 = pd.concat([df_cycle_v2_d2, df_cycle_v4_d2, df_cycle_v8_d2, df_cycle_v16_d2], axis=1)
display(df_cycle_whole_d2)
df_cycle_whole_d2.columns = ut.d2_index2

df_cycle_whole_d2_pct = np.reciprocal((df_cycle_whole_d2.T / df_cycle_v2_d2["V2-D2 SV Fence"].T).T)
df_cycle_means_d2 = df_cycle_whole_d2_pct.mean()
display(df_cycle_means_d2)
# plt.figure()
# df_cycle_means_d2.plot.line(style=['bo-'], title="Relative Performance of V2-D2 / V4-D2 / V8-D2 / V16-D2", figsize=(10, 3))
# plt.savefig("relative_performance.pdf", bbox_inches='tight')

# D4シリーズ
df_cycle_whole_d4 = pd.concat([df_cycle_v4_d4, df_cycle_v8_d4, df_cycle_v16_d4, df_cycle_v32_d4], axis=1)
display(df_cycle_whole_d4)
df_cycle_whole_d4.columns = ut.d4_index2

df_cycle_whole_d4_pct = np.reciprocal((df_cycle_whole_d4.T / df_cycle_v4_d4["V4-D4 SV Fence"].T).T)
df_cycle_means_d4 = df_cycle_whole_d4_pct.mean()
display(df_cycle_means_d4)
# plt.figure()
# df_cycle_means_d4.plot.line(style=['bo-'], title="Relative Performance of V4-D4 / V8-D4 / V16-D4 / V32-D2", figsize=(10, 3))
# plt.savefig("relative_performance.pdf", bbox_inches='tight')


#%%
# V4-D2のサイクル数でグラフを作る

import pandas as pd
import util_power as ut_p

v2_d2_power = ut_p.get_power_with_vlen_dlen(128, 128)
df_power_detail_v2_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v2_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v2_d2.columns = list(map(lambda b: "V2-D2 " + b, ut.pipe_conf2))
df_power_detail_v2_d2.index = ut.benchmarks

v4_d2_power = ut_p.get_power_with_vlen_dlen(256, 128)
df_power_detail_v4_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v4_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v4_d2.columns = list(map(lambda b: "V4-D2 " + b, ut.pipe_conf2))
df_power_detail_v4_d2.index = ut.benchmarks

v8_d2_power = ut_p.get_power_with_vlen_dlen(512, 128)
df_power_detail_v8_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v8_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v8_d2.columns = list(map(lambda b: "V8-D2 " + b, ut.pipe_conf2))
df_power_detail_v8_d2.index = ut.benchmarks

v16_d2_power = ut_p.get_power_with_vlen_dlen(1024, 128)
df_power_detail_v16_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(v16_d2_power[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_detail_v16_d2.columns = list(map(lambda b: "V16-D2 " + b, ut.pipe_conf2))
df_power_detail_v16_d2.index = ut.benchmarks

df_energy_v2_d2 = df_power_detail_v2_d2 * df_cycle_v2_d2
df_sum_energy_v2_d2 = df_energy_v2_d2.sum()

df_energy_v4_d2 = df_power_detail_v4_d2 * df_cycle_v4_d2
df_sum_energy_v4_d2 = df_energy_v4_d2.sum()

df_energy_v8_d2 = df_power_detail_v8_d2 * df_cycle_v8_d2
df_sum_energy_v8_d2 = df_energy_v8_d2.sum()

df_energy_v16_d2 = df_power_detail_v16_d2 * df_cycle_v16_d2
df_sum_energy_v16_d2 = df_energy_v16_d2.sum()

#%%
# V2-D2のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_group_v2_d2 = ut_p.get_group_power_with_vlen_dlen(128, 128)

df_power_group_v2_d2 = pd.DataFrame(power_group_v2_d2, index=ut.benchmarks).fillna(0.0) 
df_power_group_v2_d2.columns = list(map(lambda b: "V2-D2 " + b, df_power_group_v2_d2.columns))

df_power_group_bench_sum_v2_d2  = pd.DataFrame()
df_energy_group_bench_sum_v2_d2 = pd.DataFrame()

for c in df_power_group_v2_d2.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_group_v2_d2.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v2_d2.loc[b].loc[c]
  # 行の追加
  df_power_group_bench_sum_v2_d2  = pd.concat([df_power_group_bench_sum_v2_d2 , p], axis=1)
  df_energy_group_bench_sum_v2_d2 = pd.concat([df_energy_group_bench_sum_v2_d2, e], axis=1)

df_power_group_bench_sum_v2_d2 = df_power_group_bench_sum_v2_d2.fillna(0.0)
df_energy_group_bench_sum_v2_d2 = df_energy_group_bench_sum_v2_d2.fillna(0.0)

# 各アプリケーション毎に電力グラフを作る

power_modules = [
  'Fetch',
  'Scalar Rename',
  'Scheduler',
  'Scalar FU + RF',
  'Vector FU',
  'Vector FU',
  'Vector RF',
  'L1D Cache',
  'Scalar LSU',
  'Vector Rename',
  'Vector LSU',
]


#display(pd.concat([pd.DataFrame(df_power_group_v2_d2.loc['axpy']).T.applymap(lambda cell: cell[m]) for m in power_modules]))
pd.concat([pd.DataFrame(pd.concat([pd.DataFrame(df_power_group_v2_d2.loc[b]).T.applymap(lambda cell: cell[m]).rename(index={b:m}) for m in power_modules])) 
           for b in ut.benchmarks], axis=1) \
             .to_csv('csv/v2_d2_power_with_app.csv')

#%%

# V4-D2のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_group_v4_d2 = ut_p.get_group_power_with_vlen_dlen(256, 128)

df_power_group_v4_d2 = pd.DataFrame(power_group_v4_d2, index=ut.benchmarks).fillna(0.0) 
df_power_group_v4_d2.columns = list(map(lambda b: "V4-D2 " + b, df_power_group_v4_d2.columns))

df_power_group_bench_sum_v4_d2  = pd.DataFrame()
df_energy_group_bench_sum_v4_d2 = pd.DataFrame()

for c in df_power_group_v4_d2.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_group_v4_d2.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v4_d2.loc[b].loc[c]
  # 行の追加
  df_power_group_bench_sum_v4_d2  = pd.concat([df_power_group_bench_sum_v4_d2, p],  axis=1)
  df_energy_group_bench_sum_v4_d2 = pd.concat([df_energy_group_bench_sum_v4_d2, e], axis=1)

# V8-D2のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_group_v8_d2 = ut_p.get_group_power_with_vlen_dlen(512, 128)

df_power_group_v8_d2 = pd.DataFrame(power_group_v8_d2, index=ut.benchmarks).fillna(0.0) 
df_power_group_v8_d2.columns = list(map(lambda b: "V8-D2 " + b, df_power_group_v8_d2.columns))

df_power_group_bench_sum_v8_d2  = pd.DataFrame()
df_energy_group_bench_sum_v8_d2 = pd.DataFrame()

for c in df_power_group_v8_d2.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_group_v8_d2.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v8_d2.loc[b].loc[c]
  # 行の追加
  df_power_group_bench_sum_v8_d2  = pd.concat([df_power_group_bench_sum_v8_d2, p], axis=1)
  df_energy_group_bench_sum_v8_d2 = pd.concat([df_energy_group_bench_sum_v8_d2, e], axis=1)

# v16-D2のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_group_v16_d2 = ut_p.get_group_power_with_vlen_dlen(1024, 128)

df_power_group_v16_d2 = pd.DataFrame(power_group_v16_d2, index=ut.benchmarks).fillna(0.0) 
df_power_group_v16_d2.columns = list(map(lambda b: "V16-D2 " + b, df_power_group_v16_d2.columns))

df_power_group_bench_sum_v16_d2  = pd.DataFrame()
df_energy_group_bench_sum_v16_d2 = pd.DataFrame()

for c in df_power_group_v16_d2.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_group_v16_d2.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v16_d2.loc[b].loc[c]
  # 行の追加
  df_power_group_bench_sum_v16_d2  = pd.concat([df_power_group_bench_sum_v16_d2, p], axis=1)
  df_energy_group_bench_sum_v16_d2 = pd.concat([df_energy_group_bench_sum_v16_d2, e], axis=1)


# V4-D4のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_group_v4_d4 = ut_p.get_group_power_with_vlen_dlen(256, 256)

df_power_group_v4_d4 = pd.DataFrame(power_group_v4_d4, index=ut.benchmarks).fillna(0.0) 
df_power_group_v4_d4.columns = list(map(lambda b: "V4-D4 " + b, df_power_group_v4_d4.columns))

df_power_group_bench_sum_v4_d4 = pd.DataFrame()
df_energy_group_bench_sum_v4_d4 = pd.DataFrame()

for c in df_power_group_v4_d4.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_group_v4_d4.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v4_d4.loc[b].loc[c]
  # 行の追加
  df_power_group_bench_sum_v4_d4  = pd.concat([df_power_group_bench_sum_v4_d4, p], axis=1)
  df_energy_group_bench_sum_v4_d4 = pd.concat([df_energy_group_bench_sum_v4_d4, e], axis=1)


# V8-D4のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_group_v8_d4 = ut_p.get_group_power_with_vlen_dlen(512, 256)

df_power_group_v8_d4 = pd.DataFrame(power_group_v8_d4, index=ut.benchmarks).fillna(0.0) 
df_power_group_v8_d4.columns = list(map(lambda b: "V8-D4 " + b, df_power_group_v8_d4.columns))

df_power_group_bench_sum_v8_d4  = pd.DataFrame()
df_energy_group_bench_sum_v8_d4 = pd.DataFrame()

for c in df_power_group_v8_d4.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_group_v8_d4.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v8_d4.loc[b].loc[c]
  # 行の追加
  df_power_group_bench_sum_v8_d4  = pd.concat([df_power_group_bench_sum_v8_d4, p],  axis=1)
  df_energy_group_bench_sum_v8_d4 = pd.concat([df_energy_group_bench_sum_v8_d4, e], axis=1)


# V16-D4のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_group_v16_d4 = ut_p.get_group_power_with_vlen_dlen(1024, 256)

df_power_group_v16_d4 = pd.DataFrame(power_group_v16_d4, index=ut.benchmarks).fillna(0.0) 
df_power_group_v16_d4.columns = list(map(lambda b: "V16-D4 " + b, df_power_group_v16_d4.columns))

df_power_group_bench_sum_v16_d4  = pd.DataFrame()
df_energy_group_bench_sum_v16_d4 = pd.DataFrame()

for c in df_power_group_v16_d4.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_group_v16_d4.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v16_d4.loc[b].loc[c]
  # 行の追加
  df_power_group_bench_sum_v16_d4  = pd.concat([df_power_group_bench_sum_v16_d4, p], axis=1)
  df_energy_group_bench_sum_v16_d4 = pd.concat([df_energy_group_bench_sum_v16_d4, e], axis=1)


# V32-D4のエネルギー詳細を取得する
# 作りたいもの：
#  行：各モジュールの消費エネルギー(各ベンチマークのものの総合計)
#  列：各コンフィグレーション

power_group_v32_d4 = ut_p.get_group_power_with_vlen_dlen(2048, 256)

df_power_group_v32_d4 = pd.DataFrame(power_group_v32_d4, index=ut.benchmarks).fillna(0.0) 
df_power_group_v32_d4.columns = list(map(lambda b: "V32-D4 " + b, df_power_group_v32_d4.columns))

df_power_group_bench_sum_v32_d4  = pd.DataFrame()
df_energy_group_bench_sum_v32_d4 = pd.DataFrame()

for c in df_power_group_v32_d4.columns:
  p = pd.Series(name=c)
  e = pd.Series(name=c)
  for b in ut.benchmarks:
    for d in df_power_group_v32_d4.loc[b].loc[c].items():
      # d[0] 各ユニットの名前
      # d[1] 各ユニットの消費電力
      p.loc[d[0]] = p.get(d[0], 0) + d[1]
      e.loc[d[0]] = e.get(d[0], 0) + d[1] * df_cycle_v32_d4.loc[b].loc[c]
  # 行の追加
  df_power_group_bench_sum_v32_d4  = pd.concat([df_power_group_bench_sum_v32_d4, p], axis=1)
  df_energy_group_bench_sum_v32_d4 = pd.concat([df_energy_group_bench_sum_v32_d4, e], axis=1)


#%%
# 全部の電力を比較

df_power_base_v2_d2      = pd.DataFrame()
df_power_base_pct_v2_d2  = pd.DataFrame()
df_power_base_v4_d2      = pd.DataFrame()
df_power_base_pct_v4_d2  = pd.DataFrame()
df_power_base_v8_d2      = pd.DataFrame()
df_power_base_pct_v8_d2  = pd.DataFrame()
df_power_base_v16_d2     = pd.DataFrame()
df_power_base_pct_v16_d2 = pd.DataFrame()
df_power_prop_v2_d2      = pd.DataFrame()
df_power_prop_pct_v2_d2  = pd.DataFrame()
df_power_prop_v4_d2      = pd.DataFrame()
df_power_prop_pct_v4_d2  = pd.DataFrame()
df_power_prop_v8_d2      = pd.DataFrame()
df_power_prop_pct_v8_d2  = pd.DataFrame()
df_power_prop_v16_d2     = pd.DataFrame()
df_power_prop_pct_v16_d2 = pd.DataFrame()

for b in ut.benchmarks:
  df_power_base_v2_d2    [b] = pd.Series(df_power_group_v2_d2.loc[b].loc['V2-D2 BASE'])
  df_power_base_pct_v2_d2[b] = df_power_base_v2_d2[b] / df_power_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_prop_v2_d2    [b] = pd.Series(df_power_group_v2_d2.loc[b].loc['V2-D2 PROP'])
  df_power_prop_pct_v2_d2[b] = df_power_prop_v2_d2[b] / df_power_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_base_v4_d2    [b] = pd.Series(df_power_group_v4_d2.loc[b].loc['V4-D2 BASE'])
  df_power_base_pct_v4_d2[b] = df_power_base_v4_d2[b] / df_power_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_prop_v4_d2    [b] = pd.Series(df_power_group_v4_d2.loc[b].loc['V4-D2 PROP'])
  df_power_prop_pct_v4_d2[b] = df_power_prop_v4_d2[b] / df_power_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_base_v8_d2    [b] = pd.Series(df_power_group_v8_d2.loc[b].loc['V8-D2 BASE'])
  df_power_base_pct_v8_d2[b] = df_power_base_v8_d2[b] / df_power_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_prop_v8_d2    [b] = pd.Series(df_power_group_v8_d2.loc[b].loc['V8-D2 PROP'])
  df_power_prop_pct_v8_d2[b] = df_power_prop_v8_d2[b] / df_power_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_base_v16_d2    [b] = pd.Series(df_power_group_v16_d2.loc[b].loc['V16-D2 BASE'])
  df_power_base_pct_v16_d2[b] = df_power_base_v16_d2[b] / df_power_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_prop_v16_d2    [b] = pd.Series(df_power_group_v16_d2.loc[b].loc['V16-D2 PROP'])
  df_power_prop_pct_v16_d2[b] = df_power_prop_v16_d2[b] / df_power_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化


# 最終的に欲しいV2-D2 PROP/V2-D2 BASE / V8-D2 PROP / V8-D8 PROPのグラフを作る
df_power_whole_d2_pct = pd.concat([df_power_prop_pct_v2_d2.T.mean(),
                                    df_power_base_pct_v2_d2.T.mean(),
                                    df_power_prop_pct_v4_d2.T.mean(),
                                    df_power_base_pct_v4_d2.T.mean(),
                                    df_power_prop_pct_v8_d2.T.mean(),
                                    df_power_base_pct_v8_d2.T.mean(),
                                    df_power_prop_pct_v16_d2.T.mean(),
                                    df_power_base_pct_v16_d2.T.mean(),], axis=1,
                           keys = ["V2-D2 PROP", "V2-D2 BASE", "V4-D2 PROP", "V4-D2 BASE", "V8-D2 PROP", "V8-D2 BASE", "V16-D2 PROP", "V16-D2 BASE"])

df_power_whole_d2_pct.T.plot(kind='bar', stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_power_whole_d2_pct.to_csv("csv/power_d2.csv")

df_power_base_v4_d4      = pd.DataFrame()
df_power_base_pct_v4_d4  = pd.DataFrame()
df_power_base_v8_d4      = pd.DataFrame()
df_power_base_pct_v8_d4  = pd.DataFrame()
df_power_base_v16_d4     = pd.DataFrame()
df_power_base_pct_v16_d4 = pd.DataFrame()
df_power_base_v32_d4     = pd.DataFrame()
df_power_base_pct_v32_d4 = pd.DataFrame()
df_power_prop_v4_d4      = pd.DataFrame()
df_power_prop_pct_v4_d4  = pd.DataFrame()
df_power_prop_v8_d4      = pd.DataFrame()
df_power_prop_pct_v8_d4  = pd.DataFrame()
df_power_prop_v16_d4     = pd.DataFrame()
df_power_prop_pct_v16_d4 = pd.DataFrame()
df_power_prop_v32_d4     = pd.DataFrame()
df_power_prop_pct_v32_d4 = pd.DataFrame()

for b in ut.benchmarks:
  df_power_base_v4_d4    [b] = pd.Series(df_power_group_v4_d4.loc[b].loc['V4-D4 BASE'])
  df_power_base_pct_v4_d4[b] = df_power_base_v4_d4[b] / df_power_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_prop_v4_d4    [b] = pd.Series(df_power_group_v4_d4.loc[b].loc['V4-D4 PROP'])
  df_power_prop_pct_v4_d4[b] = df_power_prop_v4_d4[b] / df_power_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_base_v8_d4    [b] = pd.Series(df_power_group_v8_d4.loc[b].loc['V8-D4 BASE'])
  df_power_base_pct_v8_d4[b] = df_power_base_v8_d4[b] / df_power_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_prop_v8_d4    [b] = pd.Series(df_power_group_v8_d4.loc[b].loc['V8-D4 PROP'])
  df_power_prop_pct_v8_d4[b] = df_power_prop_v8_d4[b] / df_power_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_base_v16_d4    [b] = pd.Series(df_power_group_v16_d4.loc[b].loc['V16-D4 BASE'])
  df_power_base_pct_v16_d4[b] = df_power_base_v16_d4[b] / df_power_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_prop_v16_d4    [b] = pd.Series(df_power_group_v16_d4.loc[b].loc['V16-D4 PROP'])
  df_power_prop_pct_v16_d4[b] = df_power_prop_v16_d4[b] / df_power_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_base_v32_d4    [b] = pd.Series(df_power_group_v32_d4.loc[b].loc['V32-D4 BASE'])
  df_power_base_pct_v32_d4[b] = df_power_base_v32_d4[b] / df_power_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_power_prop_v32_d4    [b] = pd.Series(df_power_group_v32_d4.loc[b].loc['V32-D4 PROP'])
  df_power_prop_pct_v32_d4[b] = df_power_prop_v32_d4[b] / df_power_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化


# 最終的に欲しいV2-D2 PROP/V2-D2 BASE / V8-D2 PROP / V8-D8 PROPのグラフを作る
df_power_whole_d4_pct = pd.concat([df_power_prop_pct_v4_d4.T.mean(),
                                   df_power_base_pct_v4_d4.T.mean(),
                                   df_power_prop_pct_v8_d4.T.mean(),
                                   df_power_base_pct_v8_d4.T.mean(),
                                   df_power_prop_pct_v16_d4.T.mean(),
                                   df_power_base_pct_v16_d4.T.mean(),
                                   df_power_prop_pct_v32_d4.T.mean(),
                                   df_power_base_pct_v32_d4.T.mean()], axis=1,
                           keys = ["V4-D4 PROP", "V4-D4 BASE", "V8-D4 PROP", "V8-D4 BASE", "V16-D4 PROP", "V16-D4 BASE", "V32-D4 PROP", "V32-D4 BASE"])

df_power_whole_d4_pct.T.plot(kind='bar', stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_power_whole_d4_pct.to_csv("csv/power_d4.csv")


#%% 各アプリケーション毎にグラフを作り直し
# 全部のエネルギーを比較

df_energy_base_v2_d2      = pd.DataFrame()
df_energy_base_pct_v2_d2  = pd.DataFrame()
df_energy_base_v4_d2      = pd.DataFrame()
df_energy_base_pct_v4_d2  = pd.DataFrame()
df_energy_base_v8_d2      = pd.DataFrame()
df_energy_base_pct_v8_d2  = pd.DataFrame()
df_energy_base_v16_d2     = pd.DataFrame()
df_energy_base_pct_v16_d2 = pd.DataFrame()
df_energy_prop_v2_d2      = pd.DataFrame()
df_energy_prop_pct_v2_d2  = pd.DataFrame()
df_energy_prop_v4_d2      = pd.DataFrame()
df_energy_prop_pct_v4_d2  = pd.DataFrame()
df_energy_prop_v8_d2      = pd.DataFrame()
df_energy_prop_pct_v8_d2  = pd.DataFrame()
df_energy_prop_v16_d2     = pd.DataFrame()
df_energy_prop_pct_v16_d2 = pd.DataFrame()

for b in ut.benchmarks:
  df_energy_base_v2_d2    [b] = pd.Series(df_power_group_v2_d2.loc[b].loc['V2-D2 BASE']) * df_cycle_v2_d2.loc[b].loc['V2-D2 BASE']
  df_energy_base_pct_v2_d2[b] = df_energy_base_v2_d2[b] / df_energy_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_prop_v2_d2    [b] = pd.Series(df_power_group_v2_d2.loc[b].loc['V2-D2 PROP']) * df_cycle_v2_d2.loc[b].loc['V2-D2 PROP']
  df_energy_prop_pct_v2_d2[b] = df_energy_prop_v2_d2[b] / df_energy_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_base_v4_d2    [b] = pd.Series(df_power_group_v4_d2.loc[b].loc['V4-D2 BASE']) * df_cycle_v4_d2.loc[b].loc['V4-D2 BASE']
  df_energy_base_pct_v4_d2[b] = df_energy_base_v4_d2[b] / df_energy_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_prop_v4_d2    [b] = pd.Series(df_power_group_v4_d2.loc[b].loc['V4-D2 PROP']) * df_cycle_v4_d2.loc[b].loc['V4-D2 PROP']
  df_energy_prop_pct_v4_d2[b] = df_energy_prop_v4_d2[b] / df_energy_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_base_v8_d2    [b] = pd.Series(df_power_group_v8_d2.loc[b].loc['V8-D2 BASE']) * df_cycle_v8_d2.loc[b].loc['V8-D2 BASE']
  df_energy_base_pct_v8_d2[b] = df_energy_base_v8_d2[b] / df_energy_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_prop_v8_d2    [b] = pd.Series(df_power_group_v8_d2.loc[b].loc['V8-D2 PROP']) * df_cycle_v8_d2.loc[b].loc['V8-D2 PROP']
  df_energy_prop_pct_v8_d2[b] = df_energy_prop_v8_d2[b] / df_energy_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_base_v16_d2    [b] = pd.Series(df_power_group_v16_d2.loc[b].loc['V16-D2 BASE']) * df_cycle_v16_d2.loc[b].loc['V16-D2 BASE']
  df_energy_base_pct_v16_d2[b] = df_energy_base_v16_d2[b] / df_energy_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_prop_v16_d2    [b] = pd.Series(df_power_group_v16_d2.loc[b].loc['V16-D2 PROP']) * df_cycle_v16_d2.loc[b].loc['V16-D2 PROP']
  df_energy_prop_pct_v16_d2[b] = df_energy_prop_v16_d2[b] / df_energy_base_v2_d2[b].sum()   # V2-D2のエネルギーで割って正規化


# 最終的に欲しいV2-D2 PROP/V2-D2 BASE / V8-D2 PROP / V8-D8 PROPのグラフを作る
df_energy_whole_d2_pct = pd.concat([df_energy_prop_pct_v2_d2.T.mean(),
                                    df_energy_base_pct_v2_d2.T.mean(),
                                    df_energy_prop_pct_v4_d2.T.mean(),
                                    df_energy_base_pct_v4_d2.T.mean(),
                                    df_energy_prop_pct_v8_d2.T.mean(),
                                    df_energy_base_pct_v8_d2.T.mean(),
                                    df_energy_prop_pct_v16_d2.T.mean(),
                                    df_energy_base_pct_v16_d2.T.mean(),], axis=1,
                           keys = ["V2-D2 PROP", "V2-D2 BASE", "V4-D2 PROP", "V4-D2 BASE", "V8-D2 PROP", "V8-D2 BASE", "V16-D2 PROP", "V16-D2 BASE"])

df_energy_whole_d2_pct.T.plot(kind='bar', stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_energy_whole_d2_pct.to_csv("csv/energy_d2.csv")

df_energy_base_v4_d4      = pd.DataFrame()
df_energy_base_pct_v4_d4  = pd.DataFrame()
df_energy_base_v8_d4      = pd.DataFrame()
df_energy_base_pct_v8_d4  = pd.DataFrame()
df_energy_base_v16_d4      = pd.DataFrame()
df_energy_base_pct_v16_d4  = pd.DataFrame()
df_energy_base_v32_d4     = pd.DataFrame()
df_energy_base_pct_v32_d4 = pd.DataFrame()
df_energy_prop_v4_d4      = pd.DataFrame()
df_energy_prop_pct_v4_d4  = pd.DataFrame()
df_energy_prop_v8_d4      = pd.DataFrame()
df_energy_prop_pct_v8_d4  = pd.DataFrame()
df_energy_prop_v16_d4      = pd.DataFrame()
df_energy_prop_pct_v16_d4  = pd.DataFrame()
df_energy_prop_v32_d4     = pd.DataFrame()
df_energy_prop_pct_v32_d4 = pd.DataFrame()

for b in ut.benchmarks:
  df_energy_base_v4_d4    [b] = pd.Series(df_power_group_v4_d4.loc[b].loc['V4-D4 BASE']) * df_cycle_v4_d4.loc[b].loc['V4-D4 BASE']
  df_energy_base_pct_v4_d4[b] = df_energy_base_v4_d4[b] / df_energy_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_prop_v4_d4    [b] = pd.Series(df_power_group_v4_d4.loc[b].loc['V4-D4 PROP']) * df_cycle_v4_d4.loc[b].loc['V4-D4 PROP']
  df_energy_prop_pct_v4_d4[b] = df_energy_prop_v4_d4[b] / df_energy_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_base_v8_d4    [b] = pd.Series(df_power_group_v8_d4.loc[b].loc['V8-D4 BASE']) * df_cycle_v8_d4.loc[b].loc['V8-D4 BASE']
  df_energy_base_pct_v8_d4[b] = df_energy_base_v8_d4[b] / df_energy_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_prop_v8_d4    [b] = pd.Series(df_power_group_v8_d4.loc[b].loc['V8-D4 PROP']) * df_cycle_v8_d4.loc[b].loc['V8-D4 PROP']
  df_energy_prop_pct_v8_d4[b] = df_energy_prop_v8_d4[b] / df_energy_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_base_v16_d4    [b] = pd.Series(df_power_group_v16_d4.loc[b].loc['V16-D4 BASE']) * df_cycle_v16_d4.loc[b].loc['V16-D4 BASE']
  df_energy_base_pct_v16_d4[b] = df_energy_base_v16_d4[b] / df_energy_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_prop_v16_d4    [b] = pd.Series(df_power_group_v16_d4.loc[b].loc['V16-D4 PROP']) * df_cycle_v16_d4.loc[b].loc['V16-D4 PROP']
  df_energy_prop_pct_v16_d4[b] = df_energy_prop_v16_d4[b] / df_energy_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_base_v32_d4    [b] = pd.Series(df_power_group_v32_d4.loc[b].loc['V32-D4 BASE']) * df_cycle_v32_d4.loc[b].loc['V32-D4 BASE']
  df_energy_base_pct_v32_d4[b] = df_energy_base_v32_d4[b] / df_energy_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化

  df_energy_prop_v32_d4    [b] = pd.Series(df_power_group_v32_d4.loc[b].loc['V32-D4 PROP']) * df_cycle_v32_d4.loc[b].loc['V32-D4 PROP']
  df_energy_prop_pct_v32_d4[b] = df_energy_prop_v32_d4[b] / df_energy_base_v4_d4[b].sum()   # V2-D2のエネルギーで割って正規化


# 最終的に欲しいV2-D2 PROP/V2-D2 BASE / V8-D2 PROP / V8-D8 PROPのグラフを作る
df_energy_whole_d4_pct = pd.concat([df_energy_prop_pct_v4_d4.T.mean(),
                                    df_energy_base_pct_v4_d4.T.mean(),
                                    df_energy_prop_pct_v8_d4.T.mean(),
                                    df_energy_base_pct_v8_d4.T.mean(),
                                    df_energy_prop_pct_v16_d4.T.mean(),
                                    df_energy_base_pct_v16_d4.T.mean(),
                                    df_energy_prop_pct_v32_d4.T.mean(),
                                    df_energy_base_pct_v32_d4.T.mean()], axis=1,
                           keys = ["V4-D4 PROP", "V4-D4 BASE", "V8-D4 PROP", "V8-D4 BASE", "V16-D4 PROP", "V16-D4 BASE", "V32-D4 PROP", "V32-D4 BASE"])

df_energy_whole_d4_pct.T.plot(kind='bar', stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
df_energy_whole_d4_pct.to_csv("csv/energy_d4.csv")


#%%
# # 全部のエネルギーを計算
# df_energy_whole_d2 = pd.concat([df_energy_group_bench_sum_v2_d2, 
#                                 df_energy_group_bench_sum_v4_d2,
#                                 df_energy_group_bench_sum_v8_d2,
#                                 df_energy_group_bench_sum_v16_d2], axis=1)
# # df_energy_whole_d2.columns = ut.d2_index2
# df_energy_whole_d2.to_csv("csv/energy_d2.csv")
# 
# df_energy_whole_d4 = pd.concat([df_energy_group_bench_sum_v4_d4,
#                                 df_energy_group_bench_sum_v8_d4,
#                                 df_energy_group_bench_sum_v16_d4,
#                                 df_energy_group_bench_sum_v32_d4], axis=1)
# df_energy_whole_d4.to_csv("csv/energy_d4.csv")
# # df_energy_whole_d4.columns = ut.d4_index2

# display(df_energy_whole_d2)
# energy_graph = df_energy_whole_d2.T.plot(kind='bar', title="Energy Estimation of V2-D2 V4-D2 V8-D2 V16-D2", stacked=True)
# handles, labels = energy_graph.get_legend_handles_labels()
# handles = handles[::-1]
# labels = labels[::-1]
# energy_graph.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
# plt.ylim(0.0, df_energy_whole_d4.sum().max() * 1.1)
# plt.show()
# 
# # plt.savefig("relative_energy.pdf", bbox_inches='tight')
# 
# display(df_energy_whole_d4)
# energy_graph = df_energy_whole_d4.T.plot(kind='bar', title="Energy Estimation of V4-D4 V8-D4 V16-D4 V32-D4", stacked=True)
# handles, labels = energy_graph.get_legend_handles_labels()
# handles = handles[::-1]
# labels = labels[::-1]
# energy_graph.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
# plt.show()


# %%
# D2 : 性能とエネルギーの分布図を作る

import numpy as np

# df_energy_whole_d2_pct = df_energy_whole_d2 / df_energy_whole_d2.sum().min()

d2_index_list = ['V2-D2', 'V4-D2', 'V8-D2', 'V16-D2']

# df_perf_d2_fence    = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='SV Fence$').mean(),     columns=['SV Fence']    ).set_axis(d2_index_list, axis=0)
# df_perf_d2_lsuino   = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='SV MEM Fence$').mean(), columns=['SV MEM Fence']).set_axis(d2_index_list, axis=0)
# df_perf_d2_nomerge  = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='Prop1$').mean(),        columns=['Prop1']       ).set_axis(d2_index_list, axis=0)
df_perf_d2_proposal = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='PROP$').mean(), columns=['PROP'] ).set_axis(d2_index_list, axis=0)
df_perf_d2_ooo      = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='BASE$').mean(),          columns=['BASE']      ).set_axis(d2_index_list, axis=0)

# df_energy_d2_fence    = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='SV Fence$').sum(),     columns=['SV Fence']    ).set_axis(d2_index_list, axis=0)
# df_energy_d2_lsuino   = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='SV MEM Fence$').sum(), columns=['SV MEM Fence']).set_axis(d2_index_list, axis=0)
# df_energy_d2_nomerge  = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='Prop1$').sum(),        columns=['Prop1']       ).set_axis(d2_index_list, axis=0)
df_energy_d2_proposal = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='PROP$').sum(), columns=['PROP'] ).set_axis(d2_index_list, axis=0)
df_energy_d2_ooo      = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='BASE$').sum(),          columns=['BASE']      ).set_axis(d2_index_list, axis=0)

# df_area_d2_fence    = pd.DataFrame(df_area_whole_d2.filter(regex='SV Fence$').sum(),     columns=['SV Fence']    ).set_axis(d2_index_list, axis=0)
# df_area_d2_lsuino   = pd.DataFrame(df_area_whole_d2.filter(regex='SV MEM Fence$').sum(), columns=['SV MEM Fence']).set_axis(d2_index_list, axis=0)
# df_area_d2_nomerge  = pd.DataFrame(df_area_whole_d2.filter(regex='Prop1$').sum(),        columns=['Prop1']       ).set_axis(d2_index_list, axis=0)
df_area_d2_proposal = pd.DataFrame(df_area_whole_d2.filter(regex='PROP$').sum(), columns=['PROP'] ).set_axis(d2_index_list, axis=0)
df_area_d2_ooo      = pd.DataFrame(df_area_whole_d2.filter(regex='BASE$').sum(),          columns=['BASE']      ).set_axis(d2_index_list, axis=0)

# plt.scatter(df_energy_d2_fence, df_perf_d2_fence, label='SV Fence', color='blue')
# plt.plot   (df_energy_d2_fence, df_perf_d2_fence, color='blue')
# plt.axline((0, 0), (df_energy_d2_fence['SV Fence']['V4-D2'], 
#                     df_perf_d2_fence  ['SV Fence']['V4-D2']), color='blue', lw=0.5)
# 
# plt.scatter(df_energy_d2_nomerge, df_perf_d2_nomerge, label='Prop1', color='green')
# plt.plot   (df_energy_d2_nomerge, df_perf_d2_nomerge, label='Prop1', color='green')
# plt.axline((0, 0), (df_energy_d2_nomerge['Prop1']['V4-D2'], 
#                     df_perf_d2_nomerge  ['Prop1']['V4-D2']), color='green', lw=0.5)

plt.scatter(df_energy_d2_proposal, df_perf_d2_proposal, label='PROP', color='purple')
plt.plot   (df_energy_d2_proposal, df_perf_d2_proposal, label='PROP', color='purple')
plt.axline((0, 0), (df_energy_d2_proposal['PROP']['V4-D2'], 
                    df_perf_d2_proposal  ['PROP']['V4-D2']), color='purple', lw=0.5)

plt.scatter(df_energy_d2_ooo, df_perf_d2_ooo, label='BASE', color='red')
plt.plot   (df_energy_d2_ooo, df_perf_d2_ooo, label='BASE', color='red')
plt.axline((0, 0), (df_energy_d2_ooo['BASE']['V4-D2'], 
                    df_perf_d2_ooo  ['BASE']['V4-D2']), color='red', lw=0.5)

plt.xlim(0.0, df_energy_whole_d2_pct.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d2_pct.mean().max() * 1.1)
plt.xlabel("Energy (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
# plt.savefig("energy_perf_d2.pdf", bbox_inches='tight')

#%%
# D4 : 性能とエネルギーの分布図を作る

# df_energy_whole_d4_pct = df_energy_whole_d4 / df_energy_whole_d4.sum().min()

d4_index_list = ['V4-D4', 'V8-D4', 'V16-D4', 'V32-D4']

# df_perf_d4_fence    = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='SV Fence$').mean(),    columns=['SV Fence']   ).set_axis(d4_index_list, axis=0)
# df_perf_d4_lsuino   = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='SV MEM Fence$').mean(),   columns=['SV MEM Fence']  ).set_axis(d4_index_list, axis=0)
# df_perf_d4_nomerge  = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='Prop1$').mean(),  columns=['Prop1'] ).set_axis(d4_index_list, axis=0)
df_perf_d4_proposal = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='PROP$').mean(), columns=['PROP']).set_axis(d4_index_list, axis=0)
df_perf_d4_ooo      = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='BASE$').mean(),      columns=['BASE']         ).set_axis(d4_index_list, axis=0)

# df_energy_d4_fence    = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='SV Fence$').sum(),    columns=['SV Fence']   ).set_axis(d4_index_list, axis=0)
# df_energy_d4_lsuino   = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='SV MEM Fence$').sum(),   columns=['SV MEM Fence']  ).set_axis(d4_index_list, axis=0)
# df_energy_d4_nomerge  = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='Prop1$').sum(),  columns=['Prop1'] ).set_axis(d4_index_list, axis=0)
df_energy_d4_proposal = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='PROP$').sum(), columns=['PROP']).set_axis(d4_index_list, axis=0)
df_energy_d4_ooo      = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='BASE$').sum(),      columns=['BASE']         ).set_axis(d4_index_list, axis=0)

# df_area_d4_fence    = pd.DataFrame(df_area_whole_d4.filter(regex='SV Fence$').sum(),    columns=['SV Fence']   ).set_axis(d4_index_list, axis=0)
# df_area_d4_lsuino   = pd.DataFrame(df_area_whole_d4.filter(regex='SV MEM Fence$').sum(),   columns=['SV MEM Fence']  ).set_axis(d4_index_list, axis=0)
# df_area_d4_nomerge  = pd.DataFrame(df_area_whole_d4.filter(regex='Prop1$').sum(),  columns=['Prop1'] ).set_axis(d4_index_list, axis=0)
df_area_d4_proposal = pd.DataFrame(df_area_whole_d4.filter(regex='PROP$').sum(), columns=['PROP']).set_axis(d4_index_list, axis=0)
df_area_d4_ooo      = pd.DataFrame(df_area_whole_d4.filter(regex='BASE$').sum(),      columns=['BASE']         ).set_axis(d4_index_list, axis=0)

# plt.scatter(df_energy_d4_fence, df_perf_d4_fence, label='SV Fence', color='blue')
# plt.plot   (df_energy_d4_fence, df_perf_d4_fence, color='blue')
# plt.axline((0, 0), (df_energy_d4_fence['SV Fence']['V4-D4'], 
#                     df_perf_d4_fence  ['SV Fence']['V4-D4']), color='blue', lw=0.5)
# 
# plt.scatter(df_energy_d4_nomerge, df_perf_d4_nomerge, label='Prop1', color='green')
# plt.plot   (df_energy_d4_nomerge, df_perf_d4_nomerge, label='Prop1', color='green')
# plt.axline((0, 0), (df_energy_d4_nomerge['Prop1']['V4-D4'], 
#                     df_perf_d4_nomerge  ['Prop1']['V4-D4']), color='green', lw=0.5)

plt.scatter(df_energy_d4_proposal, df_perf_d4_proposal, label='PROP', color='purple')
plt.plot   (df_energy_d4_proposal, df_perf_d4_proposal, label='PROP', color='purple')
plt.axline((0, 0), (df_energy_d4_proposal['PROP']['V4-D4'], 
                    df_perf_d4_proposal  ['PROP']['V4-D4']), color='purple', lw=0.5)

plt.scatter(df_energy_d4_ooo, df_perf_d4_ooo, label='BASE', color='red')
plt.plot   (df_energy_d4_ooo, df_perf_d4_ooo, label='BASE', color='red')
plt.axline((0, 0), (df_energy_d4_ooo['BASE']['V4-D4'], 
                    df_perf_d4_ooo  ['BASE']['V4-D4']), color='red', lw=0.5)

plt.xlim(0.0, df_energy_whole_d4_pct.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d4_pct.mean().max() * 1.1)
plt.xlabel("Energy (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
# plt.savefig("energy_perf_d4.pdf", bbox_inches='tight')


# %%
# 性能の折れ線グラフを作る
import matplotlib.pyplot as plt

# plt.plot(df_perf_d2_fence)
# plt.plot(df_perf_d2_lsuino)
# plt.plot(df_perf_d2_nomerge)
plt.plot(df_perf_d2_proposal)
plt.plot(df_perf_d2_ooo)
plt.ylim(0.0, 2.0)
plt.show()

plt.cla()

# plt.plot(df_perf_d4_fence)
# plt.plot(df_perf_d4_lsuino)
# plt.plot(df_perf_d4_nomerge)
plt.plot(df_perf_d4_proposal)
plt.plot(df_perf_d4_ooo)
plt.ylim(0.0, 2.0)


# %%
# 各ベンチマークにおける相対性能グラフを作成

# for b in ut.benchmarks:
#   display(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="SV Fence$")    .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="SV Fence$")   .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="SV MEM Fence$")  .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="Prop1$") .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="PROP$").loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="BASE$")     .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.title("Performance rate of %s with %s" % (b, d2_index_list))
#   plt.ylim(0.0)
#   plt.show()
#   plt.cla()
# 
# for b in ut.benchmarks:
#   display(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="SV Fence$")    .loc[b]).set_axis(d4_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="SV Fence$")   .loc[b]).set_axis(d4_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="SV MEM Fence$")  .loc[b]).set_axis(d4_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="Prop1$") .loc[b]).set_axis(d4_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="PROP$").loc[b]).set_axis(d4_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="BASE$")     .loc[b]).set_axis(d4_index_list, axis=0))
#   plt.title("Performance rate of %s with %s" % (b, d4_index_list))
#   plt.ylim(0.0)
#   plt.show()
#   plt.cla()

  
# %%
# 性能と面積の分布図を作る D2

df_area_whole_d2_pct = df_area_whole_d2.sum() / df_area_whole_d2.sum().min()

# plt.scatter(df_area_d2_fence, df_perf_d2_fence, lw=2, label='SV Fence', color='blue')
# plt.plot   (df_area_d2_fence, df_perf_d2_fence, lw=2, color='blue')
# plt.axline((0, 0), (df_area_d2_fence['SV Fence']['V4-D2'], 
#                     df_perf_d2_fence['SV Fence']['V4-D2']), color='blue', lw=0.5)
# 
# plt.scatter(df_area_d2_nomerge, df_perf_d2_nomerge, label='Prop1', color='green')
# plt.plot   (df_area_d2_nomerge, df_perf_d2_nomerge, label='Prop1', color='green')
# plt.axline((0, 0), (df_area_d2_nomerge['Prop1']['V4-D2'], 
#                     df_perf_d2_nomerge['Prop1']['V4-D2']), color='green', lw=0.5)

plt.scatter(df_area_d2_proposal, df_perf_d2_proposal, label='PROP', color='purple')
plt.plot   (df_area_d2_proposal, df_perf_d2_proposal, label='PROP', color='purple')
plt.axline((0, 0), (df_area_d2_proposal['PROP']['V4-D2'], 
                    df_perf_d2_proposal['PROP']['V4-D2']), color='purple', lw=0.5)

plt.scatter(df_area_d2_ooo, df_perf_d2_ooo, label='BASE', color='red')
plt.plot   (df_area_d2_ooo, df_perf_d2_ooo, label='BASE', color='red')
plt.axline((0, 0), (df_area_d2_ooo['BASE']['V4-D2'], 
                    df_perf_d2_ooo['BASE']['V4-D2']), color='red', lw=0.5)

plt.xlabel("Area (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
plt.xlim(0.0, df_area_whole_d2.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d2_pct.mean().max() * 1.1)

# df_area_whole_d2_pct.to_csv("relative_area.csv")

# %%
# 性能と面積の分布図を作る D4

df_area_whole_d4_pct = df_area_whole_d4.sum() / df_area_whole_d4.sum().min()

plt.scatter(df_area_d4_proposal, df_perf_d4_proposal, label='PROP', color='purple')
plt.plot   (df_area_d4_proposal, df_perf_d4_proposal, label='PROP', color='purple')
plt.axline((0, 0), (df_area_d4_proposal['PROP']['V4-D4'], 
                    df_perf_d4_proposal['PROP']['V4-D4']), color='purple', lw=0.5)

plt.scatter(df_area_d4_ooo, df_perf_d4_ooo, label='BASE', color='red')
plt.plot   (df_area_d4_ooo, df_perf_d4_ooo, label='BASE', color='red')
plt.axline((0, 0), (df_area_d4_ooo['BASE']['V4-D4'], 
                    df_perf_d4_ooo['BASE']['V4-D4']), color='red', lw=0.5)

plt.xlabel("Area (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
plt.xlim(0.0, df_area_whole_d4.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d4_pct.mean().max() * 1.1)


# %%
# 全体表示用の一覧を出力

import utils as ut

df_d2_balance = pd.concat([df_cycle_whole_d2_pct.mean(), df_energy_whole_d2_pct.sum(), df_area_whole_d2_pct], axis=1)
# df_d2_balance = df_d2_balance.columns=['Perf', 'Energy', 'Area']
df_d2_balance = df_d2_balance.reindex(["V%d-D2 %s" % (v, c) for c in ut.pipe_conf2 for v in (2, 4, 8, 16)], axis=0)
print(df_d2_balance)
df_d2_balance.to_csv('csv/perf_energy_balance_d2.csv')

df_d4_balance = pd.concat([df_cycle_whole_d4_pct.mean(), df_energy_whole_d4_pct.sum(), df_area_whole_d4_pct], axis=1)
df_d4_balance = df_d4_balance.reindex(["V%d-D4 %s" % (v, c) for c in ut.pipe_conf2 for v in (4, 8, 16, 32)], axis=0)
print(df_d4_balance)
df_d4_balance.to_csv('csv/perf_energy_balance_d4.csv')


# %%
# オリジナル実装のサイクル数を取得する

# import pandas as pd
# import matplotlib.pyplot as plt
# import utils as ut
# import util_area as ut_a
# import util_cycle as ut_c
# import util_power as ut_p
# import numpy as np
# 
# df_cycle_v8_d2        = pd.Series([ut_c.get_cycle(sql_info, b, 'vio.v', 512, 128) for b in ut.rivec_benchmarks], index=ut.rivec_benchmarks)
# df_cycle_origin_v8_d2 = pd.Series([ut_c.get_cycle(sql_info, b + '_origin', 'vio.v', 512, 128) for b in ut.rivec_benchmarks], index=ut.rivec_benchmarks)
# 
# t = df_cycle_origin_v8_d2 / df_cycle_v8_d2
# display(pd.concat([df_cycle_origin_v8_d2, df_cycle_v8_d2],axis=1))
# display(t)

# %%
# L1Dの情報を取得する

import pandas as pd
import dcaches as dc
import utils as ut
import util_cycle as ut_c

def get_dcache_info_with_app(app, vlen, dlen, op):
    return [dc.get_dcache_info(sql_info, app, p, vlen, dlen, op) for p in ut.pipe_conf]
def get_insts_with_app(app, vlen, dlen):
    return [ut_c.get_insts(sql_info, app, p, vlen, dlen) for p in ut.pipe_conf]
    
df_dc_loads_v2_d2         = pd.DataFrame([get_dcache_info_with_app(b, 128, 128, 'loads')        for b in ut.benchmarks], columns=["V2-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_stores_v2_d2        = pd.DataFrame([get_dcache_info_with_app(b, 128, 128, 'stores')       for b in ut.benchmarks], columns=["V2-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_load_misses_v2_d2   = pd.DataFrame([get_dcache_info_with_app(b, 128, 128, 'load-misses')  for b in ut.benchmarks], columns=["V2-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_store_misses_v2_d2  = pd.DataFrame([get_dcache_info_with_app(b, 128, 128, 'store-misses') for b in ut.benchmarks], columns=["V2-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_insts_v2_d2         = pd.DataFrame([get_insts_with_app(b, 128, 128)                       for b in ut.benchmarks], columns=["V2-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)

# display(df_dc_loads_v16_d2)
# display(df_dc_stores_v16_d2)
# display(df_dc_loads_v2_d2)
# display(df_dc_load_misses_v2_d2)
# display(df_dc_insts_v2_d2)
display((df_dc_load_misses_v2_d2 + df_dc_store_misses_v2_d2) / df_dc_insts_v2_d2 * 1000)

df_dc_loads_v16_d2        = pd.DataFrame([get_dcache_info_with_app(b, 1024, 128, 'loads')        for b in ut.benchmarks], columns=["V16-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_load_misses_v16_d2  = pd.DataFrame([get_dcache_info_with_app(b, 1024, 128, 'load-misses')  for b in ut.benchmarks], columns=["V16-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_store_misses_v16_d2 = pd.DataFrame([get_dcache_info_with_app(b, 1024, 128, 'store-misses') for b in ut.benchmarks], columns=["V16-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_insts_v16_d2        = pd.DataFrame([get_insts_with_app(b, 1024, 128)                       for b in ut.benchmarks], columns=["V16-D2 " + b for b in ut.pipe_conf2], index=ut.benchmarks)

# display(df_dc_loads_v16_d2)
# display(df_dc_load_misses_v16_d2)
# display(df_dc_insts_v16_d2)
display((df_dc_load_misses_v16_d2 + df_dc_store_misses_v16_d2) / df_dc_insts_v16_d2 * 1000)

df_dc_loads_v4_d4        = pd.DataFrame([get_dcache_info_with_app(b, 256, 256, 'loads')        for b in ut.benchmarks], columns=["V4-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_stores_v4_d4       = pd.DataFrame([get_dcache_info_with_app(b, 256, 256, 'stores')       for b in ut.benchmarks], columns=["V4-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_load_misses_v4_d4  = pd.DataFrame([get_dcache_info_with_app(b, 256, 256, 'load-misses')  for b in ut.benchmarks], columns=["V4-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_store_misses_v4_d4 = pd.DataFrame([get_dcache_info_with_app(b, 256, 256, 'store-misses') for b in ut.benchmarks], columns=["V4-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_insts_v4_d4        = pd.DataFrame([get_insts_with_app(b, 256, 256)                       for b in ut.benchmarks], columns=["V4-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)

# display(df_dc_loads_v4_d4)
# display(df_dc_load_misses_v4_d4)
# display(df_dc_insts_v4_d4)  
display((df_dc_load_misses_v4_d4 + df_dc_store_misses_v4_d4) / df_dc_insts_v4_d4 * 1000)

df_dc_loads_v32_d4        = pd.DataFrame([get_dcache_info_with_app(b, 2048, 256, 'loads')        for b in ut.benchmarks], columns=["V32-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_load_misses_v32_d4  = pd.DataFrame([get_dcache_info_with_app(b, 2048, 256, 'load-misses')  for b in ut.benchmarks], columns=["V32-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_store_misses_v32_d4 = pd.DataFrame([get_dcache_info_with_app(b, 2048, 256, 'store-misses') for b in ut.benchmarks], columns=["V32-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)
df_dc_insts_v32_d4        = pd.DataFrame([get_insts_with_app(b, 2048, 256)                       for b in ut.benchmarks], columns=["V32-D4 " + b for b in ut.pipe_conf2], index=ut.benchmarks)

# display(df_dc_loads_v32_d4)
# display(df_dc_load_misses_v32_d4)
# display(df_dc_insts_v32_d4)
display((df_dc_load_misses_v32_d4 + df_dc_store_misses_v32_d4) / df_dc_insts_v32_d4 * 1000)


# %%

# 追い越しを行った回数を記録する

scalar_scalar_ooo_issue = [sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-scalar-ooo-issue']['stop'] \
                             if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('scalar-scalar-ooo-issue') else 0 for b in ut.bench_and_dhry]
scalar_vec_ooo_issue    = [sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-vec-ooo-issue']['stop'] \
                             if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('scalar-vec-ooo-issue') else 0 for b in ut.bench_and_dhry]
scalar_ooo_issue    = [sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-ooo-issue']['stop'] - \
                       sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-ooo-issue']['start'] \
                       if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('scalar-ooo-issue') else 0 for b in ut.bench_and_dhry]

vec_scalar_ooo_issue = [sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-scalar-ooo-issue']['stop'] \
                             if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('vec-scalar-ooo-issue') else 0 for b in ut.bench_and_dhry]
vec_vec_ooo_issue    = [sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-vec-ooo-issue']['stop'] \
                             if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('vec-vec-ooo-issue') else 0 for b in ut.bench_and_dhry]
vec_ooo_issue    = [sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-ooo-issue']['stop'] - \
                    sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-ooo-issue']['start'] \
                    if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('vec-ooo-issue') else 0 for b in ut.bench_and_dhry]
uops_total       = [sql_info[128][1024][b]['ooo.v']['rob_timer']['uops_total']['stop'] for b in ut.bench_and_dhry]

df_ooo_issue = pd.concat([pd.DataFrame(scalar_scalar_ooo_issue , index=ut.bench_and_dhry, columns=["スカラ命令が古いスカラ命令を追い越して発行した回数"]),
                          pd.DataFrame(scalar_vec_ooo_issue    , index=ut.bench_and_dhry, columns=["スカラ命令が古いベクトル命令を追い越して発行した回数"]),
                          pd.DataFrame(scalar_ooo_issue        , index=ut.bench_and_dhry, columns=["スカラ命令が古い命令を追い越して発行した回数"]),
                          pd.DataFrame(vec_scalar_ooo_issue    , index=ut.bench_and_dhry, columns=["ベクトルラ命令が古いスカラ命令を追い越して発行した回数"]),
                          pd.DataFrame(vec_vec_ooo_issue       , index=ut.bench_and_dhry, columns=["ベクトルラ命令が古いベクトル命令を追い越して発行した回数"]),
                          pd.DataFrame(vec_ooo_issue           , index=ut.bench_and_dhry, columns=["ベクトル命令が古い命令を追い越して発行した回数"]),
                          pd.DataFrame(uops_total              , index=ut.bench_and_dhry, columns=["全体命令数"])], axis=1)
display(df_ooo_issue)
df_ooo_issue.to_csv("csv/df_ooo_issue_d2.csv")

# %%
# 各ベンチマークにおけるスカラ命令とベクトル命令の割合を表示する

uops_vec_arith = [sql_info[128][1024][b]['ooo.v']['rob_timer']['uop_vec_arith']['stop']  if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('uop_vec_arith')  else 0 for b in ut.bench_and_dhry]
uops_vec_mem   = [sql_info[128][1024][b]['ooo.v']['rob_timer']['uop_vec_memacc']['stop'] if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('uop_vec_memacc') else 0 for b in ut.bench_and_dhry]
uops_total     = [sql_info[128][1024][b]['ooo.v']['rob_timer']['uops_total']['stop'] for b in ut.bench_and_dhry]

uops_vec_rate = ((pd.DataFrame(uops_vec_arith).T + pd.DataFrame(uops_vec_mem).T) / pd.DataFrame(uops_total).T).T
uops_vec_rate.columns=["V16-D2"]
uops_vec_rate.index=ut.bench_and_dhry

uops_vec_rate = uops_vec_rate.sort_values('V16-D2', ascending=False)
display(uops_vec_rate)
uops_vec_rate.to_csv("csv/uops_vec_rate_v16_d2.csv")

# df_vec_ooo_fence    = df_vec_ooo.filter(regex='fence$')
# df_vec_ooo_lsu_ino  = df_vec_ooo.filter(regex='lsu-inorder$')
# df_vec_ooo_ngs      = df_vec_ooo.filter(regex='ngs$')
# df_vec_ooo_vio      = df_vec_ooo.filter(regex='vio.v$')
# df_vec_ooo_ooo      = df_vec_ooo.filter(regex='ooo.v$')
# 
# df_scalar_ooo_fence    = df_scalar_ooo.filter(regex='fence$')
# df_scalar_ooo_lsu_ino  = df_scalar_ooo.filter(regex='lsu-inorder$')
# df_scalar_ooo_ngs      = df_scalar_ooo.filter(regex='ngs$')
# df_scalar_ooo_vio      = df_scalar_ooo.filter(regex='vio.v$')
# df_scalar_ooo_ooo      = df_scalar_ooo.filter(regex='ooo.v$')
# 
# display(pd.concat([pd.DataFrame(df_vec_ooo_fence  ), pd.DataFrame(df_scalar_ooo_fence  ), pd.DataFrame(df_all_uops)], axis=1))
# display(pd.concat([pd.DataFrame(df_vec_ooo_lsu_ino), pd.DataFrame(df_scalar_ooo_lsu_ino), pd.DataFrame(df_all_uops)], axis=1))
# display(pd.concat([pd.DataFrame(df_vec_ooo_ngs    ), pd.DataFrame(df_scalar_ooo_ngs    ), pd.DataFrame(df_all_uops)], axis=1))
# display(pd.concat([pd.DataFrame(df_vec_ooo_vio    ), pd.DataFrame(df_scalar_ooo_vio    ), pd.DataFrame(df_all_uops)], axis=1))
# display(pd.concat([pd.DataFrame(df_vec_ooo_ooo    ), pd.DataFrame(df_scalar_ooo_ooo    ), pd.DataFrame(df_all_uops)], axis=1))
# 
# display(pd.concat([pd.DataFrame(df_vec_ooo_fence  ), pd.DataFrame(df_vec_uops)], axis=1))
# display(pd.concat([pd.DataFrame(df_vec_ooo_lsu_ino), pd.DataFrame(df_vec_uops)], axis=1))
# display(pd.concat([pd.DataFrame(df_vec_ooo_ngs    ), pd.DataFrame(df_vec_uops)], axis=1))
# display(pd.concat([pd.DataFrame(df_vec_ooo_vio    ), pd.DataFrame(df_vec_uops)], axis=1))
# display(pd.concat([pd.DataFrame(df_vec_ooo_ooo    ), pd.DataFrame(df_vec_uops)], axis=1))

# %%
# ベクトル命令がベクトル命令に追い越された割合と、ベクトル命令がスカラ命令に追い越された割合を表示する。

uops_vec_issued            = pd.DataFrame([sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-inst-issued']['stop'] for b in ut.bench_and_dhry], index=ut.bench_and_dhry)
uop_vec_overtook_by_scalar = pd.DataFrame([sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-scalar-overtook-issue']['stop'] for b in ut.bench_and_dhry], index=ut.bench_and_dhry)
uop_vec_overtook_by_vec    = pd.DataFrame([sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-vec-overtook-issue']['stop'] for b in ut.bench_and_dhry], index=ut.bench_and_dhry)

uops_vec_overtook_rate = pd.DataFrame(
                          pd.concat([pd.DataFrame(uop_vec_overtook_by_vec / uops_vec_issued),
                                    pd.DataFrame(uop_vec_overtook_by_scalar / uops_vec_issued)], axis=1))
uops_vec_overtook_rate.loc['Average'] = uops_vec_overtook_rate.mean()

uops_vec_overtook_rate.columns=["Rate of Vector uops, overtook by Vector", "Rate of Vector uops, overtook by Scalar"]
display(uops_vec_overtook_rate)
uops_vec_overtook_rate.plot(kind='bar').legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

uops_vec_overtook_rate.to_csv("csv/uops_vec_overtook_rate_d2.csv")

# %%
# ベクトル命令のうち、ベクトル命令を追い越した割合と、スカラ命令のうち、ベクトル命令を追い越した割合

uops_vector_issued         = pd.DataFrame([sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-inst-issued']['stop'] for b in ut.benchmarks], index=ut.benchmarks)
uop_vector_overtook_vector = pd.DataFrame([sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-vec-ooo-issue']['stop'] for b in ut.benchmarks], index=ut.benchmarks)
uops_scalar_issued         = pd.DataFrame([sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-inst-issued']['stop'] for b in ut.benchmarks], index=ut.benchmarks)
uop_scalar_overtook_vector = pd.DataFrame([sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-vec-ooo-issue']['stop'] for b in ut.benchmarks], index=ut.benchmarks)

uops_vec_overtake_rate = pd.DataFrame(
                          pd.concat([pd.DataFrame(uop_vector_overtook_vector / uops_vector_issued),
                                    pd.DataFrame(uop_scalar_overtook_vector / uops_scalar_issued)], axis=1))
# uops_vec_overtake_rate.loc['Average'] = uops_vec_overtake_rate.mean()

uops_vec_overtake_rate.columns=["Reordered younger vector and older vector",
                                "Reordered younger scalar and older vector"]
display(uops_vec_overtake_rate)
uops_vec_overtake_rate.plot(kind='bar').legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

uops_vec_overtake_rate.to_csv("csv/uops_vec_overtake_rate_d2.csv")

# %%
