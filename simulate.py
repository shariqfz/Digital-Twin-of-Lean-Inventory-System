
import numpy as np

def simulate(horizon):
    '''
    horizon in hours
    Inventory stocks = 100 units (not %)
    deductions in integer units (not %)
    '''
    np.random.seed(0)
    
    if horizon:
        h_i = 100                      #initial level of container
        t_i = 0                     #intial time
        horizon = horizon * 60       #horizon time in minutes
        
        
        del_t_min = 30                  #minimum time interval between two consecutive del_h (= 30 mins)
        del_t_max = 60*2.5              #maximum time interval between two consecutive del_h (= 2.5 hours)
        
        times = [t_i]
        h = [h_i]
        del_hs = []
        del_ts = []
        
        while (h[-1] >= 0) & (times[-1] <= horizon) :
            del_t = np.random.randint(del_t_min, del_t_max)
            del_ts.append(del_t)
            del_h = int(0.1*np.random.uniform()*100) 
            del_h = del_h if del_h != 0 else 1
            del_hs.append(del_h)
            
            if (times[-1] + del_t <= horizon) & (h[-1] - del_h >= 0):
                
                times.append(times[-1] + del_t)
                h.append(h[-1] - del_h )
            
            else: break
                        
#         h = np.array(h)*100
        times = np.array(times) / 60
#         del_hs = np.array(del_hs)*100
        del_ts = np.array(del_ts) / 60
        h = np.round(h, 2); times = np.round(times, 2); del_hs = np.round(del_hs, 2); del_ts = np.round(del_ts, 2)
#         del_hs = np.where(del_hs, del_hs, stats.mode(del_hs))
        ts = np.cumsum(del_ts)
        return h, times, del_hs, del_ts, ts
