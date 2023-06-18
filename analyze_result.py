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
df_area_whole_d2.to_csv("area_d2.csv")

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
df_area_whole_d4.to_csv("area_d4.csv")


#%%
# Cycleのテーブルを作る

import pandas as pd
import utils as ut
import util_cycle as ut_c

def get_cycle_with_app(app, vlen, dlen):
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
df_cycle_v2_d2_pct = np.reciprocal((df_cycle_v2_d2.T / df_cycle_v2_d2["V2-D2 OoO"].T).T)
df_cycle_v2_d2_pct.loc['GeoMean'] = df_cycle_v2_d2_pct.mean()
df_cycle_v2_d2_pct.plot.bar(title="V2-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
# plt.savefig("v2_d2_perf.pdf", bbox_inches='tight')

display(df_cycle_v2_d2)
display(df_cycle_v2_d2_pct.loc['GeoMean'])

# V4-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v4_d2_pct = np.reciprocal((df_cycle_v4_d2.T / df_cycle_v4_d2["V4-D2 OoO"].T).T)
df_cycle_v4_d2_pct.loc['GeoMean'] = df_cycle_v4_d2_pct.mean()
df_cycle_v4_d2_pct.plot.bar(title="V4-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
# plt.savefig("v4_d2_perf.pdf", bbox_inches='tight')

display(df_cycle_v4_d2)
display(df_cycle_v4_d2_pct.loc['GeoMean'])

# V8-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v8_d2_pct = np.reciprocal((df_cycle_v8_d2.T / df_cycle_v8_d2["V8-D2 OoO"].T).T)
df_cycle_v8_d2_pct.loc['GeoMean'] = df_cycle_v8_d2_pct.mean()
df_cycle_v8_d2_pct.plot.bar(title="V8-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
# plt.savefig("v8_d2_perf.pdf", bbox_inches='tight')

display(df_cycle_v8_d2)
display(df_cycle_v8_d2_pct.loc['GeoMean'])

# V16-D2のサイクル数でグラフを作る

plt.figure()
df_cycle_v16_d2_pct = np.reciprocal((df_cycle_v16_d2.T / df_cycle_v16_d2["V16-D2 OoO"].T).T)
df_cycle_v16_d2_pct.loc['GeoMean'] = df_cycle_v16_d2_pct.mean()
df_cycle_v16_d2_pct.plot.bar(title="V16-D2 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
# plt.savefig("v16_d2_perf.pdf", bbox_inches='tight')

display(df_cycle_v16_d2)
display(df_cycle_v16_d2_pct.loc['GeoMean'])


#%%
# V4-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v4_d4_pct = np.reciprocal((df_cycle_v4_d4.T / df_cycle_v4_d4["V4-D4 OoO"].T).T)
df_cycle_v4_d4_pct.loc['GeoMean'] = df_cycle_v4_d4_pct.mean()
df_cycle_v4_d4_pct.plot.bar(title="V4-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
# plt.savefig("v4_d4_perf.pdf", bbox_inches='tight')

display(df_cycle_v4_d4)
display(df_cycle_v4_d4_pct.loc['GeoMean'])

# V8-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v8_d4_pct = np.reciprocal((df_cycle_v8_d4.T / df_cycle_v8_d4["V8-D4 OoO"].T).T)
df_cycle_v8_d4_pct.loc['GeoMean'] = df_cycle_v8_d4_pct.mean()
df_cycle_v8_d4_pct.plot.bar(title="V8-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
# plt.savefig("v8_d4_perf.pdf", bbox_inches='tight')

display(df_cycle_v8_d4)
display(df_cycle_v8_d4_pct.loc['GeoMean'])

# V16-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v16_d4_pct = np.reciprocal((df_cycle_v16_d4.T / df_cycle_v16_d4["V16-D4 OoO"].T).T)
df_cycle_v16_d4_pct.loc['GeoMean'] = df_cycle_v16_d4_pct.mean()
df_cycle_v16_d4_pct.plot.bar(title="V16-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
# plt.savefig("v16_d4_perf.pdf", bbox_inches='tight')

display(df_cycle_v16_d4)
display(df_cycle_v16_d4_pct.loc['GeoMean'])

# V32-D4のサイクル数でグラフを作る

plt.figure()
df_cycle_v32_d4_pct = np.reciprocal((df_cycle_v32_d4.T / df_cycle_v32_d4["V32-D4 OoO"].T).T)
df_cycle_v32_d4_pct.loc['GeoMean'] = df_cycle_v32_d4_pct.mean()
df_cycle_v32_d4_pct.plot.bar(title="V32-D4 Performance", figsize=(10, 3)).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
# plt.savefig("v32_d4_perf.pdf", bbox_inches='tight')

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

df_power_whole_d2 = pd.concat([df_power_v2_d2, df_power_v4_d2, df_power_v8_d2 , df_power_v16_d2], axis=1)
df_power_whole_d4 = pd.concat([df_power_v4_d4, df_power_v8_d4, df_power_v16_d4, df_power_v32_d4], axis=1)

display(df_power_whole_d2)
df_power_whole_d2.T.plot.bar(title="Power Estimation of V2-D2 / V4-D2 / V8-D2 / V16-D2", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.ylim(0.0, df_power_whole_d4.sum().max()*1.1)

display(df_power_whole_d4)
df_power_whole_d4.T.plot.bar(title="Power Estimation of V4-D4 / V8-D4 / V8-D4 / V32-D4", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.ylim(0.0, df_power_whole_d4.sum().max()*1.1)


#%%
# 全部のエネルギーを計算
df_energy_whole_d2 = pd.concat([df_energy_v2_d2, df_energy_v4_d2, df_energy_v8_d2, df_energy_v16_d2], axis=1)
# df_energy_whole_d2.columns = ut.d2_index2

df_energy_whole_d4 = pd.concat([df_energy_v4_d4, df_energy_v8_d4, df_energy_v16_d4, df_energy_v32_d4], axis=1)
# df_energy_whole_d4.columns = ut.d4_index2

display(df_energy_whole_d2)
energy_graph = df_energy_whole_d2.T.plot(kind='bar', title="Energy Estimation of V2-D2 V4-D2 V8-D2 V16-D2", stacked=True)
handles, labels = energy_graph.get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
energy_graph.legend(handles, labels, bbox_to_anchor=(1.05, 1.0), loc='upper left', )
plt.ylim(0.0, df_energy_whole_d4.sum().max() * 1.1)
plt.show()

# plt.savefig("relative_energy.pdf", bbox_inches='tight')

display(df_energy_whole_d4)
energy_graph = df_energy_whole_d4.T.plot(kind='bar', title="Energy Estimation of V4-D4 V8-D4 V16-D4 V32-D4", stacked=True)
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

df_perf_d2_fence    = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='SV Fence$').mean(),     columns=['SV Fence']    ).set_axis(d2_index_list, axis=0)
df_perf_d2_lsuino   = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='SV MEM Fence$').mean(), columns=['SV MEM Fence']).set_axis(d2_index_list, axis=0)
df_perf_d2_nomerge  = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='Prop1$').mean(),        columns=['Prop1']       ).set_axis(d2_index_list, axis=0)
df_perf_d2_proposal = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='Prop1\+Prop2$').mean(), columns=['Prop1+Prop2'] ).set_axis(d2_index_list, axis=0)
df_perf_d2_ooo      = pd.DataFrame(df_cycle_whole_d2_pct.filter(regex='OoO$').mean(),          columns=['VecOoO']      ).set_axis(d2_index_list, axis=0)

df_energy_d2_fence    = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='SV Fence$').sum(),     columns=['SV Fence']    ).set_axis(d2_index_list, axis=0)
df_energy_d2_lsuino   = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='SV MEM Fence$').sum(), columns=['SV MEM Fence']).set_axis(d2_index_list, axis=0)
df_energy_d2_nomerge  = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='Prop1$').sum(),        columns=['Prop1']       ).set_axis(d2_index_list, axis=0)
df_energy_d2_proposal = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='Prop1\+Prop2$').sum(), columns=['Prop1+Prop2'] ).set_axis(d2_index_list, axis=0)
df_energy_d2_ooo      = pd.DataFrame(df_energy_whole_d2_pct.filter(regex='OoO$').sum(),          columns=['VecOoO']      ).set_axis(d2_index_list, axis=0)

