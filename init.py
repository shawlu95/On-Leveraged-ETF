import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

key_delt = "Del (%)"

# portfolio worth
key_nrm = "Nrm"
key_mrg = "Mrg"
key_lvg = "Lvg"

# percentage gain
key_pctn = key_nrm + " (%)"
key_pctm = key_mrg + " (%)"
key_pctl = key_lvg + " (%)"

# dollar gain
key_netn = key_nrm + " ($)"
key_netm = key_mrg + " ($)"
key_netl = key_lvg + " ($)"

def Simulate_Path(deltas, fund = 100, margin = 3, leverage = 3):
    df = pd.DataFrame(columns = [key_delt,
                                 key_nrm, key_netn, key_pctn, 
                                 key_mrg, key_netm, key_pctm,
                                 key_lvg, key_netl, key_pctl])
    df = df.append({
            key_nrm : fund,
            key_mrg : fund * (margin + 1),
            key_lvg : fund
        },ignore_index = True)

    for delta in deltas:
        # portfolio worth on next day, without leverage
        nxt_n = df.iloc[-1][key_nrm] * (1 + delta)
        net_n = nxt_n - fund

        # portfolio worth on next day, buying on margin
        nxt_l = df.iloc[-1][key_mrg] * (1 + delta)
        net_m = nxt_l - fund * (margin + 1)

        # portfolio worth on next day, with 3x leverage
        nxt_p = df.iloc[-1][key_lvg] * (1 + leverage * delta)
        net_l = nxt_p - fund

        df = df.append({
            key_delt : 100 * delta,
            
            key_nrm : nxt_n,
            key_netn : net_n,
            key_pctn : 100 * net_n / fund,
            
            key_mrg : nxt_l,
            key_netm : net_m,
            key_pctm : 100 * net_m / fund,
            
            key_lvg : nxt_p,
            key_netl : net_l,
            key_pctl : 100 * net_l / fund 
        }, ignore_index = True)
    return df

def Plot_3(df, keys, xlabel = None, ylabel = None, title = None, save = False):
    plt.figure(figsize=(12, 6))
    x_vals = [datetime.strptime(dt, "%Y-%m-%d") for dt in df.index.values]
    for key in keys:
        plt.plot(x_vals, df[key].values)
    
    plt.plot(x_vals, [0] * len(x_vals), 'r--', alpha = 0.5)
    plt.legend(keys)
    
    if xlabel != None:
        plt.xlabel(xlabel)

    if ylabel != None:
        plt.ylabel(ylabel)
    
    if ylabel != None:
        plt.title(title)
        
    if save:
        plt.savefig(os.path.join(cwd, "fig", "%s.png"%ylabel))