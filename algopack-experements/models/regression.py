# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 13:28:07 2023

@author: timka
"""

import numpy as np
from sklearn.linear_model import LinearRegression

"""
/----------------------------------------------Регрессионный анализ----------------------------------
"""
def regression_trend_analysis(data):
    """
    

    Parameters
    ----------
    data : List of Integer or List of Float
        Масив значений временного ряда.

    Returns
    -------
    k : Float
        Наклон линейной регресии, kx + b.

    """
    x = np.array([i for i in range(len(data))]).reshape((-1, 1))
    y = np.array(data)
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    b = y_pred[0]
    length = len(y_pred)-1
    k = ( y_pred[length] - b ) / x[length][0]
    return  k