df_area_d2_fence    = pd.DataFrame(df_area_whole_d2.filter(regex='SV Fence$').sum(),     columns=['SV Fence']    ).set_axis(d2_index_list, axis=0)
df_area_d2_lsuino   = pd.DataFrame(df_area_whole_d2.filter(regex='SV MEM Fence$').sum(), columns=['SV MEM Fence']).set_axis(d2_index_list, axis=0)
df_area_d2_nomerge  = pd.DataFrame(df_area_whole_d2.filter(regex='Prop1$').sum(),        columns=['Prop1']       ).set_axis(d2_index_list, axis=0)
df_area_d2_proposal = pd.DataFrame(df_area_whole_d2.filter(regex='Prop1\+Prop2$').sum(), columns=['Prop1+Prop2'] ).set_axis(d2_index_list, axis=0)
df_area_d2_ooo      = pd.DataFrame(df_area_whole_d2.filter(regex='OoO$').sum(),          columns=['VecOoO']      ).set_axis(d2_index_list, axis=0)

plt.scatter(df_energy_d2_fence, df_perf_d2_fence, label='SV Fence', color='blue')
plt.plot   (df_energy_d2_fence, df_perf_d2_fence, color='blue')
plt.axline((0, 0), (df_energy_d2_fence['SV Fence']['V4-D2'], 
                    df_perf_d2_fence  ['SV Fence']['V4-D2']), color='blue', lw=0.5)

