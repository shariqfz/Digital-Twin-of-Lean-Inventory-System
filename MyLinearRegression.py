
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
