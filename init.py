import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fund = 100
leverage = 3

key_delt = "Del (%)"

# portfolio worth
key_norm = "Nrm"
key_3xn = "3x"
key_lvg = "Lvg"

# percentage gain
key_pctn = "Nrm (pct)"
key_pct3 = "3x (pct)"
key_lvgp = "Lvg (pct)"

# dollar gain
key_netn = "Nrm (USD)"
key_net3 = "3x (USD)"
key_netl = "Lvg (USD)"

def Simulate_Path(deltas):
    df = pd.DataFrame(columns = [key_delt,
                                 key_norm, key_netn, key_pctn, 
                                 key_3xn, key_net3, key_pct3,
                                 key_lvg, key_netl, key_lvgp])
    df = df.append({
            key_norm : fund,
            key_3xn : fund * leverage,
            key_lvg : fund
        },ignore_index = True)

    for delta in deltas:
        # portfolio worth on next day, without leverage
        nxt_n = df.iloc[-1][key_norm] * (1 + delta)
        
        # portfolio worth on next day, with three times fund
        nxt_l = df.iloc[-1][key_3xn] * (1 + delta)
        
        # portfolio worth on next day, with 3x leverage
        nxt_p = df.iloc[-1][key_lvg] * (1 + leverage * delta)
        
        df = df.append({
            key_delt : 100 * delta,
            
            key_norm : nxt_n,
            key_netn : nxt_n - fund,
            key_pctn : 100 * (nxt_n - fund) / fund,
            
            key_3xn : nxt_l,
            key_net3 : nxt_l - fund * leverage,
            key_pct3 : 100 * (nxt_l - fund * leverage) / (fund * leverage),
            
            key_lvg : nxt_p,
            key_netl : nxt_p - fund,
            key_lvgp : 100 * (nxt_p - fund) / fund 
        }, ignore_index = True)
    return df

def Plot_3(df, keys, xlabel = None, ylabel = None, title = None, save = False):
    plt.figure(figsize=(12, 6))
    for key in keys:
        plt.plot(df[key].values)
    plt.legend(keys)
    
    if xlabel != None:
        plt.xlabel(xlabel)

    if ylabel != None:
        plt.ylabel(ylabel)
    
    if ylabel != None:
        plt.title(title)
        
    if save:
        plt.savefig(os.path.join(cwd, "fig", "%s.png"%ylabel))