plt.scatter(df_energy_d2_nomerge, df_perf_d2_nomerge, label='Prop1', color='green')
plt.plot   (df_energy_d2_nomerge, df_perf_d2_nomerge, label='Prop1', color='green')
plt.axline((0, 0), (df_energy_d2_nomerge['Prop1']['V4-D2'], 
                    df_perf_d2_nomerge  ['Prop1']['V4-D2']), color='green', lw=0.5)

plt.scatter(df_energy_d2_proposal, df_perf_d2_proposal, label='Prop1+Prop2', color='purple')
plt.plot   (df_energy_d2_proposal, df_perf_d2_proposal, label='Prop1+Prop2', color='purple')
plt.axline((0, 0), (df_energy_d2_proposal['Prop1+Prop2']['V4-D2'], 
                    df_perf_d2_proposal  ['Prop1+Prop2']['V4-D2']), color='purple', lw=0.5)

plt.scatter(df_energy_d2_ooo, df_perf_d2_ooo, label='VecOoO', color='red')
plt.plot   (df_energy_d2_ooo, df_perf_d2_ooo, label='VecOoO', color='red')
plt.axline((0, 0), (df_energy_d2_ooo['VecOoO']['V4-D2'], 
                    df_perf_d2_ooo  ['VecOoO']['V4-D2']), color='red', lw=0.5)

plt.xlim(0.0, df_energy_whole_d2_pct.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d2_pct.mean().max() * 1.1)
plt.xlabel("Energy (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
# plt.savefig("energy_perf_d2.pdf", bbox_inches='tight')

#%%
# D4 : 性能とエネルギーの分布図を作る

df_energy_whole_d4_pct = df_energy_whole_d4 / df_energy_whole_d4.sum().min()

d4_index_list = ['V4-D4', 'V8-D4', 'V16-D4', 'V32-D4']

df_perf_d4_fence    = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='SV Fence$').mean(),    columns=['SV Fence']   ).set_axis(d4_index_list, axis=0)
df_perf_d4_lsuino   = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='SV MEM Fence$').mean(),   columns=['SV MEM Fence']  ).set_axis(d4_index_list, axis=0)
df_perf_d4_nomerge  = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='Prop1$').mean(),  columns=['Prop1'] ).set_axis(d4_index_list, axis=0)
df_perf_d4_proposal = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='Prop1\+Prop2$').mean(), columns=['Prop1+Prop2']).set_axis(d4_index_list, axis=0)
df_perf_d4_ooo      = pd.DataFrame(df_cycle_whole_d4_pct.filter(regex='OoO$').mean(),      columns=['VecOoO']         ).set_axis(d4_index_list, axis=0)

