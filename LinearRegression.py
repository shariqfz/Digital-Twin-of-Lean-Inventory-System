
import numpy as np

class Lin_reg():
    
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.m = 0
        self.c = 0
        self.y_pred = np.array([])
        self.pred = np.array([])
    
    def train(self):
        #Set an objective function
        def objective(x):
            y_pred = x[0] + x[1]*self.X  #equation of regression line
            error = y_pred - self.y      #error varibale
            return np.sum(error**2)      #Sum of squares of errors
            
        #Perfrom optimization:
        #Minimization of the objective function    
        from scipy.optimize import minimize
            
        x0 = np.array([0.0, 0.0])        #Initialize coefficients to zeroes
        result = minimize(objective, x0) #Perform minimization
        coefficients = result.x
        
        m = coefficients[1]
        c = coefficients[0]
        
        y_pred = m*self.X + c
        
        self.m = m
        self.c = c
        self.y_pred = y_pred
        
    def predict(self, x):
        pred = self.m*x + self.c
        self.pred = pred
        return pred

def perform_linear_regression(h, t, horizon):    
    #First predict time intervals, t
    M = 4
    yt = t[:M]
    xt = np.linspace(0,M-1,M)
    lr = Lin_reg(xt, yt)
    lr.train()


    lrs = []


    for k in range(0, h.shape[0]):
        if k <= M:
            lrs.append([t[:k], h[:k]])

        else:
            #L.R. fot t
            #create extrapolated x-points (here values on xl will be time values)
            xt = np.linspace(0,k-1,k)
            yt = t[:M]
            i = M
            lr = Lin_reg(xt, t[:k])
            lr.train()

            while yt[-1] < horizon:
                p = lr.predict(np.array([i]))
                yt = np.hstack([yt, p])
                i += 1
#             print('yt: ', yt, len(yt))
#             print('yt_extra: ', np.hstack([yt, lr.predict(np.array([i]))]),
#                   len(np.hstack([yt, lr.predict(np.array([i]))])))

            #L.R. for h
            xh = t[:k]
            yh = h[:k]

            lr = Lin_reg(xh, yh)
            lr.train()
            yh = lr.predict(yt)
#             print(f'yh: {yh}')

            n = sum(yh >= 0)
#             print(f'n = {n}')

            yh = yh[:n]
            yt = yt[:n]

#             print(f'yh_trunc: {yh}, len = {len(yh)}')
#             print(f'yt_trunc: {yt}, len = {len(yt)}')
#             print('------------------------------------------------------------------')

            lrs.append([yt, yh])
    return lrs
