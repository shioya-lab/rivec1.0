#%%
# V2-D2のサイクル数でグラフを作る

import pandas as pd
import matplotlib.pyplot as plt
import util_power as ut_p
import utils as ut

display(total_cycle)

v2_d2 = pd.DataFrame(ut.get_cycle_rate_with_vlen_dlen(128, 128), index=ut.benchmarks, columns=ut.pipe_conf)
v2_d2.loc["geomean"] = v2_d2.mean()
display(v2_d2)
plt.figure()
v2_d2.plot.bar(title="V2-D2 : Cycle Rate", figsize=(10, 3))
plt.legend(["VecInO Fence", "VecInO NoMerge", "VecInO Proposal", "VecOoO"], loc='center left', bbox_to_anchor=(1., .5))
plt.savefig("v2_d2_perf.pdf", bbox_inches='tight')

#%%


#%%
# V8-D2のみ面積を算出

import pandas as pd
import matplotlib.pyplot as plt

v8_d2_area_detail = calc_area("v512_d128")

df_v8_d2_area_detail = pd.DataFrame(v8_d2_area_detail).fillna(0.0)
df_v8_d2_area_detail = df_v8_d2_area_detail.reindex(elem_index)
display(df_v8_d2_area_detail)
df_v8_d2_area_detail.T.plot.bar(title="Area estimation with each configuration", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

#%%
# V2-D2のみ面積を算出

import pandas as pd
import matplotlib.pyplot as plt

v2_d2_area_detail = calc_area("v128_d128")

df_v2_d2_area_detail = pd.DataFrame(v2_d2_area_detail).fillna(0.0)
df_v2_d2_area_detail = df_v2_d2_area_detail.reindex(elem_index)
display(df_v2_d2_area_detail)
df_v2_d2_area_detail.T.plot.bar(title="Area estimation with each configuration", stacked=True).legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')


#%%
# V8-D2のエネルギーを取得する
power_detail_v8_d2 = ut_p.get_power_with_vlen_dlen(512, 128)

df_power_v8_d2 = pd.concat(list(map(lambda i: pd.DataFrame([power_detail_v8_d2[i]['vio.v.ngs'], 
                                                            power_detail_v8_d2[i]['vio.v']]).fillna(0.0), range(len(ut.benchmarks)))))
# df_power_v8_d2.columns = [range(0..len(df_power_v8_d2.columns))]
# df_power_v8_d2.index = ut.benchmarks
display(df_power_v8_d2)

plt.figure()
df_power_v8_d2.plot.bar(stacked=True, title="V8-D2 : Power Estimation").legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

# %%
# blackscholesの電力を取得する

import pandas as pd
import matplotlib.pyplot as plt
import util_power as ut_p
import utils as ut
import util_cycle as ut_c

df_power_blackscholes_v8_d2 = pd.DataFrame(ut_p.get_power_with_app('blackscholes', 512, 128))
df_cycle_blackscholes_v8_d2 = ut_c.get_cycle_with_app('blackscholes', 512, 128)
df_energy_blackscholes_v8_d2 = df_cycle_blackscholes_v8_d2 * df_power_blackscholes_v8_d2

display(df_energy_blackscholes_v8_d2)
display(df_cycle_blackscholes_v8_d2)
plt.figure()
df_energy_blackscholes_v8_d2.T.plot.bar(stacked=True, title="blackscholes V8-D2 : Energy Estimation").legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

df_power_blackscholes_v2_d2 = pd.DataFrame(ut_p.get_power_with_app('blackscholes', 128, 128))
df_cycle_blackscholes_v2_d2 = ut_c.get_cycle_with_app('blackscholes', 128, 128)
df_energy_blackscholes_v2_d2 = df_cycle_blackscholes_v2_d2 * df_power_blackscholes_v2_d2

display(df_energy_blackscholes_v2_d2)
display(df_cycle_blackscholes_v2_d2)
plt.figure()
df_energy_blackscholes_v2_d2.T.plot.bar(stacked=True, title="blackscholes V8-D2 : Energy Estimation").legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

# %%


# %%
# FFTW3の電力を取得する

import pandas as pd
import matplotlib.pyplot as plt
import util_power as ut_p
import util_cycle as ut_c
import utils as ut

df_power_fftw3_v8_d2 = pd.DataFrame(ut_p.get_power_with_app('fftw3', 512, 128))
df_cycle_fftw3_v8_d2 = ut_c.get_cycle_with_app("fftw3", 512, 128)
df_energy_fftw3_v8_d2 = df_cycle_fftw3_v8_d2 * df_power_fftw3_v8_d2

display(df_power_fftw3_v8_d2)
display(df_cycle_fftw3_v8_d2)
display(df_energy_fftw3_v8_d2)
plt.figure()
df_energy_fftw3_v8_d2.T.plot.bar(stacked=True, title="FFTW3 V8-D2 : Energy Estimation").legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')


# %%
# scatter_evalの電力を取得する

import pandas as pd
import matplotlib.pyplot as plt
import util_power as ut_p
import util_cycle as ut_c
import utils as ut

df_power_scatter_v8_d2 = pd.DataFrame(ut_p.get_power_with_app('scatter_eval', 512, 128))
df_cycle_scatter_v8_d2 = ut_c.get_cycle_with_app("scatter_eval", 512, 128)
df_energy_scatter_v8_d2 = df_cycle_scatter_v8_d2 * df_power_scatter_v8_d2

display(df_power_scatter_v8_d2)
display(df_cycle_scatter_v8_d2)
display(df_energy_scatter_v8_d2)
plt.figure()
df_energy_scatter_v8_d2.T.plot.bar(stacked=True, title="scatter_eval V8-D2 : Energy Estimation").legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

# %%