df_energy_d4_fence    = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='SV Fence$').sum(),    columns=['SV Fence']   ).set_axis(d4_index_list, axis=0)
df_energy_d4_lsuino   = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='SV MEM Fence$').sum(),   columns=['SV MEM Fence']  ).set_axis(d4_index_list, axis=0)
df_energy_d4_nomerge  = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='Prop1$').sum(),  columns=['Prop1'] ).set_axis(d4_index_list, axis=0)
df_energy_d4_proposal = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='Prop1\+Prop2$').sum(), columns=['Prop1+Prop2']).set_axis(d4_index_list, axis=0)
df_energy_d4_ooo      = pd.DataFrame(df_energy_whole_d4_pct.filter(regex='OoO$').sum(),      columns=['VecOoO']         ).set_axis(d4_index_list, axis=0)

df_area_d4_fence    = pd.DataFrame(df_area_whole_d4.filter(regex='SV Fence$').sum(),    columns=['SV Fence']   ).set_axis(d4_index_list, axis=0)
df_area_d4_lsuino   = pd.DataFrame(df_area_whole_d4.filter(regex='SV MEM Fence$').sum(),   columns=['SV MEM Fence']  ).set_axis(d4_index_list, axis=0)
df_area_d4_nomerge  = pd.DataFrame(df_area_whole_d4.filter(regex='Prop1$').sum(),  columns=['Prop1'] ).set_axis(d4_index_list, axis=0)
df_area_d4_proposal = pd.DataFrame(df_area_whole_d4.filter(regex='Prop1\+Prop2$').sum(), columns=['Prop1+Prop2']).set_axis(d4_index_list, axis=0)
df_area_d4_ooo      = pd.DataFrame(df_area_whole_d4.filter(regex='OoO$').sum(),      columns=['VecOoO']         ).set_axis(d4_index_list, axis=0)

plt.scatter(df_energy_d4_fence, df_perf_d4_fence, label='SV Fence', color='blue')
plt.plot   (df_energy_d4_fence, df_perf_d4_fence, color='blue')
plt.axline((0, 0), (df_energy_d4_fence['SV Fence']['V4-D4'], 
                    df_perf_d4_fence  ['SV Fence']['V4-D4']), color='blue', lw=0.5)

plt.scatter(df_energy_d4_nomerge, df_perf_d4_nomerge, label='Prop1', color='green')
plt.plot   (df_energy_d4_nomerge, df_perf_d4_nomerge, label='Prop1', color='green')
plt.axline((0, 0), (df_energy_d4_nomerge['Prop1']['V4-D4'], 
                    df_perf_d4_nomerge  ['Prop1']['V4-D4']), color='green', lw=0.5)

plt.scatter(df_energy_d4_proposal, df_perf_d4_proposal, label='Prop1+Prop2', color='purple')
plt.plot   (df_energy_d4_proposal, df_perf_d4_proposal, label='Prop1+Prop2', color='purple')
plt.axline((0, 0), (df_energy_d4_proposal['Prop1+Prop2']['V4-D4'], 
                    df_perf_d4_proposal  ['Prop1+Prop2']['V4-D4']), color='purple', lw=0.5)

plt.scatter(df_energy_d4_ooo, df_perf_d4_ooo, label='VecOoO', color='red')
plt.plot   (df_energy_d4_ooo, df_perf_d4_ooo, label='VecOoO', color='red')
plt.axline((0, 0), (df_energy_d4_ooo['VecOoO']['V4-D4'], 
                    df_perf_d4_ooo  ['VecOoO']['V4-D4']), color='red', lw=0.5)

