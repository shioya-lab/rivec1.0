import pandas as pd
import matplotlib.pyplot as plt
import utils as ut

# Powerの計算：各項目で必要なものを取り出す
def calc_power(conf, app):
    power_detail = dict()
    for e in ut.e_elem:
        e_name = e
        csv_data = ut.load_csv(ut.conf_filename[e_name] + "." + conf , app)
        power_detail[e_name] = dict()
        for p in ut.e_elem[e]:
            for m in ut.e_elem[e][p] :
                scale = 1.0
                if m[0] == '-':
                    scale = 0.0
                    m = m[1:]
                (c, module) = m.split(':')
                if c in csv_data:
                    power = \
                        float(csv_data[c][csv_data[c]['name'].str.contains(module + '-SubthresholdLeakage')].iloc[0]['value']) + \
                        float(csv_data[c][csv_data[c]['name'].str.contains(module + '-GateLeakage')].iloc[0]['value']) + \
                        float(csv_data[c][csv_data[c]['name'].str.contains(module + '-RuntimeDynamic')].iloc[0]['value'])
                    if e_name in ut.area_scale[conf]:
                        power = power * ut.area_scale[conf][e_name]
                    power_detail[e_name][m] = power
                else:
                    power_detail[e_name][m] = 0.0

    return power_detail

def calc_group_power(conf, app):
    power_detail = dict()
    for e in ut.e_elem:
        e_name = e
        csv_data = ut.load_csv(ut.conf_filename[e_name] + "." + conf , app)
        power_detail[e_name] = dict()
        for grp_name in ut.e_elem[e]:
            for m in ut.e_elem[e][grp_name] :
                scale = 1.0
                if m[0] == '-':
                    scale = -1.0
                    m = m[1:]
                (c, module) = m.split(':')
                if c in csv_data:
                    if grp_name in power_detail[e_name]:
                        power_detail[e_name][grp_name] = power_detail[e_name][grp_name] + \
                            (float(csv_data[c][csv_data[c]['name'].str.contains(module + '-SubthresholdLeakage')].iloc[0]['value']) + \
                             float(csv_data[c][csv_data[c]['name'].str.contains(module + '-GateLeakage')].iloc[0]['value']) + \
                             float(csv_data[c][csv_data[c]['name'].str.contains(module + '-RuntimeDynamic')].iloc[0]['value'])) * scale
                    else:
                        power_detail[e_name][grp_name] = \
                            float(csv_data[c][csv_data[c]['name'].str.contains(module + '-SubthresholdLeakage')].iloc[0]['value']) + \
                            float(csv_data[c][csv_data[c]['name'].str.contains(module + '-GateLeakage')].iloc[0]['value']) + \
                            float(csv_data[c][csv_data[c]['name'].str.contains(module + '-RuntimeDynamic')].iloc[0]['value'])
                else:
                    power_detail[e_name][m] = 0.0
            if grp_name in ut.energy_scale[conf]:
                power_detail[e_name][grp_name] = power_detail[e_name][grp_name] * \
                                                 ut.energy_scale[conf][grp_name]
    return power_detail


def get_power_with_app(app, vlen, dlen):
    return calc_power("v" + str(vlen) + "_d" + str(dlen), app)

def get_power_with_vlen_dlen(vlen, dlen):
    return list(map(lambda b: get_power_with_app(b, vlen, dlen), ut.benchmarks))

def get_group_power_with_app(app, vlen, dlen):
    return calc_group_power("v" + str(vlen) + "_d" + str(dlen), app)

def get_group_power_with_vlen_dlen(vlen, dlen):
    return list(map(lambda b: get_group_power_with_app(b, vlen, dlen), ut.benchmarks))



'''
#%%
# V2-D2のエネルギーを取得する

power_detail = get_power_with_vlen_dlen(128, 128)
# display(power_detail)
df_power_v2_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(power_detail[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_v2_d2.columns = list(map(lambda b: "V2-D2 " + b, ut.pipe_conf))
df_power_v2_d2.index = ut.benchmarks

display(df_power_v2_d2)
plt.figure()
df_power_v2_d2.plot.bar(title="V2-D2 : Power Estimation", figsize=(10, 3))
plt.legend(["VecInO Fence", "VecInO NoMerge", "VecInO Proposal", "VecOoO"], loc='center left', bbox_to_anchor=(1., .5))
df_energy_v2_d2 = df_power_v2_d2 * df_cycle_v2_d2
df_energy_v2_d2.loc["geomean"] = df_energy_v2_d2.mean()

df_energy_rate = (df_energy_v2_d2.T / df_energy_v2_d2['V2-D2 ooo.v']).T
plt.figure()
df_energy_rate.plot.bar(title="V2-D2 : Energy Estimation", figsize=(10, 3))
plt.legend(["VecInO Fence", "VecInO NoMerge", "VecInO Proposal", "VecOoO"], loc='center left', bbox_to_anchor=(1., .5))
plt.savefig("v2_d2_energy.pdf", bbox_inches='tight')
'''

'''
#%%
# V8-D2のエネルギーを取得する
power_detail = get_power_with_vlen_dlen(512, 128)

df_power_v8_d2 = pd.DataFrame(map(lambda i: pd.DataFrame(power_detail[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_v8_d2.columns = list(map(lambda b: "V8-D2 " + b, ut.pipe_conf))
df_power_v8_d2.index = ut.benchmarks

df_energy_v8_d2 = df_power_v8_d2 * df_cycle_v8_d2
df_energy_v8_d2.loc["geomean"] = df_energy_v8_d2.mean()
df_energy_rate = (df_energy_v8_d2.T / df_energy_v8_d2['V8-D2 ooo.v']).T
plt.figure()
df_energy_rate.plot.bar(title="V8-D2 : Energy Estimation", figsize=(10, 3))
plt.legend(["VecInO Fence", "VecInO NoMerge", "VecInO Proposal", "VecOoO"], loc='center left', bbox_to_anchor=(1., .5))
plt.savefig("v8_d2_energy.pdf", bbox_inches='tight')

'''

#%%

'''
# V8-D8のエネルギーを取得する
power_detail = get_power_with_vlen_dlen(512, 512)

df_power_v8_d8 = pd.DataFrame(map(lambda i: pd.DataFrame(power_detail[i]).fillna(0.0).sum(), range(len(ut.benchmarks))))
df_power_v8_d8.columns = list(map(lambda b: "V8-D8 " + b, ut.pipe_conf))
df_power_v8_d8.index = ut.benchmarks

df_energy_v8_d8 = df_power_v8_d8 * df_cycle_v8_d8
df_energy_v8_d8.loc["geomean"] = df_energy_v8_d8.mean()
df_energy_rate = (df_energy_v8_d8.T / df_energy_v8_d8['V8-D8 ooo.v']).T

plt.figure()
df_energy_rate.plot.bar(title="V8-D8 : Energy Estimation", figsize=(10, 3))
plt.legend(["VecInO Fence", "VecInO NoMerge", "VecInO Proposal", "VecOoO"], loc='center left', bbox_to_anchor=(1., .5))
plt.savefig("v8_d8_energy.pdf", bbox_inches='tight')

'''
# %%

