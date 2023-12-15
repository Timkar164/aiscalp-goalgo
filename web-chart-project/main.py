from flask import Flask, render_template, request, jsonify
from moexalgo import Market, Ticker
import pandas as pd

app = Flask(__name__)



params = {
    #'reference': ['secid', 'ts'], 
    'tradestats': ['candle', 'pr_open', 'pr_high', 'pr_low', 'pr_close', 'pr_vwap', 'pr_change', 'trades', 'vol', 'val', 'disb', 'pr_std', 'pr_vwap_b', 'pr_vwap_s', 'trades_b', 'trades_s', 'vol_b', 'vol_s', 'val_b', 'val_s'], 
    'orderstats': ['put_orders', 'cancel_orders', 'put_vol', 'put_val', 'cancel_vol', 'cancel_val', 'put_orders_b', 'put_orders_s', 'cancel_orders_b', 'cancel_orders_s', 'put_vol_b', 'put_vol_s', 'cancel_vol_b', 'cancel_vol_s', 'put_val_b', 'put_val_s', 'cancel_val_b', 'cancel_val_s', 'cancel_vwap_b', 'cancel_vwap_s', 'put_vwap_b', 'put_vwap_s'], 
    'obstats': ['spread_bbo', 'spread_lvl10', 'spread_1mio', 'levels_b', 'levels_s', 'vol_b', 'vol_s', 'val_b', 'val_s', 'imbalance_vol_bbo', 'imbalance_val_bbo', 'imbalance_vol', 'imbalance_val', 'vwap_b', 'vwap_s', 'vwap_b_1mio', 'vwap_s_1mio']
    }


def get_data_moex(list_ticker):
    buffer = {}
    res_data = {
        "categoryData": []
    }
    for item in list_ticker:
        if buffer.get(item[0]) == None:
            buffer[item[0]] = {
                'share': Ticker(item[0])
            }

        for param in params.keys():
            if item[1] in params[param]:
                buffer_param = param
                break

        if buffer[item[0]].get(buffer_param) == None:
            stock_data = getattr(buffer[item[0]]["share"], buffer_param)(date='2023-10-10', till_date='2023-10-18')
            buffer[item[0]][buffer_param] = list(stock_data)

        add_categoryData = False
        if len(res_data["categoryData"]) == 0:   
            add_categoryData = True


        key = item[0]+"_"+item[1]
        res_data[key] = {
            "name": f"{item[0]} {item[1]}",
            "chart_num": f"{item[2]}",
            "value": []
        }   

        for col in buffer[item[0]][buffer_param]:
            if add_categoryData:
                date = getattr(col, "ts")
                res_data["categoryData"].append(str(date))

            if item[1] == "candle":
                res_data[key]["value"].append((col.pr_close, col.pr_open, col.pr_low, col.pr_high))
            else:
                value = getattr(col, item[1])
                res_data[key]["value"].append(value)
            
    return jsonify(res_data)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/iframe")
def iframe():
    return render_template('iframe.html')
    

@app.route("/chart_data", methods = ['GET'])
def chart_data():
    list_ticker = []
    for i in request.args:
        list_ticker.append(request.args[i].split("|"))

    res = get_data_moex(list_ticker)
    return res

@app.route("/chart", methods = ['POST'])
def chart():
    data_form = request.form
    res = []
    for x in range(len(data_form)//2):
        res.append((data_form["tiker_"+str(x)], data_form["data_"+str(x)]))

    get_request = "?"
    for i in range(len(res)):
        get_request += f'{i}={res[i][0]}|{res[i][1]}&'
    get_request = get_request[:-1]

    chart_data = get_data_moex(res)
    return render_template('charts.html',  data={"data": chart_data, "get_request": get_request})


app.run(debug=True)