plt.xlim(0.0, df_energy_whole_d4_pct.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d4_pct.mean().max() * 1.1)
plt.xlabel("Energy (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
# plt.savefig("energy_perf_d4.pdf", bbox_inches='tight')


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
# 
# for b in ut.benchmarks:
#   display(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="SV Fence$")    .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="SV Fence$")   .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="SV MEM Fence$")  .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="Prop1$") .loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="Prop1+Prop2$").loc[b]).set_axis(d2_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d2_pct.filter(regex="OoO$")     .loc[b]).set_axis(d2_index_list, axis=0))
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
#   plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="Prop1+Prop2$").loc[b]).set_axis(d4_index_list, axis=0))
#   plt.plot(pd.DataFrame(df_cycle_whole_d4_pct.filter(regex="OoO$")     .loc[b]).set_axis(d4_index_list, axis=0))
#   plt.title("Performance rate of %s with %s" % (b, d4_index_list))
#   plt.ylim(0.0)
#   plt.show()
#   plt.cla()

  
# %%
# 性能と面積の分布図を作る

df_area_whole_d2_pct = df_area_whole_d2.sum() / df_area_whole_d2.sum().min()
df_area_whole_d4_pct = df_area_whole_d4.sum() / df_area_whole_d4.sum().min()

plt.scatter(df_area_d2_fence, df_perf_d2_fence, lw=2, label='SV Fence', color='blue')
plt.plot   (df_area_d2_fence, df_perf_d2_fence, lw=2, color='blue')
plt.axline((0, 0), (df_area_d2_fence['SV Fence']['V4-D2'], 
                    df_perf_d2_fence['SV Fence']['V4-D2']), color='blue', lw=0.5)

plt.scatter(df_area_d2_nomerge, df_perf_d2_nomerge, label='Prop1', color='green')
plt.plot   (df_area_d2_nomerge, df_perf_d2_nomerge, label='Prop1', color='green')
plt.axline((0, 0), (df_area_d2_nomerge['Prop1']['V4-D2'], 
                    df_perf_d2_nomerge['Prop1']['V4-D2']), color='green', lw=0.5)

plt.scatter(df_area_d2_proposal, df_perf_d2_proposal, label='Prop1+Prop2', color='purple')
plt.plot   (df_area_d2_proposal, df_perf_d2_proposal, label='Prop1+Prop2', color='purple')
plt.axline((0, 0), (df_area_d2_proposal['Prop1+Prop2']['V4-D2'], 
                    df_perf_d2_proposal['Prop1+Prop2']['V4-D2']), color='purple', lw=0.5)

plt.scatter(df_area_d2_ooo, df_perf_d2_ooo, label='VecOoO', color='red')
plt.plot   (df_area_d2_ooo, df_perf_d2_ooo, label='VecOoO', color='red')
plt.axline((0, 0), (df_area_d2_ooo['VecOoO']['V4-D2'], 
                    df_perf_d2_ooo['VecOoO']['V4-D2']), color='red', lw=0.5)

plt.xlabel("Area (Lower is Better)")
plt.ylabel("Performance (Higher is Better)")
plt.xlim(0.0, df_area_whole_d2.sum().max() * 1.1)
plt.ylim(0.0, df_cycle_whole_d2_pct.mean().max() * 1.1)
# plt.savefig("area_perf.pdf", bbox_inches='tight')

# df_area_whole_d2_pct.to_csv("relative_area.csv")

# %%
# 全体表示用の一覧を出力

import utils as ut

df_d2_balance = pd.concat([df_cycle_whole_d2_pct.mean(), df_energy_whole_d2_pct.sum(), df_area_whole_d2_pct], axis=1)
df_d2_balance = df_d2_balance.reindex(["V%d-D2 %s" % (v, c) for c in ut.pipe_conf2 for v in (2, 4, 8, 16)], axis=0)
print(df_d2_balance)

df_d4_balance = pd.concat([df_cycle_whole_d4_pct.mean(), df_energy_whole_d4_pct.sum(), df_area_whole_d4_pct], axis=1)
df_d4_balance = df_d4_balance.reindex(["V%d-D4 %s" % (v, c) for c in ut.pipe_conf2 for v in (4, 8, 16, 32)], axis=0)
print(df_d4_balance)


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

import pandas as pd
import utils as ut
import util_cycle as ut_c

df_vec_ooo_issue  = [pd.DataFrame([[ut_c.get_vec_ooo_issue(sql_info, b, c, v, 128) for c in ut.pipe_conf] for b in ut.benchmarks],
                                  columns=["V" + str(v) + "-D2 " + c for c in ut.pipe_conf2], index=ut.benchmarks) for v in [128, 256, 512, 1024]]
df_scalar_ooo_issue  = [pd.DataFrame([[ut_c.get_scalar_ooo_issue(sql_info, b, c, v, 128) for c in ut.pipe_conf] for b in ut.benchmarks],
                                  columns=["V" + str(v) + "-D2 " + c for c in ut.pipe_conf2], index=ut.benchmarks) for v in [128, 256, 512, 1024]]
df_all_uops_each = [pd.DataFrame([ut_c.get_whole_uops(sql_info, b, 'vio.v', v, 128) for b in ut.benchmarks],
                                  columns=["V" + str(v) + "-D2 "], index=ut.benchmarks) for v in [128, 256, 512, 1024]]
df_vec_uops_each = [pd.DataFrame([ut_c.get_vec_uops(sql_info, b, 'vio.v', v, 128) for b in ut.benchmarks],
                                  columns=["V" + str(v) + "-D2 "], index=ut.benchmarks) for v in [128, 256, 512, 1024]]

df_vec_ooo = pd.concat(df_vec_ooo_issue, axis=1)
df_scalar_ooo = pd.concat(df_scalar_ooo_issue, axis=1)
df_all_uops = pd.concat(df_all_uops_each, axis=1)
df_vec_uops = pd.concat(df_vec_uops_each, axis=1)

display(df_vec_ooo)
display(df_scalar_ooo)
display(df_all_uops)

# %%

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

# 追い越しを行った回数を記録する

scalar_ooo_issue = [sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-ooo-issue']['stop'] - sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-ooo-issue']['start']     if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('scalar-vec-ooo-issue')    else 0 for b in ut.bench_and_dhry]
vec_ooo_issue    = [sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-ooo-issue']['stop']    - sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-ooo-issue']['start']        if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('vec-vec-ooo-issue')       else 0 for b in ut.bench_and_dhry]
uops_total       = [sql_info[128][1024][b]['ooo.v']['rob_timer']['uops_total']['stop'] for b in ut.bench_and_dhry]

