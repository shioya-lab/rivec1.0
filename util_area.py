#%%
# デバッグ用：各項目で必要なものを取り出す

import utils as ut

def calc_area(conf):
    area_detail = dict()
    for e in ut.e_elem:
        e_name = e
        csv_data = ut.load_csv(ut.conf_filename[e] + "." + conf)
        area_detail[e_name] = dict()
        for grp_name in ut.e_elem[e] :
            for m in ut.e_elem[e][grp_name] :
                (c, module) = m.split(':')
                if c in csv_data:
                    area = float(csv_data[c][csv_data[c]['name'].str.contains(module + '-Area')].iloc[0]['value'])
                    if e_name in ut.area_scale[conf]:
                        area = area * ut.area_scale[conf][e_name]
                    area_detail[e_name][m] = area
                else:
                    area_detail[e_name][m] = 0.0
    return area_detail

def calc_group_area(conf):
    area_detail = dict()
    for e in ut.e_elem:
        e_name = e
        print("calc_group_area : load csv " + ut.conf_filename[e] + "." + conf)
        csv_data = ut.load_csv(ut.conf_filename[e] + "." + conf)
        area_detail[e_name] = dict()
        for grp_name in ut.e_elem[e] :
            for m in ut.e_elem[e][grp_name] :
                scale = 1.0
                if m[0] == '-':
                    scale = -1.0
                    m = m[1:]
                (c, module) = m.split(':')
                if c in csv_data:
                    if grp_name in area_detail[e_name]:
                        area_detail[e_name][grp_name] = area_detail[e_name][grp_name] + \
                            float(csv_data[c][csv_data[c]['name'].str.contains(module + '-Area')].iloc[0]['value']) * scale
                    else:
                        area_detail[e_name][grp_name] = float(csv_data[c][csv_data[c]['name'].str.contains(module + '-Area')].iloc[0]['value'])
                else:
                    area_detail[e_name][grp_name] = 0.0
            if grp_name in ut.area_scale[conf]:
                area_detail[e_name][grp_name] = area_detail[e_name][grp_name] * ut.area_scale[conf][grp_name]
    return area_detail
