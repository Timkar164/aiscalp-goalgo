from moexalgo import Market, Ticker
import pandas as pd

sber = Ticker('SBER')
stocks = Market('stocks')

res = list(sber.tradestats(date='2023-10-10', till_date='2023-10-18'))

x = "ts"
print(getattr(res[0], x))



"""
res = {}
f = open("info.txt").read().split("\n")
for i in f:
	p = i.split()
	if res.get(p[0]) == None:
		res[p[0]] = [p[1]]
	else:
		res[p[0]].append(p[1])

print(res)
exit()
"""