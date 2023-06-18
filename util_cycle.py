#%%
import sqlite3
import utils as ut

def get_cycle(sql_dict, app, pipe_conf, vlen, dlen):
    return sql_dict[dlen][vlen][app][pipe_conf]['thread']['time_by_core[0]']['roi-end'] - sql_dict[dlen][vlen][app][pipe_conf]['thread']['time_by_core[0]']['roi-begin']

    # file_str = '_%s/%s.v%s_d%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen)
    # print("Opening %s ..." % (file_str))
    # try:
    #     sql3_conn = sqlite3.connect(file_str)
    # except sqlite3.OperationalError:
    #     print ('sqlite3 file error ' + file_str)
    #     exit()
    
    # time_by_core0_index = sql3_conn.execute("SELECT * FROM 'names' WHERE objectname='thread' AND metricname='time_by_core[0]'").fetchall()[0][0]
    # roi_begin_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-begin'").fetchall()[0][0]
    # roi_end_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-end'").fetchall()[0][0]
    # 
    # start_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_begin_index, time_by_core0_index)).fetchall()[0][3]
    # stop_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_end_index, time_by_core0_index)).fetchall()[0][3]
    # cycle = stop_time - start_time
    return cycle

def get_insts(sql_dict, app, pipe_conf, vlen, dlen):
    insts = sql_dict[dlen][vlen][app][pipe_conf]['thread']['instructions_by_core[0]']
    return insts['stop']

    # file_str = '_%s/%s.v%s_d%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen)
    # # print("Opening %s ..." % (file_str))
    # try:
    #     sql3_conn = sqlite3.connect(file_str)
    # except sqlite3.OperationalError:
    #     print ('sqlite3 file error ' + file_str)
    #     exit()
    # 
    # time_by_core0_index = sql3_conn.execute("SELECT * FROM 'names' WHERE objectname='thread' AND metricname='instructions_by_core[0]'").fetchall()[0][0]
    # roi_end_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-end'").fetchall()[0][0]
# 
    # stop_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_end_index, time_by_core0_index)).fetchall()[0][3]
    # return stop_time

def get_vec_ooo_issue(sql_info, app, pipe_conf, vlen, dlen):
    vec_ooo_issue = sql_info[dlen][vlen][app][pipe_conf]['rob_timer']['vec-ooo-issue']
    return vec_ooo_issue['roi-end'] - vec_ooo_issue['roi-begin']

    # file_str = '_%s/%s.v%s_d%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen)
    # print("Opening %s ..." % (file_str))
    # try:
    #     sql3_conn = sqlite3.connect(file_str)
    # except sqlite3.OperationalError:
    #     print ('sqlite3 file error ' + file_str)
    #     exit()
    # 
    # time_by_core0_index = sql3_conn.execute("SELECT * FROM 'names' WHERE objectname='rob_timer' AND metricname='vec-ooo-issue'").fetchall()[0][0]
    # roi_begin_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-begin'").fetchall()[0][0]
    # roi_end_index   = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-end'").fetchall()[0][0]
# 
    # start_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_begin_index, time_by_core0_index)).fetchall()[0][3]
    # stop_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_end_index, time_by_core0_index)).fetchall()[0][3]
    # return stop_time - start_time

def get_scalar_ooo_issue(sql_info, app, pipe_conf, vlen, dlen):
    scalar_ooo_issue = sql_info[dlen][vlen][app][pipe_conf]['rob_timer']['scalar-ooo-issue']
    return scalar_ooo_issue['roi-end'] - scalar_ooo_issue['roi-begin']

    # file_str = '_%s/%s.v%s_d%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen)
    # # print("Opening %s ..." % (file_str))
    # try:
    #     sql3_conn = sqlite3.connect(file_str)
    # except sqlite3.OperationalError:
    #     print ('sqlite3 file error ' + file_str)
    #     exit()
    # 
    # time_by_core0_index = sql3_conn.execute("SELECT * FROM 'names' WHERE objectname='rob_timer' AND metricname='scalar-ooo-issue'").fetchall()[0][0]
    # roi_begin_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-begin'").fetchall()[0][0]
    # roi_end_index   = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-end'").fetchall()[0][0]
# 
    # start_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_begin_index, time_by_core0_index)).fetchall()[0][3]
    # stop_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_end_index, time_by_core0_index)).fetchall()[0][3]
    # return stop_time - start_time


def get_cycle_with_app(sql_info, app, vlen, dlen):
    return [get_cycle(sql_info, app, p, vlen, dlen) / 100000 for p in ut.pipe_conf]

def get_whole_uops(sql_info, app, pipe_conf, vlen, dlen):
    return sql_info[dlen][vlen][app][pipe_conf]['rob_timer']['uops_total']['stop']

    # file_str = '_%s/%s.v%s_d%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen)
    # # print("Opening %s ..." % (file_str))
    # try:
    #     sql3_conn = sqlite3.connect(file_str)
    # except sqlite3.OperationalError:
    #     print ('sqlite3 file error ' + file_str)
    #     exit()
    # 
    # uop_index = sql3_conn.execute("SELECT * FROM 'names' WHERE objectname='rob_timer' AND metricname='uops_total'").fetchall()[0][0]
    # roi_length_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='stop'").fetchall()[0][0]
    # 
    # length = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_length_index, uop_index)).fetchall()
    # return length[0][3]


def get_vec_uops(sql_info, app, pipe_conf, vlen, dlen):
    return sql_info[dlen][vlen][app][pipe_conf]['rob_timer']['uop_vec_arith']['stop'] + \
        sql_info[dlen][vlen][app][pipe_conf]['rob_timer']['uop_vec_memacc']['stop']

    # file_str = '_%s/%s.v%s_d%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen)
    # # print("Opening %s ..." % (file_str))
    # try:
    #     sql3_conn = sqlite3.connect(file_str)
    # except sqlite3.OperationalError:
    #     print ('sqlite3 file error ' + file_str)
    #     exit()
    # 
    # uop_index = sql3_conn.execute("SELECT * FROM 'names' WHERE objectname='rob_timer' AND metricname='uop_vec_arith'").fetchall()[0][0]
    # roi_length_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='stop'").fetchall()[0][0]
    # vec_arith_length = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_length_index, uop_index)).fetchall()
    # 
    # uop_index = sql3_conn.execute("SELECT * FROM 'names' WHERE objectname='rob_timer' AND metricname='uop_vec_memacc'").fetchall()[0][0]
    # roi_length_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='stop'").fetchall()[0][0]
    # vec_memacc_length = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
    #                 % (roi_length_index, uop_index)).fetchall() # 
    # return vec_arith_length[0][3] + vec_memacc_length[0][3]


# %%
