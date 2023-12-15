import backtrader as bt

class MuvingAverange(bt.Strategy): 
    #Параметры 
    params = (('pfast',20),('pslow',50),('pbar',5))

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.pfast)
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.pslow)
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None
    def next(self):
        '''
        Описать логику
        '''
        if self.order:
            return
        if not self.position:
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()
            elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.sell()
        else:
            if len(self) >= (self.bar_executed + self.params.pbar):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
                

class DsibStrategy(bt.Strategy):
    #Параметры 
    params = (('top_level',0.5),('low_level',-0.5),('pbar',5))

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None
        
    def next(self):
        '''
        Описать логику
        '''
        if self.order:
            return
        if not self.position:
            if self.datas[0].disb[0] > self.p.top_level:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()
            elif self.datas[0].disb[0] < self.p.low_level:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.sell()
        else:
            if self.position.size < 0 and (self.datas[0].disb[0] > self.p.low_level):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            elif self.position.size > 0 and (self.datas[0].disb[0] < self.p.top_level):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            else:
                pass
                
class LevelStrategy(bt.Strategy):
    #Параметры 
    params = (('pfast',20),('pslow',50),('pbar',5))

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None
        
    def next(self):
        '''
        Описать логику
        '''
        if self.order:
            return
        if not self.position:
            if self.datas[0].levels_b[0] > self.datas[0].levels_s[0]:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()
            elif self.datas[0].levels_b[0] < self.datas[0].levels_s[0]:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.sell()
        else:
            if self.position.size < 0 and (self.datas[0].levels_b[0] > self.datas[0].levels_s[0]):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            elif self.position.size > 0 and (self.datas[0].levels_b[0] < self.datas[0].levels_s[0]):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            else:
                pass
            
class CanceledOrderStrategy(bt.Strategy):
    params = (('toplevel',20000),('pbar',5))
    
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.time(0).hour
        #print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None
        
    def next(self):
        '''
        Описать логику
        '''
        if self.order:
            return
        if not self.position:
            if (self.datas[0].cancel_orders_b[0] < self.datas[0].cancel_orders_s[0]) and (self.datas[0].cancel_orders_s[0] > self.p.toplevel) and (self.datas[0].datetime.time(0).hour >= 11 and self.datas[0].datetime.time(0).hour <= 17):
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()
            elif (self.datas[0].cancel_orders_b[0] > self.datas[0].cancel_orders_s[0]) and (self.datas[0].cancel_orders_b[0] > self.p.toplevel) and (self.datas[0].datetime.time(0).hour >= 11 and self.datas[0].datetime.time(0).hour <= 17):
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.sell()
        else:
            if self.datas[0].datetime.time(0).hour >= 18:
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
                

from models.regression import regression_trend_analysis

class RegressionIndicator(bt.Indicator):
    lines = ('regression_trend',)
    params = (('period',100),('coef',0.04))
    plotinfo = dict(
        plot=True,
        plotname='regression_trend_forecast',
        subplot=True,
        plotlinelabels=True)
    def __init__(self):
        self.addminperiod(self.params.period)
    
    def next(self):
        x = self.data.get(size = self.p.period)
        #X = [(a / x[x.index(a) - 1]) - 1 for a in x]
        k = regression_trend_analysis(x)
        if k > self.p.coef:
            self.lines.regression_trend[0] = 1
        elif k < (self.p.coef * -1):
            self.lines.regression_trend[0] = -1
        else:
            self.lines.regression_trend[0] = 0
    
class LevelStrategyReg(bt.Strategy):
    #Параметры 
    params = (('pfast',20),('pslow',50),('period',10),('pbar',5))

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.regression = RegressionIndicator(self.dataclose)
        self.order = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None
        
    def next(self):
        '''
        Описать логику
        '''

        if self.order:
            return
        if not self.position:
            if (self.datas[0].levels_b[0] > self.datas[0].levels_s[0]) and (self.regression > 0):
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()
            elif (self.datas[0].levels_b[0] < self.datas[0].levels_s[0]) and (self.regression < 0):
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.sell()
        else:
            if self.position.size < 0 and (self.datas[0].levels_b[0] > self.datas[0].levels_s[0]):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            elif self.position.size > 0 and (self.datas[0].levels_b[0] < self.datas[0].levels_s[0]):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            else:
                pass
            
class LevelCanceledStrategyReg(bt.Strategy):
    #Параметры 
    params = (('pfast',20),('pslow',50),('period',10),('pbar',5),('toplevel',15000),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.regression = RegressionIndicator(self.dataclose)
        self.order = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None
        
    def next(self):
        '''
        Описать логику
        '''

        if self.order:
            return
        if not self.position:
            if (self.datas[0].levels_b[0] > self.datas[0].levels_s[0]) and (self.datas[0].cancel_orders_b[0] < self.datas[0].cancel_orders_s[0]) and (self.datas[0].cancel_orders_s[0] > self.p.toplevel) and (self.datas[0].datetime.time(0).hour >= 11 and self.datas[0].datetime.time(0).hour <= 17):
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()
            elif (self.datas[0].levels_b[0] < self.datas[0].levels_s[0]) and (self.datas[0].cancel_orders_b[0] > self.datas[0].cancel_orders_s[0]) and (self.datas[0].cancel_orders_b[0] > self.p.toplevel) and (self.datas[0].datetime.time(0).hour >= 11 and self.datas[0].datetime.time(0).hour <= 17):
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.sell()
        else:
            if self.position.size < 0 and (self.datas[0].levels_b[0] > self.datas[0].levels_s[0]):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            elif self.position.size > 0 and (self.datas[0].levels_b[0] < self.datas[0].levels_s[0]):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            else:
                pass