pd.concat([pd.DataFrame(scalar_ooo_issue , index=ut.bench_and_dhry, columns=["スカラ命令が古い命令を追い越して発行した回数"]),
           pd.DataFrame(vec_ooo_issue    , index=ut.bench_and_dhry, columns=["ベクトル命令が古い命令を追い越して発行した回数"]),
           pd.DataFrame(uops_total       , index=ut.bench_and_dhry, columns=["全体命令数"])], axis=1)

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

# 追い越しを行った回数を記録する

scalar_ooo_issue = [sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-ooo-issue']['stop'] - sql_info[128][1024][b]['ooo.v']['rob_timer']['scalar-ooo-issue']['start']     if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('scalar-vec-ooo-issue')    else 0 for b in ut.bench_and_dhry]
vec_ooo_issue    = [sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-ooo-issue']['stop']    - sql_info[128][1024][b]['ooo.v']['rob_timer']['vec-ooo-issue']['start']        if sql_info[128][1024][b]['ooo.v']['rob_timer'].get('vec-vec-ooo-issue')       else 0 for b in ut.bench_and_dhry]
uops_total       = [sql_info[128][1024][b]['ooo.v']['rob_timer']['uops_total']['stop'] for b in ut.bench_and_dhry]

pd.concat([pd.DataFrame(scalar_ooo_issue , index=ut.bench_and_dhry, columns=["スカラ命令が古い命令を追い越して発行した回数"]),
           pd.DataFrame(vec_ooo_issue    , index=ut.bench_and_dhry, columns=["ベクトル命令が古い命令を追い越して発行した回数"]),
           pd.DataFrame(uops_total       , index=ut.bench_and_dhry, columns=["全体命令数"])], axis=1)

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

