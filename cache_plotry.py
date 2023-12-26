#%%

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

axpy_dcache_hit_rd  = pd.read_csv("_axpy/vec-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_rd_hit_log.csv", header=None)
axpy_dcache_hit_wr  = pd.read_csv("_axpy/vec-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_wr_hit_log.csv", header=None)
axpy_dcache_miss_rd = pd.read_csv("_axpy/vec-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_rd_miss_log.csv", header=None)
axpy_dcache_miss_wr = pd.read_csv("_axpy/vec-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_wr_miss_log.csv", header=None)
axpy_dcache_pr = pd.read_csv("_axpy/vec-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_pr_log.csv", header=None)
axpy_dcache_ev = pd.read_csv("_axpy/vec-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_ev_log.csv", header=None)

display(axpy_dcache_pr.head())
display(axpy_dcache_pr.head())

axpy_dcache_plot = [go.Scatter(x=axpy_dcache_hit_rd[0], y=axpy_dcache_hit_rd[1], mode='markers', name="Load Hit"),
                    go.Scatter(x=axpy_dcache_hit_wr[0], y=axpy_dcache_hit_wr[1], mode='markers', name="Store Hit"),
                    go.Scatter(x=axpy_dcache_miss_rd[0], y=axpy_dcache_miss_rd[1], mode='markers', name="Load Miss"),
                    go.Scatter(x=axpy_dcache_miss_wr[0], y=axpy_dcache_miss_wr[1], mode='markers', name="Store Miss"),
                    go.Scatter(x=axpy_dcache_pr[0], y=axpy_dcache_pr[1], mode='markers', name="Prefetching"),
                    go.Scatter(x=axpy_dcache_ev[0], y=axpy_dcache_ev[1], mode='markers', name="Eviction")]
fig = go.Figure(data=axpy_dcache_plot)
fig.show()

axpy_dcache_hit_rd  = pd.read_csv("_axpy/stride-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_rd_hit_log.csv",  header=None)
axpy_dcache_hit_wr  = pd.read_csv("_axpy/stride-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_wr_hit_log.csv",  header=None)
axpy_dcache_miss_rd = pd.read_csv("_axpy/stride-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_rd_miss_log.csv", header=None)
axpy_dcache_miss_wr = pd.read_csv("_axpy/stride-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_wr_miss_log.csv", header=None)
axpy_dcache_pr = pd.read_csv("_axpy/stride-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_pr_log.csv", header=None)
axpy_dcache_ev = pd.read_csv("_axpy/stride-pref.v.v512_d128_l2_stream_l1d_pref_load/l1_dcache_cache_ev_log.csv", header=None)

display(axpy_dcache_pr.head())
display(axpy_dcache_pr.head())

axpy_dcache_plot = [go.Scatter(x=axpy_dcache_hit_rd[0],  y=axpy_dcache_hit_rd[1],  mode='markers', name="Load Hit"),
                    go.Scatter(x=axpy_dcache_hit_wr[0],  y=axpy_dcache_hit_wr[1],  mode='markers', name="Store Hit"),
                    go.Scatter(x=axpy_dcache_miss_rd[0], y=axpy_dcache_miss_rd[1], mode='markers', name="Load Miss"),
                    go.Scatter(x=axpy_dcache_miss_wr[0], y=axpy_dcache_miss_wr[1], mode='markers', name="Store Miss"),
                    go.Scatter(x=axpy_dcache_pr[0], y=axpy_dcache_pr[1], mode='markers', name="Prefetching"),
                    go.Scatter(x=axpy_dcache_ev[0], y=axpy_dcache_ev[1], mode='markers', name="Eviction")]
fig = go.Figure(data=axpy_dcache_plot, )
fig.show()

# %%
