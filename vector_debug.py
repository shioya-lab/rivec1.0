# %%

import pandas as pd
import matplotlib.pyplot as plt
import util_power as ut_p
import utils as ut
import util_cycle as ut_c


df_power_blackscholes_v2_d2 = pd.DataFrame(ut_p.get_group_power_with_app('blackscholes', 128, 128))
df_power_blackscholes_v8_d2 = pd.DataFrame(ut_p.get_group_power_with_app('blackscholes', 512, 128))
df_cycle_blackscholes_v2_d2 = ut_c.get_cycle_with_app('blackscholes', 128, 128)
df_cycle_blackscholes_v8_d2 = ut_c.get_cycle_with_app('blackscholes', 512, 128)
df_energy_blackscholes_v2_d2 = df_cycle_blackscholes_v2_d2 * df_power_blackscholes_v2_d2
df_energy_blackscholes_v8_d2 = df_cycle_blackscholes_v8_d2 * df_power_blackscholes_v8_d2

display(df_cycle_blackscholes_v2_d2)
display(df_power_blackscholes_v2_d2.loc['Vector FU'])
display(df_cycle_blackscholes_v2_d2 * df_power_blackscholes_v2_d2.loc['Vector FU'])

display(df_cycle_blackscholes_v8_d2)
display(df_power_blackscholes_v8_d2.loc['Vector FU'])
display(df_cycle_blackscholes_v8_d2 * df_power_blackscholes_v8_d2.loc['Vector FU'])

plt.figure()
df_energy_blackscholes_v2_d2.T.plot.bar(stacked=True, title="blackscholes V2-D2 : Energy Estimation").legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

plt.figure()
df_energy_blackscholes_v8_d2.T.plot.bar(stacked=True, title="blackscholes V8-D2 : Energy Estimation").legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

# %%
