#%%
import sqlite3
import os

def get_cycle(app, pipe_conf, vlen, dlen):
    file_str = '_%s/%s.v%s_d%s/sim.stats.sqlite3' % (app, pipe_conf, vlen, dlen)
    # print("Opening %s ..." % (file_str))
    sql3_conn = sqlite3.connect(file_str)

    time_by_core0_index = sql3_conn.execute("SELECT * FROM 'names' WHERE objectname='thread' AND metricname='time_by_core[0]'").fetchall()[0][0]
    roi_begin_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-begin'").fetchall()[0][0]
    roi_end_index = sql3_conn.execute("SELECT * FROM 'prefixes' WHERE prefixname='roi-end'").fetchall()[0][0]

    start_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
                    % (roi_begin_index, time_by_core0_index)).fetchall()[0][3]
    stop_time = sql3_conn.execute("SELECT * FROM 'values' WHERE prefixid='%s' AND nameid='%s'" \
                    % (roi_end_index, time_by_core0_index)).fetchall()[0][3]
    cycle = stop_time - start_time
    return